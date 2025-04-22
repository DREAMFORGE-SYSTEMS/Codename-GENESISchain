import requests
import pytest
import time
import os
from dotenv import load_dotenv

# Load environment variables from frontend .env
load_dotenv('../frontend/.env')

# Get the backend URL from environment variable
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL')

class TestGenesisChain:
    def setup_method(self):
        self.base_url = BACKEND_URL
        if not self.base_url:
            raise ValueError("REACT_APP_BACKEND_URL environment variable not set")

    def test_api_root(self):
        """Test the API root endpoint"""
        response = requests.get(f"{self.base_url}/api")
        assert response.status_code == 200
        assert response.json()["message"] == "GenesisChain API"

    def test_blockchain_operations(self):
        """Test blockchain related operations"""
        # Get initial chain
        response = requests.get(f"{self.base_url}/api/chain")
        assert response.status_code == 200
        initial_chain = response.json()
        assert "chain" in initial_chain
        assert "length" in initial_chain
        initial_length = initial_chain["length"]

        # Create a new transaction
        transaction_data = {
            "sender": "test_sender",
            "recipient": "test_recipient",
            "amount": 10.0
        }
        response = requests.post(
            f"{self.base_url}/api/transactions/new",
            json=transaction_data
        )
        assert response.status_code == 201
        assert "message" in response.json()

        # Get transactions
        response = requests.get(f"{self.base_url}/api/transactions")
        assert response.status_code == 200
        transactions = response.json()["transactions"]
        assert len(transactions) > 0
        
        # Mine a new block
        response = requests.get(f"{self.base_url}/api/mine")
        assert response.status_code == 200
        mine_result = response.json()
        assert "message" in mine_result
        assert mine_result["message"] == "New Block Forged"

        # Verify chain length increased
        response = requests.get(f"{self.base_url}/api/chain")
        assert response.status_code == 200
        new_chain = response.json()
        assert new_chain["length"] > initial_length

    def test_data_input(self):
        """Test data input functionality"""
        test_data = {
            "content": "Test data for self-replication",
            "timestamp": time.time()
        }
        
        response = requests.post(
            f"{self.base_url}/api/data-input",
            json=test_data
        )
        assert response.status_code == 200
        result = response.json()
        assert "hash" in result
        assert "message" in result
        assert result["message"] == "Data processed successfully"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])