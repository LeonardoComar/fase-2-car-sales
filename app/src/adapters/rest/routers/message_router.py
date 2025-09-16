"""
Router para Mensagens - Interface Layer

Define as rotas HTTP para operações relacionadas a mensagens.

Aplicando princípios SOLID:
- SRP: Responsável apenas por definir rotas de mensagens
- OCP: Extensível para novas rotas sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para rotas de mensagens
- DIP: Depende de abstrações (controllers) não de implementações
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Path, Body
from src.adapters.rest.controllers.message_controller import MessageController
from src.adapters.rest.dependencies import get_message_controller
from src.application.dtos.message_dto import (
    CreateMessageRequest,
    StartServiceRequest,
    UpdateMessageStatusRequest,
    MessageResponse,
    MessageCreatedResponse,
    MessageListResponse
)

# Criar o router diretamente
message_router = APIRouter()

@message_router.post(
    "/",
    response_model=MessageCreatedResponse,
    status_code=201,
    summary="Criar nova mensagem",
    description="Cria uma nova mensagem no sistema. Esta rota não requer autenticação, permitindo que visitantes enviem mensagens.",
    responses={
        201: {"description": "Mensagem criada com sucesso"},
        400: {"description": "Dados inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def create_message(
    message_data: CreateMessageRequest = Body(..., description="Dados da mensagem a ser criada"),
    controller: MessageController = Depends(get_message_controller)
) -> MessageCreatedResponse:
    """Cria uma nova mensagem."""
    return await controller.create_message(message_data)

@message_router.get(
    "/",
    response_model=MessageListResponse,
    summary="Listar mensagens",
    description="Lista mensagens com filtros opcionais e paginação.",
    responses={
        200: {"description": "Lista de mensagens retornada com sucesso"},
        400: {"description": "Parâmetros de consulta inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def get_all_messages(
    status: Optional[str] = Query(
        None,
        description="Filtrar por status",
        enum=["Pendente", "Contato iniciado", "Finalizado", "Cancelado"]
    ),
    responsible_id: Optional[int] = Query(
        None,
        gt=0,
        description="Filtrar por ID do funcionário responsável"
    ),
    vehicle_id: Optional[int] = Query(
        None,
        gt=0,
        description="Filtrar por ID do veículo relacionado"
    ),
    page: int = Query(
        1,
        ge=1,
        description="Número da página"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Itens por página"
    ),
    order_by: str = Query(
        "created_at",
        description="Campo para ordenação",
        enum=["id", "name", "email", "status", "created_at", "updated_at", "service_start_time"]
    ),
    order_direction: str = Query(
        "desc",
        description="Direção da ordenação",
        enum=["asc", "desc"]
    ),
    controller: MessageController = Depends(get_message_controller)
) -> MessageListResponse:
    """Lista mensagens com filtros opcionais."""
    return await controller.get_all_messages(
        status=status,
        responsible_id=responsible_id,
        vehicle_id=vehicle_id,
        page=page,
        limit=limit,
        order_by=order_by,
        order_direction=order_direction
    )

@message_router.get(
    "/{message_id}",
    response_model=MessageResponse,
    summary="Buscar mensagem por ID",
    description="Busca uma mensagem específica pelo seu ID.",
    responses={
        200: {"description": "Mensagem encontrada"},
        404: {"description": "Mensagem não encontrada"},
        400: {"description": "ID inválido"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def get_message_by_id(
    message_id: int = Path(..., gt=0, description="ID da mensagem"),
    controller: MessageController = Depends(get_message_controller)
) -> MessageResponse:
    """Busca uma mensagem por ID."""
    return await controller.get_message_by_id(message_id)

@message_router.patch(
    "/{message_id}/start-service",
    response_model=MessageResponse,
    summary="Iniciar atendimento",
    description="Inicia o atendimento de uma mensagem, atribuindo um responsável e alterando o status para 'Contato iniciado'.",
    responses={
        200: {"description": "Atendimento iniciado com sucesso"},
        404: {"description": "Mensagem não encontrada"},
        400: {"description": "Dados inválidos ou mensagem já possui responsável"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def start_service(
    message_id: int = Path(..., gt=0, description="ID da mensagem"),
    service_data: StartServiceRequest = Body(..., description="Dados do início de atendimento"),
    controller: MessageController = Depends(get_message_controller)
) -> MessageResponse:
    """Inicia o atendimento de uma mensagem."""
    return await controller.start_service(message_id, service_data)

@message_router.patch(
    "/{message_id}/status",
    response_model=MessageResponse,
    summary="Atualizar status da mensagem",
    description="Atualiza o status de uma mensagem.",
    responses={
        200: {"description": "Status atualizado com sucesso"},
        404: {"description": "Mensagem não encontrada"},
        400: {"description": "Status inválido"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def update_message_status(
    message_id: int = Path(..., gt=0, description="ID da mensagem"),
    status_data: UpdateMessageStatusRequest = Body(..., description="Novo status da mensagem"),
    controller: MessageController = Depends(get_message_controller)
) -> MessageResponse:
    """Atualiza o status de uma mensagem."""
    return await controller.update_status(message_id, status_data)

# Rotas específicas para cada status (seguindo padrão do sistema)
@message_router.patch(
    "/{message_id}/pending",
    response_model=MessageResponse,
    summary="Definir status como Pendente",
    description="Define o status da mensagem como 'Pendente'.",
    responses={
        200: {"description": "Status atualizado para Pendente"},
        404: {"description": "Mensagem não encontrada"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def set_pending_status(
    message_id: int = Path(..., gt=0, description="ID da mensagem"),
    controller: MessageController = Depends(get_message_controller)
) -> MessageResponse:
    """Define status como 'Pendente'."""
    return await controller.set_pending_status(message_id)

@message_router.patch(
    "/{message_id}/contact-initiated",
    response_model=MessageResponse,
    summary="Definir status como Contato iniciado",
    description="Define o status da mensagem como 'Contato iniciado'.",
    responses={
        200: {"description": "Status atualizado para Contato iniciado"},
        404: {"description": "Mensagem não encontrada"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def set_contact_initiated_status(
    message_id: int = Path(..., gt=0, description="ID da mensagem"),
    controller: MessageController = Depends(get_message_controller)
) -> MessageResponse:
    """Define status como 'Contato iniciado'."""
    return await controller.set_contact_initiated_status(message_id)

@message_router.patch(
    "/{message_id}/finished",
    response_model=MessageResponse,
    summary="Definir status como Finalizado",
    description="Define o status da mensagem como 'Finalizado'.",
    responses={
        200: {"description": "Status atualizado para Finalizado"},
        404: {"description": "Mensagem não encontrada"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def set_finished_status(
    message_id: int = Path(..., gt=0, description="ID da mensagem"),
    controller: MessageController = Depends(get_message_controller)
) -> MessageResponse:
    """Define status como 'Finalizado'."""
    return await controller.set_finished_status(message_id)

@message_router.patch(
    "/{message_id}/cancelled",
    response_model=MessageResponse,
    summary="Definir status como Cancelado",
    description="Define o status da mensagem como 'Cancelado'.",
    responses={
        200: {"description": "Status atualizado para Cancelado"},
        404: {"description": "Mensagem não encontrada"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def set_cancelled_status(
    message_id: int = Path(..., gt=0, description="ID da mensagem"),
    controller: MessageController = Depends(get_message_controller)
) -> MessageResponse:
    """Define status como 'Cancelado'."""
    return await controller.set_cancelled_status(message_id)
