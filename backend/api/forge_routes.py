from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import uuid
from enum import Enum

# Import forge components
from forge.core import QuantumForge, EnergyMonitor
from forge.assets import AssetForge, AssetType
from forge.quantum_link import QuantumLinkManager, LinkType, LinkStatus, LinkProtocol

# Create router
forge_router = APIRouter(prefix="/api/forge", tags=["forge"])

# Models for request/response
class EnergyDistributionModel(BaseModel):
    layer_distribution: Dict[str, float] = Field(..., description="Energy distribution across layers")

class CreateAssetModel(BaseModel):
    asset_type: str = Field(..., description="Type of asset to create")
    name: str = Field(..., description="Name of the asset")
    description: Optional[str] = Field(None, description="Asset description")
    metadata: Dict[str, Any] = Field({}, description="Additional metadata")
    initial_value: float = Field(0.0, description="Initial asset value")

class CreateLinkModel(BaseModel):
    source_system: str = Field(..., description="Source system")
    target_system: str = Field(..., description="Target system")
    link_type: str = Field(..., description="Type of link")
    bandwidth: float = Field(100.0, description="Link bandwidth")

class SendMessageModel(BaseModel):
    message_type: str = Field(..., description="Type of message")
    payload: Dict[str, Any] = Field(..., description="Message payload")

class TransferEnergyModel(BaseModel):
    amount: float = Field(..., description="Amount of energy to transfer")

# Global instances of our components
# In a real-world application, these would be properly managed with dependency injection
# and database persistence instead of global variables
quantum_forge = QuantumForge()
asset_forge = AssetForge(quantum_forge.qrng)
energy_monitor = EnergyMonitor(quantum_forge)
quantum_link_manager = QuantumLinkManager(quantum_forge)

# Forge core endpoints
@forge_router.get("/status")
async def get_forge_status():
    """Get the current status of THE FORGE."""
    return quantum_forge.to_dict()

@forge_router.post("/energy/allocate")
async def allocate_energy(distribution: EnergyDistributionModel):
    """Allocate energy across blockchain layers."""
    success = quantum_forge.allocate_energy(distribution.layer_distribution)
    
    if not success:
        raise HTTPException(status_code=400, detail="Energy allocation failed")
    
    return quantum_forge.to_dict()

@forge_router.post("/energy/generate")
async def generate_energy(cycles: int = Query(1, description="Number of energy generation cycles to run")):
    """Generate new quantum energy in THE FORGE."""
    energy_generated = quantum_forge.generate_quantum_energy(cycles)
    
    if energy_generated <= 0:
        raise HTTPException(status_code=400, detail="Energy generation failed")
    
    return {
        "success": True,
        "energy_generated": energy_generated,
        "forge_status": quantum_forge.to_dict()
    }

@forge_router.get("/alerts")
async def get_forge_alerts(limit: int = Query(10, description="Maximum number of alerts to return")):
    """Get recent alerts from THE FORGE."""
    return quantum_forge.get_alerts(limit)

@forge_router.get("/statistics")
async def get_energy_statistics():
    """Get energy statistics from THE FORGE."""
    return quantum_forge.get_energy_statistics()

@forge_router.get("/monitor")
async def monitor_energy_levels():
    """Monitor energy levels across the system."""
    return energy_monitor.monitor_energy_levels()

@forge_router.get("/recommendations")
async def get_energy_recommendations():
    """Get energy optimization recommendations."""
    return energy_monitor.get_layer_recommendations()

# Asset forge endpoints
@forge_router.post("/assets/create")
async def create_asset(asset_data: CreateAssetModel):
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

@forge_router.get("/assets/{asset_id}")
async def get_asset(asset_id: str):
    """Get details of a specific asset."""
    asset = asset_forge.get_asset(asset_id)
    
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return asset

@forge_router.get("/assets")
async def list_assets(limit: int = Query(100, description="Maximum number of assets to return")):
    """List all assets in THE FORGE."""
    return asset_forge.list_assets(limit)

@forge_router.post("/assets/{asset_id}/transfer")
async def transfer_asset(
    asset_id: str,
    new_owner: str = Query(..., description="Address of the new owner")
):
    """Transfer an asset to a new owner."""
    success = asset_forge.transfer_asset(asset_id, new_owner)
    
    if not success:
        raise HTTPException(status_code=400, detail="Asset transfer failed")
    
    return asset_forge.get_asset(asset_id)

@forge_router.get("/assets/creator/{creator}")
async def get_assets_by_creator(creator: str):
    """Get all assets created by a specific creator."""
    return asset_forge.get_assets_by_creator(creator)

@forge_router.get("/assets/statistics")
async def get_asset_statistics():
    """Get statistics about assets in THE FORGE."""
    return asset_forge.get_asset_statistics()

# Quantum link endpoints
@forge_router.post("/links/create")
async def create_quantum_link(link_data: CreateLinkModel):
    """Create a new quantum link between two systems."""
    try:
        link_type = LinkType[link_data.link_type]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid link type: {link_data.link_type}")
    
    connection_id = quantum_forge.establish_quantum_link(
        source_system=link_data.source_system,
        target_system=link_data.target_system,
        link_type=link_type,
        bandwidth=link_data.bandwidth
    )
    
    if not connection_id:
        raise HTTPException(status_code=400, detail="Failed to establish quantum link")
    
    link = quantum_link_manager.get_link(connection_id)
    if not link:
        raise HTTPException(status_code=500, detail="Link created but not retrievable")
    
    return link.to_dict()

@forge_router.get("/links/{connection_id}")
async def get_quantum_link(connection_id: str):
    """Get details of a specific quantum link."""
    link = quantum_link_manager.get_link(connection_id)
    
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    return link.to_dict()

@forge_router.get("/links")
async def get_all_quantum_links():
    """Get all quantum links."""
    return [link.to_dict() for link in quantum_link_manager.get_all_links()]

@forge_router.post("/links/{connection_id}/message")
async def send_message(connection_id: str, message_data: SendMessageModel):
    """Send a message over a quantum link."""
    success, result = quantum_link_manager.send_message(
        connection_id=connection_id,
        message_type=message_data.message_type,
        payload=message_data.payload
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=result.get("error", "Message sending failed"))
    
    return result

@forge_router.post("/links/{connection_id}/energy")
async def transfer_energy(connection_id: str, transfer_data: TransferEnergyModel):
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

@forge_router.post("/links/{connection_id}/terminate")
async def terminate_link(
    connection_id: str,
    reason: str = Query("Manual termination", description="Reason for termination")
):
    """Terminate a quantum link."""
    success = quantum_link_manager.terminate_link(connection_id, reason)
    
    if not success:
        raise HTTPException(status_code=400, detail="Link termination failed")
    
    return {"success": True}

@forge_router.get("/report")
async def get_forge_report():
    """Get a comprehensive report on THE FORGE status."""
    forge_data = quantum_forge.to_dict()
    energy_stats = quantum_forge.get_energy_statistics()
    monitoring_data = energy_monitor.monitor_energy_levels()
    recommendations = energy_monitor.get_layer_recommendations()
    
    return {
        "forge_status": forge_data,
        "energy_statistics": energy_stats,
        "monitoring_data": monitoring_data,
        "recommendations": recommendations
    }