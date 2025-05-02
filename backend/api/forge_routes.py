from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import uuid
from enum import Enum

# Import forge components
from forge.core import ForgeCore, EnergyDistributionRequest
from forge.assets import AssetForge, AssetType
from forge.quantum_link import QuantumLinkManager, LinkType, LinkStatus, LinkProtocol

# Create router
forge_router = APIRouter(prefix="/api/forge", tags=["forge"])

# Models for request/response
class ForgeStatusResponse(BaseModel):
    forge_id: str
    current_energy: float
    max_energy: float
    stability: float
    efficiency: float
    active: bool
    uptime: float
    layer_distribution: Dict[str, float]
    layer_recommendations: Dict[str, float]
    alert_count: int
    latest_alerts: List[Dict[str, Any]]
    status_message: str

class EnergyDistributionModel(BaseModel):
    layer_distribution: Dict[str, float] = Field(..., description="Energy distribution across layers")

class CreateAssetModel(BaseModel):
    asset_type: str = Field(..., description="Type of asset to create")
    name: str = Field(..., description="Name of the asset")
    description: str = Field(None, description="Asset description")
    metadata: Dict[str, Any] = Field({}, description="Additional metadata")
    initial_value: float = Field(0.0, description="Initial asset value")

class AssetResponse(BaseModel):
    asset_id: str
    asset_type: str
    name: str
    description: Optional[str]
    creator: str
    owner: str
    created_at: float
    value: float
    metadata: Dict[str, Any]
    quantum_signature: str
    transaction_history: List[Dict[str, Any]]

class CreateLinkModel(BaseModel):
    source_system: str = Field(..., description="Source system")
    target_system: str = Field(..., description="Target system")
    link_type: str = Field(..., description="Type of link")
    bandwidth: float = Field(100.0, description="Link bandwidth")

class LinkResponse(BaseModel):
    connection_id: str
    source_system: str
    target_system: str
    link_type: str
    link_protocol: str
    status: str
    bandwidth: float
    stability: float
    latency: float
    created_at: float
    last_activity: float
    packet_count: int
    error_count: int
    transferred_data: float
    energy_transferred: float
    quantum_metrics: Dict[str, float]
    age: float

class SendMessageModel(BaseModel):
    message_type: str = Field(..., description="Type of message")
    payload: Dict[str, Any] = Field(..., description="Message payload")

class TransferEnergyModel(BaseModel):
    amount: float = Field(..., description="Amount of energy to transfer")

# Dependency to get ForgeCore instance
def get_forge_core():
    # In a real application, this would likely be a singleton or retrieved from a database
    # For now, we'll create a new instance each time
    return ForgeCore()

# Dependency to get AssetForge instance
def get_asset_forge(forge_core: ForgeCore = Depends(get_forge_core)):
    return AssetForge(forge_core.qrng)

# Dependency to get QuantumLinkManager instance
def get_quantum_link_manager(forge_core: ForgeCore = Depends(get_forge_core)):
    return QuantumLinkManager(forge_core)

# Forge core endpoints
@forge_router.get("/status", response_model=ForgeStatusResponse)
async def get_forge_status(forge_core: ForgeCore = Depends(get_forge_core)):
    """Get the current status of THE FORGE."""
    status = forge_core.get_status()
    return status

@forge_router.post("/energy/distribute", response_model=ForgeStatusResponse)
async def distribute_energy(
    distribution: EnergyDistributionModel,
    forge_core: ForgeCore = Depends(get_forge_core)
):
    """Distribute energy across blockchain layers."""
    request = EnergyDistributionRequest(distribution.layer_distribution)
    success = forge_core.distribute_energy(request)
    
    if not success:
        raise HTTPException(status_code=400, detail="Energy distribution failed")
    
    return forge_core.get_status()

@forge_router.post("/energy/generate", response_model=ForgeStatusResponse)
async def generate_energy(
    amount: float = Query(..., description="Amount of energy to generate"),
    forge_core: ForgeCore = Depends(get_forge_core)
):
    """Generate new energy in THE FORGE."""
    success = forge_core.generate_energy(amount)
    
    if not success:
        raise HTTPException(status_code=400, detail="Energy generation failed")
    
    return forge_core.get_status()

@forge_router.get("/alerts", response_model=List[Dict[str, Any]])
async def get_forge_alerts(
    limit: int = Query(10, description="Maximum number of alerts to return"),
    forge_core: ForgeCore = Depends(get_forge_core)
):
    """Get recent alerts from THE FORGE."""
    return forge_core.get_alerts(limit)

# Asset forge endpoints
@forge_router.post("/assets/create", response_model=AssetResponse)
async def create_asset(
    asset_data: CreateAssetModel,
    asset_forge: AssetForge = Depends(get_asset_forge)
):
    """Create a new quantum asset."""
    try:
        asset_type = AssetType[asset_data.asset_type]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid asset type: {asset_data.asset_type}")
    
    # Create the asset
    asset = asset_forge.create_asset(
        asset_type=asset_type,
        name=asset_data.name,
        description=asset_data.description,
        metadata=asset_data.metadata,
        initial_value=asset_data.initial_value
    )
    
    return asset_forge.get_asset(asset.asset_id)

@forge_router.get("/assets/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: str,
    asset_forge: AssetForge = Depends(get_asset_forge)
):
    """Get details of a specific asset."""
    asset = asset_forge.get_asset(asset_id)
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return asset

@forge_router.get("/assets", response_model=List[AssetResponse])
async def list_assets(
    limit: int = Query(100, description="Maximum number of assets to return"),
    asset_forge: AssetForge = Depends(get_asset_forge)
):
    """List all assets in THE FORGE."""
    return asset_forge.list_assets(limit)

@forge_router.post("/assets/{asset_id}/transfer", response_model=AssetResponse)
async def transfer_asset(
    asset_id: str,
    new_owner: str = Query(..., description="Address of the new owner"),
    asset_forge: AssetForge = Depends(get_asset_forge)
):
    """Transfer an asset to a new owner."""
    success = asset_forge.transfer_asset(asset_id, new_owner)
    
    if not success:
        raise HTTPException(status_code=400, detail="Asset transfer failed")
    
    return asset_forge.get_asset(asset_id)

# Quantum link endpoints
@forge_router.post("/links/create", response_model=LinkResponse)
async def create_link(
    link_data: CreateLinkModel,
    quantum_link_manager: QuantumLinkManager = Depends(get_quantum_link_manager)
):
    """Create a new quantum link between two systems."""
    try:
        link_type = LinkType[link_data.link_type]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid link type: {link_data.link_type}")
    
    success, result = quantum_link_manager.create_link(
        source_system=link_data.source_system,
        target_system=link_data.target_system,
        link_type=link_type,
        bandwidth=link_data.bandwidth
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=result)
    
    connection = quantum_link_manager.get_link(result)
    if not connection:
        raise HTTPException(status_code=500, detail="Link created but not retrievable")
    
    return connection.to_dict()

@forge_router.get("/links/{connection_id}", response_model=LinkResponse)
async def get_link(
    connection_id: str,
    quantum_link_manager: QuantumLinkManager = Depends(get_quantum_link_manager)
):
    """Get details of a specific quantum link."""
    connection = quantum_link_manager.get_link(connection_id)
    
    if not connection:
        raise HTTPException(status_code=404, detail="Link not found")
    
    return connection.to_dict()

@forge_router.get("/links/system/{system_name}", response_model=List[LinkResponse])
async def get_system_links(
    system_name: str,
    quantum_link_manager: QuantumLinkManager = Depends(get_quantum_link_manager)
):
    """Get all links for a specific system."""
    return quantum_link_manager.get_system_links(system_name)

@forge_router.post("/links/{connection_id}/message", response_model=Dict[str, Any])
async def send_message(
    connection_id: str,
    message_data: SendMessageModel,
    quantum_link_manager: QuantumLinkManager = Depends(get_quantum_link_manager)
):
    """Send a message over a quantum link."""
    success, result = quantum_link_manager.send_message(
        connection_id=connection_id,
        message_type=message_data.message_type,
        payload=message_data.payload
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=result.get("error", "Message sending failed"))
    
    return result

@forge_router.post("/links/{connection_id}/energy", response_model=Dict[str, Any])
async def transfer_energy(
    connection_id: str,
    transfer_data: TransferEnergyModel,
    quantum_link_manager: QuantumLinkManager = Depends(get_quantum_link_manager)
):
    """Transfer energy over a quantum link."""
    success, amount = quantum_link_manager.transfer_energy(
        connection_id=connection_id,
        amount=transfer_data.amount
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Energy transfer failed")
    
    return {
        "success": success,
        "amount_transferred": amount
    }

@forge_router.post("/links/{connection_id}/terminate", response_model=Dict[str, bool])
async def terminate_link(
    connection_id: str,
    reason: str = Query("Manual termination", description="Reason for termination"),
    quantum_link_manager: QuantumLinkManager = Depends(get_quantum_link_manager)
):
    """Terminate a quantum link."""
    success = quantum_link_manager.terminate_link(connection_id, reason)
    
    if not success:
        raise HTTPException(status_code=400, detail="Link termination failed")
    
    return {"success": True}

@forge_router.post("/links/maintain", response_model=Dict[str, Any])
async def maintain_links(
    quantum_link_manager: QuantumLinkManager = Depends(get_quantum_link_manager)
):
    """Perform maintenance on all quantum links."""
    result = quantum_link_manager.maintain_links()
    return result

@forge_router.get("/links/statistics", response_model=Dict[str, Any])
async def get_link_statistics(
    quantum_link_manager: QuantumLinkManager = Depends(get_quantum_link_manager)
):
    """Get statistics about quantum links."""
    return quantum_link_manager.get_link_statistics()

@forge_router.get("/links/history", response_model=List[Dict[str, Any]])
async def get_link_history(
    limit: int = Query(20, description="Maximum number of events to return"),
    quantum_link_manager: QuantumLinkManager = Depends(get_quantum_link_manager)
):
    """Get recent quantum link history."""
    return quantum_link_manager.get_recent_history(limit)