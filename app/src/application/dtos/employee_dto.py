from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from src.application.dtos.address_dto import AddressDto, AddressResponseDto


class CreateEmployeeDto(BaseModel):
    """
    DTO para requisição de criação de funcionário.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Nome do funcionário")
    email: EmailStr = Field(..., description="Email do funcionário")
    phone: Optional[str] = Field(None, max_length=50, description="Telefone do funcionário")
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF do funcionário")
    
    # Dados do endereço (opcional)
    street: Optional[str] = Field(None, max_length=100, description="Rua do endereço")
    city: Optional[str] = Field(None, max_length=100, description="Cidade do endereço")
    state: Optional[str] = Field(None, max_length=100, description="Estado do endereço")
    zip_code: Optional[str] = Field(None, max_length=20, description="CEP do endereço")
    country: Optional[str] = Field(None, max_length=100, description="País do endereço")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Maria Silva",
                "email": "maria.silva@empresa.com",
                "phone": "(11) 99999-9999",
                "cpf": "123.456.789-00",
                "street": "Rua das Empresas, 456",
                "city": "São Paulo",
                "state": "SP",
                "zip_code": "01234-567",
                "country": "Brasil"
            }
        }


class UpdateEmployeeDto(BaseModel):
    """
    DTO para requisição de atualização de funcionário.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nome do funcionário")
    email: Optional[EmailStr] = Field(None, description="Email do funcionário")
    phone: Optional[str] = Field(None, max_length=50, description="Telefone do funcionário")
    cpf: Optional[str] = Field(None, min_length=11, max_length=14, description="CPF do funcionário")
    status: Optional[str] = Field(None, description="Status do funcionário (Ativo/Inativo)")
    
    # Dados do endereço (opcional)
    street: Optional[str] = Field(None, max_length=100, description="Rua do endereço")
    city: Optional[str] = Field(None, max_length=100, description="Cidade do endereço")
    state: Optional[str] = Field(None, max_length=100, description="Estado do endereço")
    zip_code: Optional[str] = Field(None, max_length=20, description="CEP do endereço")
    country: Optional[str] = Field(None, max_length=100, description="País do endereço")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Maria Silva Santos",
                "email": "maria.santos@empresa.com",
                "phone": "(11) 88888-8888",
                "status": "Ativo",
                "street": "Rua das Empresas, 789",
                "city": "São Paulo",
                "state": "SP",
                "zip_code": "01234-567",
                "country": "Brasil"
            }
        }


class EmployeeResponseDto(BaseModel):
    """
    DTO para resposta da criação/consulta de funcionário.
    """
    id: int
    name: str
    email: str
    phone: Optional[str]
    cpf: str
    status: str
    address: Optional[AddressResponseDto] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Maria Silva",
                "email": "maria.silva@empresa.com",
                "phone": "(11) 99999-9999",
                "cpf": "123.456.789-00",
                "status": "Ativo",
                "address": {
                    "id": 1,
                    "street": "Rua das Empresas, 456",
                    "city": "São Paulo",
                    "state": "SP",
                    "zip_code": "01234-567",
                    "country": "Brasil",
                    "created_at": "2024-01-01T10:00:00",
                    "updated_at": "2024-01-01T10:00:00",
                    "full_address": "Rua das Empresas, 456, São Paulo - SP, 01234-567, Brasil"
                },
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00"
            }
        }


class EmployeeListDto(BaseModel):
    """
    DTO para resposta de um funcionário na listagem.
    """
    id: int
    name: str
    email: str
    phone: Optional[str]
    cpf: str
    status: str
    city: Optional[str] = None  # Cidade do endereço para facilitar a listagem

    class Config:
        from_attributes = True
