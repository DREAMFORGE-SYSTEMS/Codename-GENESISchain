"""
API routes for quantum-enhanced features.
"""

from fastapi import APIRouter, HTTPException, Body, Query, Path
from typing import Dict, List, Any, Optional
import uuid
import time
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from crypto.quantum_resistant import QuantumResistantCrypto
    from accountability.ledger import AccountabilityLedger, StatementMetadata, StatementRecord, TrustedSource
    from randomness.quantum_randomness import create_randomness_generator
except ImportError:
    from backend.crypto.quantum_resistant import QuantumResistantCrypto
    from backend.accountability.ledger import AccountabilityLedger, StatementMetadata, StatementRecord, TrustedSource
    from backend.randomness.quantum_randomness import create_randomness_generator

# Create router
quantum_router = APIRouter(prefix="/api/quantum", tags=["quantum"])

# Create instances of our services
# In a real application, these would be properly managed with dependency injection
accountability_ledger = AccountabilityLedger()
randomness_generator = create_randomness_generator(certified=True)

# Routes for quantum-resistant cryptography
@quantum_router.post("/crypto/generate-keypair", response_model=Dict[str, str])
async def generate_keypair():
    """Generate a quantum-resistant keypair."""
    public_key, private_key = QuantumResistantCrypto.generate_keypair()
    return {
        "public_key": public_key,
        "private_key": private_key
    }

@quantum_router.post("/crypto/sign", response_model=Dict[str, str])
async def sign_message(
    message: str = Body(..., embed=True),
    private_key: str = Body(..., embed=True)
):
    """Sign a message using quantum-resistant cryptography."""
    signature = QuantumResistantCrypto.sign_message(
        message.encode('utf-8'),
        private_key
    )
    return {
        "signature": signature
    }

@quantum_router.post("/crypto/verify", response_model=Dict[str, bool])
async def verify_signature(
    message: str = Body(..., embed=True),
    signature: str = Body(..., embed=True),
    public_key: str = Body(..., embed=True)
):
    """Verify a signature using quantum-resistant cryptography."""
    is_valid = QuantumResistantCrypto.verify_signature(
        message.encode('utf-8'),
        signature,
        public_key
    )
    return {
        "is_valid": is_valid
    }

# Routes for political accountability
@quantum_router.post("/accountability/add-source", response_model=Dict[str, str])
async def add_trusted_source(
    name: str = Body(..., embed=True),
    source_type: str = Body(..., embed=True),
    url: str = Body(..., embed=True)
):
    """Add a trusted source for statement verification."""
    # Generate a key for the source
    public_key, private_key = QuantumResistantCrypto.generate_keypair()
    
    # Create a source ID
    source_id = str(uuid.uuid4())
    
    # Create and add the source
    source = TrustedSource(
        source_id=source_id,
        name=name,
        source_type=source_type,
        url=url,
        public_key=public_key
    )
    accountability_ledger.add_trusted_source(source)
    
    # Return the source ID and private key
    # In a real application, the private key would be securely provided to the source
    return {
        "source_id": source_id,
        "private_key": private_key
    }

@quantum_router.post("/accountability/record", response_model=Dict[str, str])
async def record_statement(
    statement_text: str = Body(..., embed=True),
    speaker_id: str = Body(..., embed=True),
    speaker_name: str = Body(..., embed=True),
    speaker_title: str = Body(..., embed=True),
    source_id: str = Body(..., embed=True),
    source_private_key: str = Body(..., embed=True),
    source_url: str = Body(..., embed=True),
    context_category: str = Body(..., embed=True),
    context_tags: List[str] = Body([], embed=True)
):
    """Record a statement in the accountability ledger."""
    # Create the metadata
    metadata = StatementMetadata(
        speaker_id=speaker_id,
        speaker_name=speaker_name,
        speaker_title=speaker_title,
        source_url=source_url,
        source_name=source_id,
        source_type="news", # Simplified for this example
        statement_timestamp=time.time(),
        context_category=context_category,
        context_tags=context_tags
    )
    
    # Record the statement
    record = accountability_ledger.record_statement(
        statement_text=statement_text,
        metadata=metadata,
        source_private_key=source_private_key
    )
    
    return {
        "record_id": record.record_id
    }

@quantum_router.get("/accountability/verify/{record_id}", response_model=Dict[str, Any])
async def verify_statement(record_id: str = Path(...)):
    """Verify a statement in the accountability ledger."""
    is_verified, reason = accountability_ledger.verify_record(record_id)
    
    return {
        "is_verified": is_verified,
        "reason": reason
    }

@quantum_router.get("/accountability/by-speaker/{speaker_id}", response_model=List[Dict[str, Any]])
async def get_statements_by_speaker(speaker_id: str = Path(...)):
    """Get all statements by a specific speaker."""
    records = accountability_ledger.get_statements_by_speaker(speaker_id)
    
    return [record.to_dict() for record in records]

@quantum_router.get("/accountability/by-category/{category}", response_model=List[Dict[str, Any]])
async def get_statements_by_category(category: str = Path(...)):
    """Get all statements in a specific category."""
    records = accountability_ledger.get_statements_by_category(category)
    
    return [record.to_dict() for record in records]

# Routes for quantum randomness
@quantum_router.get("/randomness/bytes", response_model=Dict[str, str])
async def get_random_bytes(
    length: int = Query(32, ge=1, le=1024),
    certified: bool = Query(False)
):
    """Generate random bytes."""
    generator = create_randomness_generator(certified=certified)
    
    if certified:
        random_bytes, certification_data = generator.generate_certified_random_bytes(length)
        return {
            "random_bytes": random_bytes.hex(),
            "certification": str(certification_data)
        }
    else:
        random_bytes = generator.generate_random_bytes(length)
        return {
            "random_bytes": random_bytes.hex()
        }

@quantum_router.get("/randomness/int", response_model=Dict[str, Any])
async def get_random_int(
    min_value: int = Query(0),
    max_value: int = Query(100),
    certified: bool = Query(False)
):
    """Generate a random integer."""
    generator = create_randomness_generator(certified=certified)
    
    if certified:
        random_int, certification_data = generator.generate_certified_random_int(min_value, max_value)
        return {
            "random_int": random_int,
            "certification": str(certification_data)
        }
    else:
        random_int = generator.generate_random_int(min_value, max_value)
        return {
            "random_int": random_int
        }

@quantum_router.get("/randomness/float", response_model=Dict[str, float])
async def get_random_float():
    """Generate a random float between 0 and 1."""
    generator = create_randomness_generator(certified=False)
    random_float = generator.generate_random_float()
    
    return {
        "random_float": random_float
    }