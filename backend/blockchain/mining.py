"""
Blockchain Mining Module

This module implements mining functionality for the GenesisChain blockchain.
It includes:
1. Functions for calculating block hashes
2. Proof-of-work algorithm
3. Mining rewards and incentives

The implementation includes quantum-resistant security features.
"""

import hashlib
import json
import threading
import time
from typing import Dict, Any, Optional, List, Tuple

# Import quantum security for enhanced entropy
from ..quantum_security import (
    QuantumRandomNumberGenerator,
    generate_secure_seed
)


def calculate_hash(block_data: Dict[str, Any]) -> str:
    """
    Calculate a hash for a block using quantum-resistant hashing.
    
    Args:
        block_data: The block data to hash
        
    Returns:
        The calculated hash
    """
    # Convert block data to a string, ensuring consistent ordering
    block_string = json.dumps(block_data, sort_keys=True)
    
    # Use SHA3-256 for quantum resistance
    return hashlib.sha3_256(block_string.encode()).hexdigest()


def calculate_merkle_root(transactions: List[Dict[str, Any]]) -> str:
    """
    Calculate the Merkle root of a list of transactions.
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        The Merkle root hash
    """
    if not transactions:
        return hashlib.sha3_256("empty".encode()).hexdigest()
    
    # Extract transaction hashes
    tx_hashes = [tx.get("hash", calculate_hash(tx)) for tx in transactions]
    
    # Implement a simple Merkle tree
    while len(tx_hashes) > 1:
        next_level = []
        
        # Process pairs of hashes
        for i in range(0, len(tx_hashes), 2):
            if i + 1 < len(tx_hashes):
                combined = tx_hashes[i] + tx_hashes[i + 1]
            else:
                # Odd number of hashes, duplicate the last one
                combined = tx_hashes[i] + tx_hashes[i]
            
            next_level.append(hashlib.sha3_256(combined.encode()).hexdigest())
        
        tx_hashes = next_level
    
    return tx_hashes[0]


def calculate_proof_of_work(block_data: Dict[str, Any], difficulty: int) -> Tuple[int, str]:
    """
    Calculate a valid proof-of-work for a block.
    
    Args:
        block_data: The block data to find proof for
        difficulty: The number of leading zeros required
        
    Returns:
        Tuple of (nonce, hash) that satisfies the difficulty requirement
    """
    # Target pattern of leading zeros
    target = '0' * difficulty
    
    # Create a copy of block data to modify the nonce
    data = block_data.copy()
    nonce = 0
    
    # Use quantum random number generator for better starting points
    qrng = QuantumRandomNumberGenerator()
    nonce = qrng.get_random_int(0, 1000000)  # Start at random point
    data["nonce"] = nonce
    
    # Calculate initial hash
    block_hash = calculate_hash(data)
    
    # Keep trying until we find a hash with the target number of leading zeros
    while block_hash[:difficulty] != target:
        nonce += 1
        data["nonce"] = nonce
        block_hash = calculate_hash(data)
        
        # Optional: every so often, introduce quantum randomness
        if nonce % 10000 == 0:
            quantum_bump = qrng.get_random_int(1, 100)
            nonce += quantum_bump
            data["nonce"] = nonce
    
    return nonce, block_hash


def mine_block(block_data: Dict[str, Any], difficulty: int, 
              max_time: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """
    Mine a block with proof-of-work.
    
    Args:
        block_data: The block data to mine
        difficulty: The mining difficulty (leading zeros)
        max_time: Maximum time to mine in seconds, or None for unlimited
        
    Returns:
        The mined block with proof-of-work, or None if time limit reached
    """
    # Start timing
    start_time = time.time()
    
    # Set up result placeholder for threading
    result = {"mined": False, "block": None}
    
    # Function to do the actual mining in a thread
    def mining_thread():
        nonlocal result
        
        try:
            # Calculate proof-of-work
            nonce, block_hash = calculate_proof_of_work(block_data, difficulty)
            
            # Add the nonce and hash to the block
            mined_block = block_data.copy()
            mined_block["nonce"] = nonce
            mined_block["hash"] = block_hash
            mined_block["mining_time"] = time.time() - start_time
            
            # Set the result if not timed out
            if not max_time or (time.time() - start_time) < max_time:
                result["mined"] = True
                result["block"] = mined_block
        except Exception as e:
            print(f"Mining error: {str(e)}")
    
    # Start mining in a thread so we can implement timeout
    thread = threading.Thread(target=mining_thread)
    thread.daemon = True
    thread.start()
    
    # Wait for mining to complete or timeout
    if max_time:
        thread.join(max_time)
        if thread.is_alive():
            # Mining took too long
            return None
    else:
        # Wait indefinitely
        thread.join()
    
    # Return the result
    return result["block"] if result["mined"] else None


def calculate_mining_reward(block_height: int, difficulty: int) -> float:
    """
    Calculate the mining reward for a block.
    
    Args:
        block_height: The height/index of the block in the chain
        difficulty: The mining difficulty
        
    Returns:
        The mining reward amount
    """
    # Base reward
    base_reward = 50.0
    
    # Halve the reward every 210,000 blocks (similar to Bitcoin)
    halvings = block_height // 210000
    reward = base_reward / (2 ** halvings)
    
    # Adjust for difficulty (simplified)
    difficulty_adjustment = 1 + (difficulty - 4) * 0.1  # +10% per difficulty level above 4
    
    return max(0.00001, reward * difficulty_adjustment)  # Minimum reward


def adjust_difficulty(last_blocks: List[Dict[str, Any]], 
                     target_time: int = 600) -> int:
    """
    Adjust mining difficulty based on recent block times.
    
    Args:
        last_blocks: List of recent blocks
        target_time: Target time per block in seconds
        
    Returns:
        The new difficulty level
    """
    if len(last_blocks) < 10:
        # Not enough blocks to adjust, use default
        return 4
    
    # Calculate average time between recent blocks
    times = [block["timestamp"] for block in last_blocks]
    time_diffs = [times[i] - times[i-1] for i in range(1, len(times))]
    avg_time = sum(time_diffs) / len(time_diffs)
    
    # Current difficulty
    current_difficulty = last_blocks[-1].get("difficulty", 4)
    
    # Adjust difficulty based on average time
    if avg_time < target_time * 0.5:
        # Blocks being mined too quickly, increase difficulty
        return current_difficulty + 1
    elif avg_time > target_time * 2:
        # Blocks being mined too slowly, decrease difficulty
        return max(1, current_difficulty - 1)  # Minimum difficulty of 1
    else:
        # Within acceptable range, keep current difficulty
        return current_difficulty


class QuantumMiner:
    """
    A miner that uses quantum-enhanced techniques for improved efficiency.
    """
    
    def __init__(self, miner_address: str, difficulty: int = 4):
        """
        Initialize a new quantum miner.
        
        Args:
            miner_address: The address to receive mining rewards
            difficulty: Initial mining difficulty
        """
        self.miner_address = miner_address
        self.difficulty = difficulty
        self.running = False
        self.mined_blocks = 0
        self.total_mining_time = 0
        self.qrng = QuantumRandomNumberGenerator()
    
    def start_mining(self, blockchain) -> None:
        """
        Start the mining process for a blockchain.
        
        Args:
            blockchain: The blockchain to mine on
        """
        self.running = True
        
        # Mining loop
        while self.running:
            # Get the latest block to determine the next block to mine
            latest_block = blockchain.get_latest_block()
            
            # Prepare transactions to include in the block
            pending_tx = blockchain.pending_transactions[:10]  # Limit to 10 transactions per block
            
            # Create mining reward transaction
            reward_amount = calculate_mining_reward(latest_block.index + 1, self.difficulty)
            reward_tx = {
                "sender": "0",  # System address for rewards
                "recipient": self.miner_address,
                "amount": reward_amount,
                "data": {"message": "Mining Reward"},
                "type": "reward",
                "timestamp": time.time(),
                "nonce": int(time.time() * 1000),
                "id": f"reward_{latest_block.index + 1}_{int(time.time())}"
            }
            reward_tx["hash"] = calculate_hash(reward_tx)
            
            # Prepare all transactions for the block
            block_transactions = [tx.to_dict() for tx in pending_tx] + [reward_tx]
            
            # Create block data
            block_data = {
                "index": latest_block.index + 1,
                "previous_hash": latest_block.hash,
                "transactions": block_transactions,
                "timestamp": time.time(),
                "merkle_root": calculate_merkle_root(block_transactions),
                "difficulty": self.difficulty
            }
            
            # Mine the block
            start_time = time.time()
            mined_block = mine_block(block_data, self.difficulty)
            mining_time = time.time() - start_time
            
            if mined_block and self.running:
                # Add the block to the blockchain
                # Note: In a real implementation, we would need to handle concurrent updates
                # and validate the block against the current chain state
                from .blockchain import Block, Transaction
                
                # Convert dictionary back to Block object
                transactions = [
                    Transaction.from_dict(tx) if isinstance(tx, dict) else tx
                    for tx in mined_block["transactions"]
                ]
                
                new_block = Block(
                    index=mined_block["index"],
                    previous_hash=mined_block["previous_hash"],
                    transactions=transactions,
                    timestamp=mined_block["timestamp"],
                    nonce=mined_block["nonce"]
                )
                
                new_block.hash = mined_block["hash"]
                new_block.merkle_root = mined_block["merkle_root"]
                new_block.difficulty = mined_block["difficulty"]
                
                # Add to chain if valid
                if new_block.verify(blockchain.security_manager):
                    blockchain.chain.append(new_block)
                    
                    # Remove the mined transactions from pending
                    for tx in pending_tx:
                        if tx in blockchain.pending_transactions:
                            blockchain.pending_transactions.remove(tx)
                    
                    # Update mining stats
                    self.mined_blocks += 1
                    self.total_mining_time += mining_time
                    
                    print(f"Block mined: {new_block.hash}")
                    print(f"Mining time: {mining_time:.2f} seconds")
                    
                    # Adjust difficulty periodically
                    if self.mined_blocks % 10 == 0:
                        last_blocks = [b.to_dict() for b in blockchain.chain[-10:]]
                        self.difficulty = adjust_difficulty(last_blocks)
                        print(f"Adjusted difficulty to {self.difficulty}")
                else:
                    print("Mined block failed verification, discarding")
            
            # Small delay before attempting to mine the next block
            # to reduce resource usage
            time.sleep(0.1)
    
    def stop_mining(self) -> None:
        """Stop the mining process"""
        self.running = False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get mining statistics.
        
        Returns:
            Dictionary of mining statistics
        """
        avg_time = self.total_mining_time / max(1, self.mined_blocks)
        
        return {
            "miner_address": self.miner_address,
            "blocks_mined": self.mined_blocks,
            "total_mining_time": self.total_mining_time,
            "average_mining_time": avg_time,
            "current_difficulty": self.difficulty,
            "hashrate_estimate": 2**self.difficulty / max(1, avg_time)  # Very rough estimate
        }