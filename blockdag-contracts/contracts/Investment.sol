// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IBDAG {
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract Investment {
    IBDAG public bdagToken;
    address public cattleTokenContract;

    struct InvestmentInfo {  // <-- Renamed struct
        address investor;
        uint256 assetId;
        uint256 tokenAmount;
        uint256 bdagAmount;
        uint256 timestamp;
    }

    mapping(address => InvestmentInfo[]) public investorHistory;
    mapping(uint256 => uint256) public totalInvested;

    event InvestmentMade(address indexed investor, uint256 indexed assetId, uint256 tokenAmount, uint256 bdagAmount);

    constructor(address _bdagToken, address _cattleToken) {
        bdagToken = IBDAG(_bdagToken);
        cattleTokenContract = _cattleToken;
    }

    function investInAsset(
        uint256 _assetId,
        uint256 _tokenAmount,
        uint256 _bdagAmount,
        address _farmer
    ) public {
        require(bdagToken.transferFrom(msg.sender, _farmer, _bdagAmount), "BDAG transfer failed");

        InvestmentInfo memory newInvestment = InvestmentInfo({ // <-- Updated struct name
            investor: msg.sender,
            assetId: _assetId,
            tokenAmount: _tokenAmount,
            bdagAmount: _bdagAmount,
            timestamp: block.timestamp
        });

        investorHistory[msg.sender].push(newInvestment);
        totalInvested[_assetId] += _bdagAmount;

        emit InvestmentMade(msg.sender, _assetId, _tokenAmount, _bdagAmount);
    }
}
