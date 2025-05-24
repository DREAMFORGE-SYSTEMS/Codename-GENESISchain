import React, { useState, useEffect } from 'react';
import './QuantumFeatures.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function QuantumFeatures() {
  // State for cryptography section
  const [keyPair, setKeyPair] = useState(null);
  const [message, setMessage] = useState('');
  const [signature, setSignature] = useState('');
  const [isVerified, setIsVerified] = useState(null);
  
  // State for accountability section
  const [trustedSources, setTrustedSources] = useState([]);
  const [selectedSource, setSelectedSource] = useState(null);
  const [statementText, setStatementText] = useState('');
  const [speakerName, setSpeakerName] = useState('');
  const [speakerTitle, setSpeakerTitle] = useState('');
  const [category, setCategory] = useState('');
  const [recordId, setRecordId] = useState('');
  const [verificationResult, setVerificationResult] = useState(null);
  
  // State for randomness section
  const [randomBytes, setRandomBytes] = useState('');
  const [randomInt, setRandomInt] = useState(null);
  const [randomFloat, setRandomFloat] = useState(null);
  const [isCertified, setIsCertified] = useState(false);
  
  // Generate a new key pair
  const generateKeyPair = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/quantum/crypto/generate-keypair`, {
        method: 'POST'
      });
      
      if (response.ok) {
        const data = await response.json();
        setKeyPair(data);
      } else {
        console.error('Failed to generate key pair');
      }
    } catch (error) {
      console.error('Error generating key pair:', error);
    }
  };
  
  // Sign a message
  const signMessage = async () => {
    if (!keyPair || !message) return;
    
    try {
      const response = await fetch(`${BACKEND_URL}/api/quantum/crypto/sign`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: message,
          private_key: keyPair.private_key
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setSignature(data.signature);
      } else {
        console.error('Failed to sign message');
      }
    } catch (error) {
      console.error('Error signing message:', error);
    }
  };
  
  // Verify a signature
  const verifySignature = async () => {
    if (!keyPair || !message || !signature) return;
    
    try {
      const response = await fetch(`${BACKEND_URL}/api/quantum/crypto/verify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: message,
          signature: signature,
          public_key: keyPair.public_key
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setIsVerified(data.is_valid);
      } else {
        console.error('Failed to verify signature');
      }
    } catch (error) {
      console.error('Error verifying signature:', error);
    }
  };
  
  // Add a trusted source
  const addTrustedSource = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/quantum/accountability/add-source`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: 'News Source',
          source_type: 'news',
          url: 'https://example.com'
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setTrustedSources([...trustedSources, {
          id: data.source_id,
          name: 'News Source',
          privateKey: data.private_key
        }]);
        setSelectedSource({
          id: data.source_id,
          name: 'News Source',
          privateKey: data.private_key
        });
      } else {
        console.error('Failed to add trusted source');
      }
    } catch (error) {
      console.error('Error adding trusted source:', error);
    }
  };
  
  // Record a statement
  const recordStatement = async () => {
    if (!selectedSource || !statementText || !speakerName) return;
    
    try {
      const response = await fetch(`${BACKEND_URL}/api/quantum/accountability/record`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          statement_text: statementText,
          speaker_id: 'speaker-' + Date.now(),
          speaker_name: speakerName,
          speaker_title: speakerTitle,
          source_id: selectedSource.id,
          source_private_key: selectedSource.privateKey,
          source_url: 'https://example.com/statement',
          context_category: category || 'general',
          context_tags: ['politics', 'public statement']
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setRecordId(data.record_id);
        setStatementText('');
        setSpeakerName('');
        setSpeakerTitle('');
        setCategory('');
      } else {
        console.error('Failed to record statement');
      }
    } catch (error) {
      console.error('Error recording statement:', error);
    }
  };
  
  // Verify a statement
  const verifyStatement = async () => {
    if (!recordId) return;
    
    try {
      const response = await fetch(`${BACKEND_URL}/api/quantum/accountability/verify/${recordId}`);
      
      if (response.ok) {
        const data = await response.json();
        setVerificationResult(data);
      } else {
        console.error('Failed to verify statement');
      }
    } catch (error) {
      console.error('Error verifying statement:', error);
    }
  };
  
  // Generate random bytes
  const generateRandomBytes = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/quantum/randomness/bytes?length=32&certified=${isCertified}`);
      
      if (response.ok) {
        const data = await response.json();
        setRandomBytes(data.random_bytes);
      } else {
        console.error('Failed to generate random bytes');
      }
    } catch (error) {
      console.error('Error generating random bytes:', error);
    }
  };
  
  // Generate random integer
  const generateRandomInt = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/quantum/randomness/int?min_value=1&max_value=100&certified=${isCertified}`);
      
      if (response.ok) {
        const data = await response.json();
        setRandomInt(data.random_int);
      } else {
        console.error('Failed to generate random integer');
      }
    } catch (error) {
      console.error('Error generating random integer:', error);
    }
  };
  
  // Generate random float
  const generateRandomFloat = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/quantum/randomness/float`);
      
      if (response.ok) {
        const data = await response.json();
        setRandomFloat(data.random_float);
      } else {
        console.error('Failed to generate random float');
      }
    } catch (error) {
      console.error('Error generating random float:', error);
    }
  };
  
  return (
    <div className="quantum-features">
      <h1 className="quantum-title">Quantum-Enhanced Features</h1>
      <p className="quantum-description">
        Explore the quantum-resistant cryptography, accountability ledger, and high-quality randomness features.
      </p>
      
      <div className="quantum-sections">
        {/* Cryptography Section */}
        <section className="quantum-section crypto-section">
          <h2>Quantum-Resistant Cryptography</h2>
          <div className="section-content">
            <button 
              className="quantum-button" 
              onClick={generateKeyPair}
            >
              Generate Key Pair
            </button>
            
            {keyPair && (
              <div className="key-pair-display">
                <div className="key-item">
                  <h4>Public Key:</h4>
                  <div className="key-value">{keyPair.public_key.substring(0, 20)}...</div>
                </div>
                <div className="key-item">
                  <h4>Private Key:</h4>
                  <div className="key-value">{keyPair.private_key.substring(0, 20)}...</div>
                </div>
              </div>
            )}
            
            <div className="form-group">
              <label>Message to Sign:</label>
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Enter a message to sign"
              />
            </div>
            
            <button 
              className="quantum-button" 
              onClick={signMessage}
              disabled={!keyPair || !message}
            >
              Sign Message
            </button>
            
            {signature && (
              <div className="signature-display">
                <h4>Signature:</h4>
                <div className="signature-value">{signature.substring(0, 20)}...</div>
                
                <button 
                  className="quantum-button verify-button" 
                  onClick={verifySignature}
                >
                  Verify Signature
                </button>
                
                {isVerified !== null && (
                  <div className={`verification-result ${isVerified ? 'valid' : 'invalid'}`}>
                    Signature is {isVerified ? 'valid' : 'invalid'}
                  </div>
                )}
              </div>
            )}
          </div>
        </section>
        
        {/* Accountability Section */}
        <section className="quantum-section accountability-section">
          <h2>Political Accountability Ledger</h2>
          <div className="section-content">
            <button 
              className="quantum-button" 
              onClick={addTrustedSource}
            >
              Add Trusted Source
            </button>
            
            {selectedSource && (
              <div className="source-display">
                <h4>Active Source:</h4>
                <div className="source-info">
                  <span className="source-name">{selectedSource.name}</span>
                  <span className="source-id">ID: {selectedSource.id.substring(0, 8)}...</span>
                </div>
              </div>
            )}
            
            <div className="form-group">
              <label>Statement:</label>
              <textarea
                value={statementText}
                onChange={(e) => setStatementText(e.target.value)}
                placeholder="Enter a public statement"
              />
            </div>
            
            <div className="form-row">
              <div className="form-group half">
                <label>Speaker Name:</label>
                <input
                  type="text"
                  value={speakerName}
                  onChange={(e) => setSpeakerName(e.target.value)}
                  placeholder="Enter speaker name"
                />
              </div>
              <div className="form-group half">
                <label>Speaker Title:</label>
                <input
                  type="text"
                  value={speakerTitle}
                  onChange={(e) => setSpeakerTitle(e.target.value)}
                  placeholder="Enter speaker title"
                />
              </div>
            </div>
            
            <div className="form-group">
              <label>Category:</label>
              <input
                type="text"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                placeholder="Enter statement category"
              />
            </div>
            
            <button 
              className="quantum-button" 
              onClick={recordStatement}
              disabled={!selectedSource || !statementText || !speakerName}
            >
              Record Statement
            </button>
            
            {recordId && (
              <div className="record-display">
                <h4>Record ID:</h4>
                <div className="record-id">{recordId}</div>
                
                <button 
                  className="quantum-button verify-button" 
                  onClick={verifyStatement}
                >
                  Verify Statement
                </button>
                
                {verificationResult && (
                  <div className={`verification-result ${verificationResult.is_verified ? 'valid' : 'invalid'}`}>
                    Statement is {verificationResult.is_verified ? 'verified' : 'invalid'}
                    {!verificationResult.is_verified && verificationResult.reason && (
                      <div className="verification-reason">
                        Reason: {verificationResult.reason}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </section>
        
        {/* Randomness Section */}
        <section className="quantum-section randomness-section">
          <h2>Quantum-Enhanced Randomness</h2>
          <div className="section-content">
            <div className="certification-toggle">
              <label>
                <input
                  type="checkbox"
                  checked={isCertified}
                  onChange={(e) => setIsCertified(e.target.checked)}
                />
                Use certified randomness
              </label>
            </div>
            
            <div className="randomness-buttons">
              <button 
                className="quantum-button" 
                onClick={generateRandomBytes}
              >
                Generate Random Bytes
              </button>
              
              <button 
                className="quantum-button" 
                onClick={generateRandomInt}
              >
                Generate Random Integer (1-100)
              </button>
              
              <button 
                className="quantum-button" 
                onClick={generateRandomFloat}
              >
                Generate Random Float
              </button>
            </div>
            
            <div className="randomness-results">
              {randomBytes && (
                <div className="result-item">
                  <h4>Random Bytes:</h4>
                  <div className="result-value bytes">{randomBytes.substring(0, 32)}...</div>
                </div>
              )}
              
              {randomInt !== null && (
                <div className="result-item">
                  <h4>Random Integer:</h4>
                  <div className="result-value">{randomInt}</div>
                </div>
              )}
              
              {randomFloat !== null && (
                <div className="result-item">
                  <h4>Random Float:</h4>
                  <div className="result-value">{randomFloat}</div>
                </div>
              )}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default QuantumFeatures;