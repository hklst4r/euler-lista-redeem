// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {IERC20} from "./erc20.sol";
import "./morpho.sol";
contract Action {
    address owner; // FILL IN YOUR EOA ADDRESS
    address usdt = 0x55d398326f99059fF775485246999027B3197955;
    address vault = 0x6402d64F035E18F9834591d3B994dFe41a0f162D; // MEV USDT ON BSC

    bytes32 satUSDMarketId = 0x2e865d41371fb021130dc872741c70564d0f5ea4856ff1542163a8b59b0b524d; // SAT USD market ON BSC
    address morpho = 0x8F73b65B4caAf64FBA2aF91cC5D4a2A1318E5D8C;

    uint256 amount;


    function letsgo(uint256 _amount) external {
        require(msg.sender == owner, "not owner");
        amount = _amount;
        IMorpho(morpho).flashLoan(usdt, _amount, "");

        _transfer_out(vault);
        _transfer_out(usdt);
    }

    fallback() external {
        require(tx.origin == owner);
        IERC20(vault).transferFrom(owner, address(this), amount);
        IERC20(usdt).approve(morpho, type(uint256).max);

        // deposit into solvBTC market
        MarketParams memory marketParams = IMorpho(morpho).idToMarketParams(satUSDMarketId);
        IMorpho(morpho).supply(marketParams, amount, 0, owner, "");

        // withdraw from re7
        IVault(vault).withdraw(amount, address(this), address(this));
    }

    function _transfer_out(address token) internal {
        uint bal = IERC20(token).balanceOf(address(this));
        if(bal == 0) return;
        IERC20(token).transfer(owner, bal);
    }

    // in case any emergency, you can call this function to do any thing
    function adminFunction(address to, bytes memory data, uint value) external {
        require(msg.sender == owner, "not owner");
        (bool success, bytes memory result) = to.call{value: value}(data);
        require(success, "call failed");
    }
}


interface IVault {
    function withdraw(uint256 amount, address receiver, address owner) external returns (uint256);
    function maxWithdraw(address owner) external view returns (uint256);
    function previewWithdraw(uint256 amount) external view returns (uint256);
}