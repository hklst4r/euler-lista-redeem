from web3 import Web3
import json
import time


RPC = "<RPC_URL>"
PRIVATE_KEY = "<PRIVATE_KEY>"
# your eoa address
OWNER = Web3.to_checksum_address("<OWNER_ADDRESS>")
# the vault address
# Re7 USD1 on BSC: 0x02A5ca3a749855d1002A78813E679584a96646d0
# MEV USDT on BSC: 0x6402d64F035E18F9834591d3B994dFe41a0f162D
CONTRACT_ADDR = Web3.to_checksum_address("<CONTRACT_ADDRESS>")
TIME_INTERVAL = 0.1 # seconds
MIN_WITHDRAW_AMOUNT = 1e18 # 1 USD
GAS_LIMIT = 2000000 # 2e6

w3 = Web3(Web3.HTTPProvider(RPC))
acct = w3.eth.account.from_key(PRIVATE_KEY)

with open("abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDR, abi=abi)

# -------------------------------
# main logic
# -------------------------------
def main():
    while True:
        # 1) Query maxRedeem(owner)
        max_redeem = contract.functions.maxWithdraw(OWNER).call()
        print("maxRedeem =", max_redeem)

        # 2) Check threshold
        if max_redeem <= MIN_WITHDRAW_AMOUNT:
            print("Below threshold, nothing to do.")
            time.sleep(TIME_INTERVAL)
            continue

        print(f"Value > {MIN_WITHDRAW_AMOUNT}, sending withdraw()…")

        # 3) Build tx: redeem(maxRedeem(owner))
        tx = contract.functions.withdraw(max_redeem, OWNER, OWNER).build_transaction({
            "from": OWNER,
            "nonce": w3.eth.get_transaction_count(OWNER),
            "gas": GAS_LIMIT,
            "gasPrice": w3.eth.gas_price
        })

        # 4) Sign & send
        signed = acct.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)

        print("Sent tx:", tx_hash.hex())
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Confirmed in block:", receipt.blockNumber)


if __name__ == "__main__":
    main()
