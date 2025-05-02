"""
NexusLayer - Intermediary Bridge Layer

This module implements the NexusLayer for the GenesisChain + DreamChain architecture.
NexusLayer serves as the communication, verification, and security compartmentalization
layer between the quantum-resistant GenesisChain foundation and the feature-rich
DreamChain application layer.
"""

from .bridge import BridgeManager, MessageType, SecurityGateway
from .isolation import SecurityBulkhead, SecurityZone, IsolationLevel
from .verification import VerificationGate, ProofValidator, ValidationError

__all__ = [
    'BridgeManager',
    'MessageType',
    'SecurityGateway',
    'SecurityBulkhead',
    'SecurityZone',
    'IsolationLevel',
    'VerificationGate',
    'ProofValidator',
    'ValidationError',
]