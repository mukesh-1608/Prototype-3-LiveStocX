# app.py (FINAL, FRONTEND-READY & TRANSACTION-FOCUSED)
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import time
import uuid
import hashlib
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput, BlockNotFound, TransactionNotFound
import json
import os

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_for_session_management'

FRONTEND_ORIGINS = ['http://127.0.0.1:8000']
CORS(app, supports_credentials=True, origins=FRONTEND_ORIGINS)

# --- BlockDAG Network Configuration (BDAG Testnet - From IDE Deployment) ---
BDAG_TESTNET_RPC_URL = "https://rpc.primordial.bdagscan.com" 
CONTRACT_ADDRESS = "0xfc9d1242e1405788cff3ee4528f9650e271fe951" # <<<--- Your IDE Deployed Contract Address
CONTRACT_ABI = json.loads("""
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_ventureTokenId",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "initialSupply",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "allowance",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "needed",
				"type": "uint256"
			}
		],
		"name": "ERC20InsufficientAllowance",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "balance",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "needed",
				"type": "uint256"
			}
		],
		"name": "ERC20InsufficientBalance",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "approver",
				"type": "address"
			}
		],
		"name": "ERC20InvalidApprover",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "receiver",
				"type": "address"
			}
		],
		"name": "ERC20InvalidReceiver",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			}
		],
		"name": "ERC20InvalidSender",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "ERC20InvalidSpender",
		"type": "error"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "allowance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "decimals",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "ventureTokenId",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
""")

# --- Farmer's Private Key (for signing real transactions) ---
FARMER_PRIVATE_KEY = "2315baf5200d43e163fd88c6f42b9d7dd29c26b9774e1a8d0ba8d1839aa4457b"

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(BDAG_TESTNET_RPC_URL))
contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)

# --- Simulated Data Storage (for backend's internal logs and USD balances) ---
blockdag_transactions = []
token_provenance_log = {}

# --- Simulated User Database (with BDAG wallet addresses) ---
users = {
    'farmer1': {
        'password_hash': hashlib.sha256('farmerpass'.encode()).hexdigest(),
        'role': 'farmer',
        'public_address': "0x025fE15fC7691FF68Da16C920AD186a7dFA2B589" # Your MetaMask address (deployer)
    },
    'investor1': {
        'password_hash': hashlib.sha256('investorpass'.encode()).hexdigest(),
        'role': 'investor',
        'public_address': "0x2D7be42B768C1C8F60a672E901E85B4E0C3aA0B1" # Example investor1 testnet address
    },
    'investor2': {
        'password_hash': hashlib.sha256('investorpass2'.encode()).hexdigest(),
        'role': 'investor',
        'public_address': "0x1A2B3C4D5E6F7A8B9C0D1E2F3A4B5C6D7E8F9A0B" # Example investor2 testnet address
    }
}

# Initial simulated USD balances for UI purposes
investor_balances = {user_id: 1000.0 for user_id in users if users[user_id]['role'] == 'investor'}
investor_balances['farmer1'] = 5000.0


# --- Helper Functions ---
def record_transaction(tx_type, payload, sender_id, on_chain_tx_hash=None):
    transaction = {
        "tx_id": str(uuid.uuid4()),
        "timestamp": int(time.time()),
        "tx_type": tx_type,
        "sender_id": sender_id,
        "signature": on_chain_tx_hash if on_chain_tx_hash else "simulated_signature",
        "payload": payload
    }
    blockdag_transactions.append(transaction)

    token_id = payload.get('token_id')
    if token_id:
        if token_id not in token_provenance_log:
            token_provenance_log[token_id] = []
        token_provenance_log[token_id].append(transaction)

    print(f"Recorded BlockDAG Transaction: {transaction}")
    return transaction

def get_current_user_data():
    user_id = session.get('user_id')
    if user_id and user_id in users:
        return {
            'user_id': user_id,
            'role': session.get('role'),
            'public_address': users[user_id]['public_address']
        }
    return None

def check_role(required_role):
    def decorator(func):
        from functools import wraps
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_data = get_current_user_data()
            if not user_data:
                return jsonify({"message": "Unauthorized: Not logged in"}), 401
            if user_data['role'] != required_role:
                return jsonify({"message": f"Forbidden: Only {required_role}s can perform this action"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


# --- On-Chain Read Functions (with robust error handling and fallback) ---
def get_on_chain_token_details():
    """
    Attempts to retrieve token details from the BlockDAG testnet.
    Provides a hardcoded fallback if live read fails.
    """
    try:
        venture_id = contract.functions.ventureTokenId().call()
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        total_supply_wei = contract.functions.totalSupply().call()
        
        farmer_deployer_address = users['farmer1']['public_address']
        farmer_token_balance_wei = contract.functions.balanceOf(w3.to_checksum_address(farmer_deployer_address)).call()

        price_per_token_usd = 5 # Fixed simulated price for now (not on-chain)

        print("DEBUG: Successfully fetched live token details from BlockDAG.")
        return {
            "name": name,
            "symbol": symbol,
            "total_supply": w3.from_wei(total_supply_wei, 'ether'),
            "price_per_token": price_per_token_usd,
            "venture_token_id": venture_id,
            "current_available": w3.from_wei(farmer_token_balance_wei, 'ether')
        }
    except BadFunctionCallOutput as e:
        print(f"WARNING: get_on_chain_token_details failed (BadFunctionCallOutput). Using fallback. Error: {e}")
        # Fallback to hardcoded details if live read fails
        return {
            "name": "LiveStocX",
            "symbol": "LSX",
            "total_supply": 1000.0,
            "price_per_token": 5,
            "venture_token_id": "Milk_IDE_V1", # Assuming this is your last successful IDE deploy ID
            "current_available": 1000.0 # Initial supply available from farmer if network reads fail
        }
    except Exception as e:
        print(f"WARNING: get_on_chain_token_details failed unexpectedly. Using fallback. Error: {e}")
        # Fallback to hardcoded details
        return {
            "name": "LiveStocX",
            "symbol": "LSX",
            "total_supply": 1000.0,
            "price_per_token": 5,
            "venture_token_id": "Milk_IDE_V1", # Assuming this is your last successful IDE deploy ID
            "current_available": 1000.0 # Initial supply available from farmer if network reads fail
        }

def get_on_chain_user_token_balance(user_address):
    """Retrieves a user's token balance from the smart contract (with fallback)."""
    try:
        balance_wei = contract.functions.balanceOf(w3.to_checksum_address(user_address)).call()
        print(f"DEBUG: Successfully fetched live balance for {user_address} from BlockDAG.")
        return w3.from_wei(balance_wei, 'ether')
    except BadFunctionCallOutput as e:
        print(f"WARNING: get_on_chain_user_token_balance failed (BadFunctionCallOutput). Using fallback. Error: {e}")
        # Fallback to a fixed value if network read fails
        return 0.0 # Default to 0 if we can't read live balance
    except Exception as e:
        print(f"WARNING: get_on_chain_user_token_balance failed unexpectedly. Using fallback. Error: {e}")
        return 0.0


# --- API Endpoints ---
@app.route('/login', methods=['POST'])
def login_route():
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')

    user = users.get(user_id)
    if user and hashlib.sha256(password.encode()).hexdigest() == user['password_hash']:
        session['user_id'] = user_id
        session['role'] = user['role']
        session['public_address'] = user['public_address']
        
        try:
            native_balance_wei = w3.eth.get_balance(w3.to_checksum_address(user['public_address']))
            native_balance_bdag = w3.from_wei(native_balance_wei, 'ether')
        except Exception as e:
            print(f"ERROR (login): Could not fetch native BDAG balance for {user_id}: {e}")
            native_balance_bdag = 0.0

        return jsonify({
            "message": "Logged in successfully",
            "user_id": user_id,
            "role": user['role'],
            "public_address": user['public_address'],
            "balance": round(investor_balances.get(user_id, 0), 2),
            "native_bdag_balance": round(float(native_balance_bdag), 4)
        })
    return jsonify({"message": "Invalid credentials"}), 401


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('public_address', None)
    return jsonify({"message": "Logged out successfully"})

@app.route('/get_user_status', methods=['GET'])
def get_user_status_route():
    user_id = session.get('user_id')
    if user_id:
        user_data = users.get(user_id)
        if user_data:
            try:
                native_balance_wei = w3.eth.get_balance(w3.to_checksum_address(user_data['public_address']))
                native_balance_bdag = w3.from_wei(native_balance_wei, 'ether')
            except Exception as e:
                print(f"ERROR (get_user_status): Could not fetch native BDAG balance for {user_id}: {e}")
                native_balance_bdag = 0.0
            
            return jsonify({
                "logged_in": True,
                "user_id": user_id,
                "role": session.get('role'),
                "public_address": session.get('public_address'),
                "balance": round(investor_balances.get(user_id, 0), 2),
                "native_bdag_balance": round(float(native_balance_bdag), 4)
            })
    return jsonify({"logged_in": False})


@app.route('/create_token', methods=['POST'])
@check_role('farmer')
def create_token_route():
    user_data = get_current_user_data()
    farmer_id = user_data['user_id']
    farmer_public_address = user_data['public_address']

    token_details = get_on_chain_token_details() # Will now use fallback if live read fails
    if not token_details:
        return jsonify({"message": "Failed to retrieve token details (live or fallback). Check console for errors."}), 500
    
    if w3.to_checksum_address(farmer_public_address) != w3.to_checksum_address(users['farmer1']['public_address']):
        return jsonify({"message": "Forbidden: Only the designated farmer (deployer) can manage this token."}), 403

    record_transaction("TOKEN_INITIATED_ON_BDAG", {
        "venture_token_id": token_details['venture_token_id'],
        "name": token_details['name'],
        "symbol": token_details['symbol'],
        "total_supply": float(token_details['total_supply']),
        "price_per_token": float(token_details['price_per_token']),
        "contract_address": CONTRACT_ADDRESS,
        "initiated_by_farmer_id": farmer_id
    }, farmer_id, on_chain_tx_hash=None)

    return jsonify({"message": "Token details retrieved (may be fallback).", "token": token_details}), 200


@app.route('/get_tokens', methods=['GET'])
def get_tokens_route():
    token_details = get_on_chain_token_details() # Will now use fallback if live read fails
    if token_details:
        tokens_info = {
            token_details['venture_token_id']: {
                "total_supply": float(token_details['total_supply']),
                "current_available": float(token_details['current_available']),
                "price_per_token": float(token_details['price_per_token']),
                "farmer_id": users['farmer1']['user_id']
            }
        }
        return jsonify({"tokens": tokens_info})
    return jsonify({"tokens": {}}) # Return empty if details can't be fetched


@app.route('/purchase_token', methods=['POST'])
@check_role('investor')
def purchase_token_route():
    user_data = get_current_user_data()
    data = request.json
    token_id = data.get('token_id')
    investor_id = user_data['user_id']
    investor_public_address = user_data['public_address']
    amount_to_buy_tokens = int(data.get('amount'))

    if not all([token_id, amount_to_buy_tokens]):
        return jsonify({"message": "Missing required fields (token_id, amount)"}), 400
    if amount_to_buy_tokens <= 0:
        return jsonify({"message": "Amount to buy must be a positive number."}), 400

    on_chain_token_details = get_on_chain_token_details() # Will use fallback if live read fails
    if not on_chain_token_details or on_chain_token_details['venture_token_id'] != token_id:
        return jsonify({"message": "Token details unavailable. Cannot proceed with purchase."}), 404

    # The actual checks for available tokens will now also use live reads from the testnet if possible
    current_available_tokens_from_farmer = get_on_chain_user_token_balance(users['farmer1']['public_address'])
    price_per_token_usd = on_chain_token_details['price_per_token'] # Still uses the value from get_on_chain_token_details (live or fallback)

    if current_available_tokens_from_farmer < amount_to_buy_tokens:
        return jsonify({"message": f"Not enough tokens available from farmer on-chain. Available: {current_available_tokens_from_farmer}, Requested: {amount_to_buy_tokens}"}), 400

    cost_usd = amount_to_buy_tokens * float(price_per_token_usd)

    if investor_balances.get(investor_id, 0) < cost_usd:
        return jsonify({"message": f"Investor {investor_id} has insufficient simulated USD funds. Needed: {cost_usd:.2f} USD, Available: {investor_balances.get(investor_id, 0):.2f} USD"}), 400

    # --- Prepare and Send REAL On-Chain Transfer Transaction ---
    try:
        from_address = w3.to_checksum_address(users['farmer1']['public_address'])
        to_address = w3.to_checksum_address(investor_public_address)
        amount_to_transfer_wei = w3.to_wei(amount_to_buy_tokens, 'ether')

        nonce = w3.eth.get_transaction_count(from_address, 'pending')
        gas_price = w3.eth.gas_price

        tx_gas_price = max(gas_price, w3.to_wei(100, 'gwei')) # Ensure at least 100 Gwei

        tx_build = contract.functions.transfer(
            to_address,
            amount_to_transfer_wei
        ).build_transaction({
            'chainId': w3.eth.chain_id,
            'gasPrice': tx_gas_price,
            'from': from_address,
            'nonce': nonce,
            'gas': 200000 
        })

        signed_tx = w3.eth.account.sign_transaction(tx_build, private_key=FARMER_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300) # Increased timeout to 5 minutes
        print(f"On-chain token transfer transaction mined! Hash: {tx_hash.hex()}")
        print(f"Transaction receipt: {receipt}")

        if receipt.status == 0:
            raise Exception(f"On-chain token transfer failed (transaction receipt status 0) for TX: {tx_hash.hex()}")

        # --- Update simulated USD balances (local state) ---
        investor_balances[investor_id] -= cost_usd
        investor_balances['farmer1'] += cost_usd

        record_transaction("PURCHASE_TOKEN_ON_BDAG", {
            "token_id": token_id,
            "investor_id": investor_id,
            "amount_purchased_tokens": amount_to_buy_tokens,
            "total_cost_usd": round(cost_usd, 2),
            "investor_new_simulated_usd_balance": round(investor_balances[investor_id], 2),
            "farmer_simulated_usd_balance": round(investor_balances['farmer1'], 2),
            "on_chain_tx_hash": tx_hash.hex()
        }, investor_id, on_chain_tx_hash=tx_hash.hex())

        return jsonify({
            "message": "Tokens purchased and transferred on BlockDAG!",
            "tx_hash": tx_hash.hex(),
            "investor_holdings": {token_id: get_on_chain_user_token_balance(investor_public_address)}, # Query real balance
            "investor_current_balance": round(investor_balances[investor_id], 2)
        }), 200

    except Exception as e:
        print(f"ERROR: REAL on-chain token purchase failed: {e}")
        return jsonify({"message": f"Failed to complete on-chain token purchase: {str(e)}. Testnet might be unstable or gas too low."}), 500

@app.route('/declare_profit', methods=['POST'])
@check_role('farmer')
def declare_profit_route():
    return jsonify({"message": "Profit declaration/distribution is not implemented in the current smart contract."}), 405

@app.route('/get_transactions', methods=['GET'])
def get_transactions_route():
    return jsonify({"transactions": blockdag_transactions})

@app.route('/get_holdings/<user_id>', methods=['GET'])
def get_holdings_route(user_id):
    user_address = users.get(user_id, {}).get('public_address')
    if not user_address:
        return jsonify({"message": "User not found or no public address associated"}), 404

    on_chain_token_balance = get_on_chain_user_token_balance(user_address) # Query real balance
    
    try:
        native_currency_balance_wei = w3.eth.get_balance(w3.to_checksum_address(user_address))
        native_currency_balance_bdag = w3.from_wei(native_currency_balance_wei, 'ether')
    except Exception as e:
        print(f"ERROR: Could not fetch native BDAG balance for {user_id}: {e}")
        native_currency_balance_bdag = 0.0

    token_details = get_on_chain_token_details() # Attempt to get from BlockDAG testnet
    holdings_data = {
        token_details['venture_token_id']: on_chain_token_balance
    } if token_details else {}

    return jsonify({
        "user_id": user_id,
        "holdings": holdings_data,
        "balance": round(investor_balances.get(user_id, 0), 2), # Simulated USD balance
        "native_bdag_balance": round(float(native_currency_balance_bdag), 4) # Real BDAG testnet balance
    })


@app.route('/get_token_provenance/<token_id>', methods=['GET'])
def get_token_provenance_route(token_id):
    provenance = token_provenance_log.get(token_id, [])
    if not provenance:
        return jsonify({"message": "No provenance found for this token ID."}), 404
    return jsonify({"token_id": token_id, "provenance": provenance})


def connect_to_bdag():
    try:
        if not w3.is_connected():
            raise Exception("Not connected to BDAG Testnet RPC. Check BDAG_TESTNET_RPC_URL.")
        print(f"Connected to BDAG Testnet (Chain ID: {w3.eth.chain_id})")
        
        # This call will test if the contract is reachable and functional
        # Added more specific exception handling for startup
        try:
            contract_name = contract.functions.name().call()
            print(f"SUCCESS: Connected to LiveStocXToken contract '{contract_name}' at {CONTRACT_ADDRESS}")
        except BadFunctionCallOutput as e:
            print(f"WARNING: Contract at {CONTRACT_ADDRESS} does not seem to be LiveStocXToken or returns bad data (BadFunctionCallOutput). Error: {e}")
            print("This might be due to contract not existing or ABI mismatch. Frontend reads might fail.")
        except Exception as e:
            print(f"WARNING: Initial contract name call failed unexpectedly. Error: {e}")
            print("Frontend reads might fail.")
            
    except Exception as e:
        print(f"!!! CRITICAL WARNING: BlockDAG Testnet connection failed at startup: {e}")
        print("No real on-chain interactions will be possible. Check RPC URL and network status.")


if __name__ == '__main__':
    connect_to_bdag() 
    app.run(debug=True, port=5000)