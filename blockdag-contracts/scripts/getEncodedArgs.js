// getEncodedArgs.js (in your blockdag-contracts/scripts/ directory)
const hre = require("hardhat");

async function main() {
  // Get the contract factory for LiveStocXToken
  const LiveStocXToken = await hre.ethers.getContractFactory("LiveStocXToken");

  // Define your constructor arguments exactly as they were when you deployed
  const ventureTokenId = "Milk";
  const initialSupply = hre.ethers.parseUnits("1000", 18); // 1000 tokens with 18 decimals

  // ABI-encode the constructor arguments
  const encodedArguments = LiveStocXToken.interface.encodeDeploy([
    ventureTokenId,
    initialSupply
  ]);

  console.log("--------------------------------------------------");
  console.log("ABI-Encoded Constructor Arguments (COPY THIS PART):");
  // The `encodedArguments` string includes the contract bytecode prefix.
  // Etherscan-like explorers usually want *only* the constructor arguments part.
  // This is often found by taking the last 64 characters (32 bytes * 2 hex chars per byte) for each argument,
  // but the safest way is to know the bytecode length and skip it.
  // A simpler method is to just take the part after the known bytecode if the explorer requires it.
  // However, many explorers are smart enough to just take the raw constructor arguments (JSON array or individual fields).

  // For this type of input field, it usually wants *only* the encoded arguments, not the bytecode prefix.
  // We'll calculate the expected length of the bytecode based on the deployed contract:
  const bytecode = LiveStocXToken.bytecode;
  const constructorArgumentsOnly = encodedArguments.substring(bytecode.length);
  console.log(constructorArgumentsOnly);
  console.log("--------------------------------------------------");

  console.log("\nIf the explorer has separate fields for arguments, use these:");
  console.log(`_ventureTokenId (string): "${ventureTokenId}"`);
  console.log(`initialSupply (uint256): "${initialSupply.toString()}"`); // Use .toString() for BigNumber
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });