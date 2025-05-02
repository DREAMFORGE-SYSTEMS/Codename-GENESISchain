"""
THE FORGE Quantum Link Module

This module implements QUANTUM-LINK Technology for THE FORGE, enabling
cross-dimensional connections between different blockchain systems.
QUANTUM-LINKs provide secure, high-bandwidth channels for communication
and energy transfer across the blockchain architecture.

Key components:
1. QuantumLinkManager: Manages QUANTUM-LINKs
2. LinkStatus: Tracks status of links
3. LinkProtocol: Protocols for quantum communication
"""

import hashlib
import json
import time
import uuid
import math
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Union, Tuple, Set

# Import quantum security for enhanced entropy
from quantum_security import QuantumRandomNumberGenerator


class LinkType(Enum):
    """Types of quantum links"""
    ENERGY = auto()      # Energy transfer link
    DATA = auto()        # Data transfer link
    SECURITY = auto()    # Security validation link
    DIMENSIONAL = auto() # Cross-dimensional link
    EMERGENCY = auto()   # Emergency communication link


class LinkStatus(Enum):
    """Status of a quantum link"""
    INITIALIZING = auto()  # Link is being established
    ACTIVE = auto()        # Link is active and stable
    UNSTABLE = auto()      # Link is active but unstable
    DEGRADED = auto()      # Link is active but degraded
    DISCONNECTED = auto()  # Link is temporarily disconnected
    TERMINATED = auto()    # Link is permanently terminated


class LinkProtocol:
    """
    Protocols for quantum communication over QUANTUM-LINKs.
    
    Defines the methods and standards for secure, quantum-resistant
    communication between blockchain systems across dimensions.
    """
    
    # Protocol identifiers
    ENERGY_TRANSFER = "QLP-ENERGY-1.0"
    DATA_SYNC = "QLP-SYNC-1.0"
    SECURITY_VALIDATION = "QLP-SECURITY-1.0"
    DIMENSIONAL_BRIDGE = "QLP-BRIDGE-1.0"
    EMERGENCY_PROTOCOL = "QLP-EMERGENCY-1.0"
    
    # Protocol headers
    HEADERS = {
        ENERGY_TRANSFER: {
            "version": "1.0",
            "encryption": "quantum-resistant",
            "compression": "none",
            "priority": "high"
        },
        DATA_SYNC: {
            "version": "1.0",
            "encryption": "quantum-resistant",
            "compression": "adaptive",
            "priority": "normal"
        },
        SECURITY_VALIDATION: {
            "version": "1.0",
            "encryption": "quantum-resistant",
            "compression": "none",
            "priority": "critical"
        },
        DIMENSIONAL_BRIDGE: {
            "version": "1.0",
            "encryption": "quantum-resistant",
            "compression": "none",
            "priority": "highest"
        },
        EMERGENCY_PROTOCOL: {
            "version": "1.0",
            "encryption": "quantum-resistant",
            "compression": "minimal",
            "priority": "emergency"
        }
    }
    
    @staticmethod
    def create_message(protocol: str, 
                      source: str,
                      destination: str,
                      message_type: str,
                      payload: Dict[str, Any],
                      qrng: QuantumRandomNumberGenerator) -> Dict[str, Any]:
        """
        Create a protocol message for transmission over a QUANTUM-LINK.
        
        Args:
            protocol: Protocol identifier
            source: Source system
            destination: Destination system
            message_type: Type of message
            payload: Message payload
            qrng: Quantum random number generator
            
        Returns:
            Protocol message
        """
        # Get protocol headers
        headers = LinkProtocol.HEADERS.get(protocol, {})
        
        # Generate quantum nonce
        quantum_nonce = qrng.get_random_bytes(16).hex()
        
        # Create message
        message = {
            "protocol": protocol,
            "headers": headers,
            "source": source,
            "destination": destination,
            "message_type": message_type,
            "timestamp": time.time(),
            "message_id": str(uuid.uuid4()),
            "quantum_nonce": quantum_nonce,
            "payload": payload
        }
        
        # Generate hash signature
        message_str = json.dumps(message, sort_keys=True)
        message["signature"] = hashlib.sha3_512(message_str.encode()).hexdigest()
        
        return message
    
    @staticmethod
    def verify_message(message: Dict[str, Any]) -> bool:
        """
        Verify a protocol message.
        
        Args:
            message: Protocol message
            
        Returns:
            True if message is valid
        """
        # Check required fields
        required_fields = ["protocol", "headers", "source", "destination", 
                          "message_type", "timestamp", "message_id", 
                          "quantum_nonce", "payload", "signature"]
                          
        if not all(field in message for field in required_fields):
            return False
            
        # Verify signature
        signature = message["signature"]
        message_copy = message.copy()
        message_copy.pop("signature")
        
        message_str = json.dumps(message_copy, sort_keys=True)
        calculated_signature = hashlib.sha3_512(message_str.encode()).hexdigest()
        
        return signature == calculated_signature
    
    @staticmethod
    def get_protocol_for_link_type(link_type: LinkType) -> str:
        """
        Get the appropriate protocol for a link type.
        
        Args:
            link_type: Type of link
            
        Returns:
            Protocol identifier
        """
        protocol_map = {
            LinkType.ENERGY: LinkProtocol.ENERGY_TRANSFER,
            LinkType.DATA: LinkProtocol.DATA_SYNC,
            LinkType.SECURITY: LinkProtocol.SECURITY_VALIDATION,
            LinkType.DIMENSIONAL: LinkProtocol.DIMENSIONAL_BRIDGE,
            LinkType.EMERGENCY: LinkProtocol.EMERGENCY_PROTOCOL
        }
        
        return protocol_map.get(link_type, LinkProtocol.DATA_SYNC)


class QuantumLinkConnection:
    """
    Represents an active quantum link connection.
    
    A QuantumLinkConnection is a specific instance of a QUANTUM-LINK
    between two systems, with defined properties and capabilities.
    """
    
    def __init__(self,
                 source_system: str,
                 target_system: str,
                 link_type: LinkType,
                 bandwidth: float = 100.0):
        """
        Initialize a new quantum link connection.
        
        Args:
            source_system: Source system
            target_system: Target system
            link_type: Type of link
            bandwidth: Link bandwidth
        """
        self.connection_id = str(uuid.uuid4())
        self.source_system = source_system
        self.target_system = target_system
        self.link_type = link_type
        self.link_protocol = LinkProtocol.get_protocol_for_link_type(link_type)
        self.status = LinkStatus.INITIALIZING
        self.bandwidth = bandwidth
        self.stability = 100.0  # Percentage
        self.latency = 0.0  # Milliseconds
        self.created_at = time.time()
        self.last_activity = self.created_at
        self.packet_count = 0
        self.error_count = 0
        self.transferred_data = 0  # Bytes
        self.energy_transferred = 0.0  # Energy units
        self.quantum_metrics = {}
        self.qrng = QuantumRandomNumberGenerator()
        
        # Initialize quantum metrics
        self._initialize_quantum_metrics()
    
    def _initialize_quantum_metrics(self) -> None:
        """Initialize quantum-specific metrics for the link"""
        self.quantum_metrics = {
            "entanglement_strength": 1.0,
            "quantum_coherence": 100.0,
            "dimensional_stability": 100.0,
            "quantum_noise": 0.0,
            "quantum_bandwidth": self.bandwidth,
            "quantum_frequency": self.qrng.get_random_float() * 1000
        }
    
    def send_message(self, 
                    message_type: str,
                    payload: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Send a message over the quantum link.
        
        Args:
            message_type: Type of message
            payload: Message payload
            
        Returns:
            Tuple of (success, message or error)
        """
        # Check if link is operational
        if self.status in [LinkStatus.DISCONNECTED, LinkStatus.TERMINATED]:
            return False, {"error": "Link is not operational"}
        
        # Create protocol message
        message = LinkProtocol.create_message(
            protocol=self.link_protocol,
            source=self.source_system,
            destination=self.target_system,
            message_type=message_type,
            payload=payload,
            qrng=self.qrng
        )
        
        # Determine message size
        message_size = len(json.dumps(message).encode())
        
        # Check if we have enough bandwidth
        if message_size > self.bandwidth:
            self.error_count += 1
            return False, {"error": "Message exceeds bandwidth"}
        
        # Update link metrics
        self.packet_count += 1
        self.transferred_data += message_size
        self.last_activity = time.time()
        
        # Calculate success probability based on stability
        success_probability = self.stability / 100.0
        
        # Simulate transmission
        if self.qrng.get_random_float() <= success_probability:
            # Simulate latency
            self.latency = (self.bandwidth / max(1.0, self.quantum_metrics["quantum_bandwidth"])) * 5.0
            
            # Update quantum metrics
            self._update_quantum_metrics_after_send()
            
            return True, message
        else:
            # Transmission failed
            self.error_count += 1
            self._update_stability(-5.0)  # Decrease stability
            
            return False, {"error": "Transmission failed", "reason": "Quantum decoherence"}
    
    def transfer_energy(self, amount: float) -> Tuple[bool, float]:
        """
        Transfer energy over the quantum link.
        
        Args:
            amount: Amount of energy to transfer
            
        Returns:
            Tuple of (success, amount transferred)
        """
        # Check if link is appropriate for energy transfer
        if self.link_type != LinkType.ENERGY and self.link_type != LinkType.DIMENSIONAL:
            return False, 0.0
        
        # Check if link is operational
        if self.status in [LinkStatus.DISCONNECTED, LinkStatus.TERMINATED]:
            return False, 0.0
        
        # Calculate maximum transfer capacity
        max_transfer = self.bandwidth * (self.stability / 100.0)
        
        # Limit transfer amount
        actual_transfer = min(amount, max_transfer)
        
        # Update link metrics
        self.energy_transferred += actual_transfer
        self.last_activity = time.time()
        
        # Calculate success probability based on stability
        success_probability = self.stability / 100.0
        
        # Simulate transfer
        if self.qrng.get_random_float() <= success_probability:
            # Update quantum metrics
            self._update_quantum_metrics_after_transfer(actual_transfer)
            
            return True, actual_transfer
        else:
            # Transfer failed
            self.error_count += 1
            self._update_stability(-5.0)  # Decrease stability
            
            return False, 0.0
    
    def _update_quantum_metrics_after_send(self) -> None:
        """Update quantum metrics after sending a message"""
        # Slightly decrease coherence with each message
        coherence_decrease = (1.0 / max(1, self.packet_count)) * 10.0
        self.quantum_metrics["quantum_coherence"] = max(
            0.0, self.quantum_metrics["quantum_coherence"] - coherence_decrease
        )
        
        # Slightly increase quantum noise
        noise_increase = (1.0 / max(1, self.packet_count)) * 5.0
        self.quantum_metrics["quantum_noise"] = min(
            100.0, self.quantum_metrics["quantum_noise"] + noise_increase
        )
        
        # Update stability based on quantum metrics
        self._update_stability_from_quantum_metrics()
    
    def _update_quantum_metrics_after_transfer(self, amount: float) -> None:
        """
        Update quantum metrics after energy transfer.
        
        Args:
            amount: Amount of energy transferred
        """
        # Energy transfer affects entanglement strength
        entanglement_decrease = (amount / 100.0) * 0.1
        self.quantum_metrics["entanglement_strength"] = max(
            0.1, self.quantum_metrics["entanglement_strength"] - entanglement_decrease
        )
        
        # Energy transfer affects dimensional stability
        stability_decrease = (amount / 100.0) * 0.2
        self.quantum_metrics["dimensional_stability"] = max(
            0.0, self.quantum_metrics["dimensional_stability"] - stability_decrease
        )
        
        # Update stability based on quantum metrics
        self._update_stability_from_quantum_metrics()
    
    def _update_stability_from_quantum_metrics(self) -> None:
        """Update link stability based on quantum metrics"""
        # Calculate stability from quantum metrics
        coherence_factor = self.quantum_metrics["quantum_coherence"] / 100.0
        entanglement_factor = self.quantum_metrics["entanglement_strength"]
        dimensional_factor = self.quantum_metrics["dimensional_stability"] / 100.0
        noise_factor = (100.0 - self.quantum_metrics["quantum_noise"]) / 100.0
        
        # Weighted calculation of stability
        new_stability = (
            coherence_factor * 0.3 +
            entanglement_factor * 0.3 +
            dimensional_factor * 0.2 +
            noise_factor * 0.2
        ) * 100.0
        
        # Set new stability
        self._update_stability(new_stability - self.stability)
    
    def _update_stability(self, change: float) -> None:
        """
        Update link stability by a specific amount.
        
        Args:
            change: Amount to change stability by
        """
        # Update stability
        self.stability = max(0.0, min(100.0, self.stability + change))
        
        # Update status based on stability
        if self.stability < 20.0:
            self.status = LinkStatus.DISCONNECTED
        elif self.stability < 40.0:
            self.status = LinkStatus.DEGRADED
        elif self.stability < 70.0:
            self.status = LinkStatus.UNSTABLE
        else:
            self.status = LinkStatus.ACTIVE
    
    def regenerate(self) -> None:
        """Regenerate link stability and quantum metrics over time"""
        # Only regenerate if the link isn't terminated
        if self.status == LinkStatus.TERMINATED:
            return
        
        # Calculate time since last activity
        time_since_activity = time.time() - self.last_activity
        
        # Only regenerate after a period of inactivity
        if time_since_activity > 30.0:
            # Regenerate stability
            stability_regen = min(5.0, time_since_activity * 0.05)
            self._update_stability(stability_regen)
            
            # Regenerate quantum coherence
            coherence_regen = min(3.0, time_since_activity * 0.03)
            self.quantum_metrics["quantum_coherence"] = min(
                100.0, self.quantum_metrics["quantum_coherence"] + coherence_regen
            )
            
            # Reduce quantum noise
            noise_reduction = min(2.0, time_since_activity * 0.02)
            self.quantum_metrics["quantum_noise"] = max(
                0.0, self.quantum_metrics["quantum_noise"] - noise_reduction
            )
            
            # Regenerate entanglement strength
            entanglement_regen = min(0.05, time_since_activity * 0.0005)
            self.quantum_metrics["entanglement_strength"] = min(
                1.0, self.quantum_metrics["entanglement_strength"] + entanglement_regen
            )
            
            # Regenerate dimensional stability
            stability_regen = min(2.0, time_since_activity * 0.02)
            self.quantum_metrics["dimensional_stability"] = min(
                100.0, self.quantum_metrics["dimensional_stability"] + stability_regen
            )
            
            # If disconnected but stability is now adequate, reconnect
            if self.status == LinkStatus.DISCONNECTED and self.stability >= 20.0:
                self.status = LinkStatus.UNSTABLE
    
    def terminate(self, reason: str) -> None:
        """
        Permanently terminate the quantum link.
        
        Args:
            reason: Reason for termination
        """
        self.status = LinkStatus.TERMINATED
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the quantum link connection to a dictionary representation.
        
        Returns:
            Dictionary representation of the quantum link connection
        """
        # Regenerate link before returning status
        self.regenerate()
        
        return {
            "connection_id": self.connection_id,
            "source_system": self.source_system,
            "target_system": self.target_system,
            "link_type": self.link_type.name,
            "link_protocol": self.link_protocol,
            "status": self.status.name,
            "bandwidth": self.bandwidth,
            "stability": self.stability,
            "latency": self.latency,
            "created_at": self.created_at,
            "last_activity": self.last_activity,
            "packet_count": self.packet_count,
            "error_count": self.error_count,
            "transferred_data": self.transferred_data,
            "energy_transferred": self.energy_transferred,
            "quantum_metrics": self.quantum_metrics,
            "age": time.time() - self.created_at
        }


class QuantumLinkManager:
    """
    Manages QUANTUM-LINKs between different systems.
    
    The QuantumLinkManager is responsible for creating, monitoring, and
    maintaining QUANTUM-LINKs for THE FORGE, enabling secure cross-dimensional
    communication between blockchain systems.
    """
    
    def __init__(self, quantum_forge):
        """
        Initialize a new quantum link manager.
        
        Args:
            quantum_forge: The quantum forge providing energy
        """
        self.manager_id = str(uuid.uuid4())
        self.quantum_forge = quantum_forge
        self.connections = {}  # connection_id -> QuantumLinkConnection
        self.system_links = {}  # system_name -> set(connection_ids)
        self.created_at = time.time()
        self.last_maintenance = self.created_at
        self.maintenance_interval = 60.0  # seconds
        self.link_history = []
        self.qrng = QuantumRandomNumberGenerator()
    
    def create_link(self,
                   source_system: str,
                   target_system: str,
                   link_type: LinkType,
                   bandwidth: float = 100.0) -> Tuple[bool, Optional[str]]:
        """
        Create a new QUANTUM-LINK between two systems.
        
        Args:
            source_system: Source system
            target_system: Target system
            link_type: Type of link
            bandwidth: Link bandwidth
            
        Returns:
            Tuple of (success, connection_id or error message)
        """
        # Calculate energy cost for link creation
        energy_cost = self._calculate_link_energy_cost(link_type, bandwidth)
        
        # Check if we have enough energy
        if self.quantum_forge.current_energy < energy_cost:
            return False, "Insufficient energy in THE FORGE"
        
        # Consume energy
        self.quantum_forge.current_energy -= energy_cost
        
        # Create the connection
        connection = QuantumLinkConnection(
            source_system=source_system,
            target_system=target_system,
            link_type=link_type,
            bandwidth=bandwidth
        )
        
        # Store the connection
        self.connections[connection.connection_id] = connection
        
        # Update system links mapping
        for system in [source_system, target_system]:
            if system not in self.system_links:
                self.system_links[system] = set()
            self.system_links[system].add(connection.connection_id)
        
        # Add to history
        self.link_history.append({
            "event": "link_created",
            "timestamp": time.time(),
            "connection_id": connection.connection_id,
            "source_system": source_system,
            "target_system": target_system,
            "link_type": link_type.name,
            "energy_cost": energy_cost
        })
        
        return True, connection.connection_id
    
    def _calculate_link_energy_cost(self, link_type: LinkType, bandwidth: float) -> float:
        """
        Calculate energy cost for creating a link.
        
        Args:
            link_type: Type of link
            bandwidth: Link bandwidth
            
        Returns:
            Energy cost
        """
        # Base cost by link type
        base_costs = {
            LinkType.ENERGY: 100.0,
            LinkType.DATA: 50.0,
            LinkType.SECURITY: 75.0,
            LinkType.DIMENSIONAL: 200.0,
            LinkType.EMERGENCY: 30.0
        }
        
        base_cost = base_costs.get(link_type, 50.0)
        
        # Adjust for bandwidth
        bandwidth_factor = bandwidth / 100.0
        
        # Add quantum fluctuation
        fluctuation = 0.9 + self.qrng.get_random_float() * 0.2  # 0.9-1.1
        
        return base_cost * bandwidth_factor * fluctuation
    
    def get_link(self, connection_id: str) -> Optional[QuantumLinkConnection]:
        """
        Get a quantum link connection.
        
        Args:
            connection_id: ID of the connection
            
        Returns:
            The connection or None if not found
        """
        return self.connections.get(connection_id)
    
    def get_system_links(self, system_name: str) -> List[Dict[str, Any]]:
        """
        Get all links for a system.
        
        Args:
            system_name: Name of the system
            
        Returns:
            List of connections for the system
        """
        connection_ids = self.system_links.get(system_name, set())
        return [
            self.connections[conn_id].to_dict()
            for conn_id in connection_ids
            if conn_id in self.connections
        ]
    
    def send_message(self,
                    connection_id: str,
                    message_type: str,
                    payload: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Send a message over a quantum link.
        
        Args:
            connection_id: ID of the connection
            message_type: Type of message
            payload: Message payload
            
        Returns:
            Tuple of (success, result or error)
        """
        # Get the connection
        connection = self.get_link(connection_id)
        if not connection:
            return False, {"error": "Connection not found"}
        
        # Send the message
        success, result = connection.send_message(message_type, payload)
        
        # Record in history if significant
        if not success or message_type == "critical":
            self.link_history.append({
                "event": "message_sent" if success else "message_failed",
                "timestamp": time.time(),
                "connection_id": connection_id,
                "message_type": message_type,
                "success": success
            })
        
        return success, result
    
    def transfer_energy(self,
                       connection_id: str,
                       amount: float) -> Tuple[bool, float]:
        """
        Transfer energy over a quantum link.
        
        Args:
            connection_id: ID of the connection
            amount: Amount of energy to transfer
            
        Returns:
            Tuple of (success, amount transferred)
        """
        # Get the connection
        connection = self.get_link(connection_id)
        if not connection:
            return False, 0.0
        
        # Transfer energy
        success, transferred = connection.transfer_energy(amount)
        
        # Record in history
        self.link_history.append({
            "event": "energy_transferred" if success else "energy_transfer_failed",
            "timestamp": time.time(),
            "connection_id": connection_id,
            "amount_requested": amount,
            "amount_transferred": transferred if success else 0.0,
            "success": success
        })
        
        return success, transferred
    
    def maintain_links(self) -> Dict[str, Any]:
        """
        Perform maintenance on all quantum links.
        
        Returns:
            Maintenance results
        """
        # Only maintain links periodically
        current_time = time.time()
        if current_time - self.last_maintenance < self.maintenance_interval:
            return {"status": "skipped", "reason": "Maintenance interval not reached"}
        
        self.last_maintenance = current_time
        
        # Metrics to track
        regenerated = 0
        terminated = 0
        
        # Process each connection
        for connection_id, connection in list(self.connections.items()):
            # Skip terminated connections
            if connection.status == LinkStatus.TERMINATED:
                continue
            
            # Regenerate the connection
            connection.regenerate()
            regenerated += 1
            
            # Check if connection has been inactive for too long
            inactivity_threshold = 24 * 60 * 60  # 24 hours
            if (current_time - connection.last_activity) > inactivity_threshold:
                # Terminate connection due to inactivity
                connection.terminate("Terminated due to prolonged inactivity")
                terminated += 1
                
                # Record in history
                self.link_history.append({
                    "event": "link_terminated",
                    "timestamp": current_time,
                    "connection_id": connection_id,
                    "reason": "Inactivity",
                    "inactivity_duration": current_time - connection.last_activity
                })
        
        # Return maintenance results
        return {
            "status": "completed",
            "timestamp": current_time,
            "links_regenerated": regenerated,
            "links_terminated": terminated
        }
    
    def terminate_link(self, connection_id: str, reason: str) -> bool:
        """
        Terminate a quantum link.
        
        Args:
            connection_id: ID of the connection
            reason: Reason for termination
            
        Returns:
            True if termination succeeded
        """
        # Get the connection
        connection = self.get_link(connection_id)
        if not connection:
            return False
        
        # Terminate the connection
        connection.terminate(reason)
        
        # Record in history
        self.link_history.append({
            "event": "link_terminated",
            "timestamp": time.time(),
            "connection_id": connection_id,
            "reason": reason
        })
        
        return True
    
    def get_link_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about quantum links.
        
        Returns:
            Link statistics
        """
        # Count links by status
        status_counts = {}
        for connection in self.connections.values():
            status = connection.status.name
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Count links by type
        type_counts = {}
        for connection in self.connections.values():
            link_type = connection.link_type.name
            type_counts[link_type] = type_counts.get(link_type, 0) + 1
        
        # Calculate total data and energy transferred
        total_data = sum(c.transferred_data for c in self.connections.values())
        total_energy = sum(c.energy_transferred for c in self.connections.values())
        
        # Get active links (not terminated)
        active_links = [c for c in self.connections.values() 
                       if c.status != LinkStatus.TERMINATED]
        
        # Calculate average stability
        avg_stability = (
            sum(c.stability for c in active_links) / max(1, len(active_links))
        )
        
        return {
            "total_links": len(self.connections),
            "active_links": len(active_links),
            "status_counts": status_counts,
            "type_counts": type_counts,
            "total_data_transferred": total_data,
            "total_energy_transferred": total_energy,
            "average_stability": avg_stability,
            "connected_systems": len(self.system_links)
        }
    
    def get_recent_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get recent link history.
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            Recent link history
        """
        return sorted(self.link_history, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the quantum link manager to a dictionary representation.
        
        Returns:
            Dictionary representation of the quantum link manager
        """
        return {
            "manager_id": self.manager_id,
            "created_at": self.created_at,
            "last_maintenance": self.last_maintenance,
            "maintenance_interval": self.maintenance_interval,
            "connection_count": len(self.connections),
            "system_count": len(self.system_links),
            "systems": list(self.system_links.keys()),
            "statistics": self.get_link_statistics(),
            "recent_history": self.get_recent_history(5)
        }