// deploy.js (in blockdag-contracts/scripts/) - Forces a new deployment with Milk_V7
const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners(); // Get the signer (your MetaMask account)
  // Fetch the latest confirmed nonce from the network. This is crucial for avoiding "nonce too low" or "replacement transaction underpriced" errors.
  const currentNonce = await deployer.provider.getTransactionCount(deployer.address, 'latest'); 

  const LiveStocXToken = await hre.ethers.getContractFactory("LiveStocXToken");

  // Constructor arguments for your LiveStocXToken contract
  const ventureTokenId = "Milk_V7"; // <--- CHANGED THIS AGAIN to guarantee a new, unique deployment
  const initialSupply = hre.ethers.parseUnits("1000", 18); // 1000 tokens with 18 decimals

  console.log(`Deploying LiveStocXToken with ventureTokenId: "${ventureTokenId}" and initialSupply: ${initialSupply.toString()}...`);
  console.log(`Using deployer address: ${deployer.address}`);
  console.log(`Latest confirmed nonce for deployer: ${currentNonce}`);
  console.log(`Attempting deployment with nonce: ${currentNonce}`); // Use this nonce for the new transaction

  try {
    const liveStocXToken = await LiveStocXToken.deploy(
      ventureTokenId,
      initialSupply,
      { nonce: currentNonce } // Explicitly pass the current confirmed nonce
    );

    await liveStocXToken.waitForDeployment();

    const newContractAddress = liveStocXToken.target;
    const deploymentTxHash = liveStocXToken.deploymentTransaction().hash;

    console.log(`LiveStocXToken deployed to: ${newContractAddress}`);
    console.log(`Transaction hash: ${deploymentTxHash}`);

    // --- ATTEMPT PROGRAMMATIC VERIFICATION (will likely fail without API key) ---
    console.log("\nAttempting programmatic verification...");
    try {
      await hre.run("verify:verify", {
        address: newContractAddress,
        constructorArguments: [
          ventureTokenId,
          initialSupply
        ],
      });
      console.log("Contract verified successfully!");
    } catch (verifyError) {
      console.error("Programmatic verification failed (as expected without API key):", verifyError.message);
      console.log("\n--- IMPORTANT: Manual Verification Details ---");
      console.log(`Please perform manual verification on the explorer using the **Standard JSON Input** method:`);
      console.log(`  Contract Address: ${newContractAddress}`);
      console.log(`  Compiler Version: 0.8.20 (from artifacts/build-info)`);
      console.log(`  Optimizer: Disabled (runs: 200)`);
      console.log(`  EVM Version: Paris`);
      console.log(`  Constructor Args (JSON array): ["${ventureTokenId}", "${initialSupply.toString()}"]`);
      console.log(`  Explorer URL: https://primordial.bdagscan.com/contract/${newContractAddress}`);
      console.log("  Find your build-info JSON in: D:\\BlockDAG-LiveStocX-Prototype\\blockdag-contracts\\artifacts\\build-info\\");
      console.log("  **Paste the ENTIRE content of the build-info JSON into the source code input.**");
      console.log("-----------------------------------------------");
    }

  } catch (deployError) {
    console.error("Deployment failed:", deployError.message);
    process.exit(1); // Exit with error if deployment itself fails
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });