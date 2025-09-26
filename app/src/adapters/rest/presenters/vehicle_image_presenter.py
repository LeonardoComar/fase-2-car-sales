"""Presenter para imagens de veículos."""

from typing import Optional
from src.application.dtos.vehicle_image_dto import VehicleImageResponseDTO
from src.domain.entities.vehicle_image import VehicleImage


class VehicleImagePresenter:
    """Presenter para respostas de imagens de veículos."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
    
    def to_response_dto(self, vehicle_image: VehicleImage) -> VehicleImageResponseDTO:
        """Converte uma entidade VehicleImage para DTO de resposta com URLs completas."""
        
        # Constrói as URLs completas
        url = f"{self.base_url}{vehicle_image.path}"
        thumbnail_url = f"{self.base_url}{vehicle_image.thumbnail_path}" if vehicle_image.thumbnail_path else None
        
        return VehicleImageResponseDTO(
            id=vehicle_image.id,
            vehicle_id=vehicle_image.vehicle_id,
            filename=vehicle_image.filename,
            path=vehicle_image.path,
            thumbnail_path=vehicle_image.thumbnail_path,
            url=url,
            thumbnail_url=thumbnail_url,
            position=vehicle_image.position,
            is_primary=vehicle_image.is_primary,
            uploaded_at=vehicle_image.uploaded_at
        )