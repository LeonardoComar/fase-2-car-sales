"""
Caso de uso para criação de mensagem - Application Layer

Implementa a lógica de aplicação para criar uma nova mensagem.
Aplicando Clean Architecture e princípios SOLID.
"""

from uuid import UUID
from typing import Optional

from src.domain.entities.message import Message
from src.domain.ports.message_repository import MessageRepository
from src.application.dtos.message_dto import MessageCreateDto, MessageResponseDto


class CreateMessageUseCase:
    """
    Caso de uso para criar uma nova mensagem.
    
    Aplicando princípios SOLID:
    - SRP: Responsável apenas pela criação de mensagens
    - OCP: Extensível para novas validações
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
    
    async def execute(self, message_data: MessageCreateDto) -> MessageResponseDto:
        """
        Executa a criação de uma nova mensagem.
        
        Args:
            message_data: Dados da mensagem a ser criada
            
        Returns:
            MessageResponseDto: Dados da mensagem criada
            
        Raises:
            ValueError: Se dados inválidos
            Exception: Se erro na persistência
        """
        # Criar entidade de domínio
        message = Message.create_message(
            name=message_data.name,
            email=message_data.email,
            message=message_data.message,
            vehicle_id=message_data.vehicle_id,
            phone=message_data.phone
        )
        
        # Persistir mensagem
        saved_message = await self._message_repository.save(message)
        
        # Converter para DTO de resposta
        return self._to_response_dto(saved_message)
    
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
