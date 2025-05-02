import React, { useState, useEffect } from 'react';
import './ThreeLayerArchitecture.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function ThreeLayerArchitecture() {
  const [genesisStatus, setGenesisStatus] = useState(null);
  const [nexusStatus, setNexusStatus] = useState(null);
  const [dreamStatus, setDreamStatus] = useState(null);
  const [crossLayerStatus, setCrossLayerStatus] = useState(null);
  const [securityLevel, setSecurityLevel] = useState('STANDARD');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStatuses();
  }, []);

  const fetchStatuses = async () => {
    setLoading(true);
    setError(null);

    try {
      // Fetch status for all layers
      const genesisResponse = await fetch(`${BACKEND_URL}/api/genesis/status`);
      const nexusResponse = await fetch(`${BACKEND_URL}/api/nexus/status`);
      const dreamResponse = await fetch(`${BACKEND_URL}/api/dream/status`);
      const crossLayerResponse = await fetch(`${BACKEND_URL}/api/cross-layer/status`);

      if (!genesisResponse.ok || !nexusResponse.ok || !dreamResponse.ok || !crossLayerResponse.ok) {
        throw new Error('Failed to fetch layer statuses');
      }

      const genesisData = await genesisResponse.json();
      const nexusData = await nexusResponse.json();
      const dreamData = await dreamResponse.json();
      const crossLayerData = await crossLayerResponse.json();

      setGenesisStatus(genesisData);
      setNexusStatus(nexusData);
      setDreamStatus(dreamData);
      setCrossLayerStatus(crossLayerData);
      
      if (genesisData.security_level) {
        setSecurityLevel(genesisData.security_level);
      }
    } catch (err) {
      console.error('Error fetching layer statuses:', err);
      setError('Failed to fetch layer data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleSecurityLevelChange = async (level) => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/genesis/security/level`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ level })
      });

      if (!response.ok) {
        throw new Error('Failed to update security level');
      }

      setSecurityLevel(level);
      // Refresh statuses to show updated information
      fetchStatuses();
    } catch (err) {
      console.error('Error updating security level:', err);
      setError('Failed to update security level. Please try again later.');
    }
  };

  if (loading) {
    return (
      <div className="three-layer-container loading">
        <div className="loading-spinner"></div>
        <p>Loading architecture status...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="three-layer-container error">
        <div className="error-message">
          <h3>Error</h3>
          <p>{error}</p>
          <button onClick={fetchStatuses}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="three-layer-container">
      <h1>Three-Layer Blockchain Architecture</h1>
      <p className="architecture-description">
        A quantum-resistant blockchain architecture with three specialized layers for security, communication, and application functionality.
      </p>

      <div className="security-controls">
        <h2>Security Controls</h2>
        <div className="security-level-selector">
          <p>Current Security Level: <span className={`security-level ${securityLevel}`}>{securityLevel}</span></p>
          <div className="security-buttons">
            <button 
              className={`security-button STANDARD ${securityLevel === 'STANDARD' ? 'active' : ''}`} 
              onClick={() => handleSecurityLevelChange('STANDARD')}
            >
              STANDARD
            </button>
            <button 
              className={`security-button HIGH ${securityLevel === 'HIGH' ? 'active' : ''}`} 
              onClick={() => handleSecurityLevelChange('HIGH')}
            >
              HIGH
            </button>
            <button 
              className={`security-button VERY_HIGH ${securityLevel === 'VERY_HIGH' ? 'active' : ''}`} 
              onClick={() => handleSecurityLevelChange('VERY_HIGH')}
            >
              VERY HIGH
            </button>
            <button 
              className={`security-button QUANTUM ${securityLevel === 'QUANTUM' ? 'active' : ''}`} 
              onClick={() => handleSecurityLevelChange('QUANTUM')}
            >
              QUANTUM
            </button>
            <button 
              className={`security-button PARANOID ${securityLevel === 'PARANOID' ? 'active' : ''}`} 
              onClick={() => handleSecurityLevelChange('PARANOID')}
            >
              PARANOID
            </button>
          </div>
        </div>
      </div>

      <div className="layers-visualization">
        <div className="layer dream-layer">
          <h2>DreamChain</h2>
          <div className="layer-description">
            <p>Application Layer for user-friendly features and high throughput</p>
          </div>
          <div className="layer-status">
            <div className={`status-indicator ${dreamStatus?.status === 'operational' ? 'operational' : 'error'}`}>
              {dreamStatus?.status === 'operational' ? 'ONLINE' : 'OFFLINE'}
            </div>
            <div className="layer-metrics">
              <div className="metric">
                <span className="metric-label">Chain Length:</span>
                <span className="metric-value">{dreamStatus?.chain_length || 0}</span>
              </div>
              <div className="metric">
                <span className="metric-label">Accounts:</span>
                <span className="metric-value">{dreamStatus?.account_count || 0}</span>
              </div>
              <div className="metric">
                <span className="metric-label">Pending Tx:</span>
                <span className="metric-value">{dreamStatus?.pending_transactions || 0}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="connection-arrow">
          <div className="arrow-line"></div>
          <div className="arrow-head"></div>
        </div>

        <div className="layer nexus-layer">
          <h2>NexusLayer</h2>
          <div className="layer-description">
            <p>Bridge Layer for communication, verification, and security isolation</p>
          </div>
          <div className="layer-status">
            <div className={`status-indicator ${nexusStatus?.status === 'operational' ? 'operational' : 'error'}`}>
              {nexusStatus?.status === 'operational' ? 'ONLINE' : 'OFFLINE'}
            </div>
            <div className="layer-metrics">
              <div className="metric">
                <span className="metric-label">Bridges:</span>
                <span className="metric-value">{Object.keys(nexusStatus?.bridges || {}).length}</span>
              </div>
              <div className="metric">
                <span className="metric-label">Security Zones:</span>
                <span className="metric-value">{nexusStatus?.security_zones?.count || 0}</span>
              </div>
              <div className="metric">
                <span className="metric-label">Isolated Zones:</span>
                <span className="metric-value">{nexusStatus?.security_zones?.isolated || 0}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="connection-arrow">
          <div className="arrow-line"></div>
          <div className="arrow-head"></div>
        </div>

        <div className="layer genesis-layer">
          <h2>GenesisChain</h2>
          <div className="layer-description">
            <p>Foundation Layer with quantum-resistant security and consensus</p>
          </div>
          <div className="layer-status">
            <div className={`status-indicator ${genesisStatus?.status === 'operational' ? 'operational' : 'error'}`}>
              {genesisStatus?.status === 'operational' ? 'ONLINE' : 'OFFLINE'}
            </div>
            <div className="layer-metrics">
              <div className="metric">
                <span className="metric-label">Chain Length:</span>
                <span className="metric-value">{genesisStatus?.chain_length || 0}</span>
              </div>
              <div className="metric">
                <span className="metric-label">Security:</span>
                <span className="metric-value">{genesisStatus?.security_level || 'STANDARD'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="cross-layer-metrics">
        <h2>Cross-Layer System Status</h2>
        <div className={`system-status ${crossLayerStatus?.overall_status === 'operational' ? 'operational' : 'error'}`}>
          {crossLayerStatus?.overall_status === 'operational' ? 'SYSTEM OPERATIONAL' : 'SYSTEM ERROR'}
        </div>
        <div className="timestamp">
          Last Updated: {crossLayerStatus ? new Date(crossLayerStatus.timestamp * 1000).toLocaleString() : 'Unknown'}
        </div>
      </div>

      <div className="architecture-features">
        <h2>Key Features</h2>
        <div className="features-grid">
          <div className="feature">
            <h3>Quantum Resistance</h3>
            <p>Secure against quantum computing attacks with post-quantum cryptography</p>
          </div>
          <div className="feature">
            <h3>Security Bulkheads</h3>
            <p>Isolation mechanisms to contain security breaches and protect critical components</p>
          </div>
          <div className="feature">
            <h3>Multi-Layer Verification</h3>
            <p>Defense-in-depth with validation across all three blockchain layers</p>
          </div>
          <div className="feature">
            <h3>Circuit Breakers</h3>
            <p>Automatic protection systems that can quickly respond to potential threats</p>
          </div>
          <div className="feature">
            <h3>Adaptive Security</h3>
            <p>Security levels that adjust based on threat environment and requirements</p>
          </div>
          <div className="feature">
            <h3>Scalable Architecture</h3>
            <p>Each layer can be optimized independently for its specific purpose</p>
          </div>
        </div>
      </div>

      <div className="refresh-controls">
        <button onClick={fetchStatuses} className="refresh-button">
          Refresh Architecture Status
        </button>
      </div>
    </div>
  );
}

export default ThreeLayerArchitecture;