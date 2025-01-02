import json
from datetime import datetime

from util import send_request


def create_account(addresses):
    """
    创建账户, 绑定多个地址，创建钱包账户，支持的链默认返回全量币种，同时可实现对资产和交易历史等信息的聚合查询。

    https://www.okx.com/zh-hans/web3/build/docs/waas/walletapi-api-create-wallet-account
    """
    req_path = "/api/v5/wallet/account/create-wallet-account"
    data = {
        "addresses": addresses
    }
    resp = send_request(req_path, method="POST", params=data)
    return resp.json()


def update_account(accountId, updateType, addresses):
    """
    更改某一钱包账户下绑定的地址。

    updateType: add: 添加 delete: 删除

    https://www.okx.com/zh-hans/web3/build/docs/waas/walletapi-api-update-wallet-account
    """
    req_path = "/api/v5/wallet/account/update-wallet-account"
    data = {
        "accountId": accountId,
        "updateType": updateType,
        "addresses": addresses
    }
    resp = send_request(req_path, method="POST", params=data)
    return resp.json()


def query_account_detail(accountId):
    """
    查询某个账户下绑定的地址。

    :param accountId:
    :return:
    """
    req_path = "/api/v5/wallet/account/account-detail"
    params = {
        "accountId": accountId
    }
    resp = send_request(req_path, method="GET", params=params)
    return resp.json()


def query_total_value_by_account(accountId):
    """
    获取账户下全量 token 和 Defi 资产总余额，支持过滤垃圾空投代币。

    :param accountId:
    :return:
    """
    req_path = "/api/v5/wallet/asset/total-value"
    params = {
        "accountId": accountId
    }
    resp = send_request(req_path, method="GET", params=params)
    return resp.json()


def delete_account(accountId):
    """
    删除已创建的账户。

    :param accountId:
    :return:
    """
    req_path = "/api/v5/wallet/account/delete-account"
    params = {
        "accountId": accountId
    }
    resp = send_request(req_path, method="POST", params=params)
    return resp.json()


def query_accounts():
    """
    列举项目下创建过的账户。

    :return:
    """
    req_path = "/api/v5/wallet/account/accounts"
    resp = send_request(req_path, method="GET")
    return resp.json()


def query_account_balance(accountId):
    """
    查询钱包账户持有的多个链或指定链的 token 余额列表。

    :param accountId:
    :return:
    """
    req_path = "/api/v5/wallet/asset/wallet-all-token-balances"
    params = {
        "accountId": accountId
    }
    resp = send_request(req_path, method="GET", params=params)
    return resp.json()


def query_account_transactions(accountId):
    """
    查询账户维度下所有或某条链的交易历史，按时间顺序倒序排序。

    :param accountId:
    :return:
    """
    req_path = "/api/v5/wallet/post-transaction/transactions"
    params = {
        "accountId": accountId
    }
    resp = send_request(req_path, method="GET", params=params)
    return resp.json()


if __name__ == '__main__':
    # addresses = [{"chainIndex": "1", "address": "0x8f12bA8e719EdD228489b0c2781bDD5b4673cD7B"},
    #              {"chainIndex": "784", "address": "0x2e3736a9c256ee5d9438370202449ee802d18785bbe2333908c7d5069b5922fe"}]
    #
    # data = create_account(addresses)

    # account_id = "74c65a13-ccb9-4fe8-9265-64e5ff40e159"
    # addresses = [{"chainIndex": "501", "address": "8yNxK642RR1vyx7WoLou8Jxjxhwsedv8BfTYc833KNRg"}]

    # data = update_account(account_id, "add", addresses)
    # data = query_account_detail(account_id)

    data = query_accounts()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    exit()
    # data = query_account_transactions(account_id)
    data = query_account_balance(account_id)
    print(json.dumps(data, indent=2, ensure_ascii=False))
