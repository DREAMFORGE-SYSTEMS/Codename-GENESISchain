"""
NexusLayer Bridge Module

This module implements the bridge functionality for communication between
GenesisChain and DreamChain. It provides:

1. Message passing between layers
2. Security gateways for controlled access
3. Resource monitoring and throttling
4. Protocol versioning and compatibility
"""

import enum
import hashlib
import json
import time
import uuid
from typing import Dict, List, Any, Optional, Callable, Union

# Import quantum security for validation
from quantum_security import (
    SecurityLevel,
    verify_signature,
    QuantumRandomNumberGenerator
)


class MessageType(enum.Enum):
    """Types of messages that can be passed between layers"""
    
    # Security messages
    SECURITY_VALIDATION = "security_validation"
    SECURITY_ALERT = "security_alert"
    EMERGENCY_LOCKDOWN = "emergency_lockdown"
    
    # Transaction messages
    TRANSACTION_SUBMIT = "transaction_submit"
    TRANSACTION_VALIDATE = "transaction_validate"
    TRANSACTION_CONFIRM = "transaction_confirm"
    
    # State messages
    STATE_UPDATE = "state_update"
    STATE_QUERY = "state_query"
    STATE_SYNC = "state_sync"
    
    # Resource management
    RESOURCE_REQUEST = "resource_request"
    RESOURCE_GRANT = "resource_grant"
    RESOURCE_RELEASE = "resource_release"
    
    # Administrative messages
    ADMIN_COMMAND = "admin_command"
    SYSTEM_METADATA = "system_metadata"


class SecurityGateway:
    """
    Security gateway for controlling access between layers.
    
    This class implements security policies for messages passing 
    between GenesisChain and DreamChain, ensuring that only authorized
    and validated messages can cross layer boundaries.
    """
    
    def __init__(self, 
                 security_level: SecurityLevel = SecurityLevel.STANDARD,
                 allowed_message_types: Optional[List[MessageType]] = None):
        """
        Initialize a new security gateway.
        
        Args:
            security_level: Security level to enforce
            allowed_message_types: List of allowed message types (None = all)
        """
        self.security_level = security_level
        self.allowed_message_types = allowed_message_types or list(MessageType)
        self.message_counters = {msg_type: 0 for msg_type in MessageType}
        self.throttling_limits = self._default_throttling_limits()
        self.gateway_id = str(uuid.uuid4())
        self.created_at = time.time()
        self.last_message_time = 0
        self.qrng = QuantumRandomNumberGenerator()
        
    def _default_throttling_limits(self) -> Dict[MessageType, int]:
        """Create default throttling limits based on message types"""
        limits = {}
        
        # Default: 100 messages per minute for most types
        for msg_type in MessageType:
            limits[msg_type] = 100
        
        # Higher limits for transaction messages
        limits[MessageType.TRANSACTION_SUBMIT] = 1000
        limits[MessageType.TRANSACTION_VALIDATE] = 1000
        
        # Lower limits for admin/security messages
        limits[MessageType.ADMIN_COMMAND] = 10
        limits[MessageType.EMERGENCY_LOCKDOWN] = 5
        
        return limits
        
    def validate_message(self, 
                         message: Dict[str, Any],
                         sender_signature: str,
                         sender_public_key: str) -> bool:
        """
        Validate a message attempting to pass through the gateway.
        
        Args:
            message: The message contents
            sender_signature: Signature from sender
            sender_public_key: Public key of sender
            
        Returns:
            True if message is valid, False otherwise
        """
        # Check message type is allowed
        if "type" not in message:
            return False
            
        try:
            msg_type = MessageType(message["type"])
        except ValueError:
            return False
            
        if msg_type not in self.allowed_message_types:
            return False
        
        # Check for throttling
        if self._is_throttled(msg_type):
            return False
        
        # Verify signature using quantum-resistant method
        message_str = json.dumps(message, sort_keys=True)
        
        # Basic validation (in production, this would use the actual verify_signature)
        is_valid = verify_signature(message_str, sender_signature, sender_public_key)
        
        if is_valid:
            # Update counters
            self.message_counters[msg_type] += 1
            self.last_message_time = time.time()
        
        return is_valid
        
    def _is_throttled(self, message_type: MessageType) -> bool:
        """Check if a message type is currently throttled"""
        # Simple time-based throttling
        # In a real implementation, this would be more sophisticated
        current_count = self.message_counters[message_type]
        limit = self.throttling_limits[message_type]
        
        # Reset counters after 60 seconds
        if time.time() - self.last_message_time > 60:
            self.message_counters = {msg_type: 0 for msg_type in MessageType}
            return False
            
        return current_count >= limit
        
    def create_passage_token(self, 
                            destination_layer: str,
                            valid_duration: int = 60) -> Dict[str, Any]:
        """
        Create a temporary token allowing passage between layers.
        
        Args:
            destination_layer: The layer this token grants access to
            valid_duration: How long the token is valid, in seconds
            
        Returns:
            A passage token
        """
        # Generate quantum random data for the token
        random_bytes = self.qrng.get_random_bytes(32)
        token_id = random_bytes.hex()
        
        # Create the token
        token = {
            "token_id": token_id,
            "gateway_id": self.gateway_id,
            "destination": destination_layer,
            "created_at": time.time(),
            "expires_at": time.time() + valid_duration,
            "security_level": self.security_level.name
        }
        
        # Add a hash for verification
        token_str = json.dumps(token, sort_keys=True)
        token["verification_hash"] = hashlib.sha3_256(token_str.encode()).hexdigest()
        
        return token
        
    def verify_passage_token(self, token: Dict[str, Any]) -> bool:
        """
        Verify a passage token is valid.
        
        Args:
            token: The passage token to verify
            
        Returns:
            True if token is valid, False otherwise
        """
        # Check token has required fields
        required_fields = ["token_id", "gateway_id", "destination", 
                           "created_at", "expires_at", "verification_hash"]
                           
        if not all(field in token for field in required_fields):
            return False
            
        # Check token hasn't expired
        if token["expires_at"] < time.time():
            return False
            
        # Verify hash
        token_copy = token.copy()
        original_hash = token_copy.pop("verification_hash")
        token_str = json.dumps(token_copy, sort_keys=True)
        calculated_hash = hashlib.sha3_256(token_str.encode()).hexdigest()
        
        return calculated_hash == original_hash
        
    def update_security_level(self, level: SecurityLevel) -> None:
        """
        Update the security level for this gateway.
        
        Args:
            level: The new security level
        """
        self.security_level = level
        
        # Adjust throttling limits based on security level
        multiplier = 1.0
        
        if level == SecurityLevel.HIGH:
            multiplier = 0.8  # 20% reduction
        elif level == SecurityLevel.VERY_HIGH:
            multiplier = 0.5  # 50% reduction
        elif level == SecurityLevel.QUANTUM:
            multiplier = 0.3  # 70% reduction
        elif level == SecurityLevel.PARANOID:
            multiplier = 0.1  # 90% reduction
            
        # Apply multiplier to all limits
        for msg_type in self.throttling_limits:
            base_limit = self._default_throttling_limits()[msg_type]
            self.throttling_limits[msg_type] = int(base_limit * multiplier)
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert gateway to dictionary for serialization"""
        return {
            "gateway_id": self.gateway_id,
            "security_level": self.security_level.name,
            "allowed_message_types": [msg_type.value for msg_type in self.allowed_message_types],
            "throttling_limits": {msg_type.value: limit 
                                 for msg_type, limit in self.throttling_limits.items()},
            "created_at": self.created_at,
            "last_message_time": self.last_message_time
        }


class BridgeManager:
    """
    Manages communication bridges between GenesisChain and DreamChain.
    
    This class maintains the collection of security gateways and handles
    the routing of messages between blockchain layers.
    """
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.STANDARD):
        """
        Initialize a new bridge manager.
        
        Args:
            security_level: The security level to enforce
        """
        self.security_level = security_level
        self.gateways = {}
        self.message_handlers = {}
        self.bridge_id = str(uuid.uuid4())
        self.created_at = time.time()
        
        # Create default gateways
        self._initialize_default_gateways()
        
    def _initialize_default_gateways(self) -> None:
        """Initialize the default security gateways"""
        # Genesis to Nexus gateway
        genesis_gateway = SecurityGateway(
            security_level=self.security_level,
            allowed_message_types=[
                MessageType.SECURITY_VALIDATION,
                MessageType.SECURITY_ALERT,
                MessageType.TRANSACTION_VALIDATE,
                MessageType.TRANSACTION_CONFIRM,
                MessageType.STATE_UPDATE,
                MessageType.ADMIN_COMMAND
            ]
        )
        
        # Nexus to Dream gateway
        dream_gateway = SecurityGateway(
            security_level=self.security_level,
            allowed_message_types=[
                MessageType.TRANSACTION_SUBMIT,
                MessageType.STATE_QUERY,
                MessageType.RESOURCE_REQUEST,
                MessageType.RESOURCE_RELEASE
            ]
        )
        
        # Add gateways
        self.gateways["genesis_to_nexus"] = genesis_gateway
        self.gateways["nexus_to_dream"] = dream_gateway
        
    def register_message_handler(self, 
                                message_type: MessageType, 
                                handler: Callable[[Dict[str, Any]], Any]) -> None:
        """
        Register a handler for a specific message type.
        
        Args:
            message_type: The type of message to handle
            handler: The function to call when that message is received
        """
        self.message_handlers[message_type] = handler
        
    def send_message(self,
                     source_layer: str,
                     destination_layer: str,
                     message_type: MessageType,
                     message_data: Dict[str, Any],
                     sender_key_pair: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send a message from one layer to another.
        
        Args:
            source_layer: The layer sending the message
            destination_layer: The layer that should receive the message
            message_type: Type of message being sent
            message_data: The message data
            sender_key_pair: Key pair for signing the message
            
        Returns:
            Response from the destination layer, or None if delivery failed
        """
        # Determine the gateway to use
        gateway_key = f"{source_layer}_to_{destination_layer}"
        
        if gateway_key not in self.gateways:
            reversed_key = f"{destination_layer}_to_{source_layer}"
            if reversed_key not in self.gateways:
                # No gateway exists
                return None
            gateway = self.gateways[reversed_key]
        else:
            gateway = self.gateways[gateway_key]
            
        # Prepare full message
        full_message = {
            "type": message_type.value,
            "source": source_layer,
            "destination": destination_layer,
            "timestamp": time.time(),
            "message_id": str(uuid.uuid4()),
            "data": message_data
        }
        
        # Sign the message
        message_str = json.dumps(full_message, sort_keys=True)
        
        # This is a simplified signing - in production this would use proper quantum signing
        private_key = sender_key_pair.get("private_key", "")
        signature = hashlib.sha3_512((message_str + private_key).encode()).hexdigest()
        
        # Validate through gateway
        public_key = sender_key_pair.get("public_key", "")
        if not gateway.validate_message(full_message, signature, public_key):
            # Message rejected by gateway
            return None
            
        # Message passed gateway, handle it
        if message_type in self.message_handlers:
            # Call the registered handler
            return self.message_handlers[message_type](full_message)
        
        # No handler registered
        return {"status": "received", "message_id": full_message["message_id"]}
        
    def create_cross_layer_token(self,
                                source_layer: str,
                                destination_layer: str,
                                valid_duration: int = 60) -> Optional[Dict[str, Any]]:
        """
        Create a token for cross-layer access.
        
        Args:
            source_layer: The layer requesting access
            destination_layer: The layer to access
            valid_duration: How long the token should be valid
            
        Returns:
            A passage token, or None if the gateway doesn't exist
        """
        gateway_key = f"{source_layer}_to_{destination_layer}"
        
        if gateway_key not in self.gateways:
            reversed_key = f"{destination_layer}_to_{source_layer}"
            if reversed_key not in self.gateways:
                return None
            gateway = self.gateways[reversed_key]
        else:
            gateway = self.gateways[gateway_key]
            
        return gateway.create_passage_token(destination_layer, valid_duration)
        
    def update_security_level(self, level: SecurityLevel) -> None:
        """
        Update the security level across all gateways.
        
        Args:
            level: The new security level
        """
        self.security_level = level
        
        # Update all gateways
        for gateway in self.gateways.values():
            gateway.update_security_level(level)
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert bridge manager to dictionary for serialization"""
        return {
            "bridge_id": self.bridge_id,
            "security_level": self.security_level.name,
            "created_at": self.created_at,
            "gateways": {name: gateway.to_dict() 
                         for name, gateway in self.gateways.items()}
        }