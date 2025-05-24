import time
import uuid
import json
import hashlib
import os
import sys
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from crypto.quantum_resistant import QuantumResistantCrypto
except ImportError:
    from backend.crypto.quantum_resistant import QuantumResistantCrypto

class StatementMetadata:
    """
    Metadata for statements recorded in the accountability ledger.
    """
    def __init__(
        self,
        speaker_id: str,
        speaker_name: str,
        speaker_title: str,
        source_url: str,
        source_name: str,
        source_type: str,
        statement_timestamp: float,
        context_category: str,
        context_tags: List[str],
        recording_timestamp: Optional[float] = None
    ):
        self.speaker_id = speaker_id
        self.speaker_name = speaker_name
        self.speaker_title = speaker_title
        self.source_url = source_url
        self.source_name = source_name
        self.source_type = source_type
        self.statement_timestamp = statement_timestamp
        self.context_category = context_category
        self.context_tags = context_tags
        self.recording_timestamp = recording_timestamp or time.time()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for storage."""
        return {
            "speaker_id": self.speaker_id,
            "speaker_name": self.speaker_name,
            "speaker_title": self.speaker_title,
            "source_url": self.source_url,
            "source_name": self.source_name, 
            "source_type": self.source_type,
            "statement_timestamp": self.statement_timestamp,
            "context_category": self.context_category,
            "context_tags": self.context_tags,
            "recording_timestamp": self.recording_timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StatementMetadata':
        """Create metadata from dictionary."""
        return cls(
            speaker_id=data["speaker_id"],
            speaker_name=data["speaker_name"],
            speaker_title=data["speaker_title"],
            source_url=data["source_url"],
            source_name=data["source_name"],
            source_type=data["source_type"],
            statement_timestamp=data["statement_timestamp"],
            context_category=data["context_category"],
            context_tags=data["context_tags"],
            recording_timestamp=data.get("recording_timestamp")
        )


class StatementRecord:
    """
    A complete statement record for the accountability ledger.
    """
    def __init__(
        self,
        statement_text: str,
        metadata: StatementMetadata,
        signature: Optional[str] = None,
        record_id: Optional[str] = None
    ):
        self.statement_text = statement_text
        self.metadata = metadata
        self.record_id = record_id or str(uuid.uuid4())
        self.signature = signature
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary for storage."""
        return {
            "record_id": self.record_id,
            "statement_text": self.statement_text,
            "metadata": self.metadata.to_dict(),
            "signature": self.signature
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StatementRecord':
        """Create record from dictionary."""
        return cls(
            statement_text=data["statement_text"],
            metadata=StatementMetadata.from_dict(data["metadata"]),
            signature=data.get("signature"),
            record_id=data["record_id"]
        )
    
    def get_record_hash(self) -> str:
        """
        Calculate a cryptographic hash of the record content.
        Used for verification and blockchain integration.
        """
        content = {
            "statement_text": self.statement_text,
            "metadata": self.metadata.to_dict()
        }
        content_str = json.dumps(content, sort_keys=True)
        return hashlib.sha3_256(content_str.encode('utf-8')).hexdigest()
    
    def sign(self, private_key: str) -> None:
        """
        Sign the record with a quantum-resistant signature.
        """
        record_hash = self.get_record_hash().encode('utf-8')
        self.signature = QuantumResistantCrypto.sign_message(record_hash, private_key)
    
    def verify_signature(self, public_key: str) -> bool:
        """
        Verify the record's signature.
        """
        if not self.signature:
            return False
        
        record_hash = self.get_record_hash().encode('utf-8')
        return QuantumResistantCrypto.verify_signature(record_hash, self.signature, public_key)


class TrustedSource:
    """
    Represents a trusted source for statement verification.
    """
    def __init__(
        self,
        source_id: str,
        name: str,
        source_type: str,
        url: str,
        public_key: str,
        reputation_score: float = 0.0
    ):
        self.source_id = source_id
        self.name = name
        self.source_type = source_type
        self.url = url
        self.public_key = public_key
        self.reputation_score = reputation_score
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert source to dictionary for storage."""
        return {
            "source_id": self.source_id,
            "name": self.name,
            "source_type": self.source_type,
            "url": self.url,
            "public_key": self.public_key,
            "reputation_score": self.reputation_score
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TrustedSource':
        """Create source from dictionary."""
        return cls(
            source_id=data["source_id"],
            name=data["name"],
            source_type=data["source_type"],
            url=data["url"],
            public_key=data["public_key"],
            reputation_score=data.get("reputation_score", 0.0)
        )


class AccountabilityLedger:
    """
    The main ledger for tracking and verifying public statements.
    Implements quantum-resistant signatures for tamper-proof records.
    """
    def __init__(self, database_path: str = None):
        self.records: Dict[str, StatementRecord] = {}
        self.trusted_sources: Dict[str, TrustedSource] = {}
        self.database_path = database_path
        
    def add_trusted_source(self, source: TrustedSource) -> None:
        """Add a trusted source to the ledger."""
        self.trusted_sources[source.source_id] = source
        
    def record_statement(
        self,
        statement_text: str,
        metadata: StatementMetadata,
        source_private_key: str
    ) -> StatementRecord:
        """
        Record a new statement in the ledger.
        Signs the statement with the source's private key.
        """
        # Create the record
        record = StatementRecord(statement_text, metadata)
        
        # Sign the record
        record.sign(source_private_key)
        
        # Store the record
        self.records[record.record_id] = record
        
        return record
    
    def verify_record(self, record_id: str) -> Tuple[bool, Optional[str]]:
        """
        Verify a record's signature against its trusted source.
        Returns (is_verified, reason_if_not_verified)
        """
        record = self.records.get(record_id)
        if not record:
            return False, "Record not found"
        
        source_id = record.metadata.source_name
        source = self.trusted_sources.get(source_id)
        if not source:
            return False, "Source not trusted"
        
        if not record.verify_signature(source.public_key):
            return False, "Invalid signature"
        
        return True, None
    
    def get_statements_by_speaker(self, speaker_id: str) -> List[StatementRecord]:
        """Get all statements by a specific speaker."""
        return [
            record for record in self.records.values()
            if record.metadata.speaker_id == speaker_id
        ]
    
    def get_statements_by_category(self, category: str) -> List[StatementRecord]:
        """Get all statements in a specific category."""
        return [
            record for record in self.records.values()
            if record.metadata.context_category == category
        ]
    
    def get_statements_by_tag(self, tag: str) -> List[StatementRecord]:
        """Get all statements with a specific tag."""
        return [
            record for record in self.records.values()
            if tag in record.metadata.context_tags
        ]
    
    def get_statements_by_date_range(
        self,
        start_timestamp: float,
        end_timestamp: float
    ) -> List[StatementRecord]:
        """Get all statements within a date range."""
        return [
            record for record in self.records.values()
            if start_timestamp <= record.metadata.statement_timestamp <= end_timestamp
        ]
    
    def get_cross_referenced_statements(
        self, 
        statement_text: str,
        similarity_threshold: float = 0.8
    ) -> List[StatementRecord]:
        """
        Find statements that are similar to the given text.
        Uses a simple similarity metric for demonstration.
        """
        # A real implementation would use more sophisticated text similarity
        # This is a simplified version for illustration
        similar_records = []
        for record in self.records.values():
            # Simple similarity check (would use NLP in a real implementation)
            if statement_text.lower() in record.statement_text.lower():
                similar_records.append(record)
        
        return similar_records
    
    def save_to_database(self) -> None:
        """Save the ledger state to the database."""
        if not self.database_path:
            return
        
        data = {
            "records": {
                record_id: record.to_dict() 
                for record_id, record in self.records.items()
            },
            "trusted_sources": {
                source_id: source.to_dict()
                for source_id, source in self.trusted_sources.items()
            }
        }
        
        with open(self.database_path, 'w') as f:
            json.dump(data, f)
    
    def load_from_database(self) -> None:
        """Load the ledger state from the database."""
        if not self.database_path or not os.path.exists(self.database_path):
            return
        
        with open(self.database_path, 'r') as f:
            data = json.load(f)
        
        self.records = {
            record_id: StatementRecord.from_dict(record_data)
            for record_id, record_data in data.get("records", {}).items()
        }
        
        self.trusted_sources = {
            source_id: TrustedSource.from_dict(source_data)
            for source_id, source_data in data.get("trusted_sources", {}).items()
        }
        
    def prepare_for_blockchain(self, record_id: str) -> Dict[str, Any]:
        """
        Prepare a record for inclusion in the blockchain.
        Returns a serialized version suitable for the blockchain.
        """
        record = self.records.get(record_id)
        if not record:
            raise ValueError(f"Record {record_id} not found")
        
        # Create a blockchain-ready representation
        blockchain_data = {
            "record_id": record.record_id,
            "statement_hash": record.get_record_hash(),
            "signature": record.signature,
            "metadata": {
                "speaker_id": record.metadata.speaker_id,
                "speaker_name": record.metadata.speaker_name,
                "source": record.metadata.source_name,
                "timestamp": record.metadata.statement_timestamp,
                "category": record.metadata.context_category,
                "tags": record.metadata.context_tags
            }
        }
        
        return blockchain_data