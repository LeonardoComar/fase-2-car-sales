"""
Caso de uso para atribuir responsável a mensagem - Application Layer

Implementa a lógica de aplicação para atribuir um funcionário responsável
por uma mensagem e gerenciar o status do atendimento.
"""

from uuid import UUID
from typing import Optional

from src.domain.entities.message import Message
from src.domain.ports.message_repository import MessageRepository
from src.application.dtos.message_dto import MessageAssignDto, MessageResponseDto


class AssignMessageUseCase:
    """
    Caso de uso para atribuir responsável a mensagem.
    
    Aplicando princípios SOLID:
    - SRP: Responsável apenas pela atribuição de mensagens
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
    
    async def execute(self, message_id: UUID, assign_data: MessageAssignDto) -> Optional[MessageResponseDto]:
        """
        Executa a atribuição de responsável a uma mensagem.
        
        Args:
            message_id: ID da mensagem
            assign_data: Dados de atribuição
            
        Returns:
            Optional[MessageResponseDto]: Dados da mensagem atualizada ou None se não encontrada
            
        Raises:
            ValueError: Se operação não permitida
            Exception: Se erro na persistência
        """
        # Buscar mensagem existente
        message = await self._message_repository.find_by_id(message_id)
        
        if not message:
            return None
        
        # Atribuir responsável
        message.assign_responsible(assign_data.responsible_id)
        
        # Persistir alterações
        updated_message = await self._message_repository.save(message)
        
        # Converter para DTO de resposta
        return self._to_response_dto(updated_message)
    
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
