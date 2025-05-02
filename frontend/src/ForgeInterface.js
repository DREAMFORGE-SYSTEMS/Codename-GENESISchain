import { useState, useEffect } from "react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function ForgeInterface() {
  const [forgeStatus, setForgeStatus] = useState(null);
  const [energyStatistics, setEnergyStatistics] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [assets, setAssets] = useState([]);
  const [quantumLinks, setQuantumLinks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("status");
  const [notification, setNotification] = useState(null);
  
  // New asset form state
  const [newAsset, setNewAsset] = useState({
    asset_type: "QUANTUM_TOKEN",
    name: "",
    description: "",
    metadata: {},
    initial_value: 1.0
  });
  
  // New link form state
  const [newLink, setNewLink] = useState({
    source_system: "",
    target_system: "",
    link_type: "QUANTUM_ENTANGLED",
    bandwidth: 100.0
  });
  
  // Energy allocation form state
  const [energyAllocation, setEnergyAllocation] = useState({
    layer_distribution: {
      "GenesisChain": 33.33,
      "NexusLayer": 33.33,
      "DreamChain": 33.34
    }
  });

  useEffect(() => {
    fetchForgeStatus();
    fetchEnergyStatistics();
    fetchRecommendations();
    fetchAssets();
    fetchQuantumLinks();
  }, []);

  const showNotification = (message, type = "success") => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const fetchForgeStatus = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/forge/status`);
      if (response.ok) {
        const data = await response.json();
        setForgeStatus(data);
      } else {
        console.error("Error fetching forge status:", await response.text());
      }
    } catch (error) {
      console.error("Error fetching forge status:", error);
    }
  };

  const fetchEnergyStatistics = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/forge/statistics`);
      if (response.ok) {
        const data = await response.json();
        setEnergyStatistics(data);
      } else {
        console.error("Error fetching energy statistics:", await response.text());
      }
    } catch (error) {
      console.error("Error fetching energy statistics:", error);
    }
  };

  const fetchRecommendations = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/forge/recommendations`);
      if (response.ok) {
        const data = await response.json();
        setRecommendations(data);
      } else {
        console.error("Error fetching recommendations:", await response.text());
      }
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
  };

  const fetchAssets = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/forge/assets`);
      if (response.ok) {
        const data = await response.json();
        setAssets(data);
      } else {
        console.error("Error fetching assets:", await response.text());
      }
    } catch (error) {
      console.error("Error fetching assets:", error);
    }
  };

  const fetchQuantumLinks = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/forge/links`);
      if (response.ok) {
        const data = await response.json();
        setQuantumLinks(data);
      } else {
        console.error("Error fetching quantum links:", await response.text());
      }
    } catch (error) {
      console.error("Error fetching quantum links:", error);
    }
  };

  const handleGenerateEnergy = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/forge/energy/generate?cycles=1`);
      if (response.ok) {
        const data = await response.json();
        await fetchForgeStatus();
        await fetchEnergyStatistics();
        showNotification(`Generated ${data.energy_generated.toFixed(2)} units of quantum energy!`);
      } else {
        const errorData = await response.json();
        showNotification(`Error: ${errorData.detail || "Failed to generate energy"}`, "error");
      }
    } catch (error) {
      console.error("Error generating energy:", error);
      showNotification("Failed to generate energy", "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleAllocateEnergy = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/forge/energy/allocate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(energyAllocation)
      });
      
      if (response.ok) {
        await fetchForgeStatus();
        showNotification("Energy successfully allocated across layers!");
      } else {
        const errorData = await response.json();
        showNotification(`Error: ${errorData.detail || "Failed to allocate energy"}`, "error");
      }
    } catch (error) {
      console.error("Error allocating energy:", error);
      showNotification("Failed to allocate energy", "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateAsset = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/forge/assets/create`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(newAsset)
      });
      
      if (response.ok) {
        const asset = await response.json();
        await fetchAssets();
        setNewAsset({
          asset_type: "QUANTUM_TOKEN",
          name: "",
          description: "",
          metadata: {},
          initial_value: 1.0
        });
        showNotification(`Asset "${asset.name}" created successfully!`);
      } else {
        const errorData = await response.json();
        showNotification(`Error: ${errorData.detail || "Failed to create asset"}`, "error");
      }
    } catch (error) {
      console.error("Error creating asset:", error);
      showNotification("Failed to create asset", "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateLink = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/forge/links/create`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(newLink)
      });
      
      if (response.ok) {
        const link = await response.json();
        await fetchQuantumLinks();
        setNewLink({
          source_system: "",
          target_system: "",
          link_type: "QUANTUM_ENTANGLED",
          bandwidth: 100.0
        });
        showNotification(`Quantum link created successfully!`);
      } else {
        const errorData = await response.json();
        showNotification(`Error: ${errorData.detail || "Failed to create quantum link"}`, "error");
      }
    } catch (error) {
      console.error("Error creating quantum link:", error);
      showNotification("Failed to create quantum link", "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleTerminateLink = async (linkId) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/forge/links/${linkId}/terminate`, {
        method: "POST"
      });
      
      if (response.ok) {
        await fetchQuantumLinks();
        showNotification("Quantum link terminated successfully");
      } else {
        const errorData = await response.json();
        showNotification(`Error: ${errorData.detail || "Failed to terminate link"}`, "error");
      }
    } catch (error) {
      console.error("Error terminating link:", error);
      showNotification("Failed to terminate link", "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleEnergyInputChange = (layer, value) => {
    const newDistribution = { ...energyAllocation.layer_distribution };
    newDistribution[layer] = parseFloat(value) || 0;
    
    // Ensure the total is 100%
    const total = Object.values(newDistribution).reduce((sum, val) => sum + val, 0);
    if (total !== 100) {
      // Adjust the other layers proportionally
      const otherLayers = Object.keys(newDistribution).filter(l => l !== layer);
      if (otherLayers.length > 0) {
        const remainingEnergy = 100 - newDistribution[layer];
        if (remainingEnergy > 0) {
          const currentOtherTotal = otherLayers.reduce((sum, l) => sum + newDistribution[l], 0);
          otherLayers.forEach(l => {
            newDistribution[l] = currentOtherTotal > 0 
              ? (newDistribution[l] / currentOtherTotal) * remainingEnergy 
              : remainingEnergy / otherLayers.length;
          });
        } else {
          // If one layer has 100 or more, set others to 0
          otherLayers.forEach(l => {
            newDistribution[l] = 0;
          });
          // Cap the current layer at 100
          newDistribution[layer] = 100;
        }
      }
    }
    
    // Round to 2 decimal places
    Object.keys(newDistribution).forEach(l => {
      newDistribution[l] = parseFloat(newDistribution[l].toFixed(2));
    });
    
    setEnergyAllocation({ layer_distribution: newDistribution });
  };

  const handleNewAssetChange = (e) => {
    const { name, value } = e.target;
    
    if (name === "metadata") {
      try {
        const metadata = JSON.parse(value);
        setNewAsset({ ...newAsset, metadata });
      } catch (error) {
        // Invalid JSON, keep as string for now
        setNewAsset({ ...newAsset, [name]: value });
      }
    } else if (name === "initial_value") {
      setNewAsset({ ...newAsset, [name]: parseFloat(value) || 0 });
    } else {
      setNewAsset({ ...newAsset, [name]: value });
    }
  };

  const handleNewLinkChange = (e) => {
    const { name, value } = e.target;
    
    if (name === "bandwidth") {
      setNewLink({ ...newLink, [name]: parseFloat(value) || 0 });
    } else {
      setNewLink({ ...newLink, [name]: value });
    }
  };

  return (
    <div className="forge-interface">
      {notification && (
        <div className={`notification ${notification.type}`}>
          {notification.message}
        </div>
      )}

      <div className="forge-header">
        <h2>THE FORGE</h2>
        <p className="tagline">Quantum Energy Core & Asset Management System</p>
      </div>

      <div className="forge-tabs">
        <button 
          className={activeTab === "status" ? "active" : ""} 
          onClick={() => setActiveTab("status")}
        >
          Forge Status
        </button>
        <button 
          className={activeTab === "energy" ? "active" : ""} 
          onClick={() => setActiveTab("energy")}
        >
          Energy Management
        </button>
        <button 
          className={activeTab === "assets" ? "active" : ""} 
          onClick={() => setActiveTab("assets")}
        >
          Quantum Assets
        </button>
        <button 
          className={activeTab === "links" ? "active" : ""} 
          onClick={() => setActiveTab("links")}
        >
          Quantum Links
        </button>
      </div>

      <div className="forge-content">
        {activeTab === "status" && (
          <div className="forge-status-container">
            <h3>Forge Core Status</h3>
            
            {forgeStatus ? (
              <div className="forge-status-details">
                <div className="forge-status-card primary">
                  <h4>Quantum Forge Core</h4>
                  <div className="forge-id">ID: {forgeStatus.forge_id}</div>
                  <div className="forge-status-indicator">
                    <span className={`status-badge ${forgeStatus.active ? "active" : "inactive"}`}>
                      {forgeStatus.active ? "ACTIVE" : "INACTIVE"}
                    </span>
                  </div>
                  <div className="energy-meter">
                    <div className="energy-label">Energy Level</div>
                    <div className="energy-bar-container">
                      <div 
                        className="energy-bar" 
                        style={{ width: `${(forgeStatus.current_energy / forgeStatus.max_energy) * 100}%` }}
                      ></div>
                    </div>
                    <div className="energy-value">
                      {forgeStatus.current_energy.toFixed(2)} / {forgeStatus.max_energy.toFixed(2)}
                    </div>
                  </div>
                </div>
                
                <div className="forge-metrics">
                  <div className="metric-card">
                    <h4>Stability</h4>
                    <div className="metric-value">{(forgeStatus.stability * 100).toFixed(2)}%</div>
                  </div>
                  <div className="metric-card">
                    <h4>Efficiency</h4>
                    <div className="metric-value">{(forgeStatus.efficiency * 100).toFixed(2)}%</div>
                  </div>
                  <div className="metric-card">
                    <h4>Uptime</h4>
                    <div className="metric-value">{forgeStatus.uptime.toFixed(2)} hrs</div>
                  </div>
                  <div className="metric-card">
                    <h4>Alerts</h4>
                    <div className="metric-value">{forgeStatus.alert_count}</div>
                  </div>
                </div>
                
                <div className="energy-distribution">
                  <h4>Energy Distribution</h4>
                  <div className="distribution-bars">
                    {Object.entries(forgeStatus.layer_distribution).map(([layer, percentage]) => (
                      <div key={layer} className="layer-distribution">
                        <div className="layer-name">{layer}</div>
                        <div className="distribution-bar-container">
                          <div 
                            className={`distribution-bar ${layer}`}
                            style={{ width: `${percentage}%` }}
                          ></div>
                        </div>
                        <div className="distribution-value">{percentage.toFixed(2)}%</div>
                      </div>
                    ))}
                  </div>
                </div>
                
                {forgeStatus.latest_alerts.length > 0 && (
                  <div className="forge-alerts">
                    <h4>Latest Alerts</h4>
                    <ul className="alert-list">
                      {forgeStatus.latest_alerts.map((alert, index) => (
                        <li key={index} className={`alert-item ${alert.severity.toLowerCase()}`}>
                          <span className="alert-time">
                            {new Date(alert.timestamp * 1000).toLocaleTimeString()}
                          </span>
                          <span className="alert-message">{alert.message}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                
                <div className="forge-status-message">
                  <div className="message-box">
                    <h4>Status Message</h4>
                    <p>{forgeStatus.status_message}</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="loading-state">Loading Forge status...</div>
            )}
          </div>
        )}
        
        {activeTab === "energy" && (
          <div className="energy-management-container">
            <div className="energy-management-column">
              <h3>Energy Generation & Allocation</h3>
              
              <div className="energy-generation">
                <h4>Quantum Energy Generation</h4>
                <p className="description">
                  Generate new quantum energy to power the blockchain architecture.
                </p>
                <button 
                  onClick={handleGenerateEnergy} 
                  disabled={isLoading}
                  className="generate-button"
                >
                  {isLoading ? "Generating..." : "Generate Quantum Energy"}
                </button>
              </div>
              
              <div className="energy-allocation">
                <h4>Energy Allocation</h4>
                <p className="description">
                  Allocate energy across the three layers of the blockchain architecture.
                </p>
                <form onSubmit={handleAllocateEnergy} className="allocation-form">
                  {Object.entries(energyAllocation.layer_distribution).map(([layer, percentage]) => (
                    <div key={layer} className="allocation-input-group">
                      <label>{layer}</label>
                      <div className="allocation-slider-container">
                        <input 
                          type="range" 
                          min="0" 
                          max="100" 
                          step="1"
                          value={percentage} 
                          onChange={(e) => handleEnergyInputChange(layer, e.target.value)} 
                        />
                        <input 
                          type="number" 
                          min="0" 
                          max="100" 
                          step="0.01"
                          value={percentage} 
                          onChange={(e) => handleEnergyInputChange(layer, e.target.value)} 
                        />
                        <span className="percentage-symbol">%</span>
                      </div>
                    </div>
                  ))}
                  <button 
                    type="submit" 
                    disabled={isLoading}
                    className="allocate-button"
                  >
                    {isLoading ? "Allocating..." : "Allocate Energy"}
                  </button>
                </form>
              </div>
            </div>
            
            <div className="energy-statistics-column">
              <h3>Energy Statistics & Recommendations</h3>
              
              {energyStatistics ? (
                <div className="energy-statistics">
                  <div className="stat-card">
                    <h4>Energy Generated</h4>
                    <div className="stat-value">{energyStatistics.total_energy_generated.toFixed(2)}</div>
                  </div>
                  <div className="stat-card">
                    <h4>Energy Consumed</h4>
                    <div className="stat-value">{energyStatistics.total_energy_consumed.toFixed(2)}</div>
                  </div>
                  <div className="stat-card">
                    <h4>Generation Rate</h4>
                    <div className="stat-value">{energyStatistics.generation_rate.toFixed(2)}/hr</div>
                  </div>
                  <div className="stat-card">
                    <h4>Consumption Rate</h4>
                    <div className="stat-value">{energyStatistics.consumption_rate.toFixed(2)}/hr</div>
                  </div>
                </div>
              ) : (
                <div className="loading-state">Loading energy statistics...</div>
              )}
              
              {recommendations ? (
                <div className="energy-recommendations">
                  <h4>Optimization Recommendations</h4>
                  <div className="recommendations-list">
                    {Object.entries(recommendations).map(([layer, value]) => (
                      <div key={layer} className="recommendation-item">
                        <div className="layer-name">{layer}</div>
                        <div className="recommended-value">
                          {value.toFixed(2)}% 
                          <span className={value > energyAllocation.layer_distribution[layer] ? "increase" : "decrease"}>
                            {value > energyAllocation.layer_distribution[layer] ? "▲" : "▼"}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                  <button 
                    className="apply-recommendations-button"
                    onClick={() => setEnergyAllocation({ layer_distribution: recommendations })}
                  >
                    Apply Recommendations
                  </button>
                </div>
              ) : (
                <div className="loading-state">Loading recommendations...</div>
              )}
              
              <div className="energy-info-box">
                <h4>About Quantum Energy Management</h4>
                <ul>
                  <li><strong>Generation:</strong> Creates new energy through quantum processes</li>
                  <li><strong>Allocation:</strong> Distributes energy to maintain optimal blockchain operation</li>
                  <li><strong>Optimization:</strong> AI-assisted recommendations for optimal energy distribution</li>
                  <li><strong>Efficiency:</strong> Higher efficiency means more transactions per energy unit</li>
                </ul>
              </div>
            </div>
          </div>
        )}
        
        {activeTab === "assets" && (
          <div className="assets-container">
            <div className="assets-column">
              <h3>Quantum Assets</h3>
              
              <div className="assets-list">
                {assets.length > 0 ? (
                  assets.map((asset) => (
                    <div key={asset.asset_id} className="asset-card">
                      <div className="asset-header">
                        <h4>{asset.name}</h4>
                        <span className={`asset-type ${asset.asset_type.toLowerCase()}`}>
                          {asset.asset_type}
                        </span>
                      </div>
                      <div className="asset-details">
                        <p><strong>ID:</strong> {asset.asset_id}</p>
                        <p><strong>Value:</strong> {asset.value.toFixed(2)}</p>
                        <p><strong>Creator:</strong> {asset.creator}</p>
                        <p><strong>Owner:</strong> {asset.owner}</p>
                        {asset.description && (
                          <p><strong>Description:</strong> {asset.description}</p>
                        )}
                        <p className="asset-timestamp">
                          Created: {new Date(asset.created_at * 1000).toLocaleString()}
                        </p>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="empty-state">
                    <p>No quantum assets found. Create your first asset!</p>
                  </div>
                )}
              </div>
            </div>
            
            <div className="create-asset-column">
              <h3>Create New Asset</h3>
              
              <form onSubmit={handleCreateAsset} className="create-asset-form">
                <div className="form-group">
                  <label>Asset Type</label>
                  <select
                    name="asset_type"
                    value={newAsset.asset_type}
                    onChange={handleNewAssetChange}
                    required
                  >
                    <option value="QUANTUM_TOKEN">Quantum Token</option>
                    <option value="ENERGY_CERTIFICATE">Energy Certificate</option>
                    <option value="SECURITY_CREDENTIAL">Security Credential</option>
                    <option value="DIGITAL_ASSET">Digital Asset</option>
                    <option value="SMART_CONTRACT">Smart Contract</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label>Name</label>
                  <input
                    type="text"
                    name="name"
                    value={newAsset.name}
                    onChange={handleNewAssetChange}
                    required
                    placeholder="Asset Name"
                  />
                </div>
                
                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    name="description"
                    value={newAsset.description}
                    onChange={handleNewAssetChange}
                    placeholder="Asset Description"
                    rows={3}
                  />
                </div>
                
                <div className="form-group">
                  <label>Initial Value</label>
                  <input
                    type="number"
                    name="initial_value"
                    step="0.01"
                    min="0"
                    value={newAsset.initial_value}
                    onChange={handleNewAssetChange}
                    required
                  />
                </div>
                
                <div className="form-group">
                  <label>Metadata (JSON)</label>
                  <textarea
                    name="metadata"
                    value={typeof newAsset.metadata === 'object' ? JSON.stringify(newAsset.metadata, null, 2) : newAsset.metadata}
                    onChange={handleNewAssetChange}
                    placeholder='{"key": "value"}'
                    rows={4}
                  />
                </div>
                
                <button type="submit" disabled={isLoading} className="create-button">
                  {isLoading ? "Creating..." : "Create Asset"}
                </button>
              </form>
              
              <div className="asset-info-box">
                <h4>About Quantum Assets</h4>
                <ul>
                  <li><strong>Quantum Tokens:</strong> Native currency with quantum security</li>
                  <li><strong>Energy Certificates:</strong> Represents ownership of quantum energy</li>
                  <li><strong>Security Credentials:</strong> Access tokens for secure operations</li>
                  <li><strong>Digital Assets:</strong> Secure representation of digital goods</li>
                  <li><strong>Smart Contracts:</strong> Self-executing quantum-secure agreements</li>
                </ul>
              </div>
            </div>
          </div>
        )}
        
        {activeTab === "links" && (
          <div className="quantum-links-container">
            <div className="links-column">
              <h3>Quantum Links</h3>
              
              <div className="links-list">
                {quantumLinks.length > 0 ? (
                  quantumLinks.map((link) => (
                    <div key={link.connection_id} className="link-card">
                      <div className="link-header">
                        <h4>
                          <span className="system-name">{link.source_system}</span>
                          <span className="link-arrow">↔</span>
                          <span className="system-name">{link.target_system}</span>
                        </h4>
                        <span className={`link-status ${link.status.toLowerCase()}`}>
                          {link.status}
                        </span>
                      </div>
                      
                      <div className="link-details">
                        <div className="link-metrics">
                          <div className="metric">
                            <span className="metric-label">Stability</span>
                            <span className="metric-value">{(link.stability * 100).toFixed(2)}%</span>
                          </div>
                          <div className="metric">
                            <span className="metric-label">Bandwidth</span>
                            <span className="metric-value">{link.bandwidth.toFixed(2)}</span>
                          </div>
                          <div className="metric">
                            <span className="metric-label">Latency</span>
                            <span className="metric-value">{link.latency.toFixed(4)}s</span>
                          </div>
                        </div>
                        
                        <p><strong>Type:</strong> {link.link_type}</p>
                        <p><strong>Protocol:</strong> {link.link_protocol}</p>
                        <p><strong>Energy Transferred:</strong> {link.energy_transferred.toFixed(2)}</p>
                        <p><strong>Data Transferred:</strong> {link.transferred_data.toFixed(2)} KB</p>
                        <p className="link-timestamp">
                          Created: {new Date(link.created_at * 1000).toLocaleString()}
                        </p>
                        <p className="link-timestamp">
                          Last Activity: {new Date(link.last_activity * 1000).toLocaleString()}
                        </p>
                        
                        {link.status !== "TERMINATED" && (
                          <button
                            onClick={() => handleTerminateLink(link.connection_id)}
                            className="terminate-button"
                          >
                            Terminate Link
                          </button>
                        )}
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="empty-state">
                    <p>No quantum links found. Establish your first link!</p>
                  </div>
                )}
              </div>
            </div>
            
            <div className="create-link-column">
              <h3>Establish New Quantum Link</h3>
              
              <form onSubmit={handleCreateLink} className="create-link-form">
                <div className="form-group">
                  <label>Source System</label>
                  <input
                    type="text"
                    name="source_system"
                    value={newLink.source_system}
                    onChange={handleNewLinkChange}
                    required
                    placeholder="Source System Name"
                  />
                </div>
                
                <div className="form-group">
                  <label>Target System</label>
                  <input
                    type="text"
                    name="target_system"
                    value={newLink.target_system}
                    onChange={handleNewLinkChange}
                    required
                    placeholder="Target System Name"
                  />
                </div>
                
                <div className="form-group">
                  <label>Link Type</label>
                  <select
                    name="link_type"
                    value={newLink.link_type}
                    onChange={handleNewLinkChange}
                    required
                  >
                    <option value="QUANTUM_ENTANGLED">Quantum Entangled</option>
                    <option value="HYBRID_SECURE">Hybrid Secure</option>
                    <option value="HIGH_BANDWIDTH">High Bandwidth</option>
                    <option value="LOW_LATENCY">Low Latency</option>
                    <option value="ENERGY_EFFICIENT">Energy Efficient</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label>Bandwidth</label>
                  <input
                    type="number"
                    name="bandwidth"
                    step="0.1"
                    min="1"
                    value={newLink.bandwidth}
                    onChange={handleNewLinkChange}
                    required
                  />
                </div>
                
                <button type="submit" disabled={isLoading} className="create-button">
                  {isLoading ? "Establishing..." : "Establish Link"}
                </button>
              </form>
              
              <div className="link-info-box">
                <h4>About Quantum Links</h4>
                <ul>
                  <li><strong>Quantum Entangled:</strong> Highest security, quantum-resistant communication</li>
                  <li><strong>Hybrid Secure:</strong> Balance of security and performance</li>
                  <li><strong>High Bandwidth:</strong> Optimized for large data transfers</li>
                  <li><strong>Low Latency:</strong> Optimized for speed and responsiveness</li>
                  <li><strong>Energy Efficient:</strong> Minimizes energy consumption</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ForgeInterface;