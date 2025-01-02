import json
from util import send_request


class OkxDex(object):
    def query_supported_chain():
        """
        https://www.okx.com/api/v5/dex/cross-chain/supported/chain
        :return:
        """
        url = "/api/v5/dex/cross-chain/supported/chain"
        resp = send_request(url, method="GET")
        return resp.json()

    def save_supported_chain(self):
        chains = self.query_supported_chain()['data']
        data = [{x['chainName']: x for x in chains}]
        with open('bridge_chains.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def query_supported_tokens(chainId):
        """
        获取币种列表。此接口的返回结果是欧易 DEX 认为的主流代币和平台代币。你可以指定该列表之外的代币在欧易 DEX 询价和兑换。
        :return:
        """
        url = "/api/v5/dex/aggregator/all-tokens"
        data = {
            "chainId": chainId
        }
        resp = send_request(url, method="GET", params=data)
        return resp.json()
    
    @staticmethod
    def query_supported_tokens_by_bridge(chainId):
        url = "/api/v5/dex/cross-chain/supported/tokens"
        data = {
            "chainId": chainId
        }
        resp = send_request(url, method="GET", params=data)
        return resp.json()

    @staticmethod
    def query_supported_token_pairs_by_bridge(fromChainId):
        url = "/api/v5/dex/cross-chain/supported/bridge-tokens-pairs"
        data = {
            "fromChainId": fromChainId
        }
        resp = send_request(url, method="GET", params=data)
        return resp.json()
    
    def query_supported_bridges(chainId):
        url = "/api/v5/dex/cross-chain/supported/bridges"
        data = {
            "chainId": chainId
        }
        resp = send_request(url, method="GET", params=data)
        return resp.json()
    
    def approve_transaction(chainId, tokenContractAddress, approveAmount):
        """
        获取交易授权所需要的数据
        :return:
        """
        url = "/api/v5/dex/aggregator/approve-transaction"
        data = {
            "chainId": chainId,
            "tokenContractAddress": tokenContractAddress,
            "approveAmount": approveAmount
        }
        resp = send_request(url, method="GET", params=data)
        return resp.json()


if __name__ == '__main__':
    # data = OkxDex().query_supported_token_pairs_by_bridge('1')
    # data = OkxDex().query_supported_tokens_by_bridge('1')
    data = OkxDex().query_supported_tokens('1')
    print(data)