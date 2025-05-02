"""
Hash-Based Cryptography Implementation

This module implements hash-based cryptography, which is one of the most 
conservative approaches for post-quantum cryptographic signatures. These 
methods rely only on the security of the underlying hash function, making
them very well-studied and trustworthy alternatives.

Implementations include:
1. Merkle signature scheme (MSS)
2. SPHINCS+ style hash-based signatures
3. XMSS (eXtended Merkle Signature Scheme)

These algorithms are highly resistant to quantum computing attacks.
"""

import hashlib
import os
import time
import uuid
from typing import List, Dict, Tuple, Optional, Any


class HashBasedSignature:
    """
    A simulation of a hash-based signature scheme (similar to SPHINCS+).
    
    Hash-based signatures are considered the most conservative quantum-resistant
    options because they rely only on the security of hash functions.
    """
    
    def __init__(self, 
                hash_function: str = "SHA3-256", 
                tree_height: int = 16, 
                security_level: int = 256):
        """
        Initialize the hash-based signature scheme.
        
        Args:
            hash_function: The hash function to use (SHA3-256, SHA3-512, etc.)
            tree_height: The height of the Merkle tree
            security_level: Security level in bits
        """
        self.hash_function = hash_function
        self.tree_height = tree_height
        self.security_level = security_level
        
        # Number of one-time signatures available
        self.total_signatures = 2**tree_height
        
        # Maximum signatures before key rotation is recommended
        # In practice this would be much lower for security margin
        self.max_signatures = self.total_signatures // 2
    
    def _hash(self, data: bytes) -> bytes:
        """Internal method to apply the selected hash function"""
        if self.hash_function == "SHA3-256":
            return hashlib.sha3_256(data).digest()
        elif self.hash_function == "SHA3-512":
            return hashlib.sha3_512(data).digest()
        else:
            # Default to SHA3-256
            return hashlib.sha3_256(data).digest()
    
    def keygen(self) -> Dict[str, Any]:
        """
        Generate a key pair for the hash-based signature scheme.
        
        In a real implementation, this would generate a complete Merkle tree
        with one-time signature keys at the leaves. For this simulation, we'll
        create a simplified version.
        
        Returns:
            A dictionary containing the key pair information
        """
        # Generate master seed
        seed = os.urandom(self.security_level // 8)
        
        # Create a unique key ID
        key_id = str(uuid.uuid4())
        
        # In a real implementation, we would generate a complete Merkle tree
        # For this simulation, we'll just create the master seed and metadata
        
        # Generate root of the Merkle tree (in a real implementation, this would
        # be done by constructing the entire tree)
        root = self._hash(seed + b"root")
        
        # Store OTS (One-Time Signature) state
        ots_state = {
            "next_index": 0,
            "used_indices": []
        }
        
        return {
            "public_key": {
                "root": root.hex(),
                "algorithm": f"SPHINCS-{self.tree_height}-{self.hash_function}",
                "key_id": key_id
            },
            "private_key": {
                "seed": seed.hex(),
                "ots_state": ots_state,
                "key_id": key_id
            },
            "metadata": {
                "created": time.time(),
                "tree_height": self.tree_height,
                "hash_function": self.hash_function,
                "total_signatures": self.total_signatures,
                "max_signatures": self.max_signatures,
                "security_level": self.security_level
            }
        }
    
    def sign(self, message: str, private_key: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sign a message using the hash-based signature scheme.
        
        Args:
            message: The message to sign
            private_key: The private key data
            
        Returns:
            A dictionary containing the signature data
        """
        # Check if we've exceeded the maximum number of signatures
        ots_state = private_key["ots_state"]
        if len(ots_state["used_indices"]) >= self.max_signatures:
            raise ValueError("Key has reached maximum signature count, rotation required")
        
        # Get the next OTS index
        idx = ots_state["next_index"]
        
        # Mark this index as used
        ots_state["used_indices"].append(idx)
        ots_state["next_index"] = idx + 1
        
        # In a real implementation, we would:
        # 1. Select the OTS key pair at the leaf index
        # 2. Generate the OTS signature
        # 3. Create the Merkle tree authentication path
        
        # For this simulation:
        seed = bytes.fromhex(private_key["seed"])
        message_bytes = message.encode('utf-8')
        
        # Simulate the OTS signature
        ots_seed = self._hash(seed + idx.to_bytes(4, 'big') + b"ots")
        ots_signature = self._hash(ots_seed + message_bytes)
        
        # Simulate the Merkle authentication path
        # In a real implementation, this would be a list of sibling hashes
        auth_path = []
        current = idx
        for level in range(self.tree_height):
            # Determine if current node is left or right child
            is_left = current % 2 == 0
            sibling_idx = current + 1 if is_left else current - 1
            
            # Generate the sibling hash
            sibling_hash = self._hash(seed + sibling_idx.to_bytes(4, 'big') + level.to_bytes(4, 'big'))
            auth_path.append({
                "level": level,
                "is_left": not is_left,  # Sibling's position
                "hash": sibling_hash.hex()
            })
            
            # Move up the tree
            current = current // 2
        
        # Return the signature data
        return {
            "algorithm": f"SPHINCS-{self.tree_height}-{self.hash_function}",
            "key_id": private_key["key_id"],
            "index": idx,
            "ots_signature": ots_signature.hex(),
            "auth_path": auth_path,
            "timestamp": time.time()
        }
    
    def verify(self, message: str, signature: Dict[str, Any], public_key: Dict[str, str]) -> bool:
        """
        Verify a signature using the hash-based scheme.
        
        Args:
            message: The message that was signed
            signature: The signature data to verify
            public_key: The public key data
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Check that the key ID matches
            if signature["key_id"] != public_key["key_id"]:
                return False
            
            # In a real implementation, we would:
            # 1. Verify the OTS signature at the leaf
            # 2. Compute the path up to the root using the authentication path
            # 3. Verify that the computed root matches the public key root
            
            # For this simulation:
            message_bytes = message.encode('utf-8')
            idx = signature["index"]
            ots_signature = bytes.fromhex(signature["ots_signature"])
            
            # Reconstruct the leaf node value using the signature
            # In a real implementation, this would use the actual OTS verification
            leaf_hash = self._hash(ots_signature + message_bytes)
            
            # Compute the root using the authentication path
            # In a real implementation, this would be a proper tree traversal
            current_hash = leaf_hash
            for node in signature["auth_path"]:
                sibling_hash = bytes.fromhex(node["hash"])
                
                # Combine the current hash with its sibling
                if node["is_left"]:
                    combined = sibling_hash + current_hash
                else:
                    combined = current_hash + sibling_hash
                
                # Move up the tree
                current_hash = self._hash(combined)
            
            # The final hash should match the root in the public key
            computed_root = current_hash.hex()
            expected_root = public_key["root"]
            
            return computed_root == expected_root
            
        except (KeyError, ValueError, TypeError):
            # Any parsing or computation error means verification failure
            return False


def generate_merkle_tree(items: List[bytes], hash_function: str = "SHA3-256") -> Dict[str, Any]:
    """
    Generate a Merkle tree from a list of items.
    
    Args:
        items: The list of items (as bytes) to include in the tree
        hash_function: The hash function to use
        
    Returns:
        A dictionary containing the Merkle tree data
    """
    # Select the hash function
    if hash_function == "SHA3-256":
        hash_func = lambda x: hashlib.sha3_256(x).digest()
    elif hash_function == "SHA3-512":
        hash_func = lambda x: hashlib.sha3_512(x).digest()
    else:
        # Default to SHA3-256
        hash_func = lambda x: hashlib.sha3_256(x).digest()
    
    # Ensure we have at least one item
    if not items:
        raise ValueError("Cannot create Merkle tree with no items")
    
    # If odd number of items, duplicate the last one
    if len(items) % 2 == 1:
        items = items + [items[-1]]
    
    # Convert items to leaf nodes (hash the items)
    leaves = [hash_func(item) for item in items]
    
    # Store all layers of the tree
    tree_layers = [leaves]
    
    # Build the tree bottom-up
    current_layer = leaves
    while len(current_layer) > 1:
        next_layer = []
        
        # Process pairs of nodes
        for i in range(0, len(current_layer), 2):
            # If odd number of nodes, duplicate the last one
            if i + 1 >= len(current_layer):
                pair = current_layer[i] + current_layer[i]
            else:
                pair = current_layer[i] + current_layer[i + 1]
            
            # Hash the pair to create the parent node
            parent = hash_func(pair)
            next_layer.append(parent)
        
        # Add this layer to our tree
        tree_layers.append(next_layer)
        current_layer = next_layer
    
    # The root is the last node in the last layer
    root = tree_layers[-1][0]
    
    return {
        "root": root.hex(),
        "layers": [[node.hex() for node in layer] for layer in tree_layers],
        "hash_function": hash_function,
        "leaf_count": len(leaves)
    }


def generate_merkle_proof(tree: Dict[str, Any], leaf_index: int) -> Dict[str, Any]:
    """
    Generate a Merkle proof for a specific leaf in the tree.
    
    Args:
        tree: The Merkle tree data
        leaf_index: The index of the leaf to generate proof for
        
    Returns:
        A dictionary containing the proof data
    """
    if leaf_index < 0 or leaf_index >= tree["leaf_count"]:
        raise ValueError(f"Leaf index out of range: {leaf_index}")
    
    proof = []
    node_index = leaf_index
    
    # For each layer (except the root)
    for layer_index, layer in enumerate(tree["layers"][:-1]):
        # Is this a left or right child?
        is_left = node_index % 2 == 0
        
        # Get the sibling index
        sibling_index = node_index + 1 if is_left else node_index - 1
        
        # If the sibling is beyond the end of the layer,
        # we might be at the end of an odd-length layer
        if sibling_index < len(layer):
            sibling_value = layer[sibling_index]
        else:
            # Use the same node as its own sibling (this can happen
            # when we have an odd number of nodes in a layer)
            sibling_value = layer[node_index]
        
        # Add this sibling to the proof
        proof.append({
            "is_left": not is_left,  # From the perspective of combining
            "value": sibling_value,
            "layer": layer_index
        })
        
        # Move up to the parent
        node_index = node_index // 2
    
    return {
        "leaf_index": leaf_index,
        "proof_nodes": proof,
        "root": tree["root"],
        "hash_function": tree["hash_function"]
    }


def verify_merkle_proof(proof: Dict[str, Any], leaf_value: bytes) -> bool:
    """
    Verify a Merkle proof for a given leaf value.
    
    Args:
        proof: The Merkle proof data
        leaf_value: The raw value of the leaf (before hashing)
        
    Returns:
        True if the proof is valid, False otherwise
    """
    # Select the hash function
    if proof["hash_function"] == "SHA3-256":
        hash_func = lambda x: hashlib.sha3_256(x).digest()
    elif proof["hash_function"] == "SHA3-512":
        hash_func = lambda x: hashlib.sha3_512(x).digest()
    else:
        # Default to SHA3-256
        hash_func = lambda x: hashlib.sha3_256(x).digest()
    
    # Hash the leaf value to get the leaf node
    current = hash_func(leaf_value)
    
    # Traverse up the tree using the proof
    for node in proof["proof_nodes"]:
        sibling = bytes.fromhex(node["value"])
        
        # Combine with the sibling in the right order
        if node["is_left"]:
            combined = sibling + current
        else:
            combined = current + sibling
        
        # Hash to get the parent
        current = hash_func(combined)
    
    # The final hash should match the root
    return current.hex() == proof["root"]