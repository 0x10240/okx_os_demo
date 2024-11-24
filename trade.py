import json
from util import send_request

"""
交易广播 API 接口，提供获取签名数据、广播交易，以及跟踪发送后的交易等服务。


https://www.okx.com/zh-hans/web3/build/docs/waas/walletapi-api-intro-transaction-api
"""


def get_sign_info(chainIndex, fromAddr, toAddr):
    """
    该接口提供各个链，签名交易时所需数据。 例如 EVM 网络所需的网络费用、nonce 。UTXO 模型网络需要的费率，输出大小等最参数。

    :return:
    """
    req_path = "/api/v5/wallet/pre-transaction/sign-info"
    data = {
        "chainIndex": chainIndex,
        "fromAddr": fromAddr,
        "toAddr": toAddr,
    }
    resp = send_request(req_path, method="POST", params=data)
    return resp.json()


def get_gas_price(chainIndex):
    """
    动态获取各个链的预估 gas price，支持 EIP-1559，覆盖 EVM、UTXO 模型的网络。

    :return:
    """
    req_path = "/api/v5/wallet/pre-transaction/gas-price"
    data = {
        "chainIndex": chainIndex
    }
    resp = send_request(req_path, method="GET", params=data)
    return resp.json()


def get_gas_limit(chainIndex, fromAddr, toAddr):
    """
    通过交易信息的预执行，获取预估消耗的 Gaslimit 。当前仅支持 EVM 的网络。

    :param chainIndex:
    :return:
    """
    req_path = "/api/v5/wallet/pre-transaction/gas-limit"
    data = {
        "chainIndex": chainIndex,
        "fromAddr": fromAddr,
        "toAddr": toAddr,
    }
    resp = send_request(req_path, method="POST", params=data)
    return resp.json()


def get_nonce(chainIndex, address):
    """
    支持 EVM 链查询 Nonce，返回即将上链的 nonce 和内存池 pending 排队的 nonce。

    :param chainIndex:
    :param address:
    :return:
    """
    req_path = "/api/v5/wallet/pre-transaction/nonce"
    data = {
        "chainIndex": chainIndex,
        "address": address,
    }
    resp = send_request(req_path, method="GET", params=data)
    return resp.json()


def get_sui_object(chainIndex, address):
    """
    查询SUI 链上的所有对象。

    :param chainIndex:
    :param address:
    :return:
    """
    req_path = "/api/v5/wallet/pre-transaction/sui-object"
    data = {
        "chainIndex": chainIndex,
        "address": address
    }
    resp = send_request(req_path, method="GET", params=data)
    return resp.json()


if __name__ == '__main__':
    chainIndex = "784"
    fromAddr = "0xda603ecf56dea638fa22915453ee142f71baf352d0f4c600111b53ff9a200c73"
    toAddr = "0xda603ecf56dea638fa22915453ee142f71baf352d0f4c600111b53ff9a200c73"

    # data = get_sign_info(chainIndex, fromAddr, toAddr)
    # data = get_nonce("1", "0x4679239cad2e33c7516924f73cec1365ab01a274")

    token_addr = "0x2e3736a9c256ee5d9438370202449ee802d18785bbe2333908c7d5069b5922fe"
    data = get_sui_object(chainIndex, fromAddr)

    print(json.dumps(data, indent=2, ensure_ascii=False))
