"""
Quantum-Resistant Wallet Implementation

This module implements a wallet system for the GenesisChain blockchain.
It includes:
1. QuantumWallet class for managing addresses and keys
2. Functions for creating and managing wallets
3. Functions for signing transactions securely

All cryptographic operations use quantum-resistant algorithms.
"""

import hashlib
import json
import os
import time
import uuid
from typing import Dict, List, Any, Optional, Tuple

# Import the quantum security modules
from ..quantum_security import (
    QuantumResistantKeyPair,
    generate_keypair,
    sign_message,
    verify_signature,
    LatticeBasedSignature,
    HashBasedSignature,
    SecurityLayerManager,
    SecurityLevel,
    create_default_security_manager
)


class QuantumWallet:
    """
    A quantum-resistant cryptocurrency wallet.
    
    This wallet manages multiple key pairs for different quantum-resistant
    algorithms, providing defense in depth.
    """
    
    def __init__(self, name: Optional[str] = None):
        """
        Initialize a new wallet.
        
        Args:
            name: Optional user-friendly name for the wallet
        """
        self.id = str(uuid.uuid4())
        self.name = name or f"Wallet-{self.id[:8]}"
        self.created_at = time.time()
        self.updated_at = self.created_at
        
        # Multiple key pairs for different algorithms
        self.key_pairs = {}
        
        # Default address derived from main key pair
        self.address = ""
        
        # Transaction history
        self.transactions = []
        
        # Security manager for this wallet
        self.security_manager = create_default_security_manager(SecurityLevel.STANDARD)
    
    def generate_keys(self, security_level: SecurityLevel = SecurityLevel.STANDARD) -> None:
        """
        Generate all required key pairs for the wallet based on security level.
        
        Args:
            security_level: The security level to use
        """
        # Update the security manager
        self.security_manager.set_security_level(security_level)
        
        # Generate primary quantum-resistant key pair
        self.key_pairs["quantum_resistant"] = generate_keypair(
            algorithm="FALCON",
            security_level=256
        )
        
        # Set the main address based on the primary key pair
        self.address = self._derive_address(self.key_pairs["quantum_resistant"].public_key)
        
        # For higher security levels, generate additional key pairs
        if security_level.value >= SecurityLevel.HIGH.value:
            # Generate lattice-based key pair
            lattice = LatticeBasedSignature()
            self.key_pairs["lattice_based"] = lattice.keygen()
        
        if security_level.value >= SecurityLevel.VERY_HIGH.value:
            # Generate hash-based key pair
            hash_sig = HashBasedSignature()
            self.key_pairs["hash_based"] = hash_sig.keygen()
        
        self.updated_at = time.time()
    
    def _derive_address(self, public_key: str) -> str:
        """
        Derive a blockchain address from a public key.
        
        Args:
            public_key: The public key to derive from
            
        Returns:
            A blockchain address string
        """
        # Hash the public key
        h1 = hashlib.sha3_256(public_key.encode()).digest()
        h2 = hashlib.ripemd160(h1).digest() if hasattr(hashlib, 'ripemd160') else hashlib.sha3_256(h1).digest()[:20]
        
        # Add version byte (0x01 for GenesisChain)
        version_byte = bytes([0x01])
        address_bytes = version_byte + h2
        
        # Add checksum
        checksum = hashlib.sha3_256(hashlib.sha3_256(address_bytes).digest()).digest()[:4]
        address_with_checksum = address_bytes + checksum
        
        # Convert to Base58
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        value = int.from_bytes(address_with_checksum, 'big')
        result = ''
        
        while value:
            value, remainder = divmod(value, 58)
            result = alphabet[remainder] + result
        
        # Add '1's for leading zeros
        for byte in address_with_checksum:
            if byte == 0:
                result = '1' + result
            else:
                break
        
        return result
    
    def sign_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sign a transaction with all available key pairs.
        
        Args:
            transaction_data: The transaction data to sign
            
        Returns:
            The transaction with signatures added
        """
        # Convert transaction data to string for signing
        tx_string = json.dumps(transaction_data, sort_keys=True)
        
        # Create a dictionary of private keys for the security manager
        private_keys = {}
        
        # Add the quantum-resistant private key
        if "quantum_resistant" in self.key_pairs:
            keypair = self.key_pairs["quantum_resistant"]
            private_keys["quantum_resistant"] = keypair.private_key
        
        # Add the lattice-based private key if available
        if "lattice_based" in self.key_pairs:
            private_keys["lattice_based"] = self.key_pairs["lattice_based"]["private_key"]
        
        # Add the hash-based private key if available
        if "hash_based" in self.key_pairs:
            private_keys["hash_based"] = self.key_pairs["hash_based"]["private_key"]
        
        # Sign the transaction with all available keys
        signed_tx = self.security_manager.sign_transaction(transaction_data, private_keys)
        
        return signed_tx
    
    def encrypt_data(self, data: Dict[str, Any], recipient_public_keys: Dict[str, str]) -> Dict[str, Any]:
        """
        Encrypt data for a recipient using quantum-resistant encryption.
        
        Args:
            data: The data to encrypt
            recipient_public_keys: The recipient's public keys
            
        Returns:
            The encrypted data
        """
        return self.security_manager.encrypt_data(data, recipient_public_keys)
    
    def decrypt_data(self, encrypted_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Decrypt data that was encrypted for this wallet.
        
        Args:
            encrypted_data: The encrypted data
            
        Returns:
            The decrypted data, or None if decryption fails
        """
        # Create a dictionary of private keys for the security manager
        private_keys = {}
        
        # Add the quantum-resistant private key
        if "quantum_resistant" in self.key_pairs:
            keypair = self.key_pairs["quantum_resistant"]
            private_keys["quantum_resistant"] = keypair.private_key
        
        # Add the lattice-based private key if available
        if "lattice_based" in self.key_pairs:
            private_keys["lattice_based"] = self.key_pairs["lattice_based"]["private_key"]
        
        # Add the hash-based private key if available
        if "hash_based" in self.key_pairs:
            private_keys["hash_based"] = self.key_pairs["hash_based"]["private_key"]
        
        # Decrypt the data
        return self.security_manager.decrypt_data(encrypted_data, private_keys)
    
    def to_dict(self, include_private_keys: bool = False) -> Dict[str, Any]:
        """
        Convert the wallet to a dictionary.
        
        Args:
            include_private_keys: Whether to include private keys (dangerous!)
            
        Returns:
            Wallet data as a dictionary
        """
        result = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "public_keys": {}
        }
        
        # Add public keys
        if "quantum_resistant" in self.key_pairs:
            keypair = self.key_pairs["quantum_resistant"]
            result["public_keys"]["quantum_resistant"] = keypair.public_key
        
        if "lattice_based" in self.key_pairs:
            result["public_keys"]["lattice_based"] = self.key_pairs["lattice_based"]["public_key"]
        
        if "hash_based" in self.key_pairs and "public_key" in self.key_pairs["hash_based"]:
            result["public_keys"]["hash_based"] = self.key_pairs["hash_based"]["public_key"]
        
        # Include private keys if requested (dangerous!)
        if include_private_keys:
            result["private_keys"] = {}
            
            if "quantum_resistant" in self.key_pairs:
                keypair = self.key_pairs["quantum_resistant"]
                result["private_keys"]["quantum_resistant"] = keypair.private_key
            
            if "lattice_based" in self.key_pairs:
                result["private_keys"]["lattice_based"] = self.key_pairs["lattice_based"]["private_key"]
            
            if "hash_based" in self.key_pairs:
                result["private_keys"]["hash_based"] = self.key_pairs["hash_based"]["private_key"]
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QuantumWallet':
        """
        Create a wallet from a dictionary.
        
        Args:
            data: The wallet data
            
        Returns:
            A new QuantumWallet instance
        """
        wallet = cls(name=data.get("name"))
        
        wallet.id = data["id"]
        wallet.address = data["address"]
        wallet.created_at = data["created_at"]
        wallet.updated_at = data["updated_at"]
        
        # Initialize key pairs from public keys
        if "public_keys" in data:
            public_keys = data["public_keys"]
            
            if "quantum_resistant" in public_keys:
                wallet.key_pairs["quantum_resistant"] = QuantumResistantKeyPair(
                    public_key=public_keys["quantum_resistant"],
                    private_key="",  # No private key loaded
                    algorithm="FALCON",
                    key_id=str(uuid.uuid4()),
                    creation_time=wallet.created_at,
                    security_level=256
                )
            
            # Handle other key types similarly
            # (simplified for brevity)
        
        # If private keys are provided, add them
        if "private_keys" in data:
            private_keys = data["private_keys"]
            
            if "quantum_resistant" in private_keys and "quantum_resistant" in wallet.key_pairs:
                wallet.key_pairs["quantum_resistant"].private_key = private_keys["quantum_resistant"]
            
            # Handle other key types similarly
            # (simplified for brevity)
        
        return wallet
    
    def export_encrypted(self, passphrase: str) -> str:
        """
        Export the wallet in encrypted form.
        
        Args:
            passphrase: The passphrase to encrypt with
            
        Returns:
            Encrypted wallet data as a string
        """
        # Get the wallet data including private keys
        wallet_data = self.to_dict(include_private_keys=True)
        
        # Convert to JSON
        wallet_json = json.dumps(wallet_data)
        
        # In a real implementation, we would use a proper encryption scheme
        # For this simulation, we'll use a simple encryption with the passphrase
        
        # Derive a key from the passphrase
        key = hashlib.pbkdf2_hmac(
            'sha256',
            passphrase.encode(),
            b'quantum_salt',  # Salt
            100000  # Iterations
        ).hex()
        
        # "Encrypt" the wallet data (this is a simplified simulation)
        result = {
            "method": "quantum_wallet_encryption_v1",
            "salt": "quantum_salt",
            "iterations": 100000,
            "data": hashlib.sha256((key + wallet_json).encode()).hexdigest() + wallet_json
        }
        
        return json.dumps(result)
    
    @classmethod
    def import_encrypted(cls, encrypted_data: str, passphrase: str) -> Optional['QuantumWallet']:
        """
        Import a wallet from encrypted form.
        
        Args:
            encrypted_data: The encrypted wallet data
            passphrase: The passphrase to decrypt with
            
        Returns:
            The imported wallet, or None if import fails
        """
        try:
            # Parse the encrypted data
            encrypted = json.loads(encrypted_data)
            
            # Check the encryption method
            if encrypted["method"] != "quantum_wallet_encryption_v1":
                return None
            
            # Derive the key from the passphrase
            key = hashlib.pbkdf2_hmac(
                'sha256',
                passphrase.encode(),
                encrypted["salt"].encode(),
                encrypted["iterations"]
            ).hex()
            
            # Get the encrypted wallet JSON
            encrypted_wallet = encrypted["data"]
            
            # Verify and "decrypt" (this is a simplified simulation)
            hash_prefix = encrypted_wallet[:64]
            wallet_json = encrypted_wallet[64:]
            
            if hashlib.sha256((key + wallet_json).encode()).hexdigest() != hash_prefix:
                # Invalid passphrase
                return None
            
            # Parse the wallet data
            wallet_data = json.loads(wallet_json)
            
            # Create the wallet from the data
            return cls.from_dict(wallet_data)
            
        except Exception as e:
            # Any error means import failed
            print(f"Wallet import failed: {str(e)}")
            return None


def create_wallet(name: Optional[str] = None, 
                  security_level: SecurityLevel = SecurityLevel.STANDARD) -> QuantumWallet:
    """
    Create a new quantum-resistant wallet.
    
    Args:
        name: Optional name for the wallet
        security_level: Security level to use
        
    Returns:
        A new QuantumWallet
    """
    wallet = QuantumWallet(name)
    wallet.generate_keys(security_level)
    return wallet


def get_wallet_balance(wallet: QuantumWallet, blockchain) -> float:
    """
    Get the balance of a wallet on the blockchain.
    
    Args:
        wallet: The wallet to check
        blockchain: The blockchain to check against
        
    Returns:
        The wallet's balance
    """
    return blockchain.get_balance(wallet.address)