// hardhat.config.js (COMPLETE, AGGRESSIVE GAS PRICE)
require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: false,
        runs: 200
      },
      viaIR: false,
    },
  },
  networks: {
    bdagTestnet: {
      url: process.env.BDAG_TESTNET_RPC_URL || "https://rpc.primordial.bdagscan.com",
      accounts: process.env.FARMER_PRIVATE_KEY ? [process.env.FARMER_PRIVATE_KEY] : [],
      chainId: 1043,
      gasPrice: 500000000000, // <--- INCREASED GAS PRICE TO 500 Gwei (very aggressive)
      timeout: 120000, // Increased timeout to 120 seconds for slow testnet
      gas: 3000000, // Increased gas limit slightly, common for deployments
    },
  },
  etherscan: {
    apiKey: {
      bdagTestnet: ""
    },
    customChains: [
      {
        network: "bdagTestnet",
        chainId: 1043,
        urls: {
          apiURL: "https://explorer.primordial.bdagscan.com/api",
          browserURL: "https://primordial.bdagscan.com/"
        }
      }
    ]
  },
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  }
};