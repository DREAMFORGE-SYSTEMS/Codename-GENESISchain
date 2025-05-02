"""
DreamChain DApps Module

This module implements decentralized applications (DApps) for the
DreamChain application layer. DApps provide user-friendly interfaces
and functionality built on top of smart contracts.

Key components:
1. DApp: Base class for decentralized applications
2. DAppRegistry: Registry for managing DApps
"""

import hashlib
import json
import time
import uuid
from typing import Dict, List, Any, Optional, Union, Callable


class DApp:
    """
    Base class for decentralized applications (DApps) in DreamChain.
    
    DApps are user-friendly applications built on top of smart contracts
    that provide specific functionality and interfaces.
    """
    
    def __init__(self,
                 owner: str,
                 name: str,
                 description: str,
                 contracts: List[str],
                 version: str = "1.0.0",
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a new DApp.
        
        Args:
            owner: Address of the DApp owner
            name: Name of the DApp
            description: Description of the DApp
            contracts: List of contract IDs used by the DApp
            version: DApp version
            metadata: Optional additional metadata
        """
        self.dapp_id = str(uuid.uuid4())
        self.owner = owner
        self.name = name
        self.description = description
        self.contracts = contracts
        self.version = version
        self.metadata = metadata or {}
        self.created_at = time.time()
        self.updated_at = self.created_at
        self.endpoints = {}
        self.usage_stats = {
            "total_calls": 0,
            "unique_users": set(),
            "last_call": None
        }
        
        # Calculate DApp hash
        self._calculate_hash()
        
    def _calculate_hash(self) -> None:
        """Calculate the hash of the DApp"""
        dapp_data = {
            "owner": self.owner,
            "name": self.name,
            "description": self.description,
            "contracts": self.contracts,
            "version": self.version,
            "created_at": self.created_at
        }
        
        dapp_str = json.dumps(dapp_data, sort_keys=True)
        self.hash = hashlib.sha3_256(dapp_str.encode()).hexdigest()
        
    def register_endpoint(self,
                         endpoint_name: str,
                         description: str,
                         handler: Callable[[Dict[str, Any], str], Any]) -> None:
        """
        Register a new endpoint for the DApp.
        
        Args:
            endpoint_name: Name of the endpoint
            description: Description of the endpoint
            handler: Function to handle endpoint calls
        """
        self.endpoints[endpoint_name] = {
            "description": description,
            "handler": handler,
            "created_at": time.time(),
            "call_count": 0
        }
        
    def call_endpoint(self,
                     endpoint_name: str,
                     params: Dict[str, Any],
                     caller: str) -> Any:
        """
        Call a DApp endpoint.
        
        Args:
            endpoint_name: Name of the endpoint to call
            params: Endpoint parameters
            caller: Address of the caller
            
        Returns:
            Endpoint result
            
        Raises:
            ValueError: If endpoint doesn't exist
        """
        # Check if endpoint exists
        if endpoint_name not in self.endpoints:
            raise ValueError(f"Endpoint {endpoint_name} does not exist")
            
        # Get endpoint
        endpoint = self.endpoints[endpoint_name]
        
        # Update usage stats
        self.usage_stats["total_calls"] += 1
        self.usage_stats["unique_users"].add(caller)
        self.usage_stats["last_call"] = time.time()
        
        endpoint["call_count"] += 1
        
        # Call handler
        return endpoint["handler"](params, caller)
        
    def update_metadata(self, key: str, value: Any) -> None:
        """
        Update DApp metadata.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
        self.updated_at = time.time()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert DApp to dictionary"""
        # Convert usage stats (can't serialize sets)
        usage = self.usage_stats.copy()
        usage["unique_users"] = list(usage["unique_users"])
        
        return {
            "dapp_id": self.dapp_id,
            "owner": self.owner,
            "name": self.name,
            "description": self.description,
            "contracts": self.contracts,
            "version": self.version,
            "hash": self.hash,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "endpoint_count": len(self.endpoints),
            "endpoints": [name for name in self.endpoints.keys()],
            "usage_stats": usage
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DApp':
        """Create DApp from dictionary"""
        dapp = cls(
            owner=data["owner"],
            name=data["name"],
            description=data["description"],
            contracts=data["contracts"],
            version=data["version"],
            metadata=data.get("metadata", {})
        )
        
        dapp.dapp_id = data["dapp_id"]
        dapp.hash = data["hash"]
        dapp.created_at = data["created_at"]
        dapp.updated_at = data["updated_at"]
        
        # Note: endpoints and handlers are not serialized/deserialized
        # since they contain function references
        
        # Convert usage stats
        if "usage_stats" in data:
            usage = data["usage_stats"]
            dapp.usage_stats["total_calls"] = usage.get("total_calls", 0)
            dapp.usage_stats["unique_users"] = set(usage.get("unique_users", []))
            dapp.usage_stats["last_call"] = usage.get("last_call")
            
        return dapp


class DAppRegistry:
    """
    Registry for managing DApps in DreamChain.
    
    The DApp registry maintains a collection of deployed DApps
    and provides methods for DApp creation, deployment, and lookup.
    """
    
    def __init__(self):
        """Initialize a new DApp registry"""
        self.dapps = {}  # dapp_id -> DApp
        self.dapp_count = 0
        self.dapp_templates = {}  # template name -> creation function
        self.created_at = time.time()
        
        # Register built-in DApp templates
        self._register_built_in_templates()
        
    def _register_built_in_templates(self) -> None:
        """Register built-in DApp templates"""
        # Example template registration
        self.register_template("token_exchange", self._create_token_exchange)
        
    def _create_token_exchange(self, 
                              owner: str,
                              name: str,
                              contracts: List[str],
                              metadata: Optional[Dict[str, Any]] = None) -> DApp:
        """Create a token exchange DApp"""
        # Create the DApp
        dapp = DApp(
            owner=owner,
            name=name,
            description="Token Exchange DApp",
            contracts=contracts,
            metadata=metadata
        )
        
        # Register endpoints
        dapp.register_endpoint(
            endpoint_name="get_exchange_rate",
            description="Get the current exchange rate",
            handler=self._handle_get_exchange_rate
        )
        
        dapp.register_endpoint(
            endpoint_name="exchange_tokens",
            description="Exchange tokens",
            handler=self._handle_exchange_tokens
        )
        
        return dapp
        
    def _handle_get_exchange_rate(self, 
                                 params: Dict[str, Any],
                                 caller: str) -> Dict[str, Any]:
        """Handle get_exchange_rate endpoint"""
        # This is a simplified implementation
        from_token = params.get("from_token")
        to_token = params.get("to_token")
        
        # In a real implementation, this would query actual exchange rates
        return {
            "from_token": from_token,
            "to_token": to_token,
            "rate": 1.0,  # Dummy rate
            "timestamp": time.time()
        }
        
    def _handle_exchange_tokens(self,
                               params: Dict[str, Any],
                               caller: str) -> Dict[str, Any]:
        """Handle exchange_tokens endpoint"""
        # This is a simplified implementation
        from_token = params.get("from_token")
        to_token = params.get("to_token")
        amount = params.get("amount", 0)
        
        # In a real implementation, this would execute the actual exchange
        return {
            "from_token": from_token,
            "to_token": to_token,
            "amount_sent": amount,
            "amount_received": amount,  # Dummy calculation
            "fee": 0.0,
            "timestamp": time.time(),
            "status": "success"
        }
        
    def register_template(self,
                         template_name: str,
                         template_func: Callable) -> None:
        """
        Register a new DApp template.
        
        Args:
            template_name: Name of the template
            template_func: Function to create DApps from this template
        """
        self.dapp_templates[template_name] = template_func
        
    def create_from_template(self,
                            template_name: str,
                            owner: str,
                            params: Dict[str, Any]) -> DApp:
        """
        Create a DApp from a template.
        
        Args:
            template_name: Name of the template to use
            owner: Address of the DApp owner
            params: DApp parameters
            
        Returns:
            The created DApp
            
        Raises:
            ValueError: If template doesn't exist
        """
        # Check if template exists
        if template_name not in self.dapp_templates:
            raise ValueError(f"Template {template_name} does not exist")
            
        # Get template function
        template_func = self.dapp_templates[template_name]
        
        # Add owner to params
        params["owner"] = owner
        
        # Create DApp
        dapp = template_func(**params)
        
        # Register DApp
        self.dapps[dapp.dapp_id] = dapp
        self.dapp_count += 1
        
        return dapp
        
    def register_dapp(self, dapp: DApp) -> None:
        """
        Register a DApp with the registry.
        
        Args:
            dapp: The DApp to register
        """
        self.dapps[dapp.dapp_id] = dapp
        self.dapp_count += 1
        
    def get_dapp(self, dapp_id: str) -> Optional[DApp]:
        """
        Get a DApp by ID.
        
        Args:
            dapp_id: The DApp ID
            
        Returns:
            The DApp or None if not found
        """
        return self.dapps.get(dapp_id)
        
    def get_dapps_by_owner(self, owner: str) -> List[DApp]:
        """
        Get DApps by owner.
        
        Args:
            owner: The owner address
            
        Returns:
            List of DApps owned by the address
        """
        return [
            dapp for dapp in self.dapps.values()
            if dapp.owner == owner
        ]
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert registry to dictionary"""
        return {
            "dapp_count": self.dapp_count,
            "templates": list(self.dapp_templates.keys()),
            "created_at": self.created_at
        }