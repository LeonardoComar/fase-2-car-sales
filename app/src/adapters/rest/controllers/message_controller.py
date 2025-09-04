"""
Controller para Message - Adapters Layer

Responsável por receber requisições HTTP, validar dados e coordenar
a execução dos casos de uso de mensagens.
Aplicando Clean Architecture e princípios SOLID.
"""

from typing import Dict, Any, Optional
from uuid import UUID
from datetime import date

from src.application.use_cases.messages import (
    CreateMessageUseCase,
    GetMessageByIdUseCase,
    UpdateMessageUseCase,
    DeleteMessageUseCase,
    ListMessagesUseCase,
    AssignMessageUseCase,
    UpdateMessageStatusUseCase,
    GetMessagesStatisticsUseCase,
)

from src.application.dtos.message_dto import (
    MessageCreateDto,
    MessageUpdateDto,
    MessageAssignDto,
    MessageStatusUpdateDto,
    MessageSearchDto
)

from src.adapters.rest.presenters.message_presenter import MessagePresenter


class MessageController:
    """
    Controller para operações com mensagens.
    
    Aplicando princípios SOLID:
    - SRP: Responsável apenas por coordenar operações de mensagens via HTTP
    - OCP: Extensível para novos endpoints
    - LSP: Pode ser substituído por outras implementações
    - ISP: Interface coesa com métodos específicos
    - DIP: Depende de abstrações (use cases)
    """
    
    def __init__(self,
                 create_message_use_case: CreateMessageUseCase,
                 get_message_by_id_use_case: GetMessageByIdUseCase,
                 update_message_use_case: UpdateMessageUseCase,
                 delete_message_use_case: DeleteMessageUseCase,
                 list_messages_use_case: ListMessagesUseCase,
                 assign_message_use_case: AssignMessageUseCase,
                 update_message_status_use_case: UpdateMessageStatusUseCase,
                 get_messages_statistics_use_case: GetMessagesStatisticsUseCase,
                 message_presenter: MessagePresenter):
        """
        Inicializa o controller com as dependências necessárias.
        
        Args:
            create_message_use_case: Caso de uso para criar mensagem
            get_message_by_id_use_case: Caso de uso para buscar mensagem por ID
            update_message_use_case: Caso de uso para atualizar mensagem
            delete_message_use_case: Caso de uso para deletar mensagem
            list_messages_use_case: Caso de uso para listar mensagens
            assign_message_use_case: Caso de uso para atribuir responsável
            update_message_status_use_case: Caso de uso para atualizar status
            get_messages_statistics_use_case: Caso de uso para estatísticas
            message_presenter: Presenter para formatação de dados
        """
        self._create_message_use_case = create_message_use_case
        self._get_message_by_id_use_case = get_message_by_id_use_case
        self._update_message_use_case = update_message_use_case
        self._delete_message_use_case = delete_message_use_case
        self._list_messages_use_case = list_messages_use_case
        self._assign_message_use_case = assign_message_use_case
        self._update_message_status_use_case = update_message_status_use_case
        self._get_messages_statistics_use_case = get_messages_statistics_use_case
        self._presenter = message_presenter
    
    async def create_message(self, message_data: MessageCreateDto) -> Dict[str, Any]:
        """
        Cria uma nova mensagem.
        
        Args:
            message_data: Dados da mensagem a ser criada
            
        Returns:
            Dict: Resposta formatada com dados da mensagem criada
            
        Raises:
            ValueError: Se dados inválidos
            Exception: Se erro interno
        """
        # Executar caso de uso
        message_dto = await self._create_message_use_case.execute(message_data)
        
        # Formatar resposta
        return self._presenter.present_message(message_dto)
    
    async def get_message_by_id(self, message_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Busca uma mensagem por ID.
        
        Args:
            message_id: ID da mensagem
            
        Returns:
            Optional[Dict]: Dados da mensagem ou None se não encontrada
        """
        # Executar caso de uso
        message_dto = await self._get_message_by_id_use_case.execute(message_id)
        
        if not message_dto:
            return None
        
        # Formatar resposta
        return self._presenter.present_message(message_dto)
    
    async def update_message(self, message_id: UUID, update_data: MessageUpdateDto) -> Optional[Dict[str, Any]]:
        """
        Atualiza uma mensagem.
        
        Args:
            message_id: ID da mensagem
            update_data: Dados para atualização
            
        Returns:
            Optional[Dict]: Dados da mensagem atualizada ou None se não encontrada
            
        Raises:
            ValueError: Se dados inválidos ou operação não permitida
            Exception: Se erro interno
        """
        # Executar caso de uso
        message_dto = await self._update_message_use_case.execute(message_id, update_data)
        
        if not message_dto:
            return None
        
        # Formatar resposta
        return self._presenter.present_message(message_dto)
    
    async def delete_message(self, message_id: UUID) -> bool:
        """
        Remove uma mensagem.
        
        Args:
            message_id: ID da mensagem
            
        Returns:
            bool: True se removida, False se não encontrada
            
        Raises:
            Exception: Se erro interno
        """
        # Executar caso de uso
        return await self._delete_message_use_case.execute(message_id)
    
    async def list_messages(self, search_params: MessageSearchDto) -> Dict[str, Any]:
        """
        Lista mensagens com filtros.
        
        Args:
            search_params: Parâmetros de busca
            
        Returns:
            Dict: Lista de mensagens formatada
        """
        # Executar caso de uso
        messages_dto = await self._list_messages_use_case.execute(search_params)
        
        # Formatar resposta
        return self._presenter.present_message_list(messages_dto)
    
    async def assign_message(self, message_id: UUID, assign_data: MessageAssignDto) -> Optional[Dict[str, Any]]:
        """
        Atribui responsável a uma mensagem.
        
        Args:
            message_id: ID da mensagem
            assign_data: Dados de atribuição
            
        Returns:
            Optional[Dict]: Dados da mensagem atualizada ou None se não encontrada
            
        Raises:
            ValueError: Se operação não permitida
            Exception: Se erro interno
        """
        # Executar caso de uso
        message_dto = await self._assign_message_use_case.execute(message_id, assign_data)
        
        if not message_dto:
            return None
        
        # Formatar resposta
        return self._presenter.present_message(message_dto)
    
    async def update_message_status(self, message_id: UUID, status_data: MessageStatusUpdateDto) -> Optional[Dict[str, Any]]:
        """
        Atualiza status de uma mensagem.
        
        Args:
            message_id: ID da mensagem
            status_data: Dados de atualização de status
            
        Returns:
            Optional[Dict]: Dados da mensagem atualizada ou None se não encontrada
            
        Raises:
            ValueError: Se status inválido ou operação não permitida
            Exception: Se erro interno
        """
        # Executar caso de uso
        message_dto = await self._update_message_status_use_case.execute(message_id, status_data)
        
        if not message_dto:
            return None
        
        # Formatar resposta
        return self._presenter.present_message(message_dto)
    
    async def get_messages_statistics(self, start_date: Optional[date] = None, 
                                    end_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Obtém estatísticas de mensagens.
        
        Args:
            start_date: Data inicial para filtro
            end_date: Data final para filtro
            
        Returns:
            Dict: Estatísticas formatadas
        """
        # Executar caso de uso
        stats_dto = await self._get_messages_statistics_use_case.execute(start_date, end_date)
        
        # Formatar resposta
        return self._presenter.present_messages_statistics(stats_dto)
    
    async def get_pending_messages(self) -> Dict[str, Any]:
        """
        Obtém mensagens pendentes com prioridade.
        
        Returns:
            Dict: Mensagens pendentes formatadas
        """
        # Criar parâmetros de busca para mensagens pendentes
        search_params = MessageSearchDto(
            pending_only=True,
            order_by="created_at",
            order_direction="asc",  # Mais antigas primeiro
            limit=100
        )
        
        # Executar caso de uso
        messages_dto = await self._list_messages_use_case.execute(search_params)
        
        # Formatar resposta específica para pendentes
        return self._presenter.present_pending_messages(messages_dto)
    
    async def get_messages_by_vehicle(self, vehicle_id: UUID) -> Dict[str, Any]:
        """
        Obtém mensagens relacionadas a um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Dict: Mensagens do veículo formatadas
        """
        # Criar parâmetros de busca por veículo
        search_params = MessageSearchDto(
            vehicle_id=vehicle_id,
            order_by="created_at",
            order_direction="desc",
            limit=100
        )
        
        # Executar caso de uso
        messages_dto = await self._list_messages_use_case.execute(search_params)
        
        # Formatar resposta específica para veículo
        return self._presenter.present_messages_by_vehicle(str(vehicle_id), messages_dto)
    
    async def get_messages_by_responsible(self, responsible_id: UUID) -> Dict[str, Any]:
        """
        Obtém mensagens de um responsável.
        
        Args:
            responsible_id: ID do responsável
            
        Returns:
            Dict: Mensagens do responsável formatadas
        """
        # Criar parâmetros de busca por responsável
        search_params = MessageSearchDto(
            responsible_id=responsible_id,
            order_by="created_at",
            order_direction="desc",
            limit=100
        )
        
        # Executar caso de uso
        messages_dto = await self._list_messages_use_case.execute(search_params)
        
        # Formatar resposta específica para responsável
        return self._presenter.present_messages_by_responsible(str(responsible_id), messages_dto)
