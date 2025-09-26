"""
Router de Clientes - Adapter Layer

Define as rotas HTTP para operações relacionadas a clientes.
Faz a ponte entre requisições HTTP e o controller de clientes.

Aplicando princípios SOLID:
- SRP: Responsável apenas pelo roteamento de clientes
- OCP: Extensível para novas rotas sem modificar existentes
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para rotas de clientes
- DIP: Depende de abstrações (controller) não de implementações
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Path, status
from fastapi.responses import JSONResponse

from src.adapters.rest.controllers.client_controller import ClientController
from src.adapters.rest.dependencies import get_client_controller
from src.application.dtos.client_dto import CreateClientDto, UpdateClientDto
from src.adapters.rest.auth_dependencies import (
    get_current_user,
    get_current_admin_or_vendedor_user
)
from src.domain.entities.user import User


# Criar roteador para clientes
client_router = APIRouter()


@client_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Criar cliente",
    description="Cria um novo cliente no sistema. Requer autenticação: Administrador ou Vendedor",
    response_description="Cliente criado com sucesso"
)
async def create_client(
    client_data: CreateClientDto,
    controller: ClientController = Depends(get_client_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> JSONResponse:
    """
    Cria um novo cliente no sistema.
    
    - **name**: Nome completo do cliente
    - **email**: Email único do cliente  
    - **phone**: Telefone do cliente (opcional)
    - **cpf**: CPF único do cliente
    - **address**: Dados do endereço (opcional)
    
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.create_client(client_data)


@client_router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Listar clientes",
    description="Lista clientes com filtros e paginação. Requer autenticação: Administrador ou Vendedor",
    response_description="Lista de clientes"
)
async def list_clients(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registros para retornar"),
    name: Optional[str] = Query(None, description="Buscar por nome (busca parcial)"),
    cpf: Optional[str] = Query(None, description="Buscar por CPF exato"),
    controller: ClientController = Depends(get_client_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> JSONResponse:
    """
    Lista clientes com opções de busca e paginação.
    
    ### Parâmetros de busca (mutuamente exclusivos):
    - **name**: Busca clientes cujo nome contenha o termo especificado
    - **cpf**: Busca cliente com CPF exato
    
    ### Parâmetros de paginação:
    - **skip**: Número de registros para pular (padrão: 0)
    - **limit**: Número máximo de registros para retornar (padrão: 100, máximo: 500)
    
    **Nota**: Os parâmetros name e cpf não podem ser usados simultaneamente.
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.list_clients(skip=skip, limit=limit, name=name, cpf=cpf)


@client_router.get(
    "/{client_id}",
    status_code=status.HTTP_200_OK,
    summary="Buscar cliente por ID",
    description="Busca um cliente específico pelo ID. Requer autenticação: Administrador ou Vendedor",
    response_description="Dados do cliente"
)
async def get_client_by_id(
    client_id: int = Path(..., gt=0, description="ID do cliente"),
    controller: ClientController = Depends(get_client_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> JSONResponse:
    """
    Busca um cliente pelo seu ID.
    
    ### Parâmetros:
    - **client_id**: ID único do cliente no sistema
    
    ### Retorna:
    - Dados completos do cliente incluindo endereço (se cadastrado)
    - Informações de criação e última atualização
    
    ### Códigos de resposta:
    - **200**: Cliente encontrado
    - **404**: Cliente não encontrado
    - **400**: ID inválido
    
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.get_client_by_id(client_id)


@client_router.get(
    "/cpf/{cpf}",
    status_code=status.HTTP_200_OK,
    summary="Buscar cliente por CPF",
    description="Busca um cliente específico pelo CPF. Requer autenticação: Administrador ou Vendedor",
    response_description="Dados do cliente"
)
async def get_client_by_cpf(
    cpf: str = Path(..., min_length=11, max_length=14, description="CPF do cliente"),
    controller: ClientController = Depends(get_client_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> JSONResponse:
    """
    Busca um cliente pelo seu CPF.
    
    ### Parâmetros:
    - **cpf**: CPF do cliente (formato: 000.000.000-00 ou 00000000000)
    
    ### Retorna:
    - Dados completos do cliente incluindo endereço (se cadastrado)
    - Informações de criação e última atualização
    
    ### Códigos de resposta:
    - **200**: Cliente encontrado
    - **404**: Cliente não encontrado
    - **400**: CPF inválido
    
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.get_client_by_cpf(cpf)


@client_router.put(
    "/{client_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizar cliente",
    description="Atualiza os dados de um cliente existente. Requer autenticação: Administrador ou Vendedor",
    response_description="Cliente atualizado com sucesso"
)
async def update_client(
    client_id: int = Path(..., gt=0, description="ID do cliente"),
    client_data: UpdateClientDto = ...,
    controller: ClientController = Depends(get_client_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> JSONResponse:
    """
    Atualiza os dados de um cliente existente.
    
    ### Parâmetros:
    - **client_id**: ID único do cliente no sistema
    - **client_data**: Dados para atualização (todos opcionais)
    
    ### Campos atualizáveis:
    - **name**: Nome completo do cliente
    - **email**: Email do cliente (deve ser único)
    - **phone**: Telefone do cliente
    - **cpf**: CPF do cliente (deve ser único)
    - **address**: Dados do endereço
    
    ### Códigos de resposta:
    - **200**: Cliente atualizado com sucesso
    - **404**: Cliente não encontrado
    - **400**: Dados inválidos ou email/CPF já em uso
    
    **Nota**: Apenas os campos fornecidos serão atualizados.
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.update_client(client_id, client_data)


@client_router.delete(
    "/{client_id}",
    status_code=status.HTTP_200_OK,
    summary="Remover cliente",
    description="Remove um cliente do sistema. Requer autenticação: Administrador ou Vendedor",
    response_description="Cliente removido com sucesso"
)
async def delete_client(
    client_id: int = Path(..., gt=0, description="ID do cliente"),
    controller: ClientController = Depends(get_client_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> JSONResponse:
    """
    Remove um cliente do sistema.
    
    ### Parâmetros:
    - **client_id**: ID único do cliente no sistema
    
    ### Ação:
    - Remove o cliente e seu endereço associado (se houver)
    - Esta operação é irreversível
    
    ### Códigos de resposta:
    - **200**: Cliente removido com sucesso
    - **404**: Cliente não encontrado
    - **400**: ID inválido
    
    **Atenção**: Esta operação é irreversível. O cliente e todos os seus dados
    serão permanentemente removidos do sistema.
    
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.delete_client(client_id)
