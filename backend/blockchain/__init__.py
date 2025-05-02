"""
GenesisChain Blockchain Implementation

This package implements the core blockchain functionality for GenesisChain,
a quantum-resistant blockchain with advanced security features.
"""

from .blockchain import Blockchain, Block, Transaction
from .mining import mine_block, calculate_hash, calculate_proof_of_work
from .wallet import QuantumWallet, create_wallet, get_wallet_balance

__all__ = [
    'Blockchain',
    'Block',
    'Transaction',
    'mine_block',
    'calculate_hash',
    'calculate_proof_of_work',
    'QuantumWallet',
    'create_wallet',
    'get_wallet_balance'
]