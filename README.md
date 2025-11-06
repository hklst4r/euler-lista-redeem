# Euler Lista Auto Redeem Script / Euler Lista 自动赎回脚本

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
