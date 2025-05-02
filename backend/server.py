from fastapi import FastAPI, HTTPException, Body, Depends, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn
import os
import logging
from pathlib import Path
import hashlib
import json
import time
import uuid
import asyncio
import sys
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field

# Add the current directory to the Python path to allow relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# /backend
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL')
db_name = os.environ.get('DB_NAME', 'genesischain')
client = AsyncIOMotorClient(mongo_url)
db = client[db_name]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import our quantum-resistant blockchain modules after database setup
from blockchain.blockchain import Blockchain, Block, Transaction, SecurityLevel
from blockchain.wallet import QuantumWallet, create_wallet, get_wallet_balance
from blockchain.mining import mine_block, calculate_hash, calculate_proof_of_work, QuantumMiner
from quantum_security import SecurityLevel, create_default_security_manager

# API Models for request/response
class TransactionRequest(BaseModel):
    sender: str
    recipient: str
    amount: float
    data: Optional[Dict[str, Any]] = None
    transaction_type: str = "transfer"
    fee: float = 0.0
    
class BlockResponse(BaseModel):
    index: int
    timestamp: float
    transactions: List[Dict[str, Any]]
    hash: str
    previous_hash: str
    merkle_root: str
    nonce: int
    difficulty: int
    
class WalletRequest(BaseModel):
    name: Optional[str] = None
    security_level: str = "STANDARD"
    
class WalletResponse(BaseModel):
    id: str
    name: str
    address: str
    public_keys: Dict[str, str]
    created_at: float
    
class SecurityInfoResponse(BaseModel):
    active_security_level: str
    available_levels: List[str]
    active_security_features: List[str]
    quantum_resistance_status: Dict[str, Any]

# Initialize our quantum-resistant blockchain
genesis_chain = Blockchain(security_level=SecurityLevel.STANDARD)

# In-memory wallet store (in production, this would be properly secured)
wallets = {}

# Initialize a miner for the blockchain
quantum_miner = None

# Store blockchain in database
async def save_blockchain_state():
    """Save the current blockchain state to MongoDB"""
    chain_dict = genesis_chain.to_dict()
    
    # Store the blockchain state in the database
    await db.blockchain_state.update_one(
        {"_id": "current_state"},
        {"$set": chain_dict},
        upsert=True
    )
    logger.info(f"Blockchain state saved, length: {len(genesis_chain.chain)}")

async def load_blockchain_state():
    """Load blockchain state from MongoDB"""
    global genesis_chain
    
    # Check if there's a saved state
    state = await db.blockchain_state.find_one({"_id": "current_state"})
    
    if state:
        # Rebuild the blockchain from the saved state
        # Remove MongoDB _id field before reconstruction
        del state["_id"]
        genesis_chain = Blockchain.from_dict(state)
        logger.info(f"Blockchain state loaded, length: {len(genesis_chain.chain)}")
    else:
        # No existing state, use the new chain
        logger.info("No existing blockchain state found, using new chain")
        await save_blockchain_state()

# Routes for the quantum-resistant blockchain
@app.get("/api")
async def root():
    return {
        "message": "GenesisChain Quantum-Resistant Blockchain API",
        "version": "1.0.0",
        "chain_length": len(genesis_chain.chain),
        "security_level": genesis_chain.security_manager.security_level.name
    }

@app.get("/api/chain")
async def get_chain():
    """Get the current blockchain"""
    blocks = [block.to_dict() for block in genesis_chain.chain]
    return {
        "chain": blocks,
        "length": len(blocks),
        "security_level": genesis_chain.security_manager.security_level.name
    }

@app.get("/api/chain/block/{index}")
async def get_block_by_index(index: int):
    """Get a specific block by index"""
    block = genesis_chain.get_block_by_index(index)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    
    return BlockResponse(**block.to_dict())

@app.get("/api/chain/block/hash/{block_hash}")
async def get_block_by_hash(block_hash: str):
    """Get a specific block by hash"""
    block = genesis_chain.get_block_by_hash(block_hash)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    
    return BlockResponse(**block.to_dict())

@app.post("/api/transactions/new")
async def new_transaction(transaction_request: TransactionRequest = Body(...)):
    """Create a new transaction"""
    
    # Check if sending wallet exists
    sender_wallet = wallets.get(transaction_request.sender)
    if not sender_wallet:
        raise HTTPException(status_code=404, detail="Sender wallet not found")
    
    # Create transaction
    transaction = Transaction(
        sender=sender_wallet.address,
        recipient=transaction_request.recipient,
        amount=transaction_request.amount,
        data=transaction_request.data or {},
        transaction_type=transaction_request.transaction_type,
        fee=transaction_request.fee
    )
    
    # Sign the transaction with the sender's wallet
    transaction.sign(
        {
            "quantum_resistant": sender_wallet.key_pairs["quantum_resistant"].private_key
        },
        genesis_chain.security_manager
    )
    
    # Add to blockchain's pending transactions
    success = genesis_chain.add_transaction(transaction)
    
    if not success:
        raise HTTPException(status_code=400, detail="Transaction verification failed")
    
    # Save current state after transaction added
    await save_blockchain_state()
    
    return JSONResponse(
        status_code=201,
        content={
            "message": f"Transaction will be added to a future block",
            "transaction_id": transaction.id,
            "pending_transactions": len(genesis_chain.pending_transactions)
        }
    )

@app.post("/api/mine")
async def mine_new_block(miner_address: str):
    """Mine a new block with pending transactions"""
    
    # Check if miner wallet exists
    if miner_address not in wallets:
        raise HTTPException(status_code=404, detail="Miner wallet not found")
    
    miner_wallet = wallets[miner_address]
    
    # Mine a new block
    new_block = genesis_chain.mine_pending_transactions(miner_wallet.address)
    
    if not new_block:
        raise HTTPException(status_code=400, detail="Mining failed")
    
    # Save updated blockchain state
    await save_blockchain_state()
    
    return {
        "message": "New Block Forged",
        "block": BlockResponse(**new_block.to_dict()),
        "miner_reward": 1.0,  # Simplified reward amount
        "transactions_processed": len(new_block.transactions)
    }

@app.get("/api/transactions")
async def get_pending_transactions():
    """Get all pending transactions"""
    return {
        "pending_transactions": [tx.to_dict() for tx in genesis_chain.pending_transactions],
        "count": len(genesis_chain.pending_transactions)
    }

@app.get("/api/transactions/{address}")
async def get_address_transactions(address: str):
    """Get transaction history for an address"""
    history = genesis_chain.get_transaction_history(address)
    return {
        "address": address,
        "transactions": history,
        "count": len(history)
    }

@app.get("/api/transaction/{transaction_id}")
async def get_transaction(transaction_id: str):
    """Get a specific transaction by ID"""
    tx = genesis_chain.get_transaction_by_id(transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return tx

# Wallet Management API
@app.post("/api/wallets/create")
async def create_new_wallet(wallet_request: WalletRequest = Body(...)):
    """Create a new quantum-resistant wallet"""
    
    # Map string security level to enum
    security_level_map = {
        "STANDARD": SecurityLevel.STANDARD,
        "HIGH": SecurityLevel.HIGH,
        "VERY_HIGH": SecurityLevel.VERY_HIGH,
        "QUANTUM": SecurityLevel.QUANTUM,
        "PARANOID": SecurityLevel.PARANOID
    }
    
    security_level = security_level_map.get(
        wallet_request.security_level, 
        SecurityLevel.STANDARD
    )
    
    # Create the wallet
    wallet = create_wallet(wallet_request.name, security_level)
    
    # Store in our in-memory wallet store
    wallets[wallet.id] = wallet
    
    # Also store in database for persistence
    await db.wallets.insert_one(wallet.to_dict(include_private_keys=True))
    
    # Return wallet info without private keys
    return WalletResponse(
        id=wallet.id,
        name=wallet.name,
        address=wallet.address,
        public_keys=wallet.to_dict()["public_keys"],
        created_at=wallet.created_at
    )

@app.get("/api/wallets")
async def list_wallets():
    """List all wallets"""
    wallet_list = []
    
    for wallet_id, wallet in wallets.items():
        wallet_list.append({
            "id": wallet.id,
            "name": wallet.name,
            "address": wallet.address,
            "created_at": wallet.created_at,
            "balance": genesis_chain.get_balance(wallet.address)
        })
    
    return {"wallets": wallet_list, "count": len(wallet_list)}

@app.get("/api/wallets/{wallet_id}")
async def get_wallet(wallet_id: str):
    """Get wallet details"""
    if wallet_id not in wallets:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    wallet = wallets[wallet_id]
    
    return {
        "id": wallet.id,
        "name": wallet.name,
        "address": wallet.address,
        "public_keys": wallet.to_dict()["public_keys"],
        "created_at": wallet.created_at,
        "balance": genesis_chain.get_balance(wallet.address),
        "security_level": genesis_chain.security_manager.security_level.name
    }

@app.get("/api/wallets/{wallet_id}/balance")
async def get_wallet_balance(wallet_id: str):
    """Get wallet balance"""
    if wallet_id not in wallets:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    wallet = wallets[wallet_id]
    balance = genesis_chain.get_balance(wallet.address)
    
    return {
        "wallet_id": wallet.id,
        "address": wallet.address,
        "balance": balance
    }

# Security Management API
@app.get("/api/security/info")
async def get_security_info():
    """Get information about the current security configuration"""
    security_level = genesis_chain.security_manager.security_level
    
    # Get active security layers
    active_layers = []
    for layer in genesis_chain.security_manager.layers:
        if layer["enabled"]:
            active_layers.append(layer["name"])
    
    # Get active verification layers
    active_verifications = []
    for layer in genesis_chain.security_manager.verification_layers:
        if layer["enabled"]:
            active_verifications.append(layer["name"])
    
    return {
        "active_security_level": security_level.name,
        "available_levels": [level.name for level in SecurityLevel],
        "active_security_features": active_layers,
        "active_verification_methods": active_verifications,
        "quantum_resistance_status": {
            "algorithms": ["FALCON", "SPHINCS+", "Kyber", "Dilithium"],
            "security_bits": 256,
            "status": "Enabled" if security_level.value >= SecurityLevel.STANDARD.value else "Disabled"
        }
    }

@app.put("/api/security/level/{level}")
async def update_security_level(level: str):
    """Update the blockchain's security level"""
    # Map string security level to enum
    security_level_map = {
        "STANDARD": SecurityLevel.STANDARD,
        "HIGH": SecurityLevel.HIGH,
        "VERY_HIGH": SecurityLevel.VERY_HIGH,
        "QUANTUM": SecurityLevel.QUANTUM,
        "PARANOID": SecurityLevel.PARANOID
    }
    
    if level not in security_level_map:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid security level. Valid levels are: {list(security_level_map.keys())}"
        )
    
    # Update the security level
    genesis_chain.update_security_level(security_level_map[level])
    
    # Save the updated chain state
    await save_blockchain_state()
    
    return {
        "message": f"Security level updated to {level}",
        "enabled_features": [
            layer["name"] for layer in genesis_chain.security_manager.layers
            if layer["enabled"]
        ]
    }

# Function to load wallets from database on startup
async def load_wallets_from_db():
    """Load all wallets from the database"""
    global wallets
    
    wallet_docs = await db.wallets.find().to_list(length=None)
    
    for wallet_doc in wallet_docs:
        try:
            # Remove MongoDB _id field
            if "_id" in wallet_doc:
                del wallet_doc["_id"]
            
            # Create wallet from saved data
            wallet = QuantumWallet.from_dict(wallet_doc)
            
            # Add to in-memory wallet store
            wallets[wallet.id] = wallet
            
            logger.info(f"Loaded wallet: {wallet.name} ({wallet.id})")
        except Exception as e:
            logger.error(f"Error loading wallet: {str(e)}")
    
    logger.info(f"Loaded {len(wallets)} wallets from database")

@app.on_event("startup")
async def startup_event():
    """Initialize the blockchain and load data on startup"""
    global quantum_miner
    
    logger.info("Starting up GenesisChain Quantum-Resistant API")
    
    # Load blockchain state
    await load_blockchain_state()
    
    # Load wallets
    await load_wallets_from_db()
    
    # Create a default wallet if none exist
    if not wallets:
        default_wallet = create_wallet("Default Wallet")
        wallets[default_wallet.id] = default_wallet
        await db.wallets.insert_one(default_wallet.to_dict(include_private_keys=True))
        logger.info(f"Created default wallet: {default_wallet.id}")
    
    # Initialize the miner with the first wallet
    first_wallet_id = next(iter(wallets))
    miner_address = wallets[first_wallet_id].address
    quantum_miner = QuantumMiner(miner_address)
    
    logger.info(f"Initialization complete. Chain length: {len(genesis_chain.chain)}")

@app.on_event("shutdown")
async def shutdown_db_client():
    """Clean up on shutdown"""
    # Save final blockchain state
    await save_blockchain_state()
    
    # Stop the miner if running
    if quantum_miner and quantum_miner.running:
        quantum_miner.stop_mining()
    
    # Close the database connection
    client.close()
    
    logger.info("Shutdown complete")

@app.on_event("startup")
async def startup_event():
    """Initialize the blockchain and load state on startup"""
    logger.info("Starting up GenesisChain Quantum-Resistant API")
    await load_blockchain_state()

@app.on_event("shutdown")
async def shutdown_event():
    """Save blockchain state and cleanup on shutdown"""
    logger.info("Shutting down GenesisChain API")
    await save_blockchain_state()
    client.close()

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)