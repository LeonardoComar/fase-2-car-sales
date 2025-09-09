"""
Rotas REST para Client - Adapters Layer

Define os endpoints da API para gerenciamento de clientes.
Aplicando padrões REST e Clean Architecture.

Aplicando princípios SOLID:
- SRP: Responsável apenas pelas rotas de clientes
- OCP: Extensível para novos endpoints
- DIP: Depende de abstrações (controller)
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from src.application.dtos.client_dto import (
    ClientCreateDto, ClientUpdateDto, ClientSearchDto,
    ClientStatusUpdateDto
)
from src.adapters.rest.controllers.client_controller import ClientController
from src.adapters.rest.dependencies import get_client_controller


# Criar router para clientes
client_router = APIRouter(
    tags=["Clients"],
    responses={
        404: {"description": "Cliente não encontrado"},
        422: {"description": "Regra de negócio violada"},
        500: {"description": "Erro interno do servidor"}
    }
)


@client_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Criar cliente",
    description="Cria um novo cliente no sistema"
)
async def create_client(
    client_data: ClientCreateDto,
    controller: ClientController = Depends(get_client_controller)
) -> JSONResponse:
    """
    Cria um novo cliente.
    
    - **name**: Nome completo do cliente
    - **email**: Email para contato
    - **cpf**: CPF válido brasileiro
    - **phone**: Telefone para contato
    - **birth_date**: Data de nascimento (opcional)
    - **address**: Endereço completo
    - **city**: Cidade de residência
    - **state**: Estado (UF)
    - **zip_code**: CEP
    - **preferred_contact**: Forma preferida de contato
    - **notes**: Observações adicionais (opcional)
    - **credit_score**: Score de crédito (opcional)
    - **income**: Renda mensal (opcional)
    """
    return await controller.create_client(client_data)


@client_router.get(
    "/{client_id}",
    status_code=status.HTTP_200_OK,
    summary="Buscar cliente por ID",
    description="Busca um cliente específico pelo ID"
)
async def get_client_by_id(
    client_id: UUID,
    controller: ClientController = Depends(get_client_controller)
) -> JSONResponse:
    """
    Busca um cliente pelo ID.
    
    - **client_id**: ID único do cliente (UUID)
    """
    return await controller.get_client_by_id(client_id)


@client_router.get(
    "/cpf/{cpf}",
    status_code=status.HTTP_200_OK,
    summary="Buscar cliente por CPF",
    description="Busca um cliente específico pelo CPF"
)
async def get_client_by_cpf(
    cpf: str,
    controller: ClientController = Depends(get_client_controller)
) -> JSONResponse:
    """
    Busca um cliente pelo CPF.
    
    - **cpf**: CPF do cliente (formato: 123.456.789-00 ou 12345678900)
    """
    return await controller.get_client_by_cpf(cpf)


@client_router.put(
    "/{client_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizar cliente",
    description="Atualiza os dados de um cliente existente"
)
async def update_client(
    client_id: UUID,
    client_data: ClientUpdateDto,
    controller: ClientController = Depends(get_client_controller)
) -> JSONResponse:
    """
    Atualiza os dados de um cliente.
    
    - **client_id**: ID único do cliente
    - **name**: Nome completo do cliente
    - **email**: Email para contato
    - **phone**: Telefone para contato
    - **address**: Endereço completo
    - **city**: Cidade de residência
    - **state**: Estado (UF)
    - **zip_code**: CEP
    - **preferred_contact**: Forma preferida de contato
    - **notes**: Observações adicionais
    - **credit_score**: Score de crédito
    - **income**: Renda mensal
    """
    return await controller.update_client(client_id, client_data)


@client_router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar cliente",
    description="Remove um cliente do sistema"
)
async def delete_client(
    client_id: UUID,
    controller: ClientController = Depends(get_client_controller)
) -> JSONResponse:
    """
    Remove um cliente do sistema.
    
    - **client_id**: ID único do cliente
    """
    return await controller.delete_client(client_id)


@client_router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Listar clientes",
    description="Lista clientes com filtros e paginação"
)
async def list_clients(
    name: Optional[str] = Query(None, description="Filtrar por nome"),
    email: Optional[str] = Query(None, description="Filtrar por email"),
    city: Optional[str] = Query(None, description="Filtrar por cidade"),
    state: Optional[str] = Query(None, description="Filtrar por estado"),
    is_active: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    min_credit_score: Optional[int] = Query(None, description="Score mínimo de crédito"),
    max_credit_score: Optional[int] = Query(None, description="Score máximo de crédito"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Tamanho da página"),
    controller: ClientController = Depends(get_client_controller)
) -> JSONResponse:
    """
    Lista clientes com filtros opcionais e paginação.
    
    Filtros disponíveis:
    - **name**: Busca parcial por nome
    - **email**: Busca parcial por email
    - **city**: Filtrar por cidade
    - **state**: Filtrar por estado (UF)
    - **is_active**: Filtrar por status ativo/inativo
    - **min_credit_score**: Score mínimo de crédito
    - **max_credit_score**: Score máximo de crédito
    
    Paginação:
    - **page**: Número da página (padrão: 1)
    - **page_size**: Itens por página (padrão: 20, máximo: 100)
    """
    search_dto = ClientSearchDto(
        name=name,
        email=email,
        city=city,
        state=state,
        is_active=is_active,
        min_credit_score=min_credit_score,
        max_credit_score=max_credit_score,
        page=page,
        page_size=page_size
    )
    return await controller.list_clients(search_dto)


@client_router.patch(
    "/{client_id}/status",
    status_code=status.HTTP_200_OK,
    summary="Atualizar status do cliente",
    description="Ativa ou desativa um cliente"
)
async def update_client_status(
    client_id: UUID,
    status_data: ClientStatusUpdateDto,
    controller: ClientController = Depends(get_client_controller)
) -> JSONResponse:
    """
    Atualiza o status de um cliente (ativo/inativo).
    
    - **client_id**: ID único do cliente
    - **is_active**: Novo status (true para ativo, false para inativo)
    - **reason**: Motivo da alteração (opcional)
    """
    return await controller.update_client_status(client_id, status_data)


@client_router.get(
    "/search/advanced",
    status_code=status.HTTP_200_OK,
    summary="Busca avançada de clientes",
    description="Busca clientes com critérios avançados"
)
async def advanced_search_clients(
    query: Optional[str] = Query(None, description="Termo de busca geral"),
    min_income: Optional[float] = Query(None, description="Renda mínima"),
    max_income: Optional[float] = Query(None, description="Renda máxima"),
    zip_code: Optional[str] = Query(None, description="CEP para busca"),
    has_purchases: Optional[bool] = Query(None, description="Cliente com compras"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Tamanho da página"),
    controller: ClientController = Depends(get_client_controller)
) -> JSONResponse:
    """
    Busca avançada de clientes com múltiplos critérios.
    
    - **query**: Busca geral em nome, email, telefone
    - **min_income**: Renda mínima
    - **max_income**: Renda máxima  
    - **zip_code**: CEP para localização
    - **has_purchases**: Filtrar clientes com ou sem compras
    """
    search_dto = ClientSearchDto(
        query=query,
        min_income=min_income,
        max_income=max_income,
        zip_code=zip_code,
        page=page,
        page_size=page_size
    )
    return await controller.advanced_search_clients(search_dto)


@client_router.get(
    "/statistics/summary",
    status_code=status.HTTP_200_OK,
    summary="Estatísticas de clientes",
    description="Retorna estatísticas gerais dos clientes"
)
async def get_client_statistics(
    controller: ClientController = Depends(get_client_controller)
) -> JSONResponse:
    """
    Retorna estatísticas gerais dos clientes.
    
    Inclui informações como:
    - Total de clientes ativos/inativos
    - Distribuição por cidade/estado
    - Médias de score de crédito e renda
    - Clientes cadastrados por período
    """
    return await controller.get_client_statistics()
