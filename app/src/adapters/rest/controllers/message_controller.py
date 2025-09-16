"""
Controller para Mensagens - Adapter Layer

Responsável por coordenar as requisições HTTP relacionadas a mensagens.

Aplicando princípios SOLID:
- SRP: Responsável apenas por coordenar operações de mensagens
- OCP: Extensível para novas operações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para operações de mensagens
- DIP: Depende de abstrações (use cases) não de implementações
"""

from typing import List, Optional
from fastapi import HTTPException, Query
from fastapi.responses import JSONResponse
from src.application.use_cases.messages.create_message_use_case import CreateMessageUseCase
from src.application.use_cases.messages.get_message_by_id_use_case import GetMessageByIdUseCase
from src.application.use_cases.messages.get_all_messages_use_case import GetAllMessagesUseCase
from src.application.use_cases.messages.start_service_use_case import StartServiceUseCase
from src.application.use_cases.messages.update_message_status_use_case import UpdateMessageStatusUseCase
from src.application.dtos.message_dto import (
    CreateMessageRequest,
    StartServiceRequest,
    UpdateMessageStatusRequest,
    MessageResponse,
    MessageCreatedResponse,
    MessageListResponse,
    MessageFilters,
    MessageStatus
)


class MessageController:
    """
    Controller para gerenciamento de mensagens.
    
    Coordena as operações CRUD e consultas relacionadas a mensagens,
    delegando a lógica de negócio para os use cases apropriados.
    """
    
    def __init__(
        self,
        create_message_use_case: CreateMessageUseCase,
        get_message_by_id_use_case: GetMessageByIdUseCase,
        get_all_messages_use_case: GetAllMessagesUseCase,
        start_service_use_case: StartServiceUseCase,
        update_message_status_use_case: UpdateMessageStatusUseCase
    ):
        """
        Inicializa o controller com os use cases necessários.
        
        Args:
            create_message_use_case: Use case para criação de mensagens
            get_message_by_id_use_case: Use case para busca por ID
            get_all_messages_use_case: Use case para listagem de mensagens
            start_service_use_case: Use case para início de atendimento
            update_message_status_use_case: Use case para atualização de status
        """
        self._create_message_use_case = create_message_use_case
        self._get_message_by_id_use_case = get_message_by_id_use_case
        self._get_all_messages_use_case = get_all_messages_use_case
        self._start_service_use_case = start_service_use_case
        self._update_message_status_use_case = update_message_status_use_case
    
    async def create_message(self, message_data: CreateMessageRequest) -> MessageCreatedResponse:
        """
        Cria uma nova mensagem.
        
        Args:
            message_data: Dados da mensagem a ser criada
            
        Returns:
            MessageCreatedResponse: Dados da mensagem criada
            
        Raises:
            HTTPException: Em caso de erro na criação
        """
        try:
            return await self._create_message_use_case.execute(message_data)
        
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    async def get_message_by_id(self, message_id: int) -> MessageResponse:
        """
        Busca uma mensagem por ID.
        
        Args:
            message_id: ID da mensagem
            
        Returns:
            MessageResponse: Dados da mensagem encontrada
            
        Raises:
            HTTPException: Se mensagem não for encontrada ou houver erro
        """
        try:
            message = await self._get_message_by_id_use_case.execute(message_id)
            
            if not message:
                raise HTTPException(status_code=404, detail=f"Mensagem com ID {message_id} não encontrada")
            
            return message
            
        except HTTPException:
            raise
        
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    async def get_all_messages(
        self,
        status: Optional[str] = None,
        responsible_id: Optional[int] = None,
        vehicle_id: Optional[int] = None,
        page: int = 1,
        limit: int = 10,
        order_by: str = "created_at",
        order_direction: str = "desc"
    ) -> MessageListResponse:
        """
        Lista mensagens com filtros opcionais.
        
        Args:
            status: Filtro por status (opcional)
            responsible_id: Filtro por responsável (opcional)
            vehicle_id: Filtro por veículo (opcional)
            page: Número da página
            limit: Itens por página
            order_by: Campo para ordenação
            order_direction: Direção da ordenação
            
        Returns:
            MessageListResponse: Lista de mensagens e metadados de paginação
            
        Raises:
            HTTPException: Em caso de erro na listagem
        """
        try:
            # Converter status string para enum se fornecido
            status_enum = None
            if status:
                try:
                    status_enum = MessageStatus(status)
                except ValueError:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Status inválido. Valores válidos: {[s.value for s in MessageStatus]}"
                    )
            
            filters = MessageFilters(
                status=status_enum,
                responsible_id=responsible_id,
                vehicle_id=vehicle_id,
                page=page,
                limit=limit,
                order_by=order_by,
                order_direction=order_direction
            )
            
            return await self._get_all_messages_use_case.execute(filters)
            
        except HTTPException:
            raise
        
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    async def start_service(self, message_id: int, service_data: StartServiceRequest) -> MessageResponse:
        """
        Inicia o atendimento de uma mensagem.
        
        Args:
            message_id: ID da mensagem
            service_data: Dados do início de atendimento
            
        Returns:
            MessageResponse: Dados da mensagem com atendimento iniciado
            
        Raises:
            HTTPException: Em caso de erro no início do atendimento
        """
        try:
            return await self._start_service_use_case.execute(message_id, service_data)
            
        except ValueError as e:
            if "não encontrada" in str(e):
                raise HTTPException(status_code=404, detail=str(e))
            else:
                raise HTTPException(status_code=400, detail=str(e))
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    async def update_status(self, message_id: int, status_data: UpdateMessageStatusRequest) -> MessageResponse:
        """
        Atualiza o status de uma mensagem.
        
        Args:
            message_id: ID da mensagem
            status_data: Dados do novo status
            
        Returns:
            MessageResponse: Dados da mensagem com status atualizado
            
        Raises:
            HTTPException: Em caso de erro na atualização
        """
        try:
            return await self._update_message_status_use_case.execute(message_id, status_data)
            
        except ValueError as e:
            if "não encontrada" in str(e):
                raise HTTPException(status_code=404, detail=str(e))
            else:
                raise HTTPException(status_code=400, detail=str(e))
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    # Métodos de conveniência para status específicos
    async def set_pending_status(self, message_id: int) -> MessageResponse:
        """Define status como 'Pendente'."""
        status_data = UpdateMessageStatusRequest(status=MessageStatus.PENDENTE)
        return await self.update_status(message_id, status_data)
    
    async def set_contact_initiated_status(self, message_id: int) -> MessageResponse:
        """Define status como 'Contato iniciado'."""
        status_data = UpdateMessageStatusRequest(status=MessageStatus.CONTATO_INICIADO)
        return await self.update_status(message_id, status_data)
    
    async def set_finished_status(self, message_id: int) -> MessageResponse:
        """Define status como 'Finalizado'."""
        status_data = UpdateMessageStatusRequest(status=MessageStatus.FINALIZADO)
        return await self.update_status(message_id, status_data)
    
    async def set_cancelled_status(self, message_id: int) -> MessageResponse:
        """Define status como 'Cancelado'."""
        status_data = UpdateMessageStatusRequest(status=MessageStatus.CANCELADO)
        return await self.update_status(message_id, status_data)
