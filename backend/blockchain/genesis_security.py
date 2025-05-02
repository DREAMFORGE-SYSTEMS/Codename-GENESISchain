"""
GenesisChain Security Module

This module enhances the GenesisChain with additional security features
for the three-layer architecture. It provides security validation for 
DreamChain operations through the NexusLayer.

Key components:
1. GenesisSecurityManager: Security manager for GenesisChain
2. SecurityValidator: Validator for DreamChain operations
3. Circuit Breaker: Emergency security controls
"""

import hashlib
import json
import time
import uuid
from typing import Dict, List, Any, Optional, Union, Callable

# Import quantum security
from quantum_security import (
    SecurityLevel,
    create_default_security_manager,
    QuantumRandomNumberGenerator
)


class SecurityAlert:
    """
    Represents a security alert in the GenesisChain security system.
    
    Alerts are generated when potential security issues are detected
    and can trigger automatic actions based on severity.
    """
    
    SEVERITY_INFO = "info"
    SEVERITY_WARNING = "warning"
    SEVERITY_CRITICAL = "critical"
    SEVERITY_EMERGENCY = "emergency"
    
    def __init__(self,
                source: str,
                message: str,
                severity: str,
                data: Optional[Dict[str, Any]] = None):
        """
        Initialize a new security alert.
        
        Args:
            source: Source of the alert
            message: Alert message
            severity: Alert severity
            data: Additional alert data
        """
        self.alert_id = str(uuid.uuid4())
        self.source = source
        self.message = message
        self.severity = severity
        self.data = data or {}
        self.timestamp = time.time()
        self.acknowledged = False
        self.response_actions = []
        
    def add_response_action(self, 
                          action: str,
                          status: str,
                          details: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a response action to the alert.
        
        Args:
            action: The action taken
            status: Status of the action
            details: Optional action details
        """
        self.response_actions.append({
            "action": action,
            "status": status,
            "timestamp": time.time(),
            "details": details or {}
        })
        
    def acknowledge(self) -> None:
        """Acknowledge the alert"""
        self.acknowledged = True
        self.add_response_action(
            action="acknowledge",
            status="completed"
        )
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary"""
        return {
            "alert_id": self.alert_id,
            "source": self.source,
            "message": self.message,
            "severity": self.severity,
            "data": self.data,
            "timestamp": self.timestamp,
            "acknowledged": self.acknowledged,
            "response_actions": self.response_actions
        }


class CircuitBreaker:
    """
    Implements a circuit breaker for emergency security controls.
    
    Circuit breakers can quickly isolate and shut down components
    of the blockchain system in case of security emergencies.
    """
    
    # Circuit states
    STATE_CLOSED = "closed"  # Normal operation
    STATE_OPEN = "open"      # Triggered, operations blocked
    STATE_HALF_OPEN = "half_open"  # Testing if issue is resolved
    
    def __init__(self, 
                name: str,
                description: str,
                failure_threshold: int = 5,
                reset_timeout: int = 300):
        """
        Initialize a new circuit breaker.
        
        Args:
            name: Name of the circuit breaker
            description: Description of its purpose
            failure_threshold: Number of failures before triggering
            reset_timeout: Seconds before attempting reset
        """
        self.breaker_id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.state = self.STATE_CLOSED
        self.last_failure_time = 0
        self.last_state_change = time.time()
        self.trip_history = []
        
    def execute(self, operation: Callable, *args, **kwargs) -> Any:
        """
        Execute an operation with circuit breaker protection.
        
        Args:
            operation: The operation to execute
            *args, **kwargs: Arguments for the operation
            
        Returns:
            Operation result
            
        Raises:
            Exception: If circuit is open or operation fails
        """
        # Check circuit state
        if self.state == self.STATE_OPEN:
            # Check if reset timeout has elapsed
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = self.STATE_HALF_OPEN
                self._record_state_change("half_open", "Reset timeout elapsed")
            else:
                raise Exception(f"Circuit breaker {self.name} is open")
                
        try:
            # Execute the operation
            result = operation(*args, **kwargs)
            
            # If successful and circuit was half-open, close it
            if self.state == self.STATE_HALF_OPEN:
                self.state = self.STATE_CLOSED
                self.failure_count = 0
                self._record_state_change("closed", "Successful operation")
                
            return result
            
        except Exception as e:
            # Record failure
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            # Check if threshold is reached
            if (self.state == self.STATE_CLOSED and 
                self.failure_count >= self.failure_threshold):
                self.state = self.STATE_OPEN
                self._record_state_change("open", f"Failure threshold reached: {str(e)}")
                
            # If half-open circuit fails, reopen it
            elif self.state == self.STATE_HALF_OPEN:
                self.state = self.STATE_OPEN
                self._record_state_change("open", f"Failed in half-open state: {str(e)}")
                
            # Re-raise the exception
            raise
            
    def _record_state_change(self, new_state: str, reason: str) -> None:
        """Record a state change in the trip history"""
        self.trip_history.append({
            "previous_state": self.state,
            "new_state": new_state,
            "timestamp": time.time(),
            "reason": reason,
            "failure_count": self.failure_count
        })
        
        self.last_state_change = time.time()
        
    def force_open(self, reason: str) -> None:
        """
        Force the circuit breaker open.
        
        Args:
            reason: Reason for forcing open
        """
        self.state = self.STATE_OPEN
        self._record_state_change("open", f"Forced open: {reason}")
        
    def force_close(self, reason: str) -> None:
        """
        Force the circuit breaker closed.
        
        Args:
            reason: Reason for forcing closed
        """
        self.state = self.STATE_CLOSED
        self.failure_count = 0
        self._record_state_change("closed", f"Forced closed: {reason}")
        
    def is_open(self) -> bool:
        """Check if circuit breaker is open"""
        return self.state == self.STATE_OPEN
        
    def get_status(self) -> Dict[str, Any]:
        """Get current circuit breaker status"""
        return {
            "breaker_id": self.breaker_id,
            "name": self.name,
            "state": self.state,
            "failure_count": self.failure_count,
            "last_failure": self.last_failure_time,
            "last_state_change": self.last_state_change,
            "trip_count": len(self.trip_history)
        }
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert circuit breaker to dictionary"""
        return {
            "breaker_id": self.breaker_id,
            "name": self.name,
            "description": self.description,
            "failure_threshold": self.failure_threshold,
            "reset_timeout": self.reset_timeout,
            "failure_count": self.failure_count,
            "state": self.state,
            "last_failure_time": self.last_failure_time,
            "last_state_change": self.last_state_change,
            "trip_history": self.trip_history
        }


class SecurityValidator:
    """
    Validator for DreamChain operations in GenesisChain.
    
    This class validates operations from DreamChain to ensure they
    meet GenesisChain's security requirements.
    """
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.STANDARD):
        """
        Initialize a new security validator.
        
        Args:
            security_level: Security level to enforce
        """
        self.validator_id = str(uuid.uuid4())
        self.security_level = security_level
        self.validation_count = 0
        self.rejection_count = 0
        self.created_at = time.time()
        self.circuit_breakers = {}
        self.qrng = QuantumRandomNumberGenerator()
        
        # Create default circuit breakers
        self._create_default_circuit_breakers()
        
    def _create_default_circuit_breakers(self) -> None:
        """Create default circuit breakers"""
        transaction_breaker = CircuitBreaker(
            name="transaction_validator",
            description="Circuit breaker for transaction validation",
            failure_threshold=10,
            reset_timeout=60
        )
        
        block_breaker = CircuitBreaker(
            name="block_validator",
            description="Circuit breaker for block validation",
            failure_threshold=3,
            reset_timeout=300
        )
        
        self.circuit_breakers["transaction"] = transaction_breaker
        self.circuit_breakers["block"] = block_breaker
        
    def validate_transaction(self, 
                            transaction: Dict[str, Any],
                            validation_level: str = "normal") -> Dict[str, Any]:
        """
        Validate a transaction from DreamChain.
        
        Args:
            transaction: Transaction data
            validation_level: Level of validation to perform
            
        Returns:
            Validation result
            
        Raises:
            Exception: If validation fails
        """
        # Use circuit breaker
        breaker = self.circuit_breakers["transaction"]
        
        # This is a simplified implementation - in a real system, 
        # validation would involve cryptographic verification, state checks, etc.
        
        def _validate():
            # Track validation attempt
            self.validation_count += 1
            
            # Basic validation
            required_fields = ["transaction_id", "sender", "recipient", "amount"]
            for field in required_fields:
                if field not in transaction:
                    self.rejection_count += 1
                    return {
                        "valid": False,
                        "reason": f"Missing required field: {field}"
                    }
                    
            # Inject quantum randomness for extra security
            validation_nonce = self.qrng.get_random_bytes(32).hex()
            
            # Additional validation based on security level
            if self.security_level.value >= SecurityLevel.HIGH.value:
                # For high security, perform deeper validation
                if "signatures" not in transaction or not transaction["signatures"]:
                    self.rejection_count += 1
                    return {
                        "valid": False,
                        "reason": "Missing signatures"
                    }
            
            # More extensive validation for higher levels
            if validation_level == "deep" or self.security_level.value >= SecurityLevel.VERY_HIGH.value:
                # For example, validate against history, check for double spending, etc.
                # This is a simplified placeholder
                pass
                
            # Simulate validation
            tx_hash = hashlib.sha3_256(json.dumps(transaction, sort_keys=True).encode()).hexdigest()
            
            return {
                "valid": True,
                "validation_id": str(uuid.uuid4()),
                "timestamp": time.time(),
                "transaction_id": transaction.get("transaction_id"),
                "transaction_hash": tx_hash,
                "validation_nonce": validation_nonce,
                "security_level": self.security_level.name
            }
            
        # Execute with circuit breaker protection
        try:
            return breaker.execute(_validate)
        except Exception as e:
            # If circuit breaker is triggered, return error
            self.rejection_count += 1
            return {
                "valid": False,
                "reason": f"Circuit breaker triggered: {str(e)}",
                "circuit_state": breaker.state
            }
            
    def validate_block(self, 
                      block: Dict[str, Any],
                      validation_level: str = "normal") -> Dict[str, Any]:
        """
        Validate a block from DreamChain.
        
        Args:
            block: Block data
            validation_level: Level of validation to perform
            
        Returns:
            Validation result
            
        Raises:
            Exception: If validation fails
        """
        # Use circuit breaker
        breaker = self.circuit_breakers["block"]
        
        # This is a simplified implementation
        
        def _validate():
            # Track validation attempt
            self.validation_count += 1
            
            # Basic validation
            required_fields = ["block_id", "previous_hash", "merkle_root"]
            for field in required_fields:
                if field not in block:
                    self.rejection_count += 1
                    return {
                        "valid": False,
                        "reason": f"Missing required field: {field}"
                    }
                    
            # Inject quantum randomness for extra security
            validation_nonce = self.qrng.get_random_bytes(32).hex()
            
            # Additional validation based on security level
            if self.security_level.value >= SecurityLevel.HIGH.value:
                # For high security, perform deeper validation
                if "transactions" not in block or not block["transactions"]:
                    self.rejection_count += 1
                    return {
                        "valid": False,
                        "reason": "Block has no transactions"
                    }
            
            # More extensive validation for higher levels
            if validation_level == "deep" or self.security_level.value >= SecurityLevel.VERY_HIGH.value:
                # For example, validate transaction integrity, check merkle root, etc.
                # This is a simplified placeholder
                pass
                
            # Validate transactions in the block
            validated_transactions = []
            if "transaction_ids" in block:
                for tx_id in block["transaction_ids"]:
                    validated_transactions.append(tx_id)
                
            # Simulate validation
            block_hash = hashlib.sha3_256(json.dumps({
                "previous_hash": block.get("previous_hash"),
                "merkle_root": block.get("merkle_root")
            }, sort_keys=True).encode()).hexdigest()
            
            return {
                "valid": True,
                "validation_id": str(uuid.uuid4()),
                "timestamp": time.time(),
                "block_id": block.get("block_id"),
                "block_hash": block_hash,
                "validation_nonce": validation_nonce,
                "verified_transactions": validated_transactions,
                "security_level": self.security_level.name
            }
            
        # Execute with circuit breaker protection
        try:
            return breaker.execute(_validate)
        except Exception as e:
            # If circuit breaker is triggered, return error
            self.rejection_count += 1
            return {
                "valid": False,
                "reason": f"Circuit breaker triggered: {str(e)}",
                "circuit_state": breaker.state
            }
            
    def update_security_level(self, level: SecurityLevel) -> None:
        """
        Update the security level.
        
        Args:
            level: The new security level
        """
        self.security_level = level
        
    def reset_circuit_breaker(self, breaker_name: str, reason: str) -> bool:
        """
        Reset a circuit breaker.
        
        Args:
            breaker_name: Name of the circuit breaker
            reason: Reason for reset
            
        Returns:
            True if reset was successful, False otherwise
        """
        if breaker_name not in self.circuit_breakers:
            return False
            
        breaker = self.circuit_breakers[breaker_name]
        breaker.force_close(reason)
        return True
        
    def get_circuit_breaker_status(self, breaker_name: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a circuit breaker.
        
        Args:
            breaker_name: Name of the circuit breaker
            
        Returns:
            Circuit breaker status or None if not found
        """
        if breaker_name not in self.circuit_breakers:
            return None
            
        return self.circuit_breakers[breaker_name].get_status()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert validator to dictionary"""
        return {
            "validator_id": self.validator_id,
            "security_level": self.security_level.name,
            "validation_count": self.validation_count,
            "rejection_count": self.rejection_count,
            "created_at": self.created_at,
            "circuit_breakers": {name: breaker.get_status() 
                               for name, breaker in self.circuit_breakers.items()}
        }


class GenesisSecurityManager:
    """
    Security manager for GenesisChain in the three-layer architecture.
    
    This class manages security features for GenesisChain, providing
    interfaces for NexusLayer and DreamChain to interact with GenesisChain's
    security systems.
    """
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.STANDARD):
        """
        Initialize a new security manager.
        
        Args:
            security_level: Security level to enforce
        """
        self.manager_id = str(uuid.uuid4())
        self.security_level = security_level
        self.created_at = time.time()
        self.validators = {}
        self.alerts = []
        self.security_gates = {}
        self.alert_handlers = []
        self.qrng = QuantumRandomNumberGenerator()
        
        # Create default validators
        self._create_default_validators()
        
        # Create security gates
        self._create_security_gates()
        
    def _create_default_validators(self) -> None:
        """Create default validators"""
        # Create transaction validator
        tx_validator = SecurityValidator(self.security_level)
        self.validators["transaction"] = tx_validator
        
        # Create block validator
        block_validator = SecurityValidator(self.security_level)
        self.validators["block"] = block_validator
        
    def _create_security_gates(self) -> None:
        """Create security gates for different operations"""
        # Standard security gate
        self.security_gates["standard"] = {
            "name": "standard",
            "validation_level": "normal",
            "requires_approval": False,
            "approval_timeout": 0,
            "max_operations_per_minute": 100
        }
        
        # High security gate
        self.security_gates["high"] = {
            "name": "high",
            "validation_level": "deep",
            "requires_approval": False,
            "approval_timeout": 0,
            "max_operations_per_minute": 20
        }
        
        # Critical security gate
        self.security_gates["critical"] = {
            "name": "critical",
            "validation_level": "maximum",
            "requires_approval": True,
            "approval_timeout": 300,  # 5 minutes
            "max_operations_per_minute": 5
        }
        
    def validate_transaction(self, 
                            transaction: Dict[str, Any],
                            gate_name: str = "standard") -> Dict[str, Any]:
        """
        Validate a transaction using the specified security gate.
        
        Args:
            transaction: The transaction to validate
            gate_name: The security gate to use
            
        Returns:
            Validation result
        """
        # Get the security gate
        if gate_name not in self.security_gates:
            gate_name = "standard"
            
        gate = self.security_gates[gate_name]
        
        # Get validator
        validator = self.validators["transaction"]
        
        # Validate transaction
        validation_result = validator.validate_transaction(
            transaction=transaction,
            validation_level=gate["validation_level"]
        )
        
        # Handle validation result
        if not validation_result.get("valid", False):
            # Create alert for failed validation
            alert = SecurityAlert(
                source="transaction_validator",
                message=f"Transaction validation failed: {validation_result.get('reason', 'Unknown reason')}",
                severity=SecurityAlert.SEVERITY_WARNING,
                data={
                    "transaction_id": transaction.get("transaction_id"),
                    "validation_result": validation_result
                }
            )
            
            self._add_alert(alert)
            
        return validation_result
        
    def validate_block(self, 
                      block: Dict[str, Any],
                      gate_name: str = "standard") -> Dict[str, Any]:
        """
        Validate a block using the specified security gate.
        
        Args:
            block: The block to validate
            gate_name: The security gate to use
            
        Returns:
            Validation result
        """
        # Get the security gate
        if gate_name not in self.security_gates:
            gate_name = "standard"
            
        gate = self.security_gates[gate_name]
        
        # Get validator
        validator = self.validators["block"]
        
        # Validate block
        validation_result = validator.validate_block(
            block=block,
            validation_level=gate["validation_level"]
        )
        
        # Handle validation result
        if not validation_result.get("valid", False):
            # Create alert for failed validation
            alert = SecurityAlert(
                source="block_validator",
                message=f"Block validation failed: {validation_result.get('reason', 'Unknown reason')}",
                severity=SecurityAlert.SEVERITY_WARNING,
                data={
                    "block_id": block.get("block_id"),
                    "validation_result": validation_result
                }
            )
            
            self._add_alert(alert)
            
        return validation_result
        
    def _add_alert(self, alert: SecurityAlert) -> None:
        """Add an alert to the manager and trigger handlers"""
        self.alerts.append(alert)
        
        # Trigger alert handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                # Log the error but continue with other handlers
                print(f"Error in alert handler: {str(e)}")
                
        # Limit alert history
        if len(self.alerts) > 1000:
            self.alerts = self.alerts[-1000:]
            
    def register_alert_handler(self, handler: Callable[[SecurityAlert], None]) -> None:
        """
        Register a handler for security alerts.
        
        Args:
            handler: Function to call when an alert is created
        """
        self.alert_handlers.append(handler)
        
    def create_alert(self, 
                    source: str,
                    message: str,
                    severity: str,
                    data: Optional[Dict[str, Any]] = None) -> SecurityAlert:
        """
        Create a new security alert.
        
        Args:
            source: Source of the alert
            message: Alert message
            severity: Alert severity
            data: Additional alert data
            
        Returns:
            The created alert
        """
        alert = SecurityAlert(
            source=source,
            message=message,
            severity=severity,
            data=data
        )
        
        self._add_alert(alert)
        return alert
        
    def get_alert(self, alert_id: str) -> Optional[SecurityAlert]:
        """
        Get an alert by ID.
        
        Args:
            alert_id: The alert ID
            
        Returns:
            The alert or None if not found
        """
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                return alert
        return None
        
    def acknowledge_alert(self, alert_id: str) -> bool:
        """
        Acknowledge an alert.
        
        Args:
            alert_id: The alert ID
            
        Returns:
            True if acknowledged, False if not found
        """
        alert = self.get_alert(alert_id)
        if alert:
            alert.acknowledge()
            return True
        return False
        
    def get_active_alerts(self, severity: Optional[str] = None) -> List[SecurityAlert]:
        """
        Get active (unacknowledged) alerts.
        
        Args:
            severity: Optional severity filter
            
        Returns:
            List of active alerts
        """
        alerts = [a for a in self.alerts if not a.acknowledged]
        
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
            
        return alerts
        
    def reset_circuit_breaker(self, 
                             validator_type: str,
                             breaker_name: str,
                             reason: str) -> bool:
        """
        Reset a circuit breaker.
        
        Args:
            validator_type: Type of validator
            breaker_name: Name of the circuit breaker
            reason: Reason for reset
            
        Returns:
            True if reset was successful, False otherwise
        """
        if validator_type not in self.validators:
            return False
            
        validator = self.validators[validator_type]
        return validator.reset_circuit_breaker(breaker_name, reason)
        
    def update_security_level(self, level: SecurityLevel) -> None:
        """
        Update the security level.
        
        Args:
            level: The new security level
        """
        self.security_level = level
        
        # Update validators
        for validator in self.validators.values():
            validator.update_security_level(level)
            
        # Create alert for level change
        self.create_alert(
            source="security_manager",
            message=f"Security level updated to {level.name}",
            severity=SecurityAlert.SEVERITY_INFO,
            data={"new_level": level.name}
        )
        
    def get_validator_status(self, validator_type: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a validator.
        
        Args:
            validator_type: Type of validator
            
        Returns:
            Validator status or None if not found
        """
        if validator_type not in self.validators:
            return None
            
        return self.validators[validator_type].to_dict()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert security manager to dictionary"""
        return {
            "manager_id": self.manager_id,
            "security_level": self.security_level.name,
            "created_at": self.created_at,
            "validators": {name: validator.to_dict() 
                         for name, validator in self.validators.items()},
            "security_gates": self.security_gates,
            "active_alerts": len(self.get_active_alerts()),
            "total_alerts": len(self.alerts)
        }