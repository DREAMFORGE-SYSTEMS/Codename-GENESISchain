import pytest
import requests
import json
import time
from typing import Dict, Any

# Get the backend URL from environment variable or use default
BACKEND_URL = "https://5132-2401-4900-1c0f-8f2-7185-b2b3-4e1-4ae4.ngrok-free.app"

class TestGenesisChain:
    def setup_method(self):
        """Setup before each test"""
        self.base_url = BACKEND_URL
        
    def test_api_root(self):
        """Test the root endpoint"""
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
        
        # Create a new transaction
        transaction = {
            "sender": "test_sender",
            "recipient": "test_recipient",
            "amount": 10.0
        }
        response = requests.post(
            f"{self.base_url}/api/transactions/new",
            json=transaction
        )
        assert response.status_code == 201
        assert "message" in response.json()

        # Mine a new block
        response = requests.get(f"{self.base_url}/api/mine")
        assert response.status_code == 200
        mine_result = response.json()
        assert "message" in mine_result
        assert mine_result["message"] == "New Block Forged"
        assert "transactions" in mine_result
        
        # Verify chain length increased
        response = requests.get(f"{self.base_url}/api/chain")
        assert response.status_code == 200
        new_chain = response.json()
        assert new_chain["length"] > initial_chain["length"]

    def test_data_input_and_replication(self):
        """Test data input processing and self-replication"""
        test_data = {
            "content": "Testing AI generation and self-replication",
            "timestamp": time.time()
        }
        
        # Submit data
        response = requests.post(
            f"{self.base_url}/api/data-input",
            json=test_data
        )
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert result["message"] == "Data processed successfully"
        assert "generated_content" in result
        assert "images" in result["generated_content"]
        assert "audio" in result["generated_content"]
        assert "replications" in result
        
        # Get data inputs to verify
        response = requests.get(f"{self.base_url}/api/data-inputs")
        assert response.status_code == 200
        data_inputs = response.json()
        assert "data_inputs" in data_inputs
        assert len(data_inputs["data_inputs"]) > 0
        
        # Verify the latest input matches our test data
        latest_input = data_inputs["data_inputs"][0]
        assert "original_data" in latest_input
        assert "content" in latest_input["original_data"]
        assert latest_input["original_data"]["content"] == test_data["content"]
        
        # Verify self-replications were created
        replicated_entries = [d for d in data_inputs["data_inputs"] 
                            if "parent_data_id" in d and d["parent_data_id"] == latest_input["data_id"]]
        assert len(replicated_entries) > 0

    def test_transactions_list(self):
        """Test retrieving transactions list"""
        response = requests.get(f"{self.base_url}/api/transactions")
        assert response.status_code == 200
        data = response.json()
        assert "transactions" in data
        assert isinstance(data["transactions"], list)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])