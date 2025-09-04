"""
DTOs (Data Transfer Objects) para Message - Application Layer

Definem os contratos de entrada e saída para operações com mensagens.
Aplicando o padrão DTO para desacoplar a API das entidades de domínio.

Aplicando princípios SOLID:
- SRP: Cada DTO tem uma responsabilidade específica
- OCP: Extensível para novos campos sem quebrar existentes
- LSP: DTOs podem ser substituídos sem afetar o comportamento
- ISP: Interfaces específicas para cada operação
- DIP: Não dependem de implementações concretas
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, field_validator
import re


class MessageCreateDto(BaseModel):
    """
    DTO para criação de mensagem.
    
    Contém apenas os campos necessários para criar uma nova mensagem,
    aplicando validações de negócio.
    """
    
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=100,
        description="Nome do interessado"
    )
    email: EmailStr = Field(
        ...,
        max_length=100,
        description="Email do interessado"
    )
    message: str = Field(
        ..., 
        min_length=10, 
        max_length=5000,
        description="Mensagem/interesse do cliente"
    )
    phone: Optional[str] = Field(
        None,
        max_length=50,
        description="Telefone do interessado (formato brasileiro)"
    )
    vehicle_id: Optional[UUID] = Field(
        None,
        description="ID do veículo de interesse"
    )
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Valida o nome do interessado."""
        v = v.strip()
        if not v:
            raise ValueError('Nome não pode estar vazio')
        
        # Verificar se contém apenas letras, espaços e acentos
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', v):
            raise ValueError('Nome deve conter apenas letras e espaços')
        
        return v
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Valida o telefone brasileiro."""
        if not v:
            return None
        
        v = v.strip()
        if not v:
            return None
        
        # Padrão para telefone brasileiro: (11) 99999-9999 ou 11999999999
        phone_pattern = re.compile(r'^\(\d{2}\)\s\d{4,5}-\d{4}$|^\d{10,11}$')
        if not phone_pattern.match(v):
            raise ValueError('Formato de telefone inválido. Use (11) 99999-9999 ou 11999999999')
        
        return v
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        """Valida o conteúdo da mensagem."""
        v = v.strip()
        if not v:
            raise ValueError('Mensagem não pode estar vazia')
        
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "João Silva",
                "email": "joao.silva@email.com",
                "phone": "(11) 99999-9999",
                "message": "Tenho interesse no veículo anunciado. Gostaria de mais informações sobre financiamento.",
                "vehicle_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class MessageUpdateDto(BaseModel):
    """
    DTO para atualização de mensagem.
    
    Permite atualizar informações de contato e conteúdo da mensagem.
    Todos os campos são opcionais.
    """
    
    name: Optional[str] = Field(
        None,
        min_length=2, 
        max_length=100,
        description="Nome do interessado"
    )
    email: Optional[EmailStr] = Field(
        None,
        max_length=100,
        description="Email do interessado"
    )
    phone: Optional[str] = Field(
        None,
        max_length=50,
        description="Telefone do interessado"
    )
    message: Optional[str] = Field(
        None,
        min_length=10, 
        max_length=5000,
        description="Conteúdo da mensagem"
    )
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Valida o nome se fornecido."""
        if not v:
            return None
        
        v = v.strip()
        if not v:
            return None
        
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', v):
            raise ValueError('Nome deve conter apenas letras e espaços')
        
        return v
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Valida o telefone se fornecido."""
        if not v:
            return None
        
        v = v.strip()
        if not v:
            return None
        
        phone_pattern = re.compile(r'^\(\d{2}\)\s\d{4,5}-\d{4}$|^\d{10,11}$')
        if not phone_pattern.match(v):
            raise ValueError('Formato de telefone inválido. Use (11) 99999-9999 ou 11999999999')
        
        return v
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: Optional[str]) -> Optional[str]:
        """Valida a mensagem se fornecida."""
        if not v:
            return None
        
        v = v.strip()
        if not v:
            return None
        
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "João da Silva",
                "email": "joao.dasilva@email.com",
                "phone": "(11) 98888-8888",
                "message": "Atualização: Gostaria também de informações sobre seguro."
            }
        }


class MessageAssignDto(BaseModel):
    """
    DTO para atribuição de responsável.
    """
    
    responsible_id: UUID = Field(
        ...,
        description="ID do funcionário responsável"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "responsible_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class MessageStatusUpdateDto(BaseModel):
    """
    DTO para atualização de status de mensagem.
    """
    
    status: str = Field(
        ...,
        description="Novo status da mensagem"
    )
    responsible_id: Optional[UUID] = Field(
        None,
        description="ID do funcionário responsável (obrigatório para iniciar atendimento)"
    )
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Valida o status da mensagem."""
        valid_statuses = [
            "Pendente",
            "Contato iniciado", 
            "Finalizado",
            "Cancelado"
        ]
        
        if v not in valid_statuses:
            raise ValueError(f'Status deve ser um de: {", ".join(valid_statuses)}')
        
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "Contato iniciado",
                "responsible_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class MessageResponseDto(BaseModel):
    """
    DTO para resposta com dados da mensagem.
    
    Representa a mensagem completa com todos os campos
    para retorno nas APIs.
    """
    
    id: UUID
    responsible_id: Optional[UUID]
    vehicle_id: Optional[UUID]
    name: str
    email: str
    phone: Optional[str]
    message: str
    status: str
    service_start_time: Optional[datetime]
    service_duration_minutes: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    # Campos computados
    is_pending: bool
    is_in_service: bool
    is_finished: bool
    is_cancelled: bool
    has_responsible: bool
    has_vehicle: bool
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "responsible_id": "123e4567-e89b-12d3-a456-426614174001",
                "vehicle_id": "123e4567-e89b-12d3-a456-426614174002",
                "name": "João Silva",
                "email": "joao.silva@email.com",
                "phone": "(11) 99999-9999",
                "message": "Interesse no veículo anunciado",
                "status": "Contato iniciado",
                "service_start_time": "2024-01-15T10:30:00",
                "service_duration_minutes": 45,
                "created_at": "2024-01-15T09:15:00",
                "updated_at": "2024-01-15T10:30:00",
                "is_pending": False,
                "is_in_service": True,
                "is_finished": False,
                "is_cancelled": False,
                "has_responsible": True,
                "has_vehicle": True
            }
        }


class MessageSearchDto(BaseModel):
    """
    DTO para busca de mensagens com filtros.
    """
    
    status: Optional[str] = Field(
        None,
        description="Filtrar por status"
    )
    responsible_id: Optional[UUID] = Field(
        None,
        description="Filtrar por responsável"
    )
    vehicle_id: Optional[UUID] = Field(
        None,
        description="Filtrar por veículo"
    )
    email: Optional[str] = Field(
        None,
        description="Filtrar por email"
    )
    start_date: Optional[date] = Field(
        None,
        description="Data inicial para filtro"
    )
    end_date: Optional[date] = Field(
        None,
        description="Data final para filtro"
    )
    pending_only: Optional[bool] = Field(
        None,
        description="Apenas mensagens pendentes"
    )
    unassigned_only: Optional[bool] = Field(
        None,
        description="Apenas mensagens sem responsável"
    )
    overdue_hours: Optional[int] = Field(
        None,
        ge=1,
        description="Mensagens em atraso (horas)"
    )
    order_by: Optional[str] = Field(
        "created_at",
        description="Campo para ordenação"
    )
    order_direction: Optional[str] = Field(
        "desc",
        description="Direção da ordenação (asc/desc)"
    )
    skip: Optional[int] = Field(
        0,
        ge=0,
        description="Número de registros a pular (paginação)"
    )
    limit: Optional[int] = Field(
        50,
        ge=1,
        le=100,
        description="Limite de registros (paginação)"
    )
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Valida o status se fornecido."""
        if not v:
            return None
        
        valid_statuses = [
            "Pendente",
            "Contato iniciado", 
            "Finalizado",
            "Cancelado"
        ]
        
        if v not in valid_statuses:
            raise ValueError(f'Status deve ser um de: {", ".join(valid_statuses)}')
        
        return v
    
    @field_validator('order_by')
    @classmethod
    def validate_order_by(cls, v: Optional[str]) -> Optional[str]:
        """Valida o campo de ordenação."""
        if not v:
            return "created_at"
        
        valid_fields = [
            "created_at", "updated_at", "status", "name", "service_start_time"
        ]
        
        if v not in valid_fields:
            raise ValueError(f'order_by deve ser um de: {", ".join(valid_fields)}')
        
        return v
    
    @field_validator('order_direction')
    @classmethod
    def validate_order_direction(cls, v: Optional[str]) -> Optional[str]:
        """Valida a direção da ordenação."""
        if not v:
            return "desc"
        
        if v.lower() not in ["asc", "desc"]:
            raise ValueError('order_direction deve ser "asc" ou "desc"')
        
        return v.lower()
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "Pendente",
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "pending_only": True,
                "order_by": "created_at",
                "order_direction": "desc",
                "skip": 0,
                "limit": 20
            }
        }


class MessagesStatisticsDto(BaseModel):
    """
    DTO para estatísticas de mensagens.
    """
    
    total_messages: int
    pending_messages: int
    in_service_messages: int
    finished_messages: int
    cancelled_messages: int
    unassigned_messages: int
    
    # Estatísticas de tempo
    average_response_time_hours: Optional[float]
    average_service_time_minutes: Optional[float]
    
    # Distribuição por período
    messages_by_status: Dict[str, int]
    messages_by_day: Dict[str, int]
    
    # Performance
    top_performers: List[Dict[str, Any]]
    vehicles_with_most_interest: List[Dict[str, Any]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_messages": 150,
                "pending_messages": 25,
                "in_service_messages": 8,
                "finished_messages": 110,
                "cancelled_messages": 7,
                "unassigned_messages": 15,
                "average_response_time_hours": 2.5,
                "average_service_time_minutes": 35.0,
                "messages_by_status": {
                    "Pendente": 25,
                    "Contato iniciado": 8,
                    "Finalizado": 110,
                    "Cancelado": 7
                },
                "messages_by_day": {
                    "2024-01-15": 12,
                    "2024-01-16": 8,
                    "2024-01-17": 15
                },
                "top_performers": [
                    {
                        "employee_id": "123e4567-e89b-12d3-a456-426614174000",
                        "messages_handled": 25,
                        "average_service_time": 30.5
                    }
                ],
                "vehicles_with_most_interest": [
                    {
                        "vehicle_id": "123e4567-e89b-12d3-a456-426614174002",
                        "interest_count": 15,
                        "conversion_rate": 0.75
                    }
                ]
            }
        }
