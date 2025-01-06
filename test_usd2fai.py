import asyncio
from okx_dex_api import OKXDexAPI
from web3 import Web3
import os

from dotenv import load_dotenv

load_dotenv()


okx = OKXDexAPI(
    os.getenv("OK-ACCESS-KEY"),
    os.getenv("OK-API-SECRET"),
    os.getenv("OK-ACCESS-PASSPHRASE"),
    os.getenv("OK-PROJECT-ID"),
)


def sign(swap_result):
    client = Web3(Web3.HTTPProvider(os.getenv("BASE_CHAIN_RPC_URL")))
    nonce = client.eth.get_transaction_count(
        Web3.to_checksum_address("0x42c891fe3799fac46c3b82e95cc5a22a288e3178")
    )
    transaction = {
        "data": swap_result.data[0].tx.data,
        "gasPrice": int(swap_result.data[0].tx.gas_price),
        "to": swap_result.data[0].tx.to,
        "value": int(swap_result.data[0].tx.value),
        "gas": int(swap_result.data[0].tx.gas),
        "nonce": nonce,
    }
    print(transaction)
    private_key = os.getenv("PRIVATE_KEY")
    data = client.eth.account.sign_transaction(transaction, private_key)
    return data.raw_transaction.hex()


async def main():
    try:
        await okx.get_tokens("8453")

        quote_result = await okx.get_quote(
            "8453",
            "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
            "0xb33Ff54b9F7242EF1593d2C9Bcd8f9df46c77935",
            2,
        )
        print(f"Quote Result: {quote_result}")
        # import pdb;pdb.set_trace()

        approval_result = await okx.approve_transaction(
            "8453", "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913", 2000000
        )
        print(f"Approval Result: {approval_result}")

        swap_result = await okx.swap(
            "8453",
            "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
            "0xb33Ff54b9F7242EF1593d2C9Bcd8f9df46c77935",
            2,
            0.1,
            "0x42c891fe3799fac46c3b82e95cc5a22a288e3178",
        )
        print(f"Swap Result: {swap_result}")

        signed_tx = sign(swap_result)
        print(f"Signed TX Result: {signed_tx}")

        broadcast_result = await okx.broadcast_transaction(
            "0x" + signed_tx, "8453", "0x42c891fe3799fac46c3b82e95cc5a22a288e3178"
        )
        print(f"Broadcast Result: {broadcast_result}")

        data = await okx.get_transaction_orders(
            address="0x42c891fe3799fac46c3b82e95cc5a22a288e3178"
        )
        print(f"Order Result: {data}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
