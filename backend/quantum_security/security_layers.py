"""
Security Layers Module for Quantum-Resistant Blockchain

This module implements a multi-layered security approach for the blockchain.
Different security layers provide defense in depth against various attacks,
including quantum computing attacks.

Security layers include:
1. Quantum-resistant cryptography layer
2. Traditional cryptography layer (as backup)
3. Behavioral analysis layer
4. Network security layer
5. Zero-knowledge proofs layer
"""

import enum
import hashlib
import json
import time
from typing import Dict, List, Any, Callable, Optional, Tuple, Union


class SecurityLevel(enum.Enum):
    """
    Security levels for the blockchain.
    Higher levels provide stronger security but may have more overhead.
    """
    STANDARD = 0       # Good for most applications
    HIGH = 1           # Enhanced security
    VERY_HIGH = 2      # For highly sensitive operations
    QUANTUM = 3        # Maximum quantum-resistant security
    PARANOID = 4       # All security measures enabled, maximum overhead


class SecurityLayerManager:
    """
    Manages multiple security layers and enforces security policies.
    """
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.STANDARD):
        """
        Initialize the security layer manager.
        
        Args:
            security_level: The security level to enforce
        """
        self.security_level = security_level
        self.layers = []
        self.verification_layers = []
        self.audit_log = []
        self.max_audit_log_size = 1000
    
    def add_layer(self, name: str, layer_functions: Dict[str, Callable], 
                 required_level: SecurityLevel) -> None:
        """
        Add a security layer to the manager.
        
        Args:
            name: Name of the security layer
            layer_functions: Dictionary of functions provided by this layer
            required_level: Minimum security level needed to activate this layer
        """
        self.layers.append({
            "name": name,
            "functions": layer_functions,
            "required_level": required_level,
            "enabled": self.security_level.value >= required_level.value
        })
    
    def add_verification_layer(self, name: str, verify_function: Callable, 
                              required_level: SecurityLevel) -> None:
        """
        Add a verification layer for transaction/block verification.
        
        Args:
            name: Name of the verification layer
            verify_function: Function that performs verification
            required_level: Minimum security level needed to activate this layer
        """
        self.verification_layers.append({
            "name": name,
            "verify": verify_function,
            "required_level": required_level,
            "enabled": self.security_level.value >= required_level.value
        })
    
    def set_security_level(self, level: SecurityLevel) -> None:
        """
        Change the security level, which affects which layers are active.
        
        Args:
            level: The new security level
        """
        self.security_level = level
        
        # Update which layers are enabled
        for layer in self.layers:
            layer["enabled"] = self.security_level.value >= layer["required_level"].value
        
        for layer in self.verification_layers:
            layer["enabled"] = self.security_level.value >= layer["required_level"].value
        
        # Log the change
        self._log_audit("security_level_change", {
            "new_level": level.name,
            "enabled_layers": [layer["name"] for layer in self.layers if layer["enabled"]],
            "enabled_verifications": [layer["name"] for layer in self.verification_layers if layer["enabled"]]
        })
    
    def verify_transaction(self, transaction: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Verify a transaction through all active verification layers.
        
        Args:
            transaction: The transaction to verify
            
        Returns:
            Tuple of (is_valid, reasons) where reasons lists any verification failures
        """
        valid = True
        reasons = []
        
        # Run all enabled verification layers
        for layer in self.verification_layers:
            if layer["enabled"]:
                try:
                    result = layer["verify"](transaction)
                    if isinstance(result, tuple):
                        layer_valid, layer_reason = result
                    else:
                        layer_valid, layer_reason = result, None
                    
                    if not layer_valid:
                        valid = False
                        if layer_reason:
                            reasons.append(f"{layer['name']}: {layer_reason}")
                        else:
                            reasons.append(f"{layer['name']}: Verification failed")
                except Exception as e:
                    valid = False
                    reasons.append(f"{layer['name']}: Error during verification: {str(e)}")
        
        # Log verification result
        self._log_audit("transaction_verification", {
            "transaction_id": transaction.get("id", "unknown"),
            "valid": valid,
            "reasons": reasons
        })
        
        return valid, reasons
    
    def sign_transaction(self, transaction: Dict[str, Any], 
                         private_keys: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sign a transaction using active security layers.
        
        Args:
            transaction: The transaction to sign
            private_keys: Dictionary of private keys for different algorithms
            
        Returns:
            The transaction with signatures added
        """
        # Copy the transaction to avoid modifying the original
        signed_tx = transaction.copy()
        
        # Initialize signatures array if it doesn't exist
        if "signatures" not in signed_tx:
            signed_tx["signatures"] = []
        
        # Message to sign (transaction data without signatures)
        tx_data = {k: v for k, v in signed_tx.items() if k != "signatures"}
        message = json.dumps(tx_data, sort_keys=True)
        
        # Apply all enabled signing layers
        for layer in self.layers:
            if layer["enabled"] and "sign" in layer["functions"]:
                try:
                    # Get the appropriate private key for this layer
                    layer_name = layer["name"]
                    if layer_name in private_keys:
                        signature = layer["functions"]["sign"](message, private_keys[layer_name])
                        
                        signed_tx["signatures"].append({
                            "layer": layer_name,
                            "signature": signature,
                            "timestamp": time.time()
                        })
                except Exception as e:
                    # Log error but continue with other layers
                    self._log_audit("signing_error", {
                        "layer": layer["name"],
                        "error": str(e),
                        "transaction_id": transaction.get("id", "unknown")
                    })
        
        # Log successful signatures
        self._log_audit("transaction_signed", {
            "transaction_id": transaction.get("id", "unknown"),
            "signature_count": len(signed_tx["signatures"]),
            "signature_layers": [sig["layer"] for sig in signed_tx["signatures"]]
        })
        
        return signed_tx
    
    def encrypt_data(self, data: Dict[str, Any], public_keys: Dict[str, str],
                    required_layers: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Encrypt data using active security layers.
        
        Args:
            data: The data to encrypt
            public_keys: Dictionary of public keys for different algorithms
            required_layers: Optional list of specific layers to use
            
        Returns:
            Dictionary with encrypted data for each layer
        """
        result = {
            "original_data_hash": hashlib.sha3_256(json.dumps(data, sort_keys=True).encode()).hexdigest(),
            "encryption_layers": [],
            "encrypted_data": {}
        }
        
        # Apply all enabled encryption layers
        for layer in self.layers:
            layer_name = layer["name"]
            
            # Skip if not enabled or if not in required_layers (if specified)
            if not layer["enabled"] or (required_layers and layer_name not in required_layers):
                continue
                
            if "encrypt" in layer["functions"]:
                try:
                    # Get the appropriate public key for this layer
                    if layer_name in public_keys:
                        encrypted = layer["functions"]["encrypt"](data, public_keys[layer_name])
                        
                        result["encrypted_data"][layer_name] = encrypted
                        result["encryption_layers"].append(layer_name)
                except Exception as e:
                    # Log error but continue with other layers
                    self._log_audit("encryption_error", {
                        "layer": layer_name,
                        "error": str(e)
                    })
        
        # Log encryption operation
        self._log_audit("data_encrypted", {
            "layer_count": len(result["encryption_layers"]),
            "layers": result["encryption_layers"]
        })
        
        return result
    
    def decrypt_data(self, encrypted_data: Dict[str, Any], private_keys: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decrypt data that was encrypted with multiple layers.
        
        Args:
            encrypted_data: The encrypted data (output from encrypt_data)
            private_keys: Dictionary of private keys for different algorithms
            
        Returns:
            The decrypted data, or None if decryption fails
        """
        # Check if we have any successful decryption
        for layer_name in encrypted_data["encryption_layers"]:
            if layer_name in private_keys and layer_name in encrypted_data["encrypted_data"]:
                for layer in self.layers:
                    if layer["name"] == layer_name and "decrypt" in layer["functions"]:
                        try:
                            decrypted = layer["functions"]["decrypt"](
                                encrypted_data["encrypted_data"][layer_name],
                                private_keys[layer_name]
                            )
                            
                            # Verify hash matches
                            decrypted_hash = hashlib.sha3_256(json.dumps(decrypted, sort_keys=True).encode()).hexdigest()
                            if decrypted_hash == encrypted_data["original_data_hash"]:
                                self._log_audit("data_decrypted", {
                                    "layer": layer_name,
                                    "success": True
                                })
                                return decrypted
                        except Exception as e:
                            self._log_audit("decryption_error", {
                                "layer": layer_name,
                                "error": str(e)
                            })
        
        # If we get here, all decryption attempts failed
        self._log_audit("data_decryption_failed", {
            "available_layers": encrypted_data["encryption_layers"]
        })
        return None
    
    def _log_audit(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """
        Log an event to the security audit log.
        
        Args:
            event_type: Type of event
            event_data: Event data
        """
        event = {
            "timestamp": time.time(),
            "event_type": event_type,
            "security_level": self.security_level.name,
            "data": event_data
        }
        
        # Add to log, keeping size limited
        self.audit_log.append(event)
        if len(self.audit_log) > self.max_audit_log_size:
            self.audit_log = self.audit_log[-self.max_audit_log_size:]
    
    def get_audit_log(self, filter_type: Optional[str] = None, 
                     max_entries: int = 100) -> List[Dict[str, Any]]:
        """
        Get entries from the security audit log.
        
        Args:
            filter_type: Optional event type to filter by
            max_entries: Maximum number of entries to return
            
        Returns:
            List of audit log entries
        """
        if filter_type:
            filtered_log = [event for event in self.audit_log if event["event_type"] == filter_type]
        else:
            filtered_log = self.audit_log
        
        # Return most recent entries up to max_entries
        return filtered_log[-max_entries:]


# Example verification functions for different security layers

def verify_quantum_signatures(transaction: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Verify quantum-resistant signatures in a transaction.
    
    Args:
        transaction: The transaction to verify
        
    Returns:
        Tuple of (is_valid, reason)
    """
    # In a real implementation, this would verify actual quantum-resistant signatures
    signatures = transaction.get("signatures", [])
    
    # Check for quantum layer signatures
    quantum_signatures = [sig for sig in signatures if sig.get("layer") == "quantum_resistant"]
    
    if not quantum_signatures:
        return False, "No quantum-resistant signatures found"
    
    # Verify signatures (simplified)
    # In a real implementation, this would use actual verification algorithms
    is_valid = True
    for sig in quantum_signatures:
        # Verification logic would go here
        # For simulation, we'll assume all signatures are valid
        pass
    
    return is_valid, None


def analyze_transaction_behavior(transaction: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Analyze transaction for suspicious behavior patterns.
    
    Args:
        transaction: The transaction to analyze
        
    Returns:
        Tuple of (is_valid, reason)
    """
    # In a real implementation, this would use advanced analytics and ML
    
    # Example check: Transaction amount is suspiciously large
    if "amount" in transaction and transaction["amount"] > 1000000:
        return False, "Unusually large transaction amount"
    
    # Example check: Unusual timestamp (future dated)
    if "timestamp" in transaction and transaction["timestamp"] > time.time() + 3600:
        return False, "Transaction timestamp is in the future"
    
    return True, None


def verify_hash_consistency(transaction: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Verify that transaction hash is consistent with its contents.
    
    Args:
        transaction: The transaction to verify
        
    Returns:
        Tuple of (is_valid, reason)
    """
    if "hash" not in transaction:
        return True, None  # No hash to verify
    
    # Calculate expected hash
    tx_data = {k: v for k, v in transaction.items() if k not in ["hash", "signatures"]}
    tx_json = json.dumps(tx_data, sort_keys=True)
    expected_hash = hashlib.sha3_256(tx_json.encode()).hexdigest()
    
    if transaction["hash"] != expected_hash:
        return False, "Transaction hash does not match content"
    
    return True, None


# Example of creating a comprehensive security layer manager

def create_default_security_manager(level: SecurityLevel = SecurityLevel.STANDARD) -> SecurityLayerManager:
    """
    Create a security layer manager with default layers configured.
    
    Args:
        level: Security level to set
        
    Returns:
        Configured SecurityLayerManager
    """
    manager = SecurityLayerManager(level)
    
    # Add quantum-resistant cryptography layer
    from .quantum_resistant_crypto import sign_message, verify_signature, hybrid_encryption, hybrid_decryption
    
    manager.add_layer(
        "quantum_resistant",
        {
            "sign": sign_message,
            "verify": verify_signature,
            "encrypt": hybrid_encryption,
            "decrypt": hybrid_decryption
        },
        SecurityLevel.STANDARD  # Required for all security levels
    )
    
    # Add lattice-based cryptography layer
    from .lattice_crypto import LatticeBasedSignature, LatticeBasedEncryption
    
    lattice_signature = LatticeBasedSignature()
    lattice_encryption = LatticeBasedEncryption()
    
    manager.add_layer(
        "lattice_based",
        {
            "sign": lattice_signature.sign,
            "verify": lattice_signature.verify,
            "encrypt": lattice_encryption.encrypt,
            "decrypt": lattice_encryption.decrypt
        },
        SecurityLevel.HIGH  # Only required for HIGH and above
    )
    
    # Add hash-based signatures layer
    from .hash_based_crypto import HashBasedSignature
    
    hash_signature = HashBasedSignature()
    
    manager.add_layer(
        "hash_based",
        {
            "sign": hash_signature.sign,
            "verify": hash_signature.verify
        },
        SecurityLevel.VERY_HIGH  # Only required for VERY_HIGH and above
    )
    
    # Add verification layers
    manager.add_verification_layer(
        "quantum_signature_verification",
        verify_quantum_signatures,
        SecurityLevel.STANDARD
    )
    
    manager.add_verification_layer(
        "hash_consistency",
        verify_hash_consistency,
        SecurityLevel.STANDARD
    )
    
    manager.add_verification_layer(
        "behavioral_analysis",
        analyze_transaction_behavior,
        SecurityLevel.HIGH
    )
    
    return manager