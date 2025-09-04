"""
DTOs (Data Transfer Objects) para VehicleImage - Application Layer

Definem os contratos de entrada e saída para operações com imagens de veículos.
Aplicando o padrão DTO para desacoplar a API das entidades de domínio.

Aplicando princípios SOLID:
- SRP: Cada DTO tem uma responsabilidade específica
- OCP: Extensível para novos campos sem quebrar existentes
- LSP: DTOs podem ser substituídos sem afetar o comportamento
- ISP: Interfaces específicas para cada operação
- DIP: Não dependem de implementações concretas
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
import os


class VehicleImageCreateDto(BaseModel):
    """
    DTO para criação de imagem de veículo.
    
    Contém apenas os campos necessários para criar uma nova imagem,
    aplicando validações de negócio.
    """
    
    vehicle_id: UUID = Field(
        ...,
        description="ID do veículo"
    )
    filename: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Nome do arquivo da imagem"
    )
    path: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Caminho do arquivo no storage"
    )
    position: int = Field(
        1,
        ge=1,
        le=99,
        description="Posição da imagem na galeria"
    )
    is_primary: bool = Field(
        False,
        description="Se é a imagem principal do veículo"
    )
    file_size: Optional[int] = Field(
        None,
        ge=0,
        description="Tamanho do arquivo em bytes"
    )
    width: Optional[int] = Field(
        None,
        ge=1,
        description="Largura da imagem em pixels"
    )
    height: Optional[int] = Field(
        None,
        ge=1,
        description="Altura da imagem em pixels"
    )
    mime_type: Optional[str] = Field(
        None,
        max_length=100,
        description="Tipo MIME do arquivo"
    )
    
    @field_validator('filename')
    @classmethod
    def validate_filename(cls, v: str) -> str:
        """Valida o nome do arquivo."""
        v = v.strip()
        if not v:
            raise ValueError('Nome do arquivo não pode estar vazio')
        
        # Verificar extensão
        extension = os.path.splitext(v)[1].lower()
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
        
        if not extension:
            raise ValueError('Arquivo deve ter uma extensão')
        
        if extension not in allowed_extensions:
            allowed = ', '.join(allowed_extensions)
            raise ValueError(f'Extensão não permitida. Extensões válidas: {allowed}')
        
        # Verificar caracteres válidos
        import re
        if not re.match(r'^[a-zA-Z0-9._-]+$', v):
            raise ValueError('Nome do arquivo contém caracteres inválidos')
        
        return v
    
    @field_validator('path')
    @classmethod
    def validate_path(cls, v: str) -> str:
        """Valida o caminho do arquivo."""
        v = v.strip()
        if not v:
            raise ValueError('Caminho do arquivo não pode estar vazio')
        
        # Normalizar separadores
        v = v.replace('\\', '/')
        
        return v
    
    @field_validator('file_size')
    @classmethod
    def validate_file_size(cls, v: Optional[int]) -> Optional[int]:
        """Valida o tamanho do arquivo."""
        if v is not None:
            max_size = 10 * 1024 * 1024  # 10MB
            if v > max_size:
                raise ValueError(f'Arquivo muito grande. Máximo: {max_size / (1024*1024):.1f}MB')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "vehicle_id": "123e4567-e89b-12d3-a456-426614174000",
                "filename": "carro_frontal.jpg",
                "path": "/uploads/vehicles/123e4567-e89b-12d3-a456-426614174000/carro_frontal.jpg",
                "position": 1,
                "is_primary": True,
                "file_size": 2048576,
                "width": 1920,
                "height": 1080,
                "mime_type": "image/jpeg"
            }
        }


class VehicleImageUpdateDto(BaseModel):
    """
    DTO para atualização de imagem de veículo.
    
    Permite atualizar posição e status de imagem principal.
    """
    
    position: Optional[int] = Field(
        None,
        ge=1,
        le=99,
        description="Nova posição da imagem"
    )
    is_primary: Optional[bool] = Field(
        None,
        description="Se é a imagem principal"
    )
    thumbnail_path: Optional[str] = Field(
        None,
        max_length=500,
        description="Caminho da miniatura"
    )
    
    @field_validator('thumbnail_path')
    @classmethod
    def validate_thumbnail_path(cls, v: Optional[str]) -> Optional[str]:
        """Valida o caminho da miniatura."""
        if v is not None:
            v = v.strip()
            if v:
                # Normalizar separadores
                v = v.replace('\\', '/')
            else:
                v = None
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "position": 2,
                "is_primary": False,
                "thumbnail_path": "/uploads/thumbnails/123e4567-e89b-12d3-a456-426614174000/carro_frontal_thumb.jpg"
            }
        }


class VehicleImageReorderDto(BaseModel):
    """
    DTO para reordenação de imagens.
    """
    
    image_positions: Dict[UUID, int] = Field(
        ...,
        description="Mapeamento de ID da imagem para nova posição"
    )
    
    @field_validator('image_positions')
    @classmethod
    def validate_image_positions(cls, v: Dict[UUID, int]) -> Dict[UUID, int]:
        """Valida as posições das imagens."""
        if not v:
            raise ValueError('Deve haver pelo menos uma imagem para reordenar')
        
        positions = list(v.values())
        
        # Verificar se posições são válidas
        for pos in positions:
            if not isinstance(pos, int) or pos < 1 or pos > 99:
                raise ValueError('Posições devem ser números entre 1 e 99')
        
        # Verificar se não há posições duplicadas
        if len(positions) != len(set(positions)):
            raise ValueError('Não pode haver posições duplicadas')
        
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_positions": {
                    "123e4567-e89b-12d3-a456-426614174001": 1,
                    "123e4567-e89b-12d3-a456-426614174002": 2,
                    "123e4567-e89b-12d3-a456-426614174003": 3
                }
            }
        }


class VehicleImageResponseDto(BaseModel):
    """
    DTO para resposta com dados da imagem de veículo.
    
    Representa a imagem completa com todos os campos
    para retorno nas APIs.
    """
    
    id: UUID
    vehicle_id: UUID
    filename: str
    path: str
    thumbnail_path: Optional[str]
    position: int
    is_primary: bool
    file_size: Optional[int]
    width: Optional[int]
    height: Optional[int]
    mime_type: Optional[str]
    uploaded_at: datetime
    updated_at: datetime
    
    # Campos computados
    file_extension: str
    file_size_mb: Optional[float]
    aspect_ratio: Optional[float]
    is_landscape: Optional[bool]
    is_portrait: Optional[bool]
    is_square: Optional[bool]
    has_thumbnail: bool
    display_name: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "vehicle_id": "123e4567-e89b-12d3-a456-426614174001",
                "filename": "carro_frontal.jpg",
                "path": "/uploads/vehicles/123e4567-e89b-12d3-a456-426614174001/carro_frontal.jpg",
                "thumbnail_path": "/uploads/thumbnails/123e4567-e89b-12d3-a456-426614174001/carro_frontal_thumb.jpg",
                "position": 1,
                "is_primary": True,
                "file_size": 2048576,
                "width": 1920,
                "height": 1080,
                "mime_type": "image/jpeg",
                "uploaded_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00",
                "file_extension": ".jpg",
                "file_size_mb": 2.0,
                "aspect_ratio": 1.78,
                "is_landscape": True,
                "is_portrait": False,
                "is_square": False,
                "has_thumbnail": True,
                "display_name": "Imagem Principal - Posição 1"
            }
        }


class VehicleImageSearchDto(BaseModel):
    """
    DTO para busca de imagens com filtros.
    """
    
    vehicle_id: Optional[UUID] = Field(
        None,
        description="Filtrar por veículo"
    )
    is_primary: Optional[bool] = Field(
        None,
        description="Filtrar por imagem principal"
    )
    position: Optional[int] = Field(
        None,
        ge=1,
        le=99,
        description="Filtrar por posição específica"
    )
    position_range_start: Optional[int] = Field(
        None,
        ge=1,
        le=99,
        description="Início do range de posições"
    )
    position_range_end: Optional[int] = Field(
        None,
        ge=1,
        le=99,
        description="Fim do range de posições"
    )
    has_thumbnail: Optional[bool] = Field(
        None,
        description="Filtrar por ter miniatura"
    )
    min_file_size: Optional[int] = Field(
        None,
        ge=0,
        description="Tamanho mínimo do arquivo em bytes"
    )
    max_file_size: Optional[int] = Field(
        None,
        ge=0,
        description="Tamanho máximo do arquivo em bytes"
    )
    min_width: Optional[int] = Field(
        None,
        ge=1,
        description="Largura mínima em pixels"
    )
    min_height: Optional[int] = Field(
        None,
        ge=1,
        description="Altura mínima em pixels"
    )
    orientation: Optional[str] = Field(
        None,
        description="Orientação (landscape, portrait, square)"
    )
    order_by: Optional[str] = Field(
        "position",
        description="Campo para ordenação"
    )
    order_direction: Optional[str] = Field(
        "asc",
        description="Direção da ordenação (asc/desc)"
    )
    skip: Optional[int] = Field(
        0,
        ge=0,
        description="Número de registros a pular"
    )
    limit: Optional[int] = Field(
        50,
        ge=1,
        le=100,
        description="Limite de registros"
    )
    
    @field_validator('orientation')
    @classmethod
    def validate_orientation(cls, v: Optional[str]) -> Optional[str]:
        """Valida a orientação."""
        if not v:
            return None
        
        valid_orientations = ['landscape', 'portrait', 'square']
        v = v.lower()
        
        if v not in valid_orientations:
            raise ValueError(f'Orientação deve ser uma de: {", ".join(valid_orientations)}')
        
        return v
    
    @field_validator('order_by')
    @classmethod
    def validate_order_by(cls, v: Optional[str]) -> Optional[str]:
        """Valida o campo de ordenação."""
        if not v:
            return "position"
        
        valid_fields = [
            "position", "uploaded_at", "updated_at", "filename", 
            "file_size", "width", "height"
        ]
        
        if v not in valid_fields:
            raise ValueError(f'order_by deve ser um de: {", ".join(valid_fields)}')
        
        return v
    
    @field_validator('order_direction')
    @classmethod
    def validate_order_direction(cls, v: Optional[str]) -> Optional[str]:
        """Valida a direção da ordenação."""
        if not v:
            return "asc"
        
        if v.lower() not in ["asc", "desc"]:
            raise ValueError('order_direction deve ser "asc" ou "desc"')
        
        return v.lower()
    
    class Config:
        json_schema_extra = {
            "example": {
                "vehicle_id": "123e4567-e89b-12d3-a456-426614174000",
                "is_primary": True,
                "orientation": "landscape",
                "order_by": "position",
                "order_direction": "asc",
                "skip": 0,
                "limit": 10
            }
        }


class VehicleGalleryDto(BaseModel):
    """
    DTO para galeria completa de um veículo.
    """
    
    vehicle_id: UUID
    total_images: int
    primary_image: Optional[VehicleImageResponseDto]
    images: List[VehicleImageResponseDto]
    gallery_info: Dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "vehicle_id": "123e4567-e89b-12d3-a456-426614174000",
                "total_images": 5,
                "primary_image": {
                    "id": "123e4567-e89b-12d3-a456-426614174001",
                    "filename": "carro_frontal.jpg",
                    "position": 1,
                    "is_primary": True
                },
                "images": [],
                "gallery_info": {
                    "total_size_mb": 12.5,
                    "average_size_mb": 2.5,
                    "orientations": {
                        "landscape": 4,
                        "portrait": 1,
                        "square": 0
                    }
                }
            }
        }


class VehicleImageStatisticsDto(BaseModel):
    """
    DTO para estatísticas de imagens.
    """
    
    total_images: int
    total_size_mb: float
    average_size_mb: float
    vehicles_with_images: int
    vehicles_without_images: int
    vehicles_without_primary: int
    images_without_thumbnails: int
    large_images_count: int
    orphaned_images_count: int
    
    # Distribuições
    images_by_format: Dict[str, int]
    images_by_orientation: Dict[str, int]
    size_distribution: Dict[str, int]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_images": 1250,
                "total_size_mb": 2850.5,
                "average_size_mb": 2.28,
                "vehicles_with_images": 320,
                "vehicles_without_images": 15,
                "vehicles_without_primary": 8,
                "images_without_thumbnails": 45,
                "large_images_count": 12,
                "orphaned_images_count": 3,
                "images_by_format": {
                    ".jpg": 980,
                    ".png": 200,
                    ".webp": 70
                },
                "images_by_orientation": {
                    "landscape": 850,
                    "portrait": 300,
                    "square": 100
                },
                "size_distribution": {
                    "< 1MB": 400,
                    "1-3MB": 650,
                    "3-5MB": 180,
                    "> 5MB": 20
                }
            }
        }
