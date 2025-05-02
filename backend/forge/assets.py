"""
THE FORGE Asset Module

This module implements asset creation functionality for THE FORGE.
It allows the creation of digital assets like tokens, NFTs, and other
blockchain-based resources using THE FORGE's quantum energy.

Key components:
1. AssetForge: Creates and manages digital assets
2. ForgedAsset: Represents a digital asset created by THE FORGE
3. AssetRegistry: Registry for tracking and managing forged assets
"""

import hashlib
import json
import time
import uuid
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Union, Tuple

# Import quantum security for enhanced entropy
from quantum_security import QuantumRandomNumberGenerator


class AssetType(Enum):
    """Types of assets that can be forged"""
    TOKEN = auto()        # Fungible token
    NFT = auto()          # Non-fungible token
    CERTIFICATE = auto()  # Ownership certificate
    KEY = auto()          # Access key
    CONTRACT = auto()     # Smart contract
    DATA = auto()         # Data object


class AssetStatus(Enum):
    """Status of a forged asset"""
    FORGING = auto()     # Being created
    COMPLETE = auto()    # Successfully created
    UNSTABLE = auto()    # Created but unstable
    FAILED = auto()      # Creation failed
    BURNED = auto()      # Destroyed


class ForgedAsset:
    """
    Represents a digital asset created by THE FORGE.
    
    ForgedAssets are quantum-infused digital objects with unique properties
    that can represent tokens, NFTs, or other blockchain resources.
    """
    
    def __init__(self,
                 name: str,
                 asset_type: AssetType,
                 creator: str,
                 properties: Dict[str, Any] = None,
                 metadata: Dict[str, Any] = None):
        """
        Initialize a new forged asset.
        
        Args:
            name: Name of the asset
            asset_type: Type of asset
            creator: Creator of the asset
            properties: Asset properties
            metadata: Additional metadata
        """
        self.asset_id = str(uuid.uuid4())
        self.name = name
        self.asset_type = asset_type
        self.creator = creator
        self.properties = properties or {}
        self.metadata = metadata or {}
        self.status = AssetStatus.FORGING
        self.created_at = time.time()
        self.last_modified = self.created_at
        self.forge_signature = ""
        self.quantum_signature = ""
        self.quantum_properties = {}
        self.transfer_history = []
        self.qrng = QuantumRandomNumberGenerator()
        
        # Initialize with quantum properties
        self._initialize_quantum_properties()
    
    def _initialize_quantum_properties(self) -> None:
        """Initialize quantum properties of the asset"""
        # Generate quantum entropy for the asset
        quantum_entropy = self.qrng.get_random_bytes(32).hex()
        
        # Create a quantum signature
        data_to_sign = f"{self.asset_id}:{self.name}:{self.asset_type.name}:{self.creator}:{quantum_entropy}"
        self.quantum_signature = hashlib.sha3_512(data_to_sign.encode()).hexdigest()
        
        # Generate quantum properties unique to this asset
        self.quantum_properties = {
            "resonance": self.qrng.get_random_float(),
            "stability": 0.5 + self.qrng.get_random_float() * 0.5,  # 0.5-1.0
            "dimension": int(self.qrng.get_random_float() * 1000),
            "energy_signature": self.qrng.get_random_bytes(16).hex(),
            "creation_entropy": quantum_entropy[:16]
        }
    
    def complete_forging(self, forge_signature: str) -> None:
        """
        Complete the forging process for the asset.
        
        Args:
            forge_signature: Signature from THE FORGE
        """
        self.forge_signature = forge_signature
        self.status = AssetStatus.COMPLETE
        self.last_modified = time.time()
        
        # Record initial ownership in transfer history
        self.transfer_history.append({
            "from": "THE_FORGE",
            "to": self.creator,
            "timestamp": self.last_modified,
            "transaction_type": "creation"
        })
    
    def set_unstable(self, reason: str) -> None:
        """
        Mark the asset as unstable.
        
        Args:
            reason: Reason for instability
        """
        self.status = AssetStatus.UNSTABLE
        self.last_modified = time.time()
        self.metadata["unstable_reason"] = reason
    
    def set_failed(self, reason: str) -> None:
        """
        Mark the asset as failed.
        
        Args:
            reason: Reason for failure
        """
        self.status = AssetStatus.FAILED
        self.last_modified = time.time()
        self.metadata["failed_reason"] = reason
    
    def burn(self, reason: str) -> None:
        """
        Burn (destroy) the asset.
        
        Args:
            reason: Reason for burning
        """
        self.status = AssetStatus.BURNED
        self.last_modified = time.time()
        self.metadata["burned_reason"] = reason
        
        # Record final transfer to burning
        self.transfer_history.append({
            "from": self.get_current_owner(),
            "to": "BURNED",
            "timestamp": self.last_modified,
            "transaction_type": "burn"
        })
    
    def transfer(self, from_address: str, to_address: str) -> bool:
        """
        Transfer ownership of the asset.
        
        Args:
            from_address: Current owner address
            to_address: New owner address
            
        Returns:
            True if transfer succeeded, False otherwise
        """
        # Check if asset can be transferred
        if self.status != AssetStatus.COMPLETE:
            return False
        
        # Check if sender is current owner
        current_owner = self.get_current_owner()
        if current_owner != from_address:
            return False
        
        # Record transfer
        self.transfer_history.append({
            "from": from_address,
            "to": to_address,
            "timestamp": time.time(),
            "transaction_type": "transfer"
        })
        
        self.last_modified = time.time()
        return True
    
    def get_current_owner(self) -> str:
        """
        Get the current owner of the asset.
        
        Returns:
            Address of current owner
        """
        if not self.transfer_history:
            return self.creator
        
        return self.transfer_history[-1]["to"]
    
    def verify_integrity(self) -> bool:
        """
        Verify the integrity of the asset.
        
        Returns:
            True if asset integrity is valid
        """
        # Recalculate quantum signature
        data_to_sign = f"{self.asset_id}:{self.name}:{self.asset_type.name}:{self.creator}:{self.quantum_properties['creation_entropy']}"
        calculated_signature = hashlib.sha3_512(data_to_sign.encode()).hexdigest()
        
        # Check if signatures match
        return calculated_signature == self.quantum_signature
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the forged asset to a dictionary representation.
        
        Returns:
            Dictionary representation of the forged asset
        """
        return {
            "asset_id": self.asset_id,
            "name": self.name,
            "asset_type": self.asset_type.name,
            "creator": self.creator,
            "properties": self.properties,
            "metadata": self.metadata,
            "status": self.status.name,
            "created_at": self.created_at,
            "last_modified": self.last_modified,
            "forge_signature": self.forge_signature,
            "quantum_properties": self.quantum_properties,
            "current_owner": self.get_current_owner(),
            "transfer_count": len(self.transfer_history),
            "verified": self.verify_integrity()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ForgedAsset':
        """
        Create a ForgedAsset from a dictionary.
        
        Args:
            data: Dictionary with asset data
            
        Returns:
            Reconstructed ForgedAsset
        """
        asset = cls(
            name=data["name"],
            asset_type=AssetType[data["asset_type"]],
            creator=data["creator"],
            properties=data.get("properties", {}),
            metadata=data.get("metadata", {})
        )
        
        # Set stored values
        asset.asset_id = data["asset_id"]
        asset.created_at = data["created_at"]
        asset.last_modified = data["last_modified"]
        asset.forge_signature = data["forge_signature"]
        asset.quantum_signature = data.get("quantum_signature", "")
        asset.quantum_properties = data.get("quantum_properties", {})
        asset.transfer_history = data.get("transfer_history", [])
        
        # Set status
        try:
            asset.status = AssetStatus[data["status"]]
        except (KeyError, ValueError):
            asset.status = AssetStatus.UNSTABLE
        
        return asset


class AssetForge:
    """
    Creates and manages digital assets using THE FORGE's quantum energy.
    
    AssetForge is responsible for creating, modifying, and burning digital
    assets, as well as managing the energy required for these operations.
    """
    
    def __init__(self, quantum_forge):
        """
        Initialize a new asset forge.
        
        Args:
            quantum_forge: The quantum forge providing energy
        """
        self.forge_id = str(uuid.uuid4())
        self.quantum_forge = quantum_forge
        self.created_at = time.time()
        self.asset_count = 0
        self.forging_queue = []  # [(asset, energy_required), ...]
        self.forging_history = []
        self.energy_costs = {
            AssetType.TOKEN: 10.0,
            AssetType.NFT: 50.0,
            AssetType.CERTIFICATE: 30.0,
            AssetType.KEY: 25.0,
            AssetType.CONTRACT: 100.0,
            AssetType.DATA: 15.0
        }
        self.qrng = QuantumRandomNumberGenerator()
    
    def calculate_forging_cost(self, 
                              asset_type: AssetType,
                              properties: Dict[str, Any]) -> float:
        """
        Calculate the energy cost to forge an asset.
        
        Args:
            asset_type: Type of asset to forge
            properties: Asset properties
            
        Returns:
            Energy cost for forging
        """
        # Base cost from asset type
        base_cost = self.energy_costs.get(asset_type, 20.0)
        
        # Additional cost based on properties complexity
        property_cost = len(json.dumps(properties)) * 0.01
        
        # Apply quantum fluctuation
        fluctuation = 0.9 + self.qrng.get_random_float() * 0.2  # 0.9-1.1
        
        return (base_cost + property_cost) * fluctuation
    
    def forge_asset(self,
                   name: str,
                   asset_type: AssetType,
                   creator: str,
                   properties: Dict[str, Any] = None,
                   metadata: Dict[str, Any] = None) -> Tuple[ForgedAsset, bool]:
        """
        Forge a new digital asset.
        
        Args:
            name: Name of the asset
            asset_type: Type of asset
            creator: Creator of the asset
            properties: Asset properties
            metadata: Additional metadata
            
        Returns:
            Tuple of (asset, forging_successful)
        """
        # Create the asset in FORGING state
        asset = ForgedAsset(
            name=name,
            asset_type=asset_type,
            creator=creator,
            properties=properties,
            metadata=metadata
        )
        
        # Calculate energy cost
        energy_cost = self.calculate_forging_cost(asset_type, properties or {})
        
        # Check if we have enough energy
        if self.quantum_forge.current_energy < energy_cost:
            asset.set_failed("Insufficient energy in THE FORGE")
            
            # Add to history
            self.forging_history.append({
                "asset_id": asset.asset_id,
                "name": asset.name,
                "asset_type": asset_type.name,
                "creator": creator,
                "timestamp": time.time(),
                "energy_cost": energy_cost,
                "result": "failed",
                "reason": "Insufficient energy"
            })
            
            return asset, False
        
        # Consume energy for forging
        self.quantum_forge.current_energy -= energy_cost
        
        # Generate forge signature
        forge_signature = self._generate_forge_signature(asset)
        
        # Complete the forging
        asset.complete_forging(forge_signature)
        
        # Update metrics
        self.asset_count += 1
        
        # Add to history
        self.forging_history.append({
            "asset_id": asset.asset_id,
            "name": asset.name,
            "asset_type": asset_type.name,
            "creator": creator,
            "timestamp": time.time(),
            "energy_cost": energy_cost,
            "result": "success"
        })
        
        return asset, True
    
    def queue_asset_forging(self,
                           name: str,
                           asset_type: AssetType,
                           creator: str,
                           properties: Dict[str, Any] = None,
                           metadata: Dict[str, Any] = None) -> ForgedAsset:
        """
        Queue an asset for forging when energy is available.
        
        Args:
            name: Name of the asset
            asset_type: Type of asset
            creator: Creator of the asset
            properties: Asset properties
            metadata: Additional metadata
            
        Returns:
            Asset in FORGING state
        """
        # Create the asset in FORGING state
        asset = ForgedAsset(
            name=name,
            asset_type=asset_type,
            creator=creator,
            properties=properties,
            metadata=metadata
        )
        
        # Calculate energy cost
        energy_cost = self.calculate_forging_cost(asset_type, properties or {})
        
        # Add to queue
        self.forging_queue.append((asset, energy_cost))
        
        return asset
    
    def process_forging_queue(self) -> List[Dict[str, Any]]:
        """
        Process queued assets for forging.
        
        Returns:
            List of processing results
        """
        results = []
        
        # Process the queue while we have energy and items
        while self.forging_queue and self.quantum_forge.current_energy > 0:
            # Get next asset to forge
            asset, energy_cost = self.forging_queue.pop(0)
            
            # Check if we have enough energy
            if self.quantum_forge.current_energy < energy_cost:
                # Put it back in the queue and stop processing
                self.forging_queue.insert(0, (asset, energy_cost))
                break
            
            # Consume energy for forging
            self.quantum_forge.current_energy -= energy_cost
            
            # Generate forge signature
            forge_signature = self._generate_forge_signature(asset)
            
            # Complete the forging
            asset.complete_forging(forge_signature)
            
            # Update metrics
            self.asset_count += 1
            
            # Add to history
            forging_result = {
                "asset_id": asset.asset_id,
                "name": asset.name,
                "asset_type": asset.asset_type.name,
                "creator": asset.creator,
                "timestamp": time.time(),
                "energy_cost": energy_cost,
                "result": "success"
            }
            
            self.forging_history.append(forging_result)
            results.append(forging_result)
        
        return results
    
    def _generate_forge_signature(self, asset: ForgedAsset) -> str:
        """
        Generate a signature from THE FORGE for an asset.
        
        Args:
            asset: The asset to sign
            
        Returns:
            THE FORGE signature
        """
        # This simulates a quantum signing process
        # In a real implementation, this would use a quantum-resistant signature algorithm
        
        # Get quantum random entropy
        quantum_entropy = self.qrng.get_random_bytes(32)
        
        # Data to sign
        data = (
            f"{asset.asset_id}:{asset.name}:{asset.asset_type.name}:"
            f"{asset.creator}:{asset.created_at}:{self.quantum_forge.forge_id}:"
            f"{quantum_entropy.hex()}"
        )
        
        # Generate signature
        forge_signature = hashlib.sha3_512(data.encode()).hexdigest()
        
        return forge_signature
    
    def get_forging_queue_status(self) -> Dict[str, Any]:
        """
        Get status of the forging queue.
        
        Returns:
            Queue status information
        """
        total_energy_needed = sum(cost for _, cost in self.forging_queue)
        
        return {
            "queue_length": len(self.forging_queue),
            "total_energy_needed": total_energy_needed,
            "estimated_completion_time": self._estimate_completion_time(total_energy_needed),
            "queue_assets": [
                {
                    "asset_id": asset.asset_id,
                    "name": asset.name,
                    "asset_type": asset.asset_type.name,
                    "creator": asset.creator,
                    "energy_cost": cost
                }
                for asset, cost in self.forging_queue[:10]  # Show first 10
            ]
        }
    
    def _estimate_completion_time(self, energy_needed: float) -> float:
        """
        Estimate time to complete forging based on energy generation.
        
        Args:
            energy_needed: Total energy needed
            
        Returns:
            Estimated completion time in seconds
        """
        # Get forge stats to determine energy generation rate
        forge_stats = self.quantum_forge.get_energy_statistics()
        generation_rate = forge_stats.get("generation_rate", 10.0)  # per hour
        
        if generation_rate <= 0:
            return float('inf')  # Cannot estimate
        
        # Available energy plus what will be generated
        available_energy = self.quantum_forge.current_energy
        
        if available_energy >= energy_needed:
            return 0.0  # Can be done immediately
        
        # Calculate how much more energy we need
        additional_energy_needed = energy_needed - available_energy
        
        # Calculate time to generate that energy (in seconds)
        time_needed = (additional_energy_needed / generation_rate) * 3600
        
        return time_needed
    
    def get_recent_forgings(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent asset forgings.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            Recent forging history
        """
        return sorted(self.forging_history, 
                     key=lambda x: x["timestamp"], 
                     reverse=True)[:limit]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the asset forge to a dictionary representation.
        
        Returns:
            Dictionary representation of the asset forge
        """
        return {
            "forge_id": self.forge_id,
            "created_at": self.created_at,
            "asset_count": self.asset_count,
            "queue_length": len(self.forging_queue),
            "energy_costs": {k.name: v for k, v in self.energy_costs.items()},
            "recent_forgings": self.get_recent_forgings(5),
            "queue_status": self.get_forging_queue_status()
        }


class AssetRegistry:
    """
    Registry for tracking and managing forged assets.
    
    The asset registry maintains a record of all assets created by THE FORGE,
    allowing for lookup, verification, and management of these assets.
    """
    
    def __init__(self):
        """Initialize a new asset registry"""
        self.registry_id = str(uuid.uuid4())
        self.assets = {}  # asset_id -> ForgedAsset
        self.asset_count = 0
        self.created_at = time.time()
        self.last_update = self.created_at
        self.asset_types = {}  # asset_type_name -> count
        self.creators = {}  # creator_address -> count
        self.owners = {}  # owner_address -> [asset_ids]
    
    def register_asset(self, asset: ForgedAsset) -> bool:
        """
        Register an asset in the registry.
        
        Args:
            asset: The asset to register
            
        Returns:
            True if registration succeeded
        """
        # Check if asset already exists
        if asset.asset_id in self.assets:
            return False
        
        # Add to registry
        self.assets[asset.asset_id] = asset
        self.asset_count += 1
        self.last_update = time.time()
        
        # Update type count
        asset_type_name = asset.asset_type.name
        self.asset_types[asset_type_name] = self.asset_types.get(asset_type_name, 0) + 1
        
        # Update creator count
        self.creators[asset.creator] = self.creators.get(asset.creator, 0) + 1
        
        # Update owner mapping
        current_owner = asset.get_current_owner()
        if current_owner not in self.owners:
            self.owners[current_owner] = []
        self.owners[current_owner].append(asset.asset_id)
        
        return True
    
    def get_asset(self, asset_id: str) -> Optional[ForgedAsset]:
        """
        Get an asset from the registry.
        
        Args:
            asset_id: ID of the asset to retrieve
            
        Returns:
            The asset or None if not found
        """
        return self.assets.get(asset_id)
    
    def get_assets_by_owner(self, owner: str) -> List[ForgedAsset]:
        """
        Get all assets owned by an address.
        
        Args:
            owner: Owner address
            
        Returns:
            List of assets owned by the address
        """
        asset_ids = self.owners.get(owner, [])
        return [self.assets[asset_id] for asset_id in asset_ids if asset_id in self.assets]
    
    def get_assets_by_creator(self, creator: str) -> List[ForgedAsset]:
        """
        Get all assets created by an address.
        
        Args:
            creator: Creator address
            
        Returns:
            List of assets created by the address
        """
        return [asset for asset in self.assets.values() if asset.creator == creator]
    
    def get_assets_by_type(self, asset_type: AssetType) -> List[ForgedAsset]:
        """
        Get all assets of a specific type.
        
        Args:
            asset_type: Type of assets to retrieve
            
        Returns:
            List of assets of the specified type
        """
        return [
            asset for asset in self.assets.values() 
            if asset.asset_type == asset_type
        ]
    
    def update_ownership(self, asset_id: str, from_address: str, to_address: str) -> bool:
        """
        Update ownership of an asset in the registry.
        
        Args:
            asset_id: ID of the asset
            from_address: Current owner address
            to_address: New owner address
            
        Returns:
            True if update succeeded
        """
        # Check if asset exists
        if asset_id not in self.assets:
            return False
        
        asset = self.assets[asset_id]
        
        # Attempt transfer
        if not asset.transfer(from_address, to_address):
            return False
        
        # Update owner mappings
        if from_address in self.owners and asset_id in self.owners[from_address]:
            self.owners[from_address].remove(asset_id)
        
        if to_address not in self.owners:
            self.owners[to_address] = []
        
        self.owners[to_address].append(asset_id)
        self.last_update = time.time()
        
        return True
    
    def remove_asset(self, asset_id: str, reason: str) -> bool:
        """
        Remove an asset from the registry.
        
        Args:
            asset_id: ID of the asset to remove
            reason: Reason for removal
            
        Returns:
            True if removal succeeded
        """
        # Check if asset exists
        if asset_id not in self.assets:
            return False
        
        asset = self.assets[asset_id]
        
        # Burn the asset
        asset.burn(reason)
        
        # Update type count
        asset_type_name = asset.asset_type.name
        if asset_type_name in self.asset_types and self.asset_types[asset_type_name] > 0:
            self.asset_types[asset_type_name] -= 1
        
        # Update owner mapping
        current_owner = asset.get_current_owner()
        if current_owner in self.owners and asset_id in self.owners[current_owner]:
            self.owners[current_owner].remove(asset_id)
        
        # Don't actually remove from assets dict, just mark as burned
        self.last_update = time.time()
        
        return True
    
    def get_asset_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about assets in the registry.
        
        Returns:
            Asset statistics
        """
        # Count assets by status
        status_counts = {}
        for asset in self.assets.values():
            status = asset.status.name
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Calculate top creators and owners
        top_creators = sorted(
            self.creators.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        top_owners = sorted(
            [(owner, len(assets)) for owner, assets in self.owners.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "total_assets": self.asset_count,
            "asset_types": self.asset_types,
            "status_counts": status_counts,
            "top_creators": top_creators,
            "top_owners": top_owners,
            "last_update": self.last_update
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the asset registry to a dictionary representation.
        
        Returns:
            Dictionary representation of the asset registry
        """
        return {
            "registry_id": self.registry_id,
            "created_at": self.created_at,
            "last_update": self.last_update,
            "asset_count": self.asset_count,
            "creator_count": len(self.creators),
            "owner_count": len(self.owners),
            "asset_type_counts": self.asset_types,
            "statistics": self.get_asset_statistics()
        }