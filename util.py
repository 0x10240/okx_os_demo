import os
import time
import hmac
import hashlib
import base64
import json
import requests

from loguru import logger
from urllib.parse import urlencode, urljoin
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path=env_path)

# 从环境变量中获取 API 凭证和项目 ID
api_config = {
    "api_key": os.getenv('OK-ACCESS-KEY'),
    "secret_key": os.getenv('OK-API-SECRET'),
    "passphrase": os.getenv('OK-ACCESS-PASSPHRASE'),
    "project": os.getenv("OK-PROJECT-ID", "")
}


def pre_hash(timestamp, method, request_path, params):
    # 根据字符串和参数创建预签名
    query_string = ''
    if method == 'GET' and params:
        query_string = '?' + urlencode(params)
    if method == 'POST' and params:
        query_string = json.dumps(params)
    return timestamp + method + request_path + query_string


def sign(message, secret_key):
    # 使用 HMAC-SHA256 对预签名字符串进行签名
    return base64.b64encode(hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()).decode()


def create_signature(method, request_path, params):
    # 获取 ISO 8601 格式时间戳
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    # 生成签名
    message = pre_hash(timestamp, method, request_path, params)
    signature = sign(message, api_config['secret_key'])
    return signature, timestamp


def send_request(request_path, method="GET", params=None):
    # 生成签名
    signature, timestamp = create_signature(method, request_path, params)

    logger.debug(f'signature: {signature}, timestamp: {timestamp}')

    # 生成请求头
    headers = {
        'Content-Type': 'application/json',
        'OK-ACCESS-KEY': api_config['api_key'],
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': api_config['passphrase'],
        'OK-ACCESS-PROJECT': api_config['project']  # 这仅适用于 WaaS APIs
    }

    url = urljoin("https://www.okx.com", request_path)

    # 发送请求
    if method == 'POST':
        response = requests.post(url, headers=headers, data=json.dumps(params))
    else:
        response = requests.get(url, params=params, headers=headers)

    return response


def __test():
    # GET 请求示例
    get_request_path = '/api/v5/dex/aggregator/quote'
    get_params = {
        'chainId': 42161,
        'amount': 1000000000000,
        'toTokenAddress': '0xff970a61a04b1ca14834a43f5de4533ebddb5cc8',
        'fromTokenAddress': '0x82aF49447D8a07e3bd95BD0d56f35241523fBab1'
    }
    send_request('GET', get_request_path, get_params)

    # POST 请求示例
    post_request_path = '/api/v5/mktplace/nft/ordinals/listings'
    post_params = {
        'slug': 'sats'
    }

    resp = send_request(post_request_path, 'POST', post_params)
    print(resp.json())


if __name__ == '__main__':
    path = '/api/v5/dex/aggregator/all-tokens'
    get_params = {
        'chainId': 1,
    }
    resp = send_request(path, 'GET', get_params)
    print(json.dumps(resp.json(), indent=2))
