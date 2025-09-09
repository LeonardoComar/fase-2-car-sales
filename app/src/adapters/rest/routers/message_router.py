"""
Rotas REST para Message - Adapters Layer

Define as rotas HTTP para operações com mensagens seguindo padrões REST.
Aplicando Clean Architecture e princípios SOLID.
"""

from typing import Optional
from uuid import UUID
from datetime import date
from fastapi import APIRouter, HTTPException, Depends, Query, Path, status
from fastapi.responses import JSONResponse

from src.application.dtos.message_dto import (
    MessageCreateDto,
    MessageUpdateDto,
    MessageAssignDto,
    MessageStatusUpdateDto,
    MessageSearchDto
)

from src.adapters.rest.controllers.message_controller import MessageController
from src.adapters.rest.dependencies import (
    get_create_message_use_case,
    get_get_message_by_id_use_case,
    get_update_message_use_case,
    get_delete_message_use_case,
    get_list_messages_use_case,
    get_assign_message_use_case,
    get_update_message_status_use_case,
    get_get_messages_statistics_use_case,
    get_message_presenter
)

from src.adapters.rest.presenters.message_presenter import MessagePresenter


# Configuração do router
message_router = APIRouter(tags=["messages"])


def get_message_controller() -> MessageController:
    """Factory para MessageController com todas as dependências."""
    return MessageController(
        create_message_use_case=get_create_message_use_case(),
        get_message_by_id_use_case=get_get_message_by_id_use_case(),
        update_message_use_case=get_update_message_use_case(),
        delete_message_use_case=get_delete_message_use_case(),
        list_messages_use_case=get_list_messages_use_case(),
        assign_message_use_case=get_assign_message_use_case(),
        update_message_status_use_case=get_update_message_status_use_case(),
        get_messages_statistics_use_case=get_get_messages_statistics_use_case(),
        message_presenter=get_message_presenter()
    )


@message_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova mensagem",
    description="Cria uma nova mensagem de interesse em veículo",
    response_description="Mensagem criada com sucesso"
)
async def create_message(
    message_data: MessageCreateDto,
    controller: MessageController = Depends(get_message_controller)
):
    """
    Cria uma nova mensagem de interesse.
    
    - **name**: Nome do interessado (obrigatório)
    - **email**: Email do interessado (obrigatório)
    - **phone**: Telefone do interessado (opcional)
    - **message**: Mensagem/interesse (obrigatório)
    - **vehicle_id**: ID do veículo de interesse (opcional)
    """
    try:
        result = await controller.create_message(message_data)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Mensagem criada com sucesso",
                "data": result
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dados inválidos: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@message_router.get(
    "/{message_id}",
    summary="Buscar mensagem por ID",
    description="Retorna uma mensagem específica pelo ID",
    response_description="Dados da mensagem"
)
async def get_message_by_id(
    message_id: UUID = Path(..., description="ID da mensagem"),
    controller: MessageController = Depends(get_message_controller)
):
    """
    Busca uma mensagem específica pelo ID.
    """
    try:
        result = await controller.get_message_by_id(message_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensagem não encontrada"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": result
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@message_router.put(
    "/{message_id}",
    summary="Atualizar mensagem",
    description="Atualiza dados de uma mensagem existente",
    response_description="Mensagem atualizada com sucesso"
)
async def update_message(
    message_id: UUID = Path(..., description="ID da mensagem"),
    update_data: MessageUpdateDto = ...,
    controller: MessageController = Depends(get_message_controller)
):
    """
    Atualiza dados de uma mensagem existente.
    
    Apenas os campos fornecidos serão atualizados.
    """
    try:
        result = await controller.update_message(message_id, update_data)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensagem não encontrada"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Mensagem atualizada com sucesso",
                "data": result
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dados inválidos: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@message_router.delete(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar mensagem",
    description="Remove uma mensagem do sistema",
    response_description="Mensagem removida com sucesso"
)
async def delete_message(
    message_id: UUID = Path(..., description="ID da mensagem"),
    controller: MessageController = Depends(get_message_controller)
):
    """
    Remove uma mensagem do sistema.
    """
    try:
        success = await controller.delete_message(message_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensagem não encontrada"
            )
        
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content=None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@message_router.get(
    "/",
    summary="Listar mensagens",
    description="Lista mensagens com filtros opcionais",
    response_description="Lista de mensagens"
)
async def list_messages(
    status_filter: Optional[str] = Query(None, alias="status", description="Filtrar por status"),
    responsible_id: Optional[UUID] = Query(None, description="Filtrar por responsável"),
    vehicle_id: Optional[UUID] = Query(None, description="Filtrar por veículo"),
    email: Optional[str] = Query(None, description="Filtrar por email"),
    start_date: Optional[date] = Query(None, description="Data inicial"),
    end_date: Optional[date] = Query(None, description="Data final"),
    pending_only: Optional[bool] = Query(None, description="Apenas pendentes"),
    unassigned_only: Optional[bool] = Query(None, description="Apenas sem responsável"),
    overdue_hours: Optional[int] = Query(None, description="Em atraso (horas)"),
    order_by: Optional[str] = Query("created_at", description="Campo para ordenação"),
    order_direction: Optional[str] = Query("desc", description="Direção da ordenação"),
    skip: Optional[int] = Query(0, ge=0, description="Registros a pular"),
    limit: Optional[int] = Query(50, ge=1, le=100, description="Limite de registros"),
    controller: MessageController = Depends(get_message_controller)
):
    """
    Lista mensagens com filtros opcionais.
    
    Suporta paginação e diversos filtros para facilitar a busca.
    """
    try:
        # Criar DTO de busca
        search_params = MessageSearchDto(
            status=status_filter,
            responsible_id=responsible_id,
            vehicle_id=vehicle_id,
            email=email,
            start_date=start_date,
            end_date=end_date,
            pending_only=pending_only,
            unassigned_only=unassigned_only,
            overdue_hours=overdue_hours,
            order_by=order_by,
            order_direction=order_direction,
            skip=skip,
            limit=limit
        )
        
        result = await controller.list_messages(search_params)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": result
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Parâmetros inválidos: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@message_router.patch(
    "/{message_id}/assign",
    summary="Atribuir responsável",
    description="Atribui um funcionário responsável pela mensagem",
    response_description="Mensagem atualizada com responsável"
)
async def assign_message(
    message_id: UUID = Path(..., description="ID da mensagem"),
    assign_data: MessageAssignDto = ...,
    controller: MessageController = Depends(get_message_controller)
):
    """
    Atribui um funcionário responsável pela mensagem.
    """
    try:
        result = await controller.assign_message(message_id, assign_data)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensagem não encontrada"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Responsável atribuído com sucesso",
                "data": result
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dados inválidos: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@message_router.patch(
    "/{message_id}/status",
    summary="Atualizar status",
    description="Atualiza o status de atendimento da mensagem",
    response_description="Mensagem com status atualizado"
)
async def update_message_status(
    message_id: UUID = Path(..., description="ID da mensagem"),
    status_data: MessageStatusUpdateDto = ...,
    controller: MessageController = Depends(get_message_controller)
):
    """
    Atualiza o status de atendimento da mensagem.
    
    - **Pendente**: Mensagem aguardando atendimento
    - **Contato iniciado**: Atendimento em andamento
    - **Finalizado**: Atendimento concluído
    - **Cancelado**: Mensagem cancelada
    """
    try:
        result = await controller.update_message_status(message_id, status_data)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mensagem não encontrada"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Status atualizado com sucesso",
                "data": result
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dados inválidos: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@message_router.get(
    "/analytics/statistics",
    summary="Estatísticas de mensagens",
    description="Retorna estatísticas gerais sobre mensagens e atendimento",
    response_description="Estatísticas de mensagens"
)
async def get_messages_statistics(
    start_date: Optional[date] = Query(None, description="Data inicial para filtro"),
    end_date: Optional[date] = Query(None, description="Data final para filtro"),
    controller: MessageController = Depends(get_message_controller)
):
    """
    Retorna estatísticas gerais sobre mensagens e atendimento.
    
    Inclui métricas de performance, distribuição por status e rankings.
    """
    try:
        result = await controller.get_messages_statistics(start_date, end_date)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": result
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@message_router.get(
    "/pending",
    summary="Mensagens pendentes",
    description="Lista mensagens pendentes com informações de prioridade",
    response_description="Mensagens pendentes com prioridade"
)
async def get_pending_messages(
    controller: MessageController = Depends(get_message_controller)
):
    """
    Lista mensagens pendentes ordenadas por prioridade.
    
    A prioridade é calculada baseada no tempo de espera.
    """
    try:
        result = await controller.get_pending_messages()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": result
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@message_router.get(
    "/vehicle/{vehicle_id}",
    summary="Mensagens por veículo",
    description="Lista mensagens relacionadas a um veículo específico",
    response_description="Mensagens do veículo"
)
async def get_messages_by_vehicle(
    vehicle_id: UUID = Path(..., description="ID do veículo"),
    controller: MessageController = Depends(get_message_controller)
):
    """
    Lista mensagens de interesse em um veículo específico.
    
    Útil para analisar o interesse e demanda por veículos.
    """
    try:
        result = await controller.get_messages_by_vehicle(vehicle_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": result
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@message_router.get(
    "/responsible/{responsible_id}",
    summary="Mensagens por responsável",
    description="Lista mensagens atribuídas a um funcionário específico",
    response_description="Mensagens do responsável"
)
async def get_messages_by_responsible(
    responsible_id: UUID = Path(..., description="ID do funcionário responsável"),
    controller: MessageController = Depends(get_message_controller)
):
    """
    Lista mensagens atribuídas a um funcionário específico.
    
    Inclui métricas de performance do funcionário.
    """
    try:
        result = await controller.get_messages_by_responsible(responsible_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "data": result
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )
