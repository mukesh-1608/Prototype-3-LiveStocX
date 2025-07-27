// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract CattleToken is ERC20 {
    struct TokenDetails {
        uint256 assetId;
        address farmer;
        string productType;
        uint256 pricePerToken;
    }
    
    mapping(uint256 => TokenDetails) public tokenDetails;
    mapping(uint256 => uint256) public assetToTokenId;
    uint256 public nextTokenId;
    
    constructor() ERC20("CattleAssetToken", "CAT") {}
    
    function createAssetToken(
        uint256 _assetId,
        address _farmer,
        string memory _productType,
        uint256 _supply,
        uint256 _pricePerToken
    ) public returns (uint256) {
        uint256 tokenId = nextTokenId++;
        
        tokenDetails[tokenId] = TokenDetails({
            assetId: _assetId,
            farmer: _farmer,
            productType: _productType,
            pricePerToken: _pricePerToken
        });
        
        assetToTokenId[_assetId] = tokenId;
        _mint(_farmer, _supply);
        
        return tokenId;
    }
}
