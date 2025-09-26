from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from src.application.dtos.address_dto import AddressDto, AddressResponseDto


class CreateClientDto(BaseModel):
    """
    DTO para requisição de criação de cliente.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Nome do cliente")
    email: EmailStr = Field(..., description="Email do cliente")
    phone: Optional[str] = Field(None, max_length=50, description="Telefone do cliente")
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF do cliente")
    
    # Dados do endereço (opcional)
    street: Optional[str] = Field(None, max_length=100, description="Rua do endereço")
    city: Optional[str] = Field(None, max_length=100, description="Cidade do endereço")
    state: Optional[str] = Field(None, max_length=100, description="Estado do endereço")
    zip_code: Optional[str] = Field(None, max_length=20, description="CEP do endereço")
    country: Optional[str] = Field(None, max_length=100, description="País do endereço")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "João Silva",
                "email": "joao.silva@email.com",
                "phone": "(11) 99999-9999",
                "cpf": "123.456.789-00",
                "street": "Rua das Flores, 123",
                "city": "São Paulo",
                "state": "SP",
                "zip_code": "01234-567",
                "country": "Brasil"
            }
        }


class UpdateClientDto(BaseModel):
    """
    DTO para requisição de atualização de cliente.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nome do cliente")
    email: Optional[EmailStr] = Field(None, description="Email do cliente")
    phone: Optional[str] = Field(None, max_length=50, description="Telefone do cliente")
    cpf: Optional[str] = Field(None, min_length=11, max_length=14, description="CPF do cliente")
    
    # Dados do endereço (opcional)
    street: Optional[str] = Field(None, max_length=100, description="Rua do endereço")
    city: Optional[str] = Field(None, max_length=100, description="Cidade do endereço")
    state: Optional[str] = Field(None, max_length=100, description="Estado do endereço")
    zip_code: Optional[str] = Field(None, max_length=20, description="CEP do endereço")
    country: Optional[str] = Field(None, max_length=100, description="País do endereço")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "João Silva Santos",
                "email": "joao.santos@email.com",
                "phone": "(11) 88888-8888",
                "street": "Rua das Flores, 789",
                "city": "São Paulo",
                "state": "SP",
                "zip_code": "01234-567",
                "country": "Brasil"
            }
        }


class ClientResponseDto(BaseModel):
    """
    DTO para resposta da criação/consulta de cliente.
    """
    id: int
    name: str
    email: str
    phone: Optional[str]
    cpf: str
    address: Optional[AddressResponseDto] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "João Silva",
                "email": "joao.silva@email.com",
                "phone": "(11) 99999-9999",
                "cpf": "123.456.789-00",
                "address": {
                    "id": 1,
                    "street": "Rua das Flores, 123",
                    "city": "São Paulo",
                    "state": "SP",
                    "zip_code": "01234-567",
                    "country": "Brasil",
                    "full_address": "Rua das Flores, 123, São Paulo, SP, 01234-567, Brasil",
                    "created_at": "2024-01-01T10:00:00",
                    "updated_at": "2024-01-01T10:00:00"
                },
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00"
            }
        }


class ClientListDto(BaseModel):
    """
    DTO para resposta da listagem de clientes.
    """
    id: int
    name: str
    email: str
    phone: Optional[str]
    cpf: str
    city: Optional[str] = None  # Cidade do endereço para facilitar a listagem

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "João Silva",
                "email": "joao.silva@email.com",
                "phone": "(11) 99999-9999",
                "cpf": "123.456.789-00",
                "city": "São Paulo"
            }
        }
