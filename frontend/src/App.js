import { useState, useEffect } from "react";
import "./App.css";
import ThreeLayerArchitecture from "./ThreeLayerArchitecture";
import ForgeInterface from "./ForgeInterface";
import "./ForgeInterface.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [blocks, setBlocks] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [wallets, setWallets] = useState([]);
  const [securityInfo, setSecurityInfo] = useState({});
  const [selectedWallet, setSelectedWallet] = useState(null);
  const [newTransaction, setNewTransaction] = useState({
    sender: "",
    recipient: "",
    amount: 0,
    data: "",
    fee: 0.001
  });
  const [newWallet, setNewWallet] = useState({
    name: "",
    security_level: "STANDARD"
  });
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("architecture");
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    fetchBlockchain();
    fetchTransactions();
    fetchWallets();
    fetchSecurityInfo();
  }, []);

  const showNotification = (message, type = "success") => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const fetchBlockchain = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/chain`);
      const data = await response.json();
      setBlocks(data.chain);
    } catch (error) {
      console.error("Error fetching blockchain:", error);
      showNotification("Failed to fetch blockchain data", "error");
    }
  };

  const fetchTransactions = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/transactions`);
      const data = await response.json();
      setTransactions(data.pending_transactions || []);
    } catch (error) {
      console.error("Error fetching transactions:", error);
      showNotification("Failed to fetch transaction data", "error");
    }
  };

  const fetchWallets = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/wallets`);
      const data = await response.json();
      setWallets(data.wallets || []);
      
      // Set the first wallet as selected if we have wallets and none is selected
      if (data.wallets?.length > 0 && !selectedWallet) {
        setSelectedWallet(data.wallets[0]);
        setNewTransaction(prev => ({
          ...prev,
          sender: data.wallets[0].id
        }));
      }
    } catch (error) {
      console.error("Error fetching wallets:", error);
      showNotification("Failed to fetch wallet data", "error");
    }
  };

  const fetchSecurityInfo = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/security/info`);
      const data = await response.json();
      setSecurityInfo(data);
    } catch (error) {
      console.error("Error fetching security info:", error);
    }
  };

  const handleTransactionInputChange = (e) => {
    const { name, value } = e.target;
    setNewTransaction({
      ...newTransaction,
      [name]: name === "amount" || name === "fee" ? parseFloat(value) : value
    });
  };

  const handleWalletInputChange = (e) => {
    const { name, value } = e.target;
    setNewWallet({
      ...newWallet,
      [name]: value
    });
  };

  const handleTransactionSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch(`${BACKEND_URL}/api/transactions/new`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(newTransaction)
      });

      if (response.ok) {
        const result = await response.json();
        setNewTransaction(prev => ({
          ...prev,
          recipient: "",
          amount: 0,
          data: "",
          fee: 0.001
        }));
        await fetchTransactions();
        showNotification(`Transaction submitted successfully! ID: ${result.transaction_id}`);
      } else {
        const errorData = await response.json();
        showNotification(`Error: ${errorData.detail || "Failed to submit transaction"}`, "error");
      }
    } catch (error) {
      console.error("Error submitting transaction:", error);
      showNotification("Failed to submit transaction", "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateWallet = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch(`${BACKEND_URL}/api/wallets/create`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(newWallet)
      });

      if (response.ok) {
        const wallet = await response.json();
        setNewWallet({
          name: "",
          security_level: "STANDARD"
        });
        await fetchWallets();
        showNotification(`Wallet "${wallet.name}" created successfully!`);
      } else {
        const errorData = await response.json();
        showNotification(`Error: ${errorData.detail || "Failed to create wallet"}`, "error");
      }
    } catch (error) {
      console.error("Error creating wallet:", error);
      showNotification("Failed to create wallet", "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleWalletSelect = (wallet) => {
    setSelectedWallet(wallet);
    setNewTransaction(prev => ({
      ...prev,
      sender: wallet.id
    }));
  };

  const handleMining = async () => {
    if (!selectedWallet) {
      showNotification("Please select a wallet for mining rewards", "error");
      return;
    }

    setIsLoading(true);
    try {
      // Mining starts the blockchain if it's not already running
      const response = await fetch(`${BACKEND_URL}/api/mine?miner_address=${selectedWallet.id}`);
      
      if (response.ok) {
        const data = await response.json();
        await Promise.all([fetchBlockchain(), fetchTransactions(), fetchWallets()]);
        showNotification(`New block mined! Block #${data.block.index}`);
      } else {
        const errorData = await response.json();
        showNotification(`Error: ${errorData.detail || "Failed to mine block"}`, "error");
      }
    } catch (error) {
      console.error("Error mining block:", error);
      showNotification("Failed to mine block", "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdateSecurityLevel = async (level) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/security/level/${level}`, {
        method: "PUT"
      });
      
      if (response.ok) {
        const data = await response.json();
        await fetchSecurityInfo();
        showNotification(`Security level updated to ${level}`);
      } else {
        const errorData = await response.json();
        showNotification(`Error: ${errorData.detail || "Failed to update security level"}`, "error");
      }
    } catch (error) {
      console.error("Error updating security level:", error);
      showNotification("Failed to update security level", "error");
    } finally {
      setIsLoading(false);
    }
  };

  const formatHash = (hash) => {
    if (!hash) return "";
    return hash.length > 16 ? `${hash.substring(0, 8)}...${hash.substring(hash.length - 8)}` : hash;
  };

  return (
    <div className="app-container">
      {notification && (
        <div className={`notification ${notification.type}`}>
          {notification.message}
        </div>
      )}
      
      <header className="header">
        <div className="logo-container">
          <h1>GenesisChain + DreamChain</h1>
          <p className="tagline">Three-Layer Quantum-Resistant Blockchain Architecture</p>
        </div>
      </header>

      <nav className="tabs">
        <button 
          className={activeTab === "architecture" ? "active" : ""} 
          onClick={() => setActiveTab("architecture")}
        >
          Three-Layer Architecture
        </button>
        <button 
          className={activeTab === "blockchain" ? "active" : ""} 
          onClick={() => setActiveTab("blockchain")}
        >
          Blockchain
        </button>
        <button 
          className={activeTab === "transactions" ? "active" : ""} 
          onClick={() => setActiveTab("transactions")}
        >
          Transactions
        </button>
        <button 
          className={activeTab === "wallets" ? "active" : ""} 
          onClick={() => setActiveTab("wallets")}
        >
          Wallets
        </button>
        <button 
          className={activeTab === "mining" ? "active" : ""} 
          onClick={() => setActiveTab("mining")}
        >
          Mining
        </button>
        <button 
          className={activeTab === "security" ? "active" : ""} 
          onClick={() => setActiveTab("security")}
        >
          Security
        </button>
        <button  
          className={activeTab === "forge" ? "active" : ""}  
          onClick={() => setActiveTab("forge")} 
        > 
          The Forge 
        </button>
      </nav>

      <main className="content">
        {activeTab === "architecture" && (
          <ThreeLayerArchitecture />
        )}

        {activeTab === "blockchain" && (
          <div className="blockchain-container">
            <h2>Blockchain Explorer</h2>
            <div className="blocks-list">
              {blocks.map((block) => (
                <div key={block.hash} className="block-card">
                  <div className="block-header">
                    <h3>Block #{block.index}</h3>
                    <span className="timestamp">
                      {new Date(block.timestamp * 1000).toLocaleString()}
                    </span>
                  </div>
                  <div className="block-details">
                    <p>
                      <strong>Hash:</strong>{" "}
                      <span className="hash">{formatHash(block.hash)}</span>
                    </p>
                    <p>
                      <strong>Previous:</strong>{" "}
                      <span className="hash">{formatHash(block.previous_hash)}</span>
                    </p>
                    <p>
                      <strong>Merkle Root:</strong>{" "}
                      <span className="hash">{formatHash(block.merkle_root)}</span>
                    </p>
                    <p>
                      <strong>Nonce:</strong> {block.nonce}
                    </p>
                    <p>
                      <strong>Difficulty:</strong> {block.difficulty}
                    </p>
                    <p>
                      <strong>Transactions:</strong>{" "}
                      {block.transactions.length || 0}
                    </p>
                  </div>
                </div>
              ))}
              {blocks.length === 0 && (
                <div className="empty-state">
                  <p>No blocks found. Start by mining the first block!</p>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === "transactions" && (
          <div className="transactions-container">
            <h2>Transactions</h2>
            <form onSubmit={handleTransactionSubmit} className="transaction-form">
              <div className="form-group">
                <label>From Wallet</label>
                <select
                  name="sender"
                  value={newTransaction.sender}
                  onChange={handleTransactionInputChange}
                  required
                >
                  <option value="">Select Wallet</option>
                  {wallets.map((wallet) => (
                    <option key={wallet.id} value={wallet.id}>
                      {wallet.name} ({formatHash(wallet.address)}) - Balance: {wallet.balance}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Recipient</label>
                <input
                  type="text"
                  name="recipient"
                  value={newTransaction.recipient}
                  onChange={handleTransactionInputChange}
                  required
                  placeholder="Recipient address"
                />
              </div>
              <div className="form-group">
                <label>Amount</label>
                <input
                  type="number"
                  name="amount"
                  step="0.01"
                  value={newTransaction.amount}
                  onChange={handleTransactionInputChange}
                  required
                  placeholder="Amount"
                />
              </div>
              <div className="form-group">
                <label>Transaction Fee</label>
                <input
                  type="number"
                  name="fee"
                  step="0.001"
                  min="0.001"
                  value={newTransaction.fee}
                  onChange={handleTransactionInputChange}
                  required
                  placeholder="Transaction Fee"
                />
              </div>
              <div className="form-group">
                <label>Data (Optional)</label>
                <textarea
                  name="data"
                  value={newTransaction.data}
                  onChange={handleTransactionInputChange}
                  placeholder="Additional transaction data"
                  rows={3}
                />
              </div>
              <button type="submit" disabled={isLoading} className="submit-button">
                {isLoading ? "Processing..." : "Submit Transaction"}
              </button>
            </form>

            <div className="transactions-list">
              <h3>Pending Transactions</h3>
              {transactions.length > 0 ? (
                transactions.map((tx) => (
                  <div key={tx.id} className="transaction-card">
                    <div className="transaction-details">
                      <p>
                        <strong>ID:</strong> <span className="hash">{formatHash(tx.id)}</span>
                      </p>
                      <p>
                        <strong>From:</strong> <span className="address">{formatHash(tx.sender)}</span>
                      </p>
                      <p>
                        <strong>To:</strong> <span className="address">{formatHash(tx.recipient)}</span>
                      </p>
                      <p>
                        <strong>Amount:</strong> <span className="amount">{tx.amount}</span>
                      </p>
                      <p>
                        <strong>Fee:</strong> <span className="amount">{tx.fee}</span>
                      </p>
                      <p className="transaction-timestamp">
                        {new Date(tx.timestamp * 1000).toLocaleString()}
                      </p>
                    </div>
                    <div className="transaction-status">
                      <span className="pending">Pending</span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="empty-state">
                  <p>No pending transactions found. Create a new transaction!</p>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === "wallets" && (
          <div className="wallets-container">
            <h2>Quantum-Resistant Wallets</h2>
            
            <div className="wallet-columns">
              <div className="wallet-list-column">
                <h3>Your Wallets</h3>
                <div className="wallets-list">
                  {wallets.length > 0 ? (
                    wallets.map((wallet) => (
                      <div 
                        key={wallet.id} 
                        className={`wallet-card ${selectedWallet && selectedWallet.id === wallet.id ? 'selected' : ''}`}
                        onClick={() => handleWalletSelect(wallet)}
                      >
                        <h4>{wallet.name}</h4>
                        <p>
                          <strong>Address:</strong>{" "}
                          <span className="address">{formatHash(wallet.address)}</span>
                        </p>
                        <p>
                          <strong>Balance:</strong>{" "}
                          <span className="balance">{wallet.balance}</span>
                        </p>
                      </div>
                    ))
                  ) : (
                    <div className="empty-state">
                      <p>No wallets found. Create a new wallet!</p>
                    </div>
                  )}
                </div>
              </div>
              
              <div className="wallet-create-column">
                <h3>Create New Wallet</h3>
                <form onSubmit={handleCreateWallet} className="wallet-form">
                  <div className="form-group">
                    <label>Wallet Name</label>
                    <input
                      type="text"
                      name="name"
                      value={newWallet.name}
                      onChange={handleWalletInputChange}
                      required
                      placeholder="My Quantum Wallet"
                    />
                  </div>
                  <div className="form-group">
                    <label>Security Level</label>
                    <select
                      name="security_level"
                      value={newWallet.security_level}
                      onChange={handleWalletInputChange}
                      required
                    >
                      <option value="STANDARD">Standard</option>
                      <option value="HIGH">High</option>
                      <option value="VERY_HIGH">Very High</option>
                      <option value="QUANTUM">Quantum</option>
                      <option value="PARANOID">Paranoid</option>
                    </select>
                  </div>
                  <button type="submit" disabled={isLoading} className="submit-button">
                    {isLoading ? "Creating..." : "Create Wallet"}
                  </button>
                </form>
                
                <div className="info-box">
                  <h3>Security Levels</h3>
                  <p>
                    <strong>Standard:</strong> Basic quantum resistance
                  </p>
                  <p>
                    <strong>High:</strong> Added lattice-based cryptography
                  </p>
                  <p>
                    <strong>Very High:</strong> Added hash-based signatures
                  </p>
                  <p>
                    <strong>Quantum:</strong> Full quantum security suite
                  </p>
                  <p>
                    <strong>Paranoid:</strong> Maximum security with all features
                  </p>
                </div>
              </div>
            </div>

            {selectedWallet && (
              <div className="selected-wallet-details">
                <h3>Selected Wallet Details</h3>
                <div className="wallet-details-card">
                  <h4>{selectedWallet.name}</h4>
                  <p>
                    <strong>ID:</strong> <span>{selectedWallet.id}</span>
                  </p>
                  <p>
                    <strong>Address:</strong> <span>{selectedWallet.address}</span>
                  </p>
                  <p>
                    <strong>Balance:</strong> <span>{selectedWallet.balance}</span>
                  </p>
                  <p>
                    <strong>Created:</strong>{" "}
                    <span>{new Date(selectedWallet.created_at * 1000).toLocaleString()}</span>
                  </p>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === "mining" && (
          <div className="mining-container">
            <h2>Quantum-Resistant Mining</h2>
            <p className="description">
              Mining adds a new block to the chain, validates pending transactions, and generates rewards.
            </p>
            
            <div className="mining-controls">
              <div className="mining-wallet-select">
                <h3>Select Mining Wallet</h3>
                <div className="wallet-selector">
                  {wallets.map((wallet) => (
                    <div 
                      key={wallet.id} 
                      className={`wallet-option ${selectedWallet && selectedWallet.id === wallet.id ? 'selected' : ''}`}
                      onClick={() => handleWalletSelect(wallet)}
                    >
                      {wallet.name} ({formatHash(wallet.address)})
                    </div>
                  ))}
                </div>
              </div>
              
              <button 
                onClick={handleMining} 
                disabled={isLoading || !selectedWallet}
                className="mining-button"
              >
                {isLoading ? "Mining in progress..." : "Mine New Block"}
              </button>
            </div>
            
            <div className="info-box">
              <h3>About Quantum-Resistant Mining</h3>
              <p>
                <strong>Process:</strong> Uses quantum-resistant proof-of-work algorithm
              </p>
              <p>
                <strong>Protection:</strong> Secure against quantum computing attacks
              </p>
              <p>
                <strong>Verification:</strong> Multi-layered verification using quantum-resistant cryptography
              </p>
              <p>
                <strong>Reward:</strong> Miners receive newly created coins and transaction fees
              </p>
              <p>
                <strong>Difficulty:</strong> Automatically adjusts to maintain consistent block times
              </p>
            </div>
          </div>
        )}

        {activeTab === "security" && (
          <div className="security-container">
            <h2>Quantum Security Dashboard</h2>
            
            <div className="security-status">
              <div className="security-level-indicator">
                <h3>Current Security Level</h3>
                <div className={`security-level ${securityInfo.active_security_level}`}>
                  {securityInfo.active_security_level || "Loading..."}
                </div>
                
                <div className="security-level-controls">
                  <h4>Update Security Level</h4>
                  <div className="security-level-buttons">
                    {securityInfo.available_levels?.map((level) => (
                      <button
                        key={level}
                        className={`security-level-button ${level} ${level === securityInfo.active_security_level ? 'active' : ''}`}
                        onClick={() => handleUpdateSecurityLevel(level)}
                        disabled={isLoading || level === securityInfo.active_security_level}
                      >
                        {level}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
              
              <div className="security-features">
                <h3>Active Security Features</h3>
                <ul className="feature-list">
                  {securityInfo.active_security_features?.map((feature) => (
                    <li key={feature} className="security-feature">
                      <span className="feature-icon">✓</span>
                      <span className="feature-name">{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            
            <div className="quantum-security-info">
              <h3>Quantum Resistance Status</h3>
              <div className="quantum-info-card">
                <div className="quantum-status">
                  <span className="status-indicator">
                    {securityInfo.quantum_resistance_status?.status === "Enabled" ? "ACTIVE" : "INACTIVE"}
                  </span>
                </div>
                
                <div className="quantum-algorithms">
                  <h4>Quantum-Resistant Algorithms</h4>
                  <ul>
                    {securityInfo.quantum_resistance_status?.algorithms?.map((algo) => (
                      <li key={algo}>{algo}</li>
                    ))}
                  </ul>
                </div>
                
                <div className="security-strength">
                  <h4>Security Strength</h4>
                  <p>{securityInfo.quantum_resistance_status?.security_bits || 0} bits</p>
                </div>
              </div>
              
              <div className="info-box">
                <h3>About Quantum Security</h3>
                <p>
                  <strong>Quantum Attacks:</strong> Traditional cryptography (RSA, ECC) is vulnerable to quantum computers
                </p>
                <p>
                  <strong>Protection:</strong> GenesisChain uses post-quantum cryptography resistant to quantum attacks
                </p>
                <p>
                  <strong>Algorithms:</strong> Includes lattice-based, hash-based, and multivariate cryptography
                </p>
                <p>
                  <strong>Defense-in-Depth:</strong> Multiple security layers provide redundant protection
                </p>
              </div>
            </div>
          </div>
        )}
        
        {activeTab === "forge" && (
          <div className="forge-tab-container">
            <h2>THE FORGE</h2>
            <p className="description">
              Quantum Energy Core & Asset Management System for the blockchain.
            </p>
            <ForgeInterface />
          </div>
        )}
      </main>

      <footer className="footer">
        <p>GenesisChain + DreamChain - Three-Layer Quantum-Resistant Blockchain Architecture &copy; 2025</p>
      </footer>
    </div>
  );
}

export default App;