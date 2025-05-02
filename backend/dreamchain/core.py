"""
DreamChain Core Module

This module implements the core functionality of the DreamChain application layer.
It focuses on user-friendly features and high-throughput operations while
relying on the NexusLayer and GenesisChain for security.

Key components:
1. DreamChain: Main blockchain implementation for application layer
2. Transaction: Fast, application-specific transactions
3. Block: Optimized blocks for the application layer
4. Account: User account with advanced features
"""

import hashlib
import json
import time
import uuid
from typing import List, Dict, Any, Optional, Union, Callable

# Import from nexuslayer for communication with lower layers
# These will be imported at runtime to avoid circular imports
# from nexuslayer.bridge import BridgeManager, MessageType
# from nexuslayer.verification import VerificationGate


class Account:
    """
    User account in the DreamChain application layer.
    
    Accounts in DreamChain have additional features beyond basic
    blockchain addresses, such as profiles, permissions, and
    application-specific data.
    """
    
    def __init__(self, 
                 address: str,
                 name: Optional[str] = None,
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a new account.
        
        Args:
            address: The underlying blockchain address
            name: Optional user-friendly name
            metadata: Optional additional metadata
        """
        self.account_id = str(uuid.uuid4())
        self.address = address
        self.name = name or f"Account-{address[:8]}"
        self.metadata = metadata or {}
        self.balance = 0.0
        self.nonce = 0
        self.created_at = time.time()
        self.updated_at = self.created_at
        self.transactions = []
        self.permissions = {}
        
    def update_balance(self, amount: float) -> float:
        """
        Update the account balance.
        
        Args:
            amount: Amount to add (or subtract if negative)
            
        Returns:
            New balance
        """
        self.balance += amount
        self.updated_at = time.time()
        return self.balance
        
    def increment_nonce(self) -> int:
        """
        Increment the account nonce and return the new value.
        
        Returns:
            New nonce value
        """
        self.nonce += 1
        self.updated_at = time.time()
        return self.nonce
        
    def add_permission(self, 
                      permission_key: str,
                      permission_value: Any) -> None:
        """
        Add a permission to the account.
        
        Args:
            permission_key: The permission key
            permission_value: The permission value
        """
        self.permissions[permission_key] = permission_value
        self.updated_at = time.time()
        
    def has_permission(self, permission_key: str) -> bool:
        """
        Check if the account has a specific permission.
        
        Args:
            permission_key: The permission to check
            
        Returns:
            True if permission exists, False otherwise
        """
        return permission_key in self.permissions
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert account to dictionary"""
        return {
            "account_id": self.account_id,
            "address": self.address,
            "name": self.name,
            "balance": self.balance,
            "nonce": self.nonce,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
            "transactions": len(self.transactions),
            "permissions": self.permissions
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Account':
        """Create account from dictionary"""
        account = cls(
            address=data["address"],
            name=data.get("name"),
            metadata=data.get("metadata", {})
        )
        
        account.account_id = data["account_id"]
        account.balance = data["balance"]
        account.nonce = data["nonce"]
        account.created_at = data["created_at"]
        account.updated_at = data["updated_at"]
        account.permissions = data.get("permissions", {})
        
        return account


class Transaction:
    """
    Transaction in the DreamChain application layer.
    
    These transactions are optimized for speed and user experience,
    while relying on the lower layers for security validation.
    """
    
    def __init__(self,
                 sender: str,
                 recipient: str,
                 amount: float,
                 data: Optional[Dict[str, Any]] = None,
                 transaction_type: str = "transfer",
                 fee: float = 0.001):
        """
        Initialize a new transaction.
        
        Args:
            sender: Sender account address
            recipient: Recipient account address
            amount: Transaction amount
            data: Optional additional data
            transaction_type: Type of transaction
            fee: Transaction fee
        """
        self.transaction_id = str(uuid.uuid4())
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.data = data or {}
        self.type = transaction_type
        self.fee = fee
        self.timestamp = time.time()
        self.nonce = int(time.time() * 1000)
        self.hash = self._calculate_hash()
        self.signatures = []
        self.status = "pending"
        self.block_id = None
        self.verified_by_genesis = False
        self.security_proofs = []
        
    def _calculate_hash(self) -> str:
        """Calculate the hash of the transaction"""
        tx_dict = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "data": self.data,
            "type": self.type,
            "fee": self.fee,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }
        
        tx_str = json.dumps(tx_dict, sort_keys=True)
        return hashlib.sha3_256(tx_str.encode()).hexdigest()
        
    def add_signature(self, 
                     signature: str,
                     signature_type: str,
                     public_key: str) -> None:
        """
        Add a signature to the transaction.
        
        Args:
            signature: The signature data
            signature_type: Type of signature
            public_key: Public key used for signing
        """
        self.signatures.append({
            "signature": signature,
            "type": signature_type,
            "public_key": public_key,
            "timestamp": time.time()
        })
        
    def add_security_proof(self, proof: Dict[str, Any]) -> None:
        """
        Add a security proof from lower layers.
        
        Args:
            proof: The security proof data
        """
        self.security_proofs.append(proof)
        
        # If this is a GenesisChain verification, mark as verified
        if proof.get("source") == "genesischain":
            self.verified_by_genesis = True
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary"""
        return {
            "transaction_id": self.transaction_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "data": self.data,
            "type": self.type,
            "fee": self.fee,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash,
            "signatures": self.signatures,
            "status": self.status,
            "block_id": self.block_id,
            "verified_by_genesis": self.verified_by_genesis,
            "security_proofs": self.security_proofs
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """Create transaction from dictionary"""
        tx = cls(
            sender=data["sender"],
            recipient=data["recipient"],
            amount=data["amount"],
            data=data.get("data", {}),
            transaction_type=data.get("type", "transfer"),
            fee=data.get("fee", 0.001)
        )
        
        tx.transaction_id = data["transaction_id"]
        tx.timestamp = data["timestamp"]
        tx.nonce = data["nonce"]
        tx.hash = data["hash"]
        tx.signatures = data.get("signatures", [])
        tx.status = data.get("status", "pending")
        tx.block_id = data.get("block_id")
        tx.verified_by_genesis = data.get("verified_by_genesis", False)
        tx.security_proofs = data.get("security_proofs", [])
        
        return tx


class Block:
    """
    Block in the DreamChain application layer.
    
    These blocks are optimized for application needs and feature
    enhanced metadata and application-specific functionality.
    """
    
    def __init__(self,
                 previous_hash: str,
                 transactions: List[Transaction],
                 creator: str,
                 block_number: int,
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a new block.
        
        Args:
            previous_hash: Hash of the previous block
            transactions: List of transactions in this block
            creator: Address of the block creator
            block_number: Block sequence number
            metadata: Optional block metadata
        """
        self.block_id = str(uuid.uuid4())
        self.block_number = block_number
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.creator = creator
        self.timestamp = time.time()
        self.metadata = metadata or {}
        self.transaction_count = len(transactions)
        self.merkle_root = self._calculate_merkle_root()
        self.hash = self._calculate_hash()
        self.verified_by_genesis = False
        self.verification_proofs = []
        
    def _calculate_hash(self) -> str:
        """Calculate the hash of the block"""
        block_dict = {
            "block_number": self.block_number,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "creator": self.creator,
            "timestamp": self.timestamp,
            "transaction_count": self.transaction_count
        }
        
        block_str = json.dumps(block_dict, sort_keys=True)
        return hashlib.sha3_256(block_str.encode()).hexdigest()
        
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
        
    def add_verification_proof(self, proof: Dict[str, Any]) -> None:
        """
        Add a verification proof from lower layers.
        
        Args:
            proof: The verification proof data
        """
        self.verification_proofs.append(proof)
        
        # If this is a GenesisChain verification, mark as verified
        if proof.get("source") == "genesischain":
            self.verified_by_genesis = True
            
        # Update transaction statuses if included in the proof
        if "verified_transactions" in proof:
            verified_tx_ids = proof["verified_transactions"]
            for tx in self.transactions:
                if tx.transaction_id in verified_tx_ids:
                    tx.verified_by_genesis = True
                    tx.status = "confirmed"
                    tx.block_id = self.block_id
                    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary"""
        return {
            "block_id": self.block_id,
            "block_number": self.block_number,
            "previous_hash": self.previous_hash,
            "creator": self.creator,
            "timestamp": self.timestamp,
            "transaction_count": self.transaction_count,
            "merkle_root": self.merkle_root,
            "hash": self.hash,
            "verified_by_genesis": self.verified_by_genesis,
            "metadata": self.metadata,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "verification_proofs": self.verification_proofs
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Block':
        """Create block from dictionary"""
        transactions = [Transaction.from_dict(tx) for tx in data.get("transactions", [])]
        
        block = cls(
            previous_hash=data["previous_hash"],
            transactions=transactions,
            creator=data["creator"],
            block_number=data["block_number"],
            metadata=data.get("metadata", {})
        )
        
        block.block_id = data["block_id"]
        block.timestamp = data["timestamp"]
        block.transaction_count = data["transaction_count"]
        block.merkle_root = data["merkle_root"]
        block.hash = data["hash"]
        block.verified_by_genesis = data.get("verified_by_genesis", False)
        block.verification_proofs = data.get("verification_proofs", [])
        
        return block


class DreamChain:
    """
    Main implementation of the DreamChain application layer.
    
    DreamChain provides a user-friendly, high-throughput blockchain
    experience while leveraging the NexusLayer and GenesisChain
    for security and cross-layer communication.
    """
    
    def __init__(self, name: str = "DreamChain"):
        """
        Initialize a new DreamChain instance.
        
        Args:
            name: Name for this blockchain instance
        """
        self.chain_id = str(uuid.uuid4())
        self.name = name
        self.created_at = time.time()
        self.blocks = []
        self.pending_transactions = []
        self.accounts = {}  # address -> Account
        self.event_handlers = {}
        
        # Bridge to lower layers - will be initialized later
        self.bridge_manager = None
        self.verification_gate = None
        
        # Track chain metrics
        self.metrics = {
            "transaction_count": 0,
            "block_count": 0,
            "account_count": 0,
            "genesis_verifications": 0
        }
        
        # Create genesis block
        self._create_genesis_block()
        
    def _create_genesis_block(self) -> None:
        """Create the genesis block for DreamChain"""
        genesis_tx = Transaction(
            sender="0",
            recipient="dreamchain",
            amount=0,
            data={"message": "DreamChain Genesis Block"},
            transaction_type="genesis"
        )
        
        genesis_block = Block(
            previous_hash="0",
            transactions=[genesis_tx],
            creator="dreamchain",
            block_number=0,
            metadata={
                "chain_name": self.name,
                "genesis_creation_time": self.created_at
            }
        )
        
        self.blocks.append(genesis_block)
        self.metrics["block_count"] += 1
        
    def initialize_bridge(self, bridge_manager, verification_gate) -> None:
        """
        Initialize the bridge to lower layers.
        
        Args:
            bridge_manager: BridgeManager instance
            verification_gate: VerificationGate instance
        """
        self.bridge_manager = bridge_manager
        self.verification_gate = verification_gate
        
        # Register message handlers for the bridge
        self._register_bridge_handlers()
        
    def _register_bridge_handlers(self) -> None:
        """Register message handlers for the bridge"""
        if not self.bridge_manager:
            return
            
        # Import here to avoid circular imports
        from nexuslayer.bridge import MessageType
        
        # Register handlers for each message type
        self.bridge_manager.register_message_handler(
            MessageType.SECURITY_VALIDATION,
            self._handle_security_validation
        )
        
        self.bridge_manager.register_message_handler(
            MessageType.TRANSACTION_VALIDATE,
            self._handle_transaction_validation
        )
        
        self.bridge_manager.register_message_handler(
            MessageType.TRANSACTION_CONFIRM,
            self._handle_transaction_confirmation
        )
        
    def _handle_security_validation(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle security validation messages from GenesisChain"""
        data = message.get("data", {})
        validation_type = data.get("validation_type")
        
        if validation_type == "block":
            block_id = data.get("block_id")
            result = data.get("result", False)
            
            # Find the block
            for block in self.blocks:
                if block.block_id == block_id:
                    # Add verification proof
                    proof = {
                        "source": "genesischain",
                        "timestamp": time.time(),
                        "result": result,
                        "validation_data": data.get("validation_data", {})
                    }
                    
                    block.add_verification_proof(proof)
                    
                    if result:
                        self.metrics["genesis_verifications"] += 1
                        
                    # Trigger event
                    self._trigger_event("block_verified", {
                        "block_id": block_id,
                        "result": result
                    })
                    
                    return {"status": "success", "block_id": block_id}
                    
            return {"status": "error", "message": "Block not found"}
            
        elif validation_type == "transaction":
            tx_id = data.get("transaction_id")
            result = data.get("result", False)
            
            # Check pending transactions
            for tx in self.pending_transactions:
                if tx.transaction_id == tx_id:
                    # Add security proof
                    proof = {
                        "source": "genesischain",
                        "timestamp": time.time(),
                        "result": result,
                        "validation_data": data.get("validation_data", {})
                    }
                    
                    tx.add_security_proof(proof)
                    
                    # Trigger event
                    self._trigger_event("transaction_verified", {
                        "transaction_id": tx_id,
                        "result": result
                    })
                    
                    return {"status": "success", "transaction_id": tx_id}
                    
            # Check transactions in blocks
            for block in self.blocks:
                for tx in block.transactions:
                    if tx.transaction_id == tx_id:
                        # Add security proof
                        proof = {
                            "source": "genesischain",
                            "timestamp": time.time(),
                            "result": result,
                            "validation_data": data.get("validation_data", {})
                        }
                        
                        tx.add_security_proof(proof)
                        
                        # Trigger event
                        self._trigger_event("transaction_verified", {
                            "transaction_id": tx_id,
                            "result": result
                        })
                        
                        return {"status": "success", "transaction_id": tx_id}
                        
            return {"status": "error", "message": "Transaction not found"}
            
        return {"status": "error", "message": "Unknown validation type"}
        
    def _handle_transaction_validation(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle transaction validation messages from GenesisChain"""
        data = message.get("data", {})
        tx_id = data.get("transaction_id")
        validation_result = data.get("result", {})
        
        # Find the transaction
        transaction = None
        
        # Check pending transactions
        for tx in self.pending_transactions:
            if tx.transaction_id == tx_id:
                transaction = tx
                break
                
        # If not found in pending, check blocks
        if not transaction:
            for block in self.blocks:
                for tx in block.transactions:
                    if tx.transaction_id == tx_id:
                        transaction = tx
                        break
                if transaction:
                    break
                    
        if not transaction:
            return {"status": "error", "message": "Transaction not found"}
            
        # Update transaction with validation result
        proof = {
            "source": "genesischain",
            "timestamp": time.time(),
            "result": validation_result.get("valid", False),
            "validation_data": validation_result
        }
        
        transaction.add_security_proof(proof)
        
        # Trigger event
        self._trigger_event("transaction_validated", {
            "transaction_id": tx_id,
            "result": validation_result
        })
        
        return {"status": "success", "transaction_id": tx_id}
        
    def _handle_transaction_confirmation(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle transaction confirmation messages from GenesisChain"""
        data = message.get("data", {})
        tx_id = data.get("transaction_id")
        block_id = data.get("block_id")
        status = data.get("status", "confirmed")
        
        # Find the transaction
        transaction = None
        
        # Check pending transactions
        for i, tx in enumerate(self.pending_transactions):
            if tx.transaction_id == tx_id:
                transaction = tx
                # Remove from pending if confirmed
                if status == "confirmed":
                    self.pending_transactions.pop(i)
                break
                
        # If not found in pending, check blocks
        if not transaction:
            for block in self.blocks:
                for tx in block.transactions:
                    if tx.transaction_id == tx_id:
                        transaction = tx
                        break
                if transaction:
                    break
                    
        if not transaction:
            return {"status": "error", "message": "Transaction not found"}
            
        # Update transaction status
        transaction.status = status
        
        # If confirmed, add to account transaction history
        if status == "confirmed" and transaction.block_id is None:
            transaction.block_id = block_id
            
            # Update sender account
            if transaction.sender in self.accounts:
                self.accounts[transaction.sender].transactions.append(tx_id)
                
            # Update recipient account
            if transaction.recipient in self.accounts:
                self.accounts[transaction.recipient].transactions.append(tx_id)
                
        # Trigger event
        self._trigger_event("transaction_confirmed", {
            "transaction_id": tx_id,
            "block_id": block_id,
            "status": status
        })
        
        return {"status": "success", "transaction_id": tx_id}
        
    def create_account(self, 
                      address: str,
                      name: Optional[str] = None,
                      metadata: Optional[Dict[str, Any]] = None) -> Account:
        """
        Create a new account.
        
        Args:
            address: The account address
            name: Optional account name
            metadata: Optional metadata
            
        Returns:
            The new Account
        """
        # Check if account already exists
        if address in self.accounts:
            return self.accounts[address]
            
        # Create new account
        account = Account(
            address=address,
            name=name,
            metadata=metadata
        )
        
        # Add to accounts
        self.accounts[address] = account
        self.metrics["account_count"] += 1
        
        # Trigger event
        self._trigger_event("account_created", {
            "account_id": account.account_id,
            "address": address
        })
        
        return account
        
    def get_account(self, address: str) -> Optional[Account]:
        """
        Get an account by address.
        
        Args:
            address: The account address
            
        Returns:
            The Account or None if not found
        """
        return self.accounts.get(address)
        
    def create_transaction(self,
                          sender: str,
                          recipient: str,
                          amount: float,
                          data: Optional[Dict[str, Any]] = None,
                          transaction_type: str = "transfer",
                          fee: float = 0.001) -> Transaction:
        """
        Create a new transaction.
        
        Args:
            sender: Sender account address
            recipient: Recipient account address
            amount: Transaction amount
            data: Optional additional data
            transaction_type: Type of transaction
            fee: Transaction fee
            
        Returns:
            The new Transaction
            
        Raises:
            ValueError: If sender account doesn't exist or has insufficient funds
        """
        # Check if sender account exists
        if sender not in self.accounts:
            raise ValueError("Sender account does not exist")
            
        sender_account = self.accounts[sender]
        
        # Check if sender has sufficient funds
        total_cost = amount + fee
        if sender_account.balance < total_cost:
            raise ValueError("Insufficient funds")
            
        # Create transaction
        transaction = Transaction(
            sender=sender,
            recipient=recipient,
            amount=amount,
            data=data,
            transaction_type=transaction_type,
            fee=fee
        )
        
        # Use the account's nonce for additional security
        transaction.nonce = sender_account.increment_nonce()
        
        # Recalculate hash with updated nonce
        transaction.hash = transaction._calculate_hash()
        
        # Add to pending transactions
        self.pending_transactions.append(transaction)
        self.metrics["transaction_count"] += 1
        
        # Trigger event
        self._trigger_event("transaction_created", {
            "transaction_id": transaction.transaction_id,
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })
        
        # Request verification from GenesisChain
        self._request_transaction_verification(transaction)
        
        return transaction
        
    def _request_transaction_verification(self, transaction: Transaction) -> None:
        """Request verification from GenesisChain for a transaction"""
        if not self.bridge_manager:
            return
            
        # Import here to avoid circular imports
        from nexuslayer.bridge import MessageType
        
        # Create validation request
        validation_request = {
            "transaction_id": transaction.transaction_id,
            "transaction_data": transaction.to_dict(),
            "timestamp": time.time()
        }
        
        # Send through bridge to GenesisChain
        # Note: In a real implementation, this would use proper key pairs
        self.bridge_manager.send_message(
            source_layer="dreamchain",
            destination_layer="genesischain",
            message_type=MessageType.TRANSACTION_VALIDATE,
            message_data=validation_request,
            sender_key_pair={
                "public_key": "dreamchain_public_key",
                "private_key": "dreamchain_private_key"
            }
        )
        
    def create_block(self, creator: str) -> Optional[Block]:
        """
        Create a new block with pending transactions.
        
        Args:
            creator: Address of the block creator
            
        Returns:
            The new Block, or None if no pending transactions
        """
        # Check if creator account exists
        if creator not in self.accounts:
            raise ValueError("Creator account does not exist")
            
        # Check if there are pending transactions
        if not self.pending_transactions:
            return None
            
        # Get the latest block
        latest_block = self.blocks[-1]
        
        # Create a new block
        block = Block(
            previous_hash=latest_block.hash,
            transactions=self.pending_transactions[:],
            creator=creator,
            block_number=latest_block.block_number + 1
        )
        
        # Add to chain
        self.blocks.append(block)
        self.metrics["block_count"] += 1
        
        # Clear pending transactions
        self.pending_transactions = []
        
        # Trigger event
        self._trigger_event("block_created", {
            "block_id": block.block_id,
            "block_number": block.block_number,
            "transaction_count": block.transaction_count
        })
        
        # Request verification from GenesisChain
        self._request_block_verification(block)
        
        return block
        
    def _request_block_verification(self, block: Block) -> None:
        """Request verification from GenesisChain for a block"""
        if not self.bridge_manager:
            return
            
        # Import here to avoid circular imports
        from nexuslayer.bridge import MessageType
        
        # Create validation request
        validation_request = {
            "block_id": block.block_id,
            "block_number": block.block_number,
            "block_hash": block.hash,
            "previous_hash": block.previous_hash,
            "merkle_root": block.merkle_root,
            "transaction_count": block.transaction_count,
            "transaction_ids": [tx.transaction_id for tx in block.transactions],
            "timestamp": time.time()
        }
        
        # Send through bridge to GenesisChain
        # Note: In a real implementation, this would use proper key pairs
        self.bridge_manager.send_message(
            source_layer="dreamchain",
            destination_layer="genesischain",
            message_type=MessageType.SECURITY_VALIDATION,
            message_data={
                "validation_type": "block",
                "validation_data": validation_request
            },
            sender_key_pair={
                "public_key": "dreamchain_public_key",
                "private_key": "dreamchain_private_key"
            }
        )
        
    def get_block(self, block_id: str) -> Optional[Block]:
        """
        Get a block by ID.
        
        Args:
            block_id: The block ID
            
        Returns:
            The Block or None if not found
        """
        for block in self.blocks:
            if block.block_id == block_id:
                return block
        return None
        
    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """
        Get a transaction by ID.
        
        Args:
            transaction_id: The transaction ID
            
        Returns:
            The Transaction or None if not found
        """
        # Check pending transactions
        for tx in self.pending_transactions:
            if tx.transaction_id == transaction_id:
                return tx
                
        # Check blocks
        for block in self.blocks:
            for tx in block.transactions:
                if tx.transaction_id == transaction_id:
                    return tx
                    
        return None
        
    def get_account_balance(self, address: str) -> float:
        """
        Get the balance of an account.
        
        Args:
            address: The account address
            
        Returns:
            The account balance, or 0 if account doesn't exist
        """
        account = self.get_account(address)
        return account.balance if account else 0
        
    def update_account_balance(self, 
                              address: str,
                              amount: float) -> float:
        """
        Update the balance of an account.
        
        Args:
            address: The account address
            amount: Amount to add (or subtract if negative)
            
        Returns:
            The new balance
            
        Raises:
            ValueError: If account doesn't exist
        """
        account = self.get_account(address)
        if not account:
            raise ValueError("Account does not exist")
            
        return account.update_balance(amount)
        
    def register_event_handler(self, 
                              event_type: str,
                              handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        Register a handler for a specific event type.
        
        Args:
            event_type: The type of event to handle
            handler: The function to call when that event occurs
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
            
        self.event_handlers[event_type].append(handler)
        
    def _trigger_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Trigger event handlers for an event"""
        if event_type not in self.event_handlers:
            return
            
        event = {
            "type": event_type,
            "timestamp": time.time(),
            "data": event_data
        }
        
        # Call all handlers
        for handler in self.event_handlers[event_type]:
            try:
                handler(event)
            except Exception as e:
                # Log the error but continue with other handlers
                print(f"Error in event handler: {str(e)}")
                
    def to_dict(self) -> Dict[str, Any]:
        """Convert DreamChain to dictionary for serialization"""
        return {
            "chain_id": self.chain_id,
            "name": self.name,
            "created_at": self.created_at,
            "block_count": len(self.blocks),
            "pending_transaction_count": len(self.pending_transactions),
            "account_count": len(self.accounts),
            "metrics": self.metrics,
            "latest_block": self.blocks[-1].to_dict() if self.blocks else None
        }