import json
from util import send_request


def query_supported_chains():
    """
    查询支持的区块链

    https://www.okx.com/zh-hans/web3/build/docs/waas/walletapi-api-get-supported-blockchain
    """
    req_path = "/api/v5/wallet/chain/supported-chains"
    resp = send_request(req_path, method="GET")
    return resp.json()


def save_supported_chain():
    chains = query_supported_chains()['data']
    data = [{x["name"]: x for x in chains}]
    with open('chains.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def query_token_price(chainIndex, tokenAddress=""):
    """
    批量查询币种的实时价格。

    :return:
    """
    req_path = "/api/v5/wallet/token/current-price"
    params = [{
        "chainIndex": chainIndex,
        "tokenAddress": tokenAddress
    }]
    resp = send_request(req_path, method="POST", params=params)
    return resp.json()


def query_historical_price():
    """
    查询某个币种的历史价格。

    https://www.okx.com/zh-hans/web3/build/docs/waas/walletapi-api-get-historical-price
    :return:
    """
    req_path = "/api/v5/wallet/token/historical-price"
    params = {
        "chainIndex": "1",
        "limit": "5",
        "begin": "1700040600000",
        "period": "5m"
    }
    resp = send_request(req_path, method="GET", params=params)
    return resp.json()


def query_token_detail(chainIndex, tokenAddress=""):
    """
    查询单个币种的其他信息，诸如币种合约地址、代币官网 URL、社媒信息。

    https://www.okx.com/zh-hans/web3/build/docs/waas/walletapi-api-token-detail
    :return:
    """
    req_path = "/api/v5/wallet/token/token-detail"
    params = {
        "chainIndex": chainIndex,
        "tokenAddress": tokenAddress
    }
    resp = send_request(req_path, method="GET", params=params)
    return resp.json()


def query_total_value_by_address(address, chains):
    """
    获取地址下全量 token 和 Defi 资产总余额，支持过滤垃圾空投代币。

    https://www.okx.com/zh-hans/web3/build/docs/waas/walletapi-api-token-detail
    :return:
    """
    req_path = "/api/v5/wallet/asset/total-value-by-address"
    params = {
        "address": address,
        "chains": chains
    }
    resp = send_request(req_path, method="GET", params=params)
    return resp.json()


def query_all_token_balances_by_address(address, chains):
    """
    查询地址持有的多个链或指定链的 token 余额列表。

    https://www.okx.com/zh-hans/web3/build/docs/waas/walletapi-api-all-token-balances-by-address
    :return:
    """
    req_path = "/api/v5/wallet/asset/all-token-balances-by-address"
    params = {
        "address": address,
        "chains": chains
    }
    resp = send_request(req_path, method="GET", params=params)
    return resp.json()


def query_token_balances_by_address(address, token_addresses):
    """
    查询地址持有的多个链或指定链的 token 余额列表。

    token_addresses: [{chainIndex: str}, {address: str}]
    https://www.okx.com/zh-hans/web3/build/docs/waas/walletapi-api-specific-token-balance-by-address
    :return:
    """
    req_path = "/api/v5/wallet/asset/token-balances-by-address"
    params = {
        "address": address,
        "tokenAddresses": token_addresses
    }
    resp = send_request(req_path, method="POST", params=params)
    return resp.json()


def query_approvals(addresses):
    """
    分页查询单个地址，授权了哪些项目。以及每个授权项目下，授权的资产和额度。

    addresses: [{chainIndex: str}, {address: str}]
    https://www.okx.com/zh-hans/web3/build/docs/waas/walletapi-api-specific-token-balance-by-address
    :return:
    """
    req_path = "/api/v5/wallet/security/approvals"
    params = {
        "addresses": addresses
    }
    resp = send_request(req_path, method="POST", params=params)
    return resp.json()

def query_transactions_by_address(address, chains):
    """
    查询地址维度下的交易历史，按时间倒序排序。

    :param address:
    :param chains:
    :return:
    """
    req_path = "/api/v5/wallet/post-transaction/transactions-by-address"
    data = {
        "address": address,
        "chains": chains
    }
    resp = send_request(req_path, method="GET", params=data)
    return resp.json()


def broadcast_transaction(signedTx, chainIndex, address):
    req_path = "/api/v5/wallet/post-transaction/transactions-by-address"
    data = {
        "signedTx": signedTx,
        "chainIndex": chainIndex,
        "address": address
    }
    resp = send_request(req_path, method="POST", params=data)
    return resp.json()


def transaction_detail_by_txhash(chainIndex, txHash):
    req_path = "/api/v5/wallet/post-transaction/transaction-detail-by-txhash"
    data = {
        "chainIndex": chainIndex,
        "txHash": txHash,
        # "iType": '2'
    }
    resp = send_request(req_path, method="GET", params=data)
    return resp.json()
    

if __name__ == '__main__':
    # data = query_token_price("1")
    # data = query_historical_price()
    # data = query_token_detail(chainIndex="501", tokenAddress="GJtJuWD9qYcCkrwMBmtY1tpapV1sKfB2zUv9Q4aqpump")
    # data = query_total_value_by_address(address='8yNxK642RR1vyx7WoLou8Jxjxhwsedv8BfTYc833KNRg', chains='501')

    # address = "0x4679239cad2e33c7516924f73cec1365ab01a274"
    # chainIndex = "1"
    # data = query_all_token_balances_by_address(address, chainIndex)

    # addresses = [{"chainIndex": chainIndex, "address": address}]
    # data = query_approvals(addresses=addresses)


    # data = query_transactions_by_address(address, chainIndex)
    data = transaction_detail_by_txhash('8453', '0x55dd3b31b3d48b65dbb83914df392bdb1e9f53a2e8f160cc87b5961c8d3bbe22')
    print(json.dumps(data, indent=2, ensure_ascii=False))
