"""
Caso de uso para listar mensagens - Application Layer

Implementa a lógica de aplicação para buscar mensagens com filtros.
Aplicando Clean Architecture e princípios SOLID.
"""

from typing import List

from src.domain.entities.message import Message
from src.domain.ports.message_repository import MessageRepository
from src.application.dtos.message_dto import MessageSearchDto, MessageResponseDto


class ListMessagesUseCase:
    """
    Caso de uso para listar mensagens com filtros.
    
    Aplicando princípios SOLID:
    - SRP: Responsável apenas pela listagem de mensagens
    - OCP: Extensível para novos filtros
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
    
    async def execute(self, search_params: MessageSearchDto) -> List[MessageResponseDto]:
        """
        Executa a busca de mensagens com filtros.
        
        Args:
            search_params: Parâmetros de busca e filtros
            
        Returns:
            List[MessageResponseDto]: Lista de mensagens encontradas
        """
        # Preparar critérios de busca
        criteria = self._prepare_search_criteria(search_params)
        
        # Buscar mensagens específicas se filtros especiais
        if search_params.pending_only:
            messages = await self._message_repository.find_pending_messages(**criteria)
        elif search_params.unassigned_only:
            messages = await self._message_repository.find_unassigned_messages(**criteria)
        elif search_params.overdue_hours:
            messages = await self._message_repository.find_overdue_messages(
                hours_threshold=search_params.overdue_hours,
                **criteria
            )
        else:
            # Busca geral com critérios
            messages = await self._message_repository.find_by_criteria(**criteria)
        
        # Converter para DTOs de resposta
        return [self._to_response_dto(message) for message in messages]
    
    def _prepare_search_criteria(self, search_params: MessageSearchDto) -> dict:
        """Prepara critérios de busca para o repositório."""
        criteria = {}
        
        # Filtros diretos
        if search_params.status:
            criteria['status'] = search_params.status
        
        if search_params.responsible_id:
            criteria['responsible_id'] = search_params.responsible_id
        
        if search_params.vehicle_id:
            criteria['vehicle_id'] = search_params.vehicle_id
        
        if search_params.email:
            criteria['email'] = search_params.email
        
        # Filtros de data
        if search_params.start_date:
            criteria['start_date'] = search_params.start_date
        
        if search_params.end_date:
            criteria['end_date'] = search_params.end_date
        
        # Paginação e ordenação
        if search_params.skip is not None:
            criteria['skip'] = search_params.skip
        
        if search_params.limit is not None:
            criteria['limit'] = search_params.limit
        
        if search_params.order_by:
            criteria['order_by'] = search_params.order_by
        
        if search_params.order_direction:
            criteria['order_direction'] = search_params.order_direction
        
        return criteria
    
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
