"""
DreamChain Smart Contracts Module

This module implements smart contract functionality for the DreamChain
application layer, providing a user-friendly and efficient contract
execution environment.

Key components:
1. SmartContract: Base class for all contracts
2. ContractRegistry: Registry for managing contracts
3. TokenContract: Implementation of a token contract
"""

import hashlib
import json
import time
import uuid
from typing import Dict, List, Any, Optional, Union, Callable


class SmartContract:
    """
    Base class for all smart contracts in DreamChain.
    
    Smart contracts in DreamChain are designed for ease of use and
    high performance, with security guarantees from the lower layers.
    """
    
    def __init__(self, 
                 owner: str,
                 name: str,
                 code: str,
                 abi: Dict[str, Any],
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a new smart contract.
        
        Args:
            owner: Address of the contract owner
            name: Name of the contract
            code: Contract code
            abi: Contract ABI (Application Binary Interface)
            metadata: Optional additional metadata
        """
        self.contract_id = str(uuid.uuid4())
        self.owner = owner
        self.name = name
        self.code = code
        self.abi = abi
        self.metadata = metadata or {}
        self.created_at = time.time()
        self.updated_at = self.created_at
        self.state = {}
        self.functions = {}
        self.events = []
        self.verified_by_genesis = False
        
        # Calculate contract hash
        self._calculate_hash()
        
        # Register functions from ABI
        self._register_functions()
        
    def _calculate_hash(self) -> None:
        """Calculate the hash of the contract"""
        contract_data = {
            "owner": self.owner,
            "name": self.name,
            "code": self.code,
            "abi": self.abi,
            "created_at": self.created_at
        }
        
        contract_str = json.dumps(contract_data, sort_keys=True)
        self.hash = hashlib.sha3_256(contract_str.encode()).hexdigest()
        
    def _register_functions(self) -> None:
        """Register functions from the ABI"""
        for func in self.abi.get("functions", []):
            name = func.get("name")
            if name:
                self.functions[name] = func
        
    def call(self, 
            function_name: str,
            caller: str,
            args: Dict[str, Any],
            value: float = 0.0) -> Any:
        """
        Call a contract function.
        
        Args:
            function_name: Name of the function to call
            caller: Address of the caller
            args: Function arguments
            value: Value to send with the call
            
        Returns:
            Function result
            
        Raises:
            ValueError: If function doesn't exist or call fails
        """
        # Check if function exists
        if function_name not in self.functions:
            raise ValueError(f"Function {function_name} does not exist")
            
        # Get function definition
        function = self.functions[function_name]
        
        # Check if function is payable
        if not function.get("payable", False) and value > 0:
            raise ValueError(f"Function {function_name} is not payable")
            
        # Check caller permissions
        if function.get("owner_only", False) and caller != self.owner:
            raise ValueError(f"Function {function_name} can only be called by the owner")
            
        # In a real implementation, this would execute the actual code
        # For this simulation, we'll just log the call and return a dummy result
        event = {
            "type": "function_call",
            "contract_id": self.contract_id,
            "function": function_name,
            "caller": caller,
            "args": args,
            "value": value,
            "timestamp": time.time()
        }
        
        self.events.append(event)
        
        # Return a dummy result based on function
        if function_name == "get_balance":
            address = args.get("address", caller)
            return self.state.get(f"balance:{address}", 0)
            
        elif function_name == "transfer":
            recipient = args.get("to")
            amount = args.get("amount", 0)
            
            # Check sender balance
            sender_balance = self.state.get(f"balance:{caller}", 0)
            if sender_balance < amount:
                raise ValueError("Insufficient balance")
                
            # Update balances
            self.state[f"balance:{caller}"] = sender_balance - amount
            
            recipient_balance = self.state.get(f"balance:{recipient}", 0)
            self.state[f"balance:{recipient}"] = recipient_balance + amount
            
            return True
            
        # Generic fallback
        return {"status": "success", "function": function_name}
        
    def update_state(self, key: str, value: Any) -> None:
        """
        Update contract state.
        
        Args:
            key: State key
            value: State value
        """
        self.state[key] = value
        self.updated_at = time.time()
        
    def get_state(self, key: str, default: Any = None) -> Any:
        """
        Get contract state.
        
        Args:
            key: State key
            default: Default value if key doesn't exist
            
        Returns:
            State value or default
        """
        return self.state.get(key, default)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert contract to dictionary"""
        return {
            "contract_id": self.contract_id,
            "owner": self.owner,
            "name": self.name,
            "hash": self.hash,
            "abi": self.abi,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "state_keys": list(self.state.keys()),
            "function_count": len(self.functions),
            "event_count": len(self.events),
            "verified_by_genesis": self.verified_by_genesis
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SmartContract':
        """Create contract from dictionary"""
        contract = cls(
            owner=data["owner"],
            name=data["name"],
            code=data.get("code", ""),
            abi=data["abi"],
            metadata=data.get("metadata", {})
        )
        
        contract.contract_id = data["contract_id"]
        contract.hash = data["hash"]
        contract.created_at = data["created_at"]
        contract.updated_at = data["updated_at"]
        contract.verified_by_genesis = data.get("verified_by_genesis", False)
        
        # Note: state and events are typically not serialized/deserialized
        # for security and size reasons
        
        return contract


class TokenContract(SmartContract):
    """
    Implementation of a token contract for DreamChain.
    
    This contract allows creating and managing tokens on the
    DreamChain application layer.
    """
    
    def __init__(self,
                owner: str,
                name: str,
                symbol: str,
                decimals: int = 18,
                initial_supply: float = 0.0,
                metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a new token contract.
        
        Args:
            owner: Address of the contract owner
            name: Name of the token
            symbol: Token symbol
            decimals: Token decimals
            initial_supply: Initial token supply
            metadata: Optional additional metadata
        """
        # Define token ABI
        token_abi = {
            "functions": [
                {
                    "name": "transfer",
                    "inputs": [
                        {"name": "to", "type": "address"},
                        {"name": "amount", "type": "uint256"}
                    ],
                    "outputs": [{"type": "bool"}],
                    "payable": False
                },
                {
                    "name": "mint",
                    "inputs": [
                        {"name": "to", "type": "address"},
                        {"name": "amount", "type": "uint256"}
                    ],
                    "outputs": [{"type": "bool"}],
                    "payable": False,
                    "owner_only": True
                },
                {
                    "name": "get_balance",
                    "inputs": [
                        {"name": "address", "type": "address", "optional": True}
                    ],
                    "outputs": [{"type": "uint256"}],
                    "payable": False
                },
                {
                    "name": "get_total_supply",
                    "inputs": [],
                    "outputs": [{"type": "uint256"}],
                    "payable": False
                }
            ],
            "events": [
                {
                    "name": "Transfer",
                    "inputs": [
                        {"name": "from", "type": "address", "indexed": True},
                        {"name": "to", "type": "address", "indexed": True},
                        {"name": "amount", "type": "uint256"}
                    ]
                },
                {
                    "name": "Mint",
                    "inputs": [
                        {"name": "to", "type": "address", "indexed": True},
                        {"name": "amount", "type": "uint256"}
                    ]
                }
            ]
        }
        
        # Create token code (simplified for this example)
        token_code = f"""
        contract {name}Token {{
            string public name = "{name}";
            string public symbol = "{symbol}";
            uint8 public decimals = {decimals};
            uint256 public totalSupply;
            mapping(address => uint256) public balances;
            
            event Transfer(address indexed from, address indexed to, uint256 amount);
            event Mint(address indexed to, uint256 amount);
            
            constructor() {{
                totalSupply = {initial_supply};
                balances[msg.sender] = totalSupply;
            }}
            
            function transfer(address to, uint256 amount) public returns (bool) {{
                require(balances[msg.sender] >= amount, "Insufficient balance");
                balances[msg.sender] -= amount;
                balances[to] += amount;
                emit Transfer(msg.sender, to, amount);
                return true;
            }}
            
            function mint(address to, uint256 amount) public onlyOwner returns (bool) {{
                totalSupply += amount;
                balances[to] += amount;
                emit Mint(to, amount);
                return true;
            }}
            
            function get_balance(address addr) public view returns (uint256) {{
                return balances[addr];
            }}
            
            function get_total_supply() public view returns (uint256) {{
                return totalSupply;
            }}
        }}
        """
        
        # Combine token metadata
        token_metadata = {
            "token_name": name,
            "token_symbol": symbol,
            "token_decimals": decimals,
            "token_type": "DreamChain Standard Token"
        }
        
        if metadata:
            token_metadata.update(metadata)
            
        # Initialize contract
        super().__init__(
            owner=owner,
            name=f"{name} Token",
            code=token_code,
            abi=token_abi,
            metadata=token_metadata
        )
        
        # Initialize token state
        self.state["totalSupply"] = initial_supply
        self.state[f"balance:{owner}"] = initial_supply
        
    def mint(self, to: str, amount: float, caller: str) -> bool:
        """
        Mint new tokens.
        
        Args:
            to: Recipient address
            amount: Amount to mint
            caller: Address of the caller
            
        Returns:
            True if successful
            
        Raises:
            ValueError: If caller is not the owner
        """
        # Call the mint function
        return self.call(
            function_name="mint",
            caller=caller,
            args={"to": to, "amount": amount}
        )
        
    def transfer(self, from_addr: str, to: str, amount: float) -> bool:
        """
        Transfer tokens between addresses.
        
        Args:
            from_addr: Sender address
            to: Recipient address
            amount: Amount to transfer
            
        Returns:
            True if successful
            
        Raises:
            ValueError: If sender has insufficient balance
        """
        # Call the transfer function
        return self.call(
            function_name="transfer",
            caller=from_addr,
            args={"to": to, "amount": amount}
        )
        
    def get_balance(self, address: str) -> float:
        """
        Get the token balance of an address.
        
        Args:
            address: The address to check
            
        Returns:
            Token balance
        """
        # Call the get_balance function
        return self.call(
            function_name="get_balance",
            caller=address,
            args={"address": address}
        )
        
    def get_total_supply(self) -> float:
        """
        Get the total token supply.
        
        Returns:
            Total supply
        """
        # Call the get_total_supply function
        return self.call(
            function_name="get_total_supply",
            caller=self.owner,
            args={}
        )


class ContractRegistry:
    """
    Registry for managing contracts in DreamChain.
    
    The contract registry maintains a collection of deployed contracts
    and provides methods for contract creation, deployment, and lookup.
    """
    
    def __init__(self):
        """Initialize a new contract registry"""
        self.contracts = {}  # contract_id -> SmartContract
        self.contract_count = 0
        self.contract_types = {}  # contract type name -> creation function
        self.created_at = time.time()
        
        # Register built-in contract types
        self._register_built_in_contracts()
        
    def _register_built_in_contracts(self) -> None:
        """Register built-in contract types"""
        self.register_contract_type("token", TokenContract)
        
    def register_contract_type(self, 
                              type_name: str,
                              contract_class: Any) -> None:
        """
        Register a new contract type.
        
        Args:
            type_name: Name of the contract type
            contract_class: Contract class or creation function
        """
        self.contract_types[type_name] = contract_class
        
    def deploy_contract(self,
                       contract_type: str,
                       owner: str,
                       params: Dict[str, Any]) -> SmartContract:
        """
        Deploy a new contract.
        
        Args:
            contract_type: Type of contract to deploy
            owner: Address of the contract owner
            params: Contract parameters
            
        Returns:
            The deployed contract
            
        Raises:
            ValueError: If contract type doesn't exist
        """
        # Check if contract type exists
        if contract_type not in self.contract_types:
            raise ValueError(f"Contract type {contract_type} does not exist")
            
        # Create contract
        contract_class = self.contract_types[contract_type]
        
        # Add owner to params
        params["owner"] = owner
        
        # Create contract instance
        contract = contract_class(**params)
        
        # Register contract
        self.contracts[contract.contract_id] = contract
        self.contract_count += 1
        
        return contract
        
    def get_contract(self, contract_id: str) -> Optional[SmartContract]:
        """
        Get a contract by ID.
        
        Args:
            contract_id: The contract ID
            
        Returns:
            The contract or None if not found
        """
        return self.contracts.get(contract_id)
        
    def get_contracts_by_owner(self, owner: str) -> List[SmartContract]:
        """
        Get contracts by owner.
        
        Args:
            owner: The owner address
            
        Returns:
            List of contracts owned by the address
        """
        return [
            contract for contract in self.contracts.values()
            if contract.owner == owner
        ]
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert registry to dictionary"""
        return {
            "contract_count": self.contract_count,
            "contract_types": list(self.contract_types.keys()),
            "created_at": self.created_at
        }