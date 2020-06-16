# app.py
from flask import Flask, request, jsonify
import requests
import json

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_buff_price(inventory_array):
    inventory_dict = {}

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cookie": "Device-Id=DY6sBlsvEUu5htgd5zvt; _ga=GA1.2.730754564.1592248891; _gid=GA1.2.25328569.1592248891; Locale-Supported=en; game=csgo; _gat_gtag_UA_109989484_1=1; session=1-CBGworC0LSgVBGaHAFXxdvC6RSRgCBcH1o1JmpMGewPa2044657185; csrf_token=IjIwZTk1MjczZGQyZjkyNWQyMWZjNTQ4YTVmNDlhODgzMjNmZmEwZTEi.EcqmkA.-vDIPL4QkTvktqCmWc53Ek3sjYQ",
        "Host": "buff.163.com",
        "Referer": "https://buff.163.com/market/?game=csgo",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    for skin, value in inventory_array.items():
        url = 'https://buff.163.com/api/market/goods?game=csgo&page_num=1&search='+ skin

        x = requests.session()
        r = x.get(url=url, headers=headers)
        ob = json.loads(r.text)

        for item in ob['data']['items'][:1]:
            inventory_dict[item['market_hash_name']] = {
                'name': item['market_hash_name'],
                'sell': item['sell_min_price'],
                'asset_id': value['asset_id']
                }

            
    return inventory_dict

@app.route("/get_steam_inventory/", methods=['GET'])
def respond():

    steam_id = request.args.get('steam_id')

    print(steam_id)

    # Retrieve the name from url parameter
    steam_inv_dict = {}

    x = requests.session()
    r = x.get(
        url="https://steamcommunity.com/inventory/"+str(steam_id)+"/730/2?l=english&count=75"
    )
    ob = json.loads(r.text)

    for asset, item in zip(ob['assets'], ob["descriptions"]):
        if item["marketable"] == 1:
            steam_inv_dict[item["market_hash_name"]]={
                "name":item["market_hash_name"],
                "asset_id": asset['assetid']
            }

    inv_dict = get_buff_price(steam_inv_dict)

    # Return the response in json format
    return jsonify({"buff_prices": inv_dict})


if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)
