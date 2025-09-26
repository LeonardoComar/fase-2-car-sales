"""
Router para Vendas - Interface Layer

Define as rotas HTTP para operações relacionadas a vendas.

Aplicando princípios SOLID:
- SRP: Responsável apenas por definir rotas de vendas
- OCP: Extensível para novas rotas sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para rotas de vendas
- DIP: Depende de abstrações (controllers) não de implementações
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, Path, Body
from fastapi.responses import JSONResponse
from src.adapters.rest.controllers.sale_controller import SaleController
from src.adapters.rest.dependencies import get_sale_controller
from src.application.dtos.sale_dto import (
    CreateSaleRequest,
    UpdateSaleRequest,
    SaleResponse,
    SaleStatisticsResponse
)
from src.adapters.rest.auth_dependencies import (
    get_current_user,
    get_current_admin_or_vendedor_user
)
from src.domain.entities.user import User

# Criar o router diretamente
sale_router = APIRouter()

@sale_router.post(
    "/",
    response_model=SaleResponse,
    status_code=201,
    summary="Criar nova venda",
    description="Cria uma nova venda no sistema com os dados fornecidos. Requer autenticação: Administrador ou Vendedor",
    responses={
        201: {"description": "Venda criada com sucesso"},
        400: {"description": "Dados inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def create_sale(
    sale_data: CreateSaleRequest = Body(..., description="Dados da venda a ser criada"),
    controller: SaleController = Depends(get_sale_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> SaleResponse:
    """
    Cria uma nova venda.
    
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.create_sale(sale_data)

@sale_router.get(
    "/{sale_id}",
    response_model=SaleResponse,
    summary="Buscar venda por ID",
    description="Retorna os dados de uma venda específica pelo seu ID. Requer autenticação: Administrador ou Vendedor",
    responses={
        200: {"description": "Venda encontrada"},
        404: {"description": "Venda não encontrada"},
        400: {"description": "ID inválido"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def get_sale_by_id(
    sale_id: int = Path(..., description="ID da venda", gt=0),
    controller: SaleController = Depends(get_sale_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> SaleResponse:
    """
    Busca uma venda por ID.
    
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.get_sale_by_id(sale_id)

@sale_router.put(
    "/{sale_id}",
    response_model=SaleResponse,
    summary="Atualizar venda",
    description="Atualiza os dados de uma venda existente. Requer autenticação: Administrador ou Vendedor",
    responses={
        200: {"description": "Venda atualizada com sucesso"},
        404: {"description": "Venda não encontrada"},
        400: {"description": "Dados inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def update_sale(
    sale_id: int = Path(..., description="ID da venda", gt=0),
    sale_data: UpdateSaleRequest = Body(..., description="Dados para atualização da venda"),
    controller: SaleController = Depends(get_sale_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> SaleResponse:
    """
    Atualiza uma venda existente.
    
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.update_sale(sale_id, sale_data)

@sale_router.delete(
    "/{sale_id}",
    summary="Excluir venda",
    description="Remove uma venda do sistema. Requer autenticação: Administrador ou Vendedor",
    responses={
        200: {"description": "Venda excluída com sucesso"},
        404: {"description": "Venda não encontrada"},
        400: {"description": "ID inválido"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def delete_sale(
    sale_id: int = Path(..., description="ID da venda", gt=0),
    controller: SaleController = Depends(get_sale_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> dict:
    """
    Exclui uma venda.
    
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.delete_sale(sale_id)

@sale_router.patch(
    "/{sale_id}/confirm",
    response_model=SaleResponse,
    summary="Confirmar venda",
    description="Confirma uma venda alterando seu status para 'Confirmada'. Requer autenticação: Administrador ou Vendedor",
    responses={
        200: {"description": "Venda confirmada com sucesso"},
        404: {"description": "Venda não encontrada"},
        400: {"description": "Venda não pode ser confirmada"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def confirm_sale(
    sale_id: int = Path(..., description="ID da venda", gt=0),
    controller: SaleController = Depends(get_sale_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> SaleResponse:
    """
    Confirma uma venda.
    
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.confirm_sale(sale_id)

@sale_router.get(
    "/",
    summary="Listar vendas",
    description="Lista vendas com filtros opcionais para busca avançada. Requer autenticação: Administrador ou Vendedor",
    responses={
        200: {"description": "Lista de vendas"},
        400: {"description": "Parâmetros inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)
@sale_router.get(
    "",
    summary="Listar vendas",
    description="Lista vendas com filtros opcionais para busca avançada. Requer autenticação: Administrador ou Vendedor",
    responses={
        200: {"description": "Lista de vendas"},
        400: {"description": "Parâmetros inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def list_sales(
    client_id: Optional[int] = Query(None, description="Filtrar por ID do cliente", gt=0),
    employee_id: Optional[int] = Query(None, description="Filtrar por ID do funcionário", gt=0),
    status: Optional[str] = Query(None, description="Filtrar por status da venda"),
    start_date: Optional[datetime] = Query(None, description="Data inicial para filtro"),
    end_date: Optional[datetime] = Query(None, description="Data final para filtro"),
    payment_method: Optional[str] = Query(None, description="Filtrar por método de pagamento"),
    order_by_value: Optional[str] = Query(None, description="Ordenar por valor - 'asc' ou 'desc'"),
    skip: int = Query(0, description="Número de registros para pular", ge=0),
    limit: int = Query(100, description="Limite de registros retornados", gt=0, le=1000),
    controller: SaleController = Depends(get_sale_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> JSONResponse:
    """
    Lista vendas com filtros opcionais.
    
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.list_sales(
        client_id=client_id,
        employee_id=employee_id,
        status=status,
        start_date=start_date,
        end_date=end_date,
        payment_method=payment_method,
        order_by_value=order_by_value,
        skip=skip,
        limit=limit
    )

@sale_router.get(
    "/client/{client_id}",
    response_model=List[SaleResponse],
    summary="Listar vendas por cliente",
    description="Lista todas as vendas de um cliente específico. Requer autenticação: Administrador ou Vendedor",
    responses={
        200: {"description": "Lista de vendas do cliente"},
        400: {"description": "ID do cliente inválido"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def get_sales_by_client(
    client_id: int = Path(..., description="ID do cliente", gt=0),
    skip: int = Query(0, description="Número de registros para pular", ge=0),
    limit: int = Query(100, description="Limite de registros retornados", gt=0, le=1000),
    controller: SaleController = Depends(get_sale_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> List[SaleResponse]:
    """
    Lista vendas por cliente.
    
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.get_sales_by_client(
        client_id=client_id,
        skip=skip,
        limit=limit
    )

@sale_router.get(
    "/employee/{employee_id}",
    response_model=List[SaleResponse],
    summary="Listar vendas por funcionário",
    description="Lista todas as vendas de um funcionário específico. Requer autenticação: Administrador ou Vendedor",
    responses={
        200: {"description": "Lista de vendas do funcionário"},
        400: {"description": "ID do funcionário inválido"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def get_sales_by_employee(
    employee_id: int = Path(..., description="ID do funcionário", gt=0),
    skip: int = Query(0, description="Número de registros para pular", ge=0),
    limit: int = Query(100, description="Limite de registros retornados", gt=0, le=1000),
    controller: SaleController = Depends(get_sale_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> List[SaleResponse]:
    """
    Lista vendas por funcionário.
    
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.get_sales_by_employee(
        employee_id=employee_id,
        skip=skip,
        limit=limit
    )

@sale_router.get(
    "/statistics/summary",
    response_model=SaleStatisticsResponse,
    summary="Estatísticas de vendas",
    description="Retorna estatísticas detalhadas das vendas com filtros opcionais. Requer autenticação: Administrador ou Vendedor",
    responses={
        200: {"description": "Estatísticas das vendas"},
        400: {"description": "Parâmetros inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def get_sales_statistics(
    start_date: Optional[datetime] = Query(None, description="Data inicial para filtro"),
    end_date: Optional[datetime] = Query(None, description="Data final para filtro"),
    employee_id: Optional[int] = Query(None, description="Filtrar por ID do funcionário", gt=0),
    controller: SaleController = Depends(get_sale_controller),
    current_user: User = Depends(get_current_admin_or_vendedor_user)
) -> SaleStatisticsResponse:
    """
    Retorna estatísticas das vendas.
    
    Requer autenticação: Administrador ou Vendedor
    """
    return await controller.get_sales_statistics(
        start_date=start_date,
        end_date=end_date,
        employee_id=employee_id
    )
