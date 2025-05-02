# GenesisChain + DreamChain: Three-Layer Blockchain Architecture

## Overview

This project implements a quantum-resistant blockchain architecture with three specialized layers:

1. **GenesisChain** (Foundation Layer): Provides quantum-resistant security and consensus as the foundation layer
2. **NexusLayer** (Bridge Layer): Manages communication, verification, and security compartmentalization between layers
3. **DreamChain** (Application Layer): Delivers user-friendly features and high-throughput operations

Each layer has a specific purpose and security properties, creating a robust and modular blockchain system that can withstand quantum computing attacks.

## Key Features

### Quantum-Resistant Security
- Post-quantum cryptographic algorithms (lattice-based, hash-based, multivariate)
- Defense-in-depth with multiple cryptographic methods
- 256-bit security strength against quantum attacks

### Security Bulkheads
- Isolation mechanisms contain security breaches within specific zones
- Ability to "jettison" compromised components
- Multi-layer verification prevents cascading failures

### Adaptive Security Levels
- **STANDARD**: Basic quantum resistance
- **HIGH**: Enhanced security with lattice-based cryptography
- **VERY_HIGH**: Additional hash-based signatures
- **QUANTUM**: Full quantum security suite
- **PARANOID**: Maximum security with all features enabled

### Circuit Breakers
- Automatic protection systems that react to potential threats
- Isolate components when security thresholds are exceeded
- Self-healing capabilities with staged recovery

## Architecture Layers

### 1. GenesisChain (Foundation Layer)
The foundation of the architecture, GenesisChain provides:
- Quantum-resistant cryptography
- Consensus validation
- Immutable security record-keeping
- Emergency security protocols

### 2. NexusLayer (Bridge Layer)
The communication and security layer, NexusLayer provides:
- Bridge management between GenesisChain and DreamChain
- Security isolation gateways
- Verification gates for cross-layer operations
- Security compartmentalization

### 3. DreamChain (Application Layer)
The user-facing layer, DreamChain provides:
- High-throughput transaction processing
- Smart contract execution
- User-friendly features and interfaces
- Decentralized applications (DApps)

## Getting Started

### Prerequisites
- Node.js 14+ for frontend
- Python 3.8+ for backend
- MongoDB for data storage

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-organization/genesischain-dreamchain.git
   cd genesischain-dreamchain
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd frontend
   yarn install
   ```

4. **Set up environment variables**
   - Create `.env` file in the `backend` directory for MongoDB connection
   - Create `.env` file in the `frontend` directory for backend URL

5. **Start the application**
   ```bash
   # Start MongoDB
   mongod --dbpath=/path/to/data

   # Start backend
   cd backend
   python server.py

   # Start frontend
   cd frontend
   yarn start
   ```

## API Reference

The API is organized into sections for each layer:

### GenesisChain API
- `/api/genesis/status` - Get GenesisChain status
- `/api/genesis/security` - Get security information
- `/api/genesis/security/level` - Update security level
- `/api/genesis/alerts` - Get security alerts

### NexusLayer API
- `/api/nexus/status` - Get NexusLayer status
- `/api/nexus/bridges` - Get bridge information
- `/api/nexus/security/zones` - Get security zones
- `/api/nexus/security/bulkhead/isolate` - Isolate a security zone

### DreamChain API
- `/api/dream/status` - Get DreamChain status
- `/api/dream/blocks` - Get blocks
- `/api/dream/transactions` - Get transactions
- `/api/dream/accounts` - Get accounts

### Cross-Layer API
- `/api/cross-layer/status` - Get status of all three layers
- `/api/cross-layer/security` - Get security information
- `/api/cross-layer/metrics` - Get metrics for all layers

## Security

The system implements multiple layers of security protection:

1. **Quantum-Resistant Cryptography**
   - FALCON signature scheme
   - SPHINCS+ hash-based signatures
   - Kyber key encapsulation

2. **Security Isolation**
   - Security zones with different trust levels
   - Controlled interfaces between zones
   - Automatic circuit breakers

3. **Verification Gates**
   - Multi-level transaction verification
   - Cross-layer operation validation
   - Security proofs for critical operations

## License

This project is licensed under the MIT License - see the LICENSE file for details.
