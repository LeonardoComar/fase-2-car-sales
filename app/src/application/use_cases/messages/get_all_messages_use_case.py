"""
Use Case para Listar Mensagens - Application Layer

Responsável por listar mensagens com filtros aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela listagem de mensagens
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para listagem
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from src.domain.entities.message import Message
from src.domain.ports.message_repository import MessageRepository
from src.application.dtos.message_dto import MessageFilters, MessageListResponse, MessageResponse


class GetAllMessagesUseCase:
    """
    Use Case para listagem de mensagens.
    
    Coordena a busca com filtros e paginação, aplicando regras de negócio.
    """
    
    def __init__(self, message_repository: MessageRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            message_repository: Repositório de mensagens
        """
        self._message_repository = message_repository
    
    async def execute(self, filters: MessageFilters) -> MessageListResponse:
        """
        Executa a listagem de mensagens com filtros.
        
        Args:
            filters: Filtros e parâmetros de paginação
            
        Returns:
            MessageListResponse: Lista de mensagens e metadados de paginação
            
        Raises:
            ValueError: Se parâmetros inválidos forem fornecidos
            Exception: Se houver erro na busca
        """
        # Validações
        if filters.page <= 0:
            raise ValueError("Número da página deve ser positivo")
        
        if filters.limit <= 0 or filters.limit > 100:
            raise ValueError("Limite deve ser entre 1 e 100")
        
        # Calcular offset
        offset = (filters.page - 1) * filters.limit
        
        # Extrair status como string se fornecido
        status_filter = filters.status.value if filters.status else None
        
        # Buscar mensagens
        messages = await self._message_repository.get_all_messages(
            limit=filters.limit,
            offset=offset,
            order_by_value=filters.order_by,
            order_direction=filters.order_direction,
            status=status_filter,
            responsible_id=filters.responsible_id,
            vehicle_id=filters.vehicle_id
        )
        
        # Contar total
        total = await self._message_repository.count_messages(
            status=status_filter,
            responsible_id=filters.responsible_id,
            vehicle_id=filters.vehicle_id
        )
        
        # Converter mensagens para DTOs
        message_responses = [
            MessageResponse(
                id=message.id,
                name=message.name,
                email=message.email,
                phone=message.phone,
                message=message.message,
                vehicle_id=message.vehicle_id,
                responsible_id=message.responsible_id,
                status=message.status,
                service_start_time=message.service_start_time,
                created_at=message.created_at,
                updated_at=message.updated_at
            )
            for message in messages
        ]
        
        # Calcular metadados de paginação
        total_pages = (total + filters.limit - 1) // filters.limit
        has_next = filters.page < total_pages
        has_previous = filters.page > 1
        
        return MessageListResponse(
            messages=message_responses,
            total=total,
            page=filters.page,
            limit=filters.limit,
            total_pages=total_pages,
            has_next=has_next,
            has_previous=has_previous
        )
