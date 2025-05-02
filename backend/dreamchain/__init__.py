"""
DreamChain - Application Layer

This module implements the DreamChain application layer, which sits on top of
the NexusLayer and GenesisChain for a complete blockchain architecture.

DreamChain focuses on user-friendly features and applications while relying on 
the lower layers for security and communication.
"""

from .core import DreamChain, Transaction, Block, Account
from .contracts import SmartContract, ContractRegistry, TokenContract
from .apps import DApp, DAppRegistry

__all__ = [
    'DreamChain',
    'Transaction',
    'Block',
    'Account',
    'SmartContract',
    'ContractRegistry',
    'TokenContract',
    'DApp',
    'DAppRegistry',
]