from fastapi import FastAPI, HTTPException, Body
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
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

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

# Models
class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: float
    timestamp: float = Field(default_factory=time.time)
    transaction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
class Block(BaseModel):
    index: int
    timestamp: float
    transactions: List[Transaction]
    proof: int
    previous_hash: str
    block_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
class Blockchain(BaseModel):
    chain: List[Block] = []
    current_transactions: List[Transaction] = []
    
    class Config:
        arbitrary_types_allowed = True

# Initialize blockchain
blockchain = Blockchain(chain=[], current_transactions=[])

# Create genesis block
async def create_genesis_block():
    # Check if blockchain already exists in database
    existing_blocks = await db.blocks.count_documents({})
    
    if existing_blocks == 0:
        # Create genesis block if blockchain doesn't exist
        genesis_block = Block(
            index=1,
            timestamp=time.time(),
            transactions=[],
            proof=100,
            previous_hash="1"
        )
        
        # Insert genesis block to database
        await db.blocks.insert_one(genesis_block.dict())
        
        logger.info("Genesis block created")
    else:
        logger.info("Blockchain already exists, skipping genesis block creation")

# Blockchain methods
async def get_last_block():
    last_block = await db.blocks.find_one(
        sort=[("index", -1)]
    )
    return last_block

async def proof_of_work(last_proof: int) -> int:
    """
    Simple Proof of Work Algorithm:
    - Find a number p' such that hash(pp') contains 4 leading zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """
    proof = 0
    while not valid_proof(last_proof, proof):
        proof += 1
    return proof

def valid_proof(last_proof: int, proof: int) -> bool:
    """
    Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"

# Routes
@app.get("/api")
async def root():
    return {"message": "GenesisChain API"}

@app.get("/api/chain")
async def get_chain():
    blocks = await db.blocks.find().sort("index", 1).to_list(length=None)
    # Convert ObjectId to string
    for block in blocks:
        block["_id"] = str(block["_id"])
    return {"chain": blocks, "length": len(blocks)}

@app.post("/api/transactions/new")
async def new_transaction(transaction: Transaction = Body(...)):
    # Add a new transaction to the list of transactions
    await db.transactions.insert_one(transaction.dict())
    
    # Also add to current transactions (for next block)
    blockchain.current_transactions.append(transaction)
    
    return JSONResponse(
        status_code=201,
        content={"message": f"Transaction will be added to Block {(await get_last_block())['index'] + 1}"}
    )

@app.get("/api/mine")
async def mine():
    # Get the last block
    last_block = await get_last_block()
    
    # Convert MongoDB ObjectId to string to make it JSON serializable
    if '_id' in last_block:
        last_block['_id'] = str(last_block['_id'])
    
    # Calculate the proof of work
    last_proof = last_block['proof']
    proof = await proof_of_work(last_proof)
    
    # Create a new transaction to award the miner
    miner_transaction = Transaction(
        sender="0",  # "0" signifies that this node has mined a new coin
        recipient="miner-address",  # This would be the miner's address in a real implementation
        amount=1.0
    )
    
    # Store miner transaction in database
    await db.transactions.insert_one(miner_transaction.dict())
    
    # Add to current transactions
    blockchain.current_transactions.append(miner_transaction)
    
    # Collect current transactions
    current_transactions = blockchain.current_transactions.copy()
    blockchain.current_transactions = []
    
    # Create a new Block - first create a serializable version of last_block
    # by removing ObjectId
    clean_last_block = {k: v for k, v in last_block.items() if k != '_id'}
    previous_hash = hashlib.sha256(json.dumps(clean_last_block, sort_keys=True).encode()).hexdigest()
    
    block = Block(
        index=last_block['index'] + 1,
        timestamp=time.time(),
        transactions=current_transactions,
        proof=proof,
        previous_hash=previous_hash,
    )
    
    # Reset current transactions
    blockchain.current_transactions = []
    
    # Save the new block to database
    block_dict = block.dict()
    await db.blocks.insert_one(block_dict)
    
    # Also save all transactions as confirmed
    for transaction in current_transactions:
        await db.transactions.update_one(
            {"transaction_id": transaction.transaction_id},
            {"$set": {"confirmed": True, "block_id": block.block_id}}
        )
    
    return {
        "message": "New Block Forged",
        "index": block.index,
        "transactions": [tx.dict() for tx in current_transactions],
        "proof": block.proof,
        "previous_hash": block.previous_hash,
    }

@app.get("/api/transactions")
async def get_transactions():
    transactions = await db.transactions.find().to_list(length=None)
    # Convert ObjectId to string
    for tx in transactions:
        tx["_id"] = str(tx["_id"])
    return {"transactions": transactions}

# Self-replication mechanism (simplified version)
@app.post("/api/data-input")
async def process_data_input(data: Dict[str, Any] = Body(...)):
    """
    This endpoint receives external data, hashes it, and stores it.
    In a full implementation, this would trigger the AI content generation
    and self-replication loop.
    """
    # Generate a hash of the input data
    data_string = json.dumps(data, sort_keys=True)
    data_hash = hashlib.sha256(data_string.encode()).hexdigest()
    
    # Store the data and its hash
    data_record = {
        "original_data": data,
        "hash": data_hash,
        "timestamp": time.time(),
        "processed": False,
        "data_id": str(uuid.uuid4())
    }
    
    await db.data_inputs.insert_one(data_record)
    
    return {
        "message": "Data processed successfully",
        "hash": data_hash,
        "data_id": data_record["data_id"]
    }

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up GenesisChain API")
    await create_genesis_block()

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)
