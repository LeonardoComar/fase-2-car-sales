from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MessageStatus(str, Enum):
    """Enum para os status válidos de uma mensagem."""
    PENDENTE = "Pendente"
    CONTATO_INICIADO = "Contato iniciado"
    FINALIZADO = "Finalizado"
    CANCELADO = "Cancelado"


class CreateMessageRequest(BaseModel):
    """
    DTO para requisição de criação de mensagem.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Nome do remetente")
    email: EmailStr = Field(..., description="Email do remetente")
    phone: Optional[str] = Field(None, max_length=50, description="Telefone do remetente")
    message: str = Field(..., min_length=1, description="Conteúdo da mensagem")
    vehicle_id: Optional[int] = Field(None, gt=0, description="ID do veículo relacionado")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "João Silva",
                "email": "joao.silva@email.com",
                "phone": "(11) 99999-9999",
                "message": "Tenho interesse no veículo anunciado. Gostaria de mais informações sobre o preço e condições de pagamento.",
                "vehicle_id": 1
            }
        }


class StartServiceRequest(BaseModel):
    """
    DTO para requisição de início de atendimento.
    """
    responsible_id: int = Field(..., gt=0, description="ID do funcionário responsável")

    class Config:
        json_schema_extra = {
            "example": {
                "responsible_id": 1
            }
        }


class UpdateMessageStatusRequest(BaseModel):
    """
    DTO para requisição de atualização de status da mensagem.
    """
    status: MessageStatus = Field(..., description="Novo status da mensagem")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "Finalizado"
            }
        }


class MessageResponse(BaseModel):
    """
    DTO para resposta com dados da mensagem.
    """
    id: int
    name: str
    email: str
    phone: Optional[str]
    message: str
    vehicle_id: Optional[int]
    responsible_id: Optional[int]
    status: str
    service_start_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class MessageListResponse(BaseModel):
    """
    DTO para resposta de listagem de mensagens.
    """
    messages: List[MessageResponse]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_previous: bool

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {
                        "id": 1,
                        "name": "João Silva",
                        "email": "joao.silva@email.com",
                        "phone": "(11) 99999-9999",
                        "message": "Tenho interesse no veículo anunciado.",
                        "vehicle_id": 1,
                        "responsible_id": None,
                        "status": "Pendente",
                        "service_start_time": None,
                        "created_at": "2024-01-15T10:30:00",
                        "updated_at": "2024-01-15T10:30:00"
                    }
                ],
                "total": 1,
                "page": 1,
                "limit": 10,
                "total_pages": 1,
                "has_next": False,
                "has_previous": False
            }
        }


class MessageCreatedResponse(BaseModel):
    """
    DTO para resposta de mensagem criada.
    """
    id: int
    name: str
    email: str
    status: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "João Silva",
                "email": "joao.silva@email.com",
                "status": "Pendente",
                "message": "Tenho interesse no veículo anunciado.",
                "created_at": "2024-01-15T10:30:00"
            }
        }


class MessageFilters(BaseModel):
    """
    DTO para filtros de busca de mensagens.
    """
    status: Optional[MessageStatus] = Field(None, description="Filtrar por status")
    responsible_id: Optional[int] = Field(None, gt=0, description="Filtrar por responsável")
    vehicle_id: Optional[int] = Field(None, gt=0, description="Filtrar por veículo")
    page: int = Field(1, ge=1, description="Número da página")
    limit: int = Field(10, ge=1, le=100, description="Itens por página")
    order_by: Optional[str] = Field("created_at", description="Campo para ordenação")
    order_direction: Optional[str] = Field("desc", description="Direção da ordenação")

    @validator('order_by')
    def validate_order_by(cls, v):
        valid_fields = ["id", "name", "email", "status", "created_at", "updated_at", "service_start_time"]
        if v not in valid_fields:
            raise ValueError(f'Campo de ordenação deve ser um dos valores: {", ".join(valid_fields)}')
        return v

    @validator('order_direction')
    def validate_order_direction(cls, v):
        if v.lower() not in ["asc", "desc"]:
            raise ValueError('Direção da ordenação deve ser "asc" ou "desc"')
        return v.lower()

    class Config:
        json_schema_extra = {
            "example": {
                "status": "Pendente",
                "responsible_id": 1,
                "vehicle_id": 1,
                "page": 1,
                "limit": 10,
                "order_by": "created_at",
                "order_direction": "desc"
            }
        }
