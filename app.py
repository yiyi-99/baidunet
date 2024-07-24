from flask import Flask, request, jsonify
import requests
import hashlib
import time
import random
import string

app = Flask(__name__)

APPID = 'YOUR_APPID'  # 替换为您的公众号AppID
APPSECRET = 'YOUR_APPSECRET'  # 替换为您的公众号AppSecret

@app.route('/get_signature', methods=['GET'])
def get_signature():
    url = request.args.get('url')
    access_token = get_access_token()
    jsapi_ticket = get_jsapi_ticket(access_token)
    signature_data = generate_signature(jsapi_ticket, url)
    return jsonify(signature_data)

def get_access_token():
    response = requests.get(f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}')
    return response.json().get('access_token')

def get_jsapi_ticket(access_token):
    response = requests.get(f'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={access_token}&type=jsapi')
    return response.json().get('ticket')

def generate_signature(jsapi_ticket, url):
    nonce_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    timestamp = int(time.time())  # 生成当前时间的时间戳
    string1 = f"jsapi_ticket={jsapi_ticket}&noncestr={nonce_str}&timestamp={timestamp}&url={url}"
    signature = hashlib.sha1(string1.encode('utf-8')).hexdigest()
    return {
        "appId": APPID,
        "nonceStr": nonce_str,
        "timestamp": timestamp,
        "signature": signature
    }

if __name__ == '__main__':
    app.run()
