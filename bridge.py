import json
from util import send_request


class Bridge(object):
    """
    跨链API
    """
    def quote(fromChainId, toChainId, fromTokenAddress, toTokenAddress, amount, slippage):
        """
        通过 DEX 聚合器获取最优报价。

        :param fromChainId: 源链 ID
        :param toChainId: 目标链 ID 
        :param fromTokenAddress: 询价币种合约地址 (如0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE )
        :param toTokenAddress: 目标币种合约地址 (如TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8 )
        :param amount: 币种询价数量(数量需包含精度，如授权 1.00 USDT 需输入 1000000，授权 1.00 DAI 需输入 1000000000000000000 )
        :param slippage: 滑点限制，最小值：0.002，最大值：0.5。（如：0.005代表你接受这笔交易最大 0.5%滑点，0.5 就代表你接受这笔交易最大 50%的滑点）
        :return:
        """
        url = "/api/v5/dex/cross-chain/quote"
        data = {
            "fromChainId": fromChainId,
            "toChainId": toChainId,
            "fromTokenAddress": fromTokenAddress,
            "toTokenAddress": toTokenAddress,
            "amount": amount,
            "slippage": slippage,
        }
        resp = send_request(url, method="GET", params=data)
        return resp.json()

    def swap(fromChainId, toChainId, fromTokenAddress, toTokenAddress, amount, slippage, userWalletAddress):
        """
        获取跨链兑换所需的交易数据。
        :param fromChainId:
        :param toChainId:
        :param fromTokenAddress:
        :param toTokenAddress:
        :param amount:
        :param slippage:
        :param userWalletAddress:
        :return:
        """
        url = "/api/v5/dex/cross-chain/build-tx"
        data = {
            "fromChainId": fromChainId,
            "toChainId": toChainId,
            "fromTokenAddress": fromTokenAddress,
            "toTokenAddress": toTokenAddress,
            "amount": amount,
            "slippage": slippage,
            "userWalletAddress": userWalletAddress
        }
        resp = send_request(url, method="GET", params=data)
        return resp.json()

    def query_status(hash, chainId):
        url = "/api/v5/dex/cross-chain/status"
        data = {
            "hash": hash,
            "chainId": chainId
        }
        resp = send_request(url, method="GET", params=data)
        return resp.json()


if __name__ == '__main__':
    bridge = Bridge()
    # save_supported_chain()
    # exit()

    # 8453 stands for Base Chain
    # data = query_supported_tokens("8453")
    # print(data)
    # exit()
    
    # buy base_eth with eth
    data = bridge.quote("1", "8453", '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', 2000000000000, 0.002)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    # data = get_liquidity("8453")
    # print(json.dumps(data, indent=2, ensure_ascii=False))
