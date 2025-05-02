"""
GenesisChain Quantum Security Module

This package implements quantum-resistant cryptography and security features
for the GenesisChain blockchain.
"""

from .quantum_resistant_crypto import (
    QuantumResistantKeyPair,
    sign_message,
    verify_signature,
    generate_keypair,
)

from .lattice_crypto import (
    LatticeBasedSignature,
    LatticeBasedEncryption,
)

from .hash_based_crypto import (
    HashBasedSignature,
    generate_merkle_tree,
    verify_merkle_proof,
)

from .quantum_entropy import (
    QuantumRandomNumberGenerator,
    generate_secure_seed,
)

from .security_layers import (
    SecurityLevel,
    SecurityLayerManager,
    create_default_security_manager,
)

__all__ = [
    'QuantumResistantKeyPair',
    'sign_message',
    'verify_signature',
    'generate_keypair',
    'LatticeBasedSignature',
    'LatticeBasedEncryption',
    'HashBasedSignature',
    'generate_merkle_tree',
    'verify_merkle_proof',
    'QuantumRandomNumberGenerator',
    'generate_secure_seed',
    'SecurityLevel',
    'SecurityLayerManager',
    'create_default_security_manager',
]