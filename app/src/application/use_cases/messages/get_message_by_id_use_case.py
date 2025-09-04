"""
Caso de uso para buscar mensagem por ID - Application Layer

Implementa a lógica de aplicação para buscar uma mensagem específica.
Aplicando Clean Architecture e princípios SOLID.
"""

from uuid import UUID
from typing import Optional

from src.domain.entities.message import Message
from src.domain.ports.message_repository import MessageRepository
from src.application.dtos.message_dto import MessageResponseDto


class GetMessageByIdUseCase:
    """
    Caso de uso para buscar mensagem por ID.
    
    Aplicando princípios SOLID:
    - SRP: Responsável apenas pela busca de mensagem por ID
    - OCP: Extensível para novas funcionalidades
    - LSP: Pode ser substituído por outras implementações
    - ISP: Interface coesa
    - DIP: Depende de abstrações (MessageRepository)
    """
    
    def __init__(self, message_repository: MessageRepository):
        """
        Inicializa o caso de uso.
        
        Args:
            message_repository: Repositório de mensagens
        """
        self._message_repository = message_repository
    
    async def execute(self, message_id: UUID) -> Optional[MessageResponseDto]:
        """
        Executa a busca de mensagem por ID.
        
        Args:
            message_id: ID da mensagem a ser buscada
            
        Returns:
            Optional[MessageResponseDto]: Dados da mensagem ou None se não encontrada
        """
        # Buscar mensagem no repositório
        message = await self._message_repository.find_by_id(message_id)
        
        if not message:
            return None
        
        # Converter para DTO de resposta
        return self._to_response_dto(message)
    
    def _to_response_dto(self, message: Message) -> MessageResponseDto:
        """Converte entidade para DTO de resposta."""
        return MessageResponseDto(
            id=message.id,
            responsible_id=message.responsible_id,
            vehicle_id=message.vehicle_id,
            name=message.name,
            email=message.email,
            phone=message.phone,
            message=message.message,
            status=message.status,
            service_start_time=message.service_start_time,
            service_duration_minutes=message.get_service_duration_minutes(),
            created_at=message.created_at,
            updated_at=message.updated_at,
            is_pending=message.is_pending(),
            is_in_service=message.is_in_service(),
            is_finished=message.is_finished(),
            is_cancelled=message.is_cancelled(),
            has_responsible=message.has_responsible(),
            has_vehicle=message.has_vehicle()
        )
