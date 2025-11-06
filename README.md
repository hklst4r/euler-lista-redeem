## 1.  Euler Lista Auto Redeem Script / Euler Lista 自动赎回脚本

Automated redemption script for Euler Lista vaults. Monitors withdrawable balance and automatically executes withdrawals when threshold is reached.

用于 Euler Lista 金库的自动赎回脚本。监控可赎回余额，达到阈值时自动执行赎回。

## Installation / 安装

```bash
pip install web3
```

## Configuration / 配置

Edit `lista/redeem.py` and set:

编辑 `lista/redeem.py` 并设置：

- `RPC`: Blockchain RPC URL / 区块链 RPC 节点 URL
- `PRIVATE_KEY`: Your wallet private key / 钱包私钥
- `OWNER`: Your EOA address / EOA 地址
- `CONTRACT_ADDR`: Vault contract address / 金库合约地址

### Example Vaults (BSC) / 示例金库（BSC）

- **Re7 USD1**: `0x02A5ca3a749855d1002A78813E679584a96646d0`
- **MEV USDT**: `0x6402d64F035E18F9834591d3B994dFe41a0f162D`

## Usage / 使用方法

```bash
cd lista
python redeem.py
```

The script continuously monitors `maxWithdraw(OWNER)` and automatically calls `withdraw()` when the amount exceeds 1e18.

脚本持续监控 `maxWithdraw(OWNER)`，当金额超过 1e18 时自动调用 `withdraw()`。

## Customization / 自定义

- **Threshold / 阈值**: MIN_WITHDRAW_AMOUNT, modify `1e18`
- **Check interval / 检查间隔**: TIME_INTERVAL, modify `time.sleep(0.1)`
- **Gas limit / Gas 限制**: GAS_LIMIT, modify `2000000`

## Security Warning / 安全警告

⚠️ **Never commit private keys to public repositories / 切勿将私钥提交到公共仓库**

⚠️ **Ensure sufficient balance for gas fees / 确保账户有足够余额支付 gas 费用**

Please do your own research. This repo is only for reference and studying purpose and I am not responsible for its security and reliability. / 请自行研究，本仓库仅供学习与参考。不对其安全性和可靠性负责


## 2. Lista Position Alteration / 换仓合约

Swaps MEV USDT vault position to SatUSD market on Morpho. After swap, withdrawals require contract interaction or Rabby wallet.

将 MEV USDT 金库仓位换到 Morpho 的 SatUSD 市场。换仓后需通过合约交互或 Rabby 钱包取款。

### Configuration / 配置

Edit `lista/lista-alter-contract/change-position.sol` and set your EOA address:

编辑 `lista/lista-alter-contract/change-position.sol` 并设置您的 EOA 地址：

```solidity
address owner; // FILL IN YOUR EOA ADDRESS / 填入您的 EOA 地址
```

### Usage / 使用方法

1. **Deploy / 部署**: Deploy `change-position.sol` to BSC / 部署到 BSC

2. **⚠️ Approve Vault Tokens / 授权金库代币** (Required / 必需):
   ```solidity
   IERC20(vault).approve(contractAddress, amount);
   ```
   You must approve your vault tokens to the contract before calling `letsgo()`.

   调用 `letsgo()` 前必须将金库代币授权给合约。

3. **Execute / 执行**: Call `contract.letsgo(amount)` / 调用 `contract.letsgo(amount)`

### Withdrawal / 取款

⚠️ After swap, withdraw via contract interaction or Rabby wallet. Direct vault withdrawal is not possible. Withdrawl not available instantly, but will have no risk exposure to USDX.

换仓后需通过合约交互或 Rabby 钱包取款，无法直接从金库取款。且无法立即取款，但是不会对USDX有风险敞口。

### Security Warning / 安全警告

⚠️ **Only use if you fully understand smart contracts / 仅在完全理解智能合约时使用**

⚠️ **Test on local first / 请先在本地测试，确认无误再部署**