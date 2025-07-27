// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20; // Ensure this is EXACTLY ^0.8.20

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract LiveStocXToken is ERC20 {
    string public ventureTokenId; // e.g., "CBP-DairyFarm-001"

    constructor(string memory _ventureTokenId, uint256 initialSupply) ERC20("LiveStocX", "LSX") {
        ventureTokenId = _ventureTokenId;
        _mint(msg.sender, initialSupply); // Mints initialSupply to the deployer (msg.sender)
    }
}