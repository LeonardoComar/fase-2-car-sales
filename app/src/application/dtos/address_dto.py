"""
Address DTOs - Application Layer

DTOs p        schema_extra = {
            "example": {
                "id": 1,
                "street": "Rua das Empresas, 456",
                "city": "São Paulo",
                "state": "SP",
                "zip_code": "01234-567",
                "country": "Brasil",
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00",
                "full_address": "Rua das Empresas, 456, São Paulo - SP, 01234-567, Brasil"
            }
        }ncia de dados de endereços seguindo Clean Architecture
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AddressDto(BaseModel):
    """DTO para dados de endereço"""
    
    street: str = Field(..., min_length=5, max_length=200, description="Rua do endereço")
    city: str = Field(..., min_length=2, max_length=100, description="Cidade")
    state: str = Field(..., min_length=2, max_length=50, description="Estado")
    zip_code: str = Field(..., pattern=r'^\d{5}-?\d{3}$', description="CEP (formato: 12345-678)")
    country: str = Field(default="Brasil", min_length=2, max_length=50, description="País")
    
    class Config:
        schema_extra = {
            "example": {
                "street": "Rua das Flores, 123, Apto 45",
                "city": "São Paulo",
                "state": "SP",
                "zip_code": "01234-567",
                "country": "Brasil"
            }
        }


class AddressResponseDto(BaseModel):
    """DTO para resposta de endereço"""
    
    id: int
    street: str
    city: str
    state: str
    zip_code: str
    country: str
    created_at: Optional[str]
    updated_at: Optional[str]
    full_address: str
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "street": "Rua das Flores, 123, Apto 45",
                "city": "São Paulo",
                "state": "SP",
                "zip_code": "01234-567",
                "country": "Brasil",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00",
                "full_address": "Rua das Flores, 123, Apto 45, São Paulo - SP, 01234-567, Brasil"
            }
        }


class AddressCreateDto(BaseModel):
    """DTO para criação de endereço"""
    
    street: str = Field(..., min_length=5, max_length=200, description="Rua do endereço")
    city: str = Field(..., min_length=2, max_length=100, description="Cidade")
    state: str = Field(..., min_length=2, max_length=50, description="Estado")
    zip_code: str = Field(..., pattern=r'^\d{5}-?\d{3}$', description="CEP (formato: 12345-678)")
    country: str = Field(default="Brasil", min_length=2, max_length=50, description="País")
    
    class Config:
        schema_extra = {
            "example": {
                "street": "Rua das Flores, 123, Apto 45",
                "city": "São Paulo",
                "state": "SP",
                "zip_code": "01234-567",
                "country": "Brasil"
            }
        }


class AddressUpdateDto(BaseModel):
    """DTO para atualização de endereço"""
    
    street: Optional[str] = Field(None, min_length=5, max_length=200, description="Rua do endereço")
    city: Optional[str] = Field(None, min_length=2, max_length=100, description="Cidade")
    state: Optional[str] = Field(None, min_length=2, max_length=50, description="Estado")
    zip_code: Optional[str] = Field(None, pattern=r'^\d{5}-?\d{3}$', description="CEP (formato: 12345-678)")
    country: Optional[str] = Field(None, min_length=2, max_length=50, description="País")
    
    class Config:
        schema_extra = {
            "example": {
                "street": "Rua das Flores, 123, Apto 45",
                "city": "São Paulo",
                "state": "SP",
                "zip_code": "01234-567",
                "country": "Brasil"
            }
        }
