from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class VehicleImageCreateDTO(BaseModel):
    """DTO para criação de uma nova imagem de veículo."""
    
    vehicle_id: int = Field(..., description="ID do veículo", gt=0)
    filename: str = Field(..., description="Nome do arquivo da imagem", min_length=1)
    path: str = Field(..., description="Caminho do arquivo", min_length=1)
    thumbnail_path: Optional[str] = Field(None, description="Caminho da thumbnail")
    position: Optional[int] = Field(None, description="Posição da imagem", ge=1, le=10)
    is_primary: bool = Field(False, description="Se é a imagem principal")
    
    @validator('filename')
    def validate_filename(cls, v):
        if not v or not isinstance(v, str) or not v.strip():
            raise ValueError('Nome do arquivo não pode estar vazio')
        
        # Validar extensão
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        from pathlib import Path
        ext = Path(v).suffix.lower()
        if ext not in allowed_extensions:
            raise ValueError(f'Extensão {ext} não permitida. Use: {", ".join(allowed_extensions)}')
        
        return v.strip()
    
    @validator('path')
    def validate_path(cls, v):
        if not v or not isinstance(v, str) or not v.strip():
            raise ValueError('Caminho não pode estar vazio')
        return v.strip()

    class Config:
        schema_extra = {
            "example": {
                "vehicle_id": 1,
                "filename": "car_image.jpg",
                "path": "/uploads/vehicles/car_image.jpg",
                "thumbnail_path": "/uploads/vehicles/thumbnails/car_image_thumb.jpg",
                "position": 1,
                "is_primary": True
            }
        }


class VehicleImageUpdateDTO(BaseModel):
    """DTO para atualização de uma imagem de veículo."""
    
    position: Optional[int] = Field(None, description="Nova posição da imagem", ge=1, le=10)
    is_primary: Optional[bool] = Field(None, description="Se é a imagem principal")

    class Config:
        schema_extra = {
            "example": {
                "position": 2,
                "is_primary": False
            }
        }


class VehicleImageResponseDTO(BaseModel):
    """DTO para resposta de uma imagem de veículo."""
    
    id: int = Field(..., description="ID da imagem")
    vehicle_id: int = Field(..., description="ID do veículo")
    filename: str = Field(..., description="Nome do arquivo")
    path: str = Field(..., description="Caminho do arquivo")
    thumbnail_path: Optional[str] = Field(None, description="Caminho da thumbnail")
    url: str = Field(..., description="URL completa da imagem")
    thumbnail_url: Optional[str] = Field(None, description="URL completa da thumbnail")
    position: int = Field(..., description="Posição da imagem")
    is_primary: bool = Field(..., description="Se é a imagem principal")
    uploaded_at: datetime = Field(..., description="Data e hora do upload")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "vehicle_id": 1,
                "filename": "car_image.jpg",
                "path": "/uploads/vehicles/car_image.jpg",
                "thumbnail_path": "/uploads/vehicles/thumbnails/car_image_thumb.jpg",
                "position": 1,
                "is_primary": True,
                "uploaded_at": "2024-01-15T10:30:00"
            }
        }


class VehicleImageListResponseDTO(BaseModel):
    """DTO para resposta de lista de imagens de veículo."""
    
    vehicle_id: int = Field(..., description="ID do veículo")
    images: list[VehicleImageResponseDTO] = Field(..., description="Lista de imagens")
    total_images: int = Field(..., description="Total de imagens")
    primary_image: Optional[VehicleImageResponseDTO] = Field(None, description="Imagem principal")

    class Config:
        schema_extra = {
            "example": {
                "vehicle_id": 1,
                "images": [
                    {
                        "id": 1,
                        "vehicle_id": 1,
                        "filename": "car_image_1.jpg",
                        "path": "/uploads/vehicles/car_image_1.jpg",
                        "thumbnail_path": "/uploads/vehicles/thumbnails/car_image_1_thumb.jpg",
                        "position": 1,
                        "is_primary": True,
                        "uploaded_at": "2024-01-15T10:30:00"
                    }
                ],
                "total_images": 1,
                "primary_image": {
                    "id": 1,
                    "vehicle_id": 1,
                    "filename": "car_image_1.jpg",
                    "path": "/uploads/vehicles/car_image_1.jpg",
                    "thumbnail_path": "/uploads/vehicles/thumbnails/car_image_1_thumb.jpg",
                    "position": 1,
                    "is_primary": True,
                    "uploaded_at": "2024-01-15T10:30:00"
                }
            }
        }


class VehicleImageUploadResponseDTO(BaseModel):
    """DTO para resposta de upload de imagem."""
    
    success: bool = Field(..., description="Se o upload foi bem-sucedido")
    image: Optional[VehicleImageResponseDTO] = Field(None, description="Dados da imagem criada")
    message: str = Field(..., description="Mensagem de retorno")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "image": {
                    "id": 1,
                    "vehicle_id": 1,
                    "filename": "car_image.jpg",
                    "path": "/uploads/vehicles/car_image.jpg",
                    "thumbnail_path": "/uploads/vehicles/thumbnails/car_image_thumb.jpg",
                    "position": 1,
                    "is_primary": True,
                    "uploaded_at": "2024-01-15T10:30:00"
                },
                "message": "Imagem enviada com sucesso"
            }
        }
