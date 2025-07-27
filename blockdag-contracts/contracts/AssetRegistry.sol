// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AssetRegistry {
    struct CattleAsset {
        uint256 assetId;
        address farmer;
        string productType; // milk, leather, meat, etc.
        uint256 quantity;
        uint256 qualityGrade;
        string location;
        uint256 timestamp;
        bool isTokenized;
        uint256 tokenSupply;
    }
    
    mapping(uint256 => CattleAsset) public assets;
    mapping(address => uint256[]) public farmerAssets;
    uint256 public nextAssetId;
    
    event AssetRegistered(uint256 indexed assetId, address indexed farmer, string productType);
    event AssetTokenized(uint256 indexed assetId, uint256 tokenSupply);
    
    function registerAsset(
        string memory _productType,
        uint256 _quantity,
        uint256 _qualityGrade,
        string memory _location
    ) public returns (uint256) {
        uint256 assetId = nextAssetId++;
        
        assets[assetId] = CattleAsset({
            assetId: assetId,
            farmer: msg.sender,
            productType: _productType,
            quantity: _quantity,
            qualityGrade: _qualityGrade,
            location: _location,
            timestamp: block.timestamp,
            isTokenized: false,
            tokenSupply: 0
        });
        
        farmerAssets[msg.sender].push(assetId);
        emit AssetRegistered(assetId, msg.sender, _productType);
        
        return assetId;
    }
    
    function tokenizeAsset(uint256 _assetId, uint256 _tokenSupply) public {
        require(assets[_assetId].farmer == msg.sender, "Not asset owner");
        require(!assets[_assetId].isTokenized, "Already tokenized");
        
        assets[_assetId].isTokenized = true;
        assets[_assetId].tokenSupply = _tokenSupply;
        
        emit AssetTokenized(_assetId, _tokenSupply);
    }
}
