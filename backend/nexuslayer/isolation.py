"""
NexusLayer Isolation Module

This module implements security isolation mechanisms for the NexusLayer,
allowing the containment of security breaches and compartmentalization
of the blockchain architecture.

Key features:
1. Security Bulkheads: Isolation barriers to contain threats
2. Security Zones: Designated areas with specific security properties
3. Isolation Levels: Different levels of isolation for different threats
"""

import enum
import json
import time
import uuid
from typing import Dict, List, Any, Optional, Set, Callable

# Import quantum security for enhanced security
from quantum_security import (
    SecurityLevel,
    QuantumRandomNumberGenerator
)


class IsolationLevel(enum.Enum):
    """Levels of isolation that can be applied to security zones"""
    
    MONITORING = "monitoring"       # Normal monitoring, no restrictions
    RESTRICTED = "restricted"       # Limited access, increased validation
    QUARANTINE = "quarantine"       # Highly restricted, deep inspection of all traffic
    LOCKDOWN = "lockdown"           # No incoming/outgoing connections allowed
    JETTISON = "jettison"           # Complete isolation, prepared for removal


class SecurityZone:
    """
    Represents a security zone within the blockchain architecture.
    
    A security zone is a logical grouping of components with similar
    security requirements and risk profiles.
    """
    
    def __init__(self, 
                 name: str,
                 description: str,
                 security_level: SecurityLevel = SecurityLevel.STANDARD,
                 parent_zone: Optional[str] = None):
        """
        Initialize a new security zone.
        
        Args:
            name: Name of the security zone
            description: Description of the zone and its purpose
            security_level: Security level to enforce
            parent_zone: Optional parent zone ID
        """
        self.zone_id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.security_level = security_level
        self.parent_zone = parent_zone
        self.isolation_level = IsolationLevel.MONITORING
        self.created_at = time.time()
        self.last_status_change = self.created_at
        self.components = set()  # IDs of components in this zone
        self.status_history = []
        self.qrng = QuantumRandomNumberGenerator()
        
        # Add initial status
        self._add_status_event("created", {})
        
    def add_component(self, component_id: str) -> None:
        """
        Add a component to this security zone.
        
        Args:
            component_id: ID of the component to add
        """
        self.components.add(component_id)
        self._add_status_event("component_added", {"component_id": component_id})
        
    def remove_component(self, component_id: str) -> bool:
        """
        Remove a component from this security zone.
        
        Args:
            component_id: ID of the component to remove
            
        Returns:
            True if component was removed, False if not found
        """
        if component_id in self.components:
            self.components.remove(component_id)
            self._add_status_event("component_removed", {"component_id": component_id})
            return True
        return False
        
    def set_isolation_level(self, 
                           level: IsolationLevel, 
                           reason: str = "") -> None:
        """
        Change the isolation level of this security zone.
        
        Args:
            level: The new isolation level
            reason: Reason for the change
        """
        previous_level = self.isolation_level
        self.isolation_level = level
        self.last_status_change = time.time()
        
        self._add_status_event("isolation_changed", {
            "previous_level": previous_level.value,
            "new_level": level.value,
            "reason": reason
        })
        
    def update_security_level(self, level: SecurityLevel) -> None:
        """
        Update the security level for this zone.
        
        Args:
            level: The new security level
        """
        previous_level = self.security_level
        self.security_level = level
        
        self._add_status_event("security_level_changed", {
            "previous_level": previous_level.name,
            "new_level": level.name
        })
        
    def _add_status_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """Add a status event to the history"""
        event = {
            "timestamp": time.time(),
            "type": event_type,
            "details": details
        }
        
        self.status_history.append(event)
        
        # Limit history size
        if len(self.status_history) > 100:
            self.status_history = self.status_history[-100:]
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert security zone to dictionary for serialization"""
        return {
            "zone_id": self.zone_id,
            "name": self.name,
            "description": self.description,
            "security_level": self.security_level.name,
            "parent_zone": self.parent_zone,
            "isolation_level": self.isolation_level.value,
            "created_at": self.created_at,
            "last_status_change": self.last_status_change,
            "components": list(self.components),
            "status_history": self.status_history
        }


class SecurityBulkhead:
    """
    Implements a security bulkhead to isolate and contain threats.
    
    A security bulkhead controls access between security zones and
    can isolate zones in case of security threats.
    """
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.STANDARD):
        """
        Initialize a new security bulkhead.
        
        Args:
            security_level: Security level to enforce
        """
        self.bulkhead_id = str(uuid.uuid4())
        self.security_level = security_level
        self.zones = {}  # zone_id -> SecurityZone
        self.zone_connections = {}  # zone_id -> set of connected zone_ids
        self.isolation_overrides = {}  # zone_id -> IsolationLevel override
        self.created_at = time.time()
        self.emergency_mode = False
        self.alert_handlers = []
        self.qrng = QuantumRandomNumberGenerator()
        
    def create_zone(self, 
                   name: str,
                   description: str,
                   parent_zone: Optional[str] = None) -> SecurityZone:
        """
        Create a new security zone.
        
        Args:
            name: Name of the zone
            description: Description of the zone's purpose
            parent_zone: Optional parent zone ID
            
        Returns:
            The newly created SecurityZone
        """
        zone = SecurityZone(
            name=name,
            description=description,
            security_level=self.security_level,
            parent_zone=parent_zone
        )
        
        self.zones[zone.zone_id] = zone
        self.zone_connections[zone.zone_id] = set()
        
        return zone
        
    def connect_zones(self, zone1_id: str, zone2_id: str) -> bool:
        """
        Create a connection between two security zones.
        
        Args:
            zone1_id: ID of the first zone
            zone2_id: ID of the second zone
            
        Returns:
            True if connection was created, False otherwise
        """
        if zone1_id not in self.zones or zone2_id not in self.zones:
            return False
            
        # Check isolation levels
        if not self._can_connect(zone1_id, zone2_id):
            return False
            
        # Create bidirectional connection
        self.zone_connections[zone1_id].add(zone2_id)
        self.zone_connections[zone2_id].add(zone1_id)
        
        return True
        
    def disconnect_zones(self, zone1_id: str, zone2_id: str) -> bool:
        """
        Remove a connection between two security zones.
        
        Args:
            zone1_id: ID of the first zone
            zone2_id: ID of the second zone
            
        Returns:
            True if connection was removed, False otherwise
        """
        if zone1_id not in self.zones or zone2_id not in self.zones:
            return False
            
        # Remove bidirectional connection
        if zone2_id in self.zone_connections[zone1_id]:
            self.zone_connections[zone1_id].remove(zone2_id)
            
        if zone1_id in self.zone_connections[zone2_id]:
            self.zone_connections[zone2_id].remove(zone1_id)
            
        return True
        
    def isolate_zone(self, 
                    zone_id: str,
                    isolation_level: IsolationLevel,
                    reason: str = "",
                    cascade: bool = False) -> bool:
        """
        Isolate a security zone by setting its isolation level.
        
        Args:
            zone_id: ID of the zone to isolate
            isolation_level: The isolation level to apply
            reason: Reason for isolation
            cascade: Whether to cascade isolation to connected zones
            
        Returns:
            True if zone was isolated, False otherwise
        """
        if zone_id not in self.zones:
            return False
            
        # Set isolation level on the zone
        zone = self.zones[zone_id]
        zone.set_isolation_level(isolation_level, reason)
        
        # Add override
        self.isolation_overrides[zone_id] = isolation_level
        
        # Disconnect zones based on isolation level
        if isolation_level in [IsolationLevel.QUARANTINE, 
                              IsolationLevel.LOCKDOWN, 
                              IsolationLevel.JETTISON]:
            self._disconnect_all_zone_connections(zone_id)
            
        # Cascade if requested
        if cascade and self.zone_connections[zone_id]:
            connected_zones = list(self.zone_connections[zone_id])
            for connected_id in connected_zones:
                # Use a less restrictive isolation for cascaded zones
                cascade_level = self._get_cascade_isolation_level(isolation_level)
                self.isolate_zone(
                    connected_id,
                    cascade_level,
                    f"Cascaded from {zone.name} ({reason})",
                    cascade=False  # Prevent infinite recursion
                )
                
        # Trigger alerts
        self._trigger_isolation_alert(zone_id, isolation_level, reason)
                
        return True
        
    def restore_zone(self, zone_id: str) -> bool:
        """
        Restore a security zone to normal monitoring.
        
        Args:
            zone_id: ID of the zone to restore
            
        Returns:
            True if zone was restored, False otherwise
        """
        if zone_id not in self.zones:
            return False
            
        # Restore isolation level
        zone = self.zones[zone_id]
        zone.set_isolation_level(IsolationLevel.MONITORING, "Manual restoration")
        
        # Remove override
        if zone_id in self.isolation_overrides:
            del self.isolation_overrides[zone_id]
            
        return True
        
    def _can_connect(self, zone1_id: str, zone2_id: str) -> bool:
        """Check if two zones can be connected based on isolation levels"""
        zone1 = self.zones[zone1_id]
        zone2 = self.zones[zone2_id]
        
        # Cannot connect to lockdown or jettison zones
        if zone1.isolation_level in [IsolationLevel.LOCKDOWN, IsolationLevel.JETTISON]:
            return False
            
        if zone2.isolation_level in [IsolationLevel.LOCKDOWN, IsolationLevel.JETTISON]:
            return False
            
        # Quarantine zones require special handling
        if zone1.isolation_level == IsolationLevel.QUARANTINE or \
           zone2.isolation_level == IsolationLevel.QUARANTINE:
            # Allow connection only if emergency mode is active
            return self.emergency_mode
            
        return True
        
    def _disconnect_all_zone_connections(self, zone_id: str) -> None:
        """Disconnect all connections for a zone"""
        if zone_id not in self.zone_connections:
            return
            
        connected_zones = list(self.zone_connections[zone_id])
        for connected_id in connected_zones:
            self.disconnect_zones(zone_id, connected_id)
            
    def _get_cascade_isolation_level(self, level: IsolationLevel) -> IsolationLevel:
        """Get the appropriate cascade isolation level"""
        if level == IsolationLevel.JETTISON:
            return IsolationLevel.LOCKDOWN
        elif level == IsolationLevel.LOCKDOWN:
            return IsolationLevel.QUARANTINE
        elif level == IsolationLevel.QUARANTINE:
            return IsolationLevel.RESTRICTED
        else:
            return level
            
    def register_alert_handler(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """
        Register a handler for isolation alerts.
        
        Args:
            handler: Function to call when an isolation event occurs
        """
        self.alert_handlers.append(handler)
        
    def _trigger_isolation_alert(self, 
                                zone_id: str,
                                level: IsolationLevel,
                                reason: str) -> None:
        """Trigger alert handlers for an isolation event"""
        zone = self.zones[zone_id]
        
        alert = {
            "timestamp": time.time(),
            "type": "zone_isolation",
            "zone_id": zone_id,
            "zone_name": zone.name,
            "isolation_level": level.value,
            "reason": reason
        }
        
        # Call all handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                # Log the error but continue with other handlers
                print(f"Error in alert handler: {str(e)}")
                
    def update_security_level(self, level: SecurityLevel) -> None:
        """
        Update security level across all zones.
        
        Args:
            level: The new security level
        """
        self.security_level = level
        
        # Update all zones
        for zone in self.zones.values():
            zone.update_security_level(level)
            
    def activate_emergency_mode(self) -> None:
        """Activate emergency mode, allowing quarantine zone connections"""
        self.emergency_mode = True
        
    def deactivate_emergency_mode(self) -> None:
        """Deactivate emergency mode"""
        self.emergency_mode = False
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert security bulkhead to dictionary for serialization"""
        return {
            "bulkhead_id": self.bulkhead_id,
            "security_level": self.security_level.name,
            "created_at": self.created_at,
            "emergency_mode": self.emergency_mode,
            "zones": {zone_id: zone.to_dict() for zone_id, zone in self.zones.items()},
            "zone_connections": {zone_id: list(connections) 
                                for zone_id, connections in self.zone_connections.items()},
            "isolation_overrides": {zone_id: level.value 
                                   for zone_id, level in self.isolation_overrides.items()}
        }