import httplib2
import json
from datetime import datetime as dt
from pyvirtualdisplay import Display
from selenium import webdriver
import os
import tweepy

WORK_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = WORK_PATH + "/charts.json"
THRESHOLD = 3
CONSUMER_PATH = WORK_PATH + "/consumer.json"
TOKEN_PATH = WORK_PATH + "/token.json"
TWEET_PREFIX = "10分前と比較して3%以上の変動がありました\n"

def get_from_zaif(code):
    # 取得可能一覧
    # ["xem", "mona", "btc", "bch", "fscc", "sjcx", "bitcrystals", "xcp", "zaif", "jpyz", "eth", "cicc", "pepecash", "erc20.cms", "ncxc", "mosaic.cms"]
    h = httplib2.Http(".cache")
    resp, content = h.request("https://api.zaif.jp/api/1/last_price/"+code+"_jpy", "GET")
    data = content.decode('utf-8')
    return float(json.loads(data)["last_price"])

def zaif_charts():
    return {
        "MONA": { "name": "Monacoin", "price": get_from_zaif("mona") },
        "ZAIF": { "name": "ZAIFトークン", "price": get_from_zaif("zaif") },
        "XCP": { "name": "Counterparty", "price": get_from_zaif("xcp") },
        "BCY": { "name": "BitCrystals", "price": get_from_zaif("bitcrystals") },
        "SJCX": { "name": "Storjcoin X", "price": get_from_zaif("sjcx") },
        "FSCC": { "name": "フィスココイン", "price": get_from_zaif("fscc") },
        "PEPECASH": { "name": "PepeCash", "price": get_from_zaif("pepecash") },
        "CICC": { "name": "カイカコイン", "price": get_from_zaif("cicc") },
        "NCXC": { "name": "ネクスコイン", "price": get_from_zaif("ncxc") },
        "JPYZ": { "name": "Zen", "price": get_from_zaif("jpyz") },
    }

def coincheck_charts():
    prices = []

    display = Display(visible=0, size=(800, 800))
    display.start()
    # browser = webdriver.Chrome(executable_path=DRIVER_PATH)
    browser = webdriver.Firefox()
    browser.get('https://coincheck.com/ja/exchange')

    elements = browser.find_elements_by_css_selector(".currency_desc.ng-binding")

    for (idx, element) in enumerate(elements):
        if idx % 3 == 0:
            prices.append(element.text.replace("円", ""))

    browser.close()
    display.popen.terminate()

    data = {
        "BTC": { "name": "Bitcoin", "price":  float(prices[0]) },
        "ETH": { "name": "Ethereum", "price": float(prices[1]) },
        "ETC": { "name": "Ethereum Classic", "price": float(prices[2]) },
        "LSK": { "name": "Lisk", "price": float(prices[3]) },
        "FCT": { "name": "Factom", "price": float(prices[4]) },
        "XMR": { "name": "Monero", "price": float(prices[5]) },
        "REP": { "name": "Augur", "price": float(prices[6]) },
        "XRP": { "name": "Ripple", "price": float(prices[7]) },
        "ZEC": { "name": "Zcash", "price": float(prices[8]) },
        "XEM": { "name": "NEM", "price": float(prices[9]) },
        "LTC": { "name": "Litecoin", "price": float(prices[10]) },
        "DASH": { "name": "Dash", "price": float(prices[11]) },
        "BCH": { "name": "Bitcoin Cash", "price": float(prices[12]) }
    }
    return data

def all_charts():
    coincheck = coincheck_charts()
    zaif = zaif_charts()
    coincheck.update(zaif)
    return coincheck

def load_charts():
    f = open(FILE_PATH, 'r')
    return json.load(f)

def save_charts(charts):
    f = open(FILE_PATH, 'w')
    json.dump(charts, f, indent=4)

def get_fluctuations_text(charts_before, charts_after, threshold_percent=THRESHOLD):
    text = ""

    for key, value in charts_before.items():
        price_name = value["name"]
        price_before = value["price"]
        price_after = charts_after[key]["price"]

        tmp1 = float(price_after) / float(price_before)
        tmp2 = abs(1 - tmp1) * 100

        sign = "＋" if tmp1 > 1 else "－"
        up_down_info = sign + '{:.2f}'.format(tmp2) + "%"

        if tmp2 >= threshold_percent:
            text += "{0}({1}) {2}円 → {3}円 {4}\n".format(price_name, key, price_before, price_after, up_down_info)

    return text

def tweet(text):
    if len(text) == 0:
        return

    consumer = json.load( open(CONSUMER_PATH, "r") )
    token = json.load( open(TOKEN_PATH, "r") )
    auth = tweepy.OAuthHandler(consumer["CONSUMER_KEY"], consumer["CONSUMER_SECRET"])
    auth.set_access_token(token["ACCESS_TOKEN"], token["ACCESS_TOKEN_SECRET"])
    api = tweepy.API(auth)

    if len(TWEET_PREFIX + text) <= 130:
        text = TWEET_PREFIX + text
        print("tweet:", text)
        api.update_status(status=text)
    else:
        text_array = text.split("\n")

        tmp = TWEET_PREFIX
        for idx, part_text in enumerate(text_array):
            tmp += part_text + "\n"

            if idx+1 == len(text_array):
                # 最後
                print("tweet:", tmp)
                api.update_status(status=tmp)
            else:
                # 文字制限超えそうだったらツイートしてtmpを空に
                if len(tmp + text_array[idx + 1] + "\n") > 130:
                    print("tweet:", tmp)
                    api.update_status(status=tmp)
                    tmp = TWEET_PREFIX

def main():
    if os.path.exists(FILE_PATH):
        charts_past = load_charts()
        charts_now = all_charts()
        save_charts(charts_now)
        text = get_fluctuations_text(charts_past, charts_now)
        tweet(text)
    else:
        charts_now = all_charts()
        save_charts(charts_now)

if __name__ == "__main__":
    main()
