"""
Core Blockchain Implementation Module

This module implements the fundamental blockchain data structures and operations.
It includes:
1. Block class for representing individual blocks
2. Transaction class for representing transactions
3. Blockchain class for managing the overall chain

The implementation includes quantum-resistant security features.
"""

import hashlib
import json
import time
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional, Union

# Import the quantum security modules
from ..quantum_security import (
    SecurityLayerManager,
    SecurityLevel,
    create_default_security_manager,
    verify_signature
)


class Transaction:
    """
    Represents a transaction on the blockchain.
    
    Transactions include data transfer, value transfer, or code execution.
    All transactions are secured with quantum-resistant cryptography.
    """
    
    def __init__(self, 
                 sender: str,
                 recipient: str,
                 amount: float,
                 data: Optional[Dict[str, Any]] = None,
                 transaction_type: str = "transfer",
                 fee: float = 0.0,
                 nonce: Optional[int] = None):
        """
        Initialize a new transaction.
        
        Args:
            sender: The sender's address
            recipient: The recipient's address
            amount: The amount to transfer
            data: Optional additional data for the transaction
            transaction_type: Type of transaction (transfer, data, contract)
            fee: Transaction fee
            nonce: Unique nonce to prevent replay attacks
        """
        self.id = str(uuid.uuid4())
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.data = data or {}
        self.type = transaction_type
        self.fee = fee
        self.nonce = nonce or int(time.time() * 1000)
        self.timestamp = time.time()
        self.signatures = []
        self.hash = self._calculate_hash()
    
    def _calculate_hash(self) -> str:
        """Calculate the hash of the transaction"""
        tx_dict = {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "data": self.data,
            "type": self.type,
            "fee": self.fee,
            "nonce": self.nonce,
            "timestamp": self.timestamp
        }
        tx_string = json.dumps(tx_dict, sort_keys=True)
        return hashlib.sha3_256(tx_string.encode()).hexdigest()
    
    def sign(self, private_key: Dict[str, Any], security_manager: SecurityLayerManager) -> None:
        """
        Sign the transaction with the sender's private key using multiple security layers.
        
        Args:
            private_key: The sender's private key
            security_manager: Security layer manager for handling signatures
        """
        # Create a dictionary representation of the transaction without signatures
        tx_dict = {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "data": self.data,
            "type": self.type,
            "fee": self.fee,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "hash": self.hash
        }
        
        # Use the security manager to sign the transaction
        signed_tx = security_manager.sign_transaction(tx_dict, private_key)
        
        # Update the signatures list
        self.signatures = signed_tx.get("signatures", [])
    
    def verify(self, security_manager: SecurityLayerManager) -> bool:
        """
        Verify the transaction's signatures and integrity.
        
        Args:
            security_manager: Security layer manager for handling verification
        
        Returns:
            True if the transaction is valid, False otherwise
        """
        # Create a dictionary representation for verification
        tx_dict = {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "data": self.data,
            "type": self.type,
            "fee": self.fee,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "hash": self.hash,
            "signatures": self.signatures
        }
        
        # Use the security manager to verify the transaction
        is_valid, reasons = security_manager.verify_transaction(tx_dict)
        return is_valid
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the transaction to a dictionary"""
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "data": self.data,
            "type": self.type,
            "fee": self.fee,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "hash": self.hash,
            "signatures": self.signatures
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """Create a transaction from a dictionary"""
        tx = cls(
            sender=data["sender"],
            recipient=data["recipient"],
            amount=data["amount"],
            data=data.get("data", {}),
            transaction_type=data.get("type", "transfer"),
            fee=data.get("fee", 0.0),
            nonce=data.get("nonce")
        )
        tx.id = data["id"]
        tx.timestamp = data["timestamp"]
        tx.hash = data["hash"]
        tx.signatures = data.get("signatures", [])
        return tx


class Block:
    """
    Represents a block in the blockchain.
    
    Each block contains multiple transactions and links to the previous block,
    forming the blockchain. Blocks are secured with quantum-resistant cryptography.
    """
    
    def __init__(self, 
                 index: int,
                 previous_hash: str,
                 transactions: List[Transaction],
                 timestamp: Optional[float] = None,
                 nonce: int = 0):
        """
        Initialize a new block.
        
        Args:
            index: The block index/height in the chain
            previous_hash: Hash of the previous block
            transactions: List of transactions in this block
            timestamp: Block creation timestamp
            nonce: Nonce for proof-of-work
        """
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.merkle_root = self._calculate_merkle_root()
        self.hash = self._calculate_hash()
        self.difficulty = 4  # Number of leading zeros required for proof-of-work
    
    def _calculate_merkle_root(self) -> str:
        """Calculate the Merkle root of the transactions"""
        if not self.transactions:
            return hashlib.sha3_256("empty".encode()).hexdigest()
        
        # Get transaction hashes
        tx_hashes = [tx.hash for tx in self.transactions]
        
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
    
    def _calculate_hash(self) -> str:
        """Calculate the hash of the block"""
        block_dict = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_dict, sort_keys=True)
        return hashlib.sha3_256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: Optional[int] = None) -> None:
        """
        Mine the block by finding a valid proof-of-work.
        
        Args:
            difficulty: Optional difficulty override
        """
        if difficulty is not None:
            self.difficulty = difficulty
        
        # Target pattern: 'difficulty' number of leading zeros
        target = '0' * self.difficulty
        
        while self.hash[:self.difficulty] != target:
            self.nonce += 1
            self.hash = self._calculate_hash()
    
    def verify(self, security_manager: SecurityLayerManager) -> bool:
        """
        Verify the block's integrity and all its transactions.
        
        Args:
            security_manager: Security layer manager for handling verification
        
        Returns:
            True if the block is valid, False otherwise
        """
        # Verify block hash
        if self._calculate_hash() != self.hash:
            return False
        
        # Verify proof-of-work
        if self.hash[:self.difficulty] != '0' * self.difficulty:
            return False
        
        # Verify Merkle root
        if self._calculate_merkle_root() != self.merkle_root:
            return False
        
        # Verify all transactions
        for tx in self.transactions:
            if not tx.verify(security_manager):
                return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the block to a dictionary"""
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "merkle_root": self.merkle_root,
            "hash": self.hash,
            "difficulty": self.difficulty
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Block':
        """Create a block from a dictionary"""
        transactions = [Transaction.from_dict(tx) for tx in data["transactions"]]
        
        block = cls(
            index=data["index"],
            previous_hash=data["previous_hash"],
            transactions=transactions,
            timestamp=data["timestamp"],
            nonce=data["nonce"]
        )
        
        block.merkle_root = data["merkle_root"]
        block.hash = data["hash"]
        block.difficulty = data.get("difficulty", 4)
        
        return block


class Blockchain:
    """
    Represents the complete blockchain.
    
    The blockchain consists of a chain of blocks, each containing transactions.
    This implementation includes quantum-resistant security features.
    """
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.STANDARD):
        """
        Initialize a new blockchain.
        
        Args:
            security_level: The security level to enforce
        """
        # Initialize the security manager
        self.security_manager = create_default_security_manager(security_level)
        
        # Initialize the chain with the genesis block
        self.chain = [self._create_genesis_block()]
        
        # Unconfirmed transactions waiting to be mined
        self.pending_transactions = []
        
        # Set difficulty
        self.difficulty = 4
        
        # Track node addresses for a distributed network
        self.nodes = set()
    
    def _create_genesis_block(self) -> Block:
        """Create the genesis block for the blockchain"""
        # Genesis block has no previous hash and no real transactions
        genesis_tx = Transaction(
            sender="0",
            recipient="genesis",
            amount=0,
            data={"message": "Genesis Block"},
            transaction_type="genesis"
        )
        
        return Block(
            index=0,
            previous_hash="0",
            transactions=[genesis_tx],
            timestamp=time.time()
        )
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the blockchain"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """
        Add a transaction to the pending transactions pool.
        
        Args:
            transaction: The transaction to add
        
        Returns:
            True if the transaction was added, False otherwise
        """
        # Verify the transaction first
        if not transaction.verify(self.security_manager):
            return False
        
        # Add to pending transactions
        self.pending_transactions.append(transaction)
        return True
    
    def mine_pending_transactions(self, miner_address: str) -> Optional[Block]:
        """
        Mine pending transactions into a new block and add to the chain.
        
        Args:
            miner_address: The address that will receive the mining reward
        
        Returns:
            The newly created block, or None if mining failed
        """
        # Create a reward transaction for the miner
        reward_tx = Transaction(
            sender="0",  # System address for rewards
            recipient=miner_address,
            amount=1.0,  # Block reward
            data={"message": "Mining Reward"},
            transaction_type="reward"
        )
        
        # Create a new block with pending transactions plus the reward
        latest_block = self.get_latest_block()
        
        # Limit the number of transactions per block (for example, max 10)
        transactions_for_block = self.pending_transactions[:10]
        transactions_for_block.append(reward_tx)
        
        new_block = Block(
            index=latest_block.index + 1,
            previous_hash=latest_block.hash,
            transactions=transactions_for_block,
            timestamp=time.time()
        )
        
        # Mine the block
        new_block.mine_block(self.difficulty)
        
        # Verify the new block
        if not new_block.verify(self.security_manager):
            return None
        
        # Add the new block to the chain
        self.chain.append(new_block)
        
        # Remove the transactions that were included in the block
        self.pending_transactions = self.pending_transactions[10:]
        
        return new_block
    
    def is_chain_valid(self) -> bool:
        """
        Verify the entire blockchain for integrity.
        
        Returns:
            True if the blockchain is valid, False otherwise
        """
        # Check each block in the chain
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify block integrity
            if not current_block.verify(self.security_manager):
                return False
            
            # Verify block links
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_balance(self, address: str) -> float:
        """
        Calculate the balance for an address.
        
        Args:
            address: The address to check
        
        Returns:
            The current balance
        """
        balance = 0.0
        
        # Check all transactions in the blockchain
        for block in self.chain:
            for tx in block.transactions:
                if tx.recipient == address:
                    balance += tx.amount
                if tx.sender == address:
                    balance -= tx.amount
                    # Deduct the fee as well
                    balance -= tx.fee
        
        return balance
    
    def get_transaction_history(self, address: str) -> List[Dict[str, Any]]:
        """
        Get transaction history for an address.
        
        Args:
            address: The address to check
        
        Returns:
            List of transactions involving the address
        """
        history = []
        
        # Check all transactions in the blockchain
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address or tx.recipient == address:
                    history.append({
                        "transaction": tx.to_dict(),
                        "block": block.index,
                        "block_hash": block.hash,
                        "timestamp": tx.timestamp,
                        "confirmed": True
                    })
        
        # Also check pending transactions
        for tx in self.pending_transactions:
            if tx.sender == address or tx.recipient == address:
                history.append({
                    "transaction": tx.to_dict(),
                    "block": None,
                    "block_hash": None,
                    "timestamp": tx.timestamp,
                    "confirmed": False
                })
        
        # Sort by timestamp (newest first)
        history.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return history
    
    def get_block_by_hash(self, block_hash: str) -> Optional[Block]:
        """
        Find a block by its hash.
        
        Args:
            block_hash: The hash of the block to find
        
        Returns:
            The block if found, None otherwise
        """
        for block in self.chain:
            if block.hash == block_hash:
                return block
        return None
    
    def get_block_by_index(self, index: int) -> Optional[Block]:
        """
        Find a block by its index.
        
        Args:
            index: The index of the block to find
        
        Returns:
            The block if found, None otherwise
        """
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None
    
    def get_transaction_by_id(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """
        Find a transaction by its ID.
        
        Args:
            transaction_id: The ID of the transaction to find
        
        Returns:
            Transaction details if found, None otherwise
        """
        # Check all transactions in the blockchain
        for block_idx, block in enumerate(self.chain):
            for tx in block.transactions:
                if tx.id == transaction_id:
                    return {
                        "transaction": tx.to_dict(),
                        "block": block_idx,
                        "block_hash": block.hash,
                        "confirmed": True
                    }
        
        # Check pending transactions
        for tx in self.pending_transactions:
            if tx.id == transaction_id:
                return {
                    "transaction": tx.to_dict(),
                    "block": None,
                    "block_hash": None,
                    "confirmed": False
                }
        
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the blockchain to a dictionary"""
        return {
            "chain": [block.to_dict() for block in self.chain],
            "pending_transactions": [tx.to_dict() for tx in self.pending_transactions],
            "difficulty": self.difficulty,
            "length": len(self.chain),
            "nodes": list(self.nodes)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], 
                 security_level: SecurityLevel = SecurityLevel.STANDARD) -> 'Blockchain':
        """Create a blockchain from a dictionary"""
        blockchain = cls(security_level)
        
        # Replace the chain
        blockchain.chain = [Block.from_dict(block_data) for block_data in data["chain"]]
        
        # Add pending transactions
        blockchain.pending_transactions = [
            Transaction.from_dict(tx_data) for tx_data in data["pending_transactions"]
        ]
        
        # Set other properties
        blockchain.difficulty = data["difficulty"]
        blockchain.nodes = set(data.get("nodes", []))
        
        return blockchain
    
    def add_node(self, address: str) -> None:
        """
        Add a new node address to the network.
        
        Args:
            address: The address of the node (URL)
        """
        self.nodes.add(address)
    
    def update_security_level(self, level: SecurityLevel) -> None:
        """
        Update the security level for the blockchain.
        
        Args:
            level: The new security level
        """
        self.security_manager.set_security_level(level)