from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from uuid import UUID
from datetime import date

from src.application.dtos.sale_dto import (
    SaleCreateDto, SaleUpdateDto, SaleSearchDto, SaleStatusUpdateDto
)
from src.adapters.rest.controllers.sale_controller import SaleController
from src.adapters.rest.dependencies import get_sale_controller

# Criar router para vendas
sale_router = APIRouter(tags=["Sales"])


@sale_router.post("/", summary="Criar nova venda", description="Cria uma nova venda na concessionária")
async def create_sale(
    sale_data: SaleCreateDto,
    controller: SaleController = Depends(get_sale_controller)
):
    """
    Cria uma nova venda.
    
    - **client_id**: ID do cliente
    - **employee_id**: ID do funcionário vendedor
    - **vehicle_id**: ID do veículo vendido
    - **total_amount**: Valor total da venda
    - **payment_method**: Forma de pagamento
    - **sale_date**: Data da venda
    - **notes**: Observações (opcional)
    - **discount_amount**: Valor do desconto (opcional)
    - **tax_amount**: Valor dos impostos (opcional)
    - **commission_rate**: Taxa de comissão (opcional)
    """
    response, status_code = await controller.create_sale(sale_data)
    
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=response)
    
    return response


@sale_router.get("/{sale_id}", summary="Buscar venda por ID", description="Busca uma venda específica pelo ID")
async def get_sale_by_id(
    sale_id: UUID,
    controller: SaleController = Depends(get_sale_controller)
):
    """
    Busca uma venda por ID.
    
    - **sale_id**: ID único da venda
    """
    response, status_code = await controller.get_sale_by_id(sale_id)
    
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response)
    
    return response


@sale_router.put("/{sale_id}", summary="Atualizar venda", description="Atualiza os dados de uma venda")
async def update_sale(
    sale_id: UUID,
    sale_data: SaleUpdateDto,
    controller: SaleController = Depends(get_sale_controller)
):
    """
    Atualiza uma venda.
    
    - **sale_id**: ID da venda a ser atualizada
    - Campos opcionais para atualização
    """
    response, status_code = await controller.update_sale(sale_id, sale_data)
    
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response)
    
    return response


@sale_router.delete("/{sale_id}", summary="Excluir venda", description="Exclui uma venda (apenas se não paga/entregue)")
async def delete_sale(
    sale_id: UUID,
    controller: SaleController = Depends(get_sale_controller)
):
    """
    Exclui uma venda.
    
    - **sale_id**: ID da venda a ser excluída
    
    Nota: Vendas pagas ou entregues não podem ser excluídas.
    """
    response, status_code = await controller.delete_sale(sale_id)
    
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response)
    
    return response


@sale_router.get("/", summary="Listar vendas", description="Lista vendas com filtros opcionais")
async def list_sales(
    client_id: Optional[UUID] = Query(None, description="ID do cliente"),
    employee_id: Optional[UUID] = Query(None, description="ID do funcionário"),
    vehicle_id: Optional[UUID] = Query(None, description="ID do veículo"),
    status: Optional[str] = Query(None, description="Status da venda"),
    payment_method: Optional[str] = Query(None, description="Forma de pagamento"),
    start_date: Optional[date] = Query(None, description="Data inicial"),
    end_date: Optional[date] = Query(None, description="Data final"),
    min_amount: Optional[float] = Query(None, description="Valor mínimo"),
    max_amount: Optional[float] = Query(None, description="Valor máximo"),
    active_only: Optional[bool] = Query(None, description="Apenas vendas ativas"),
    completed_only: Optional[bool] = Query(None, description="Apenas vendas entregues"),
    order_by: Optional[str] = Query(None, description="Campo para ordenação"),
    order_direction: str = Query("asc", description="Direção da ordenação"),
    skip: int = Query(0, description="Registros para pular"),
    limit: int = Query(100, description="Número máximo de registros"),
    controller: SaleController = Depends(get_sale_controller)
):
    """
    Lista vendas com filtros opcionais.
    
    Suporte a filtros por:
    - Cliente, funcionário, veículo
    - Status, forma de pagamento
    - Período de datas
    - Faixa de valores
    - Paginação e ordenação
    """
    search_criteria = SaleSearchDto(
        client_id=client_id,
        employee_id=employee_id,
        vehicle_id=vehicle_id,
        status=status,
        payment_method=payment_method,
        start_date=start_date,
        end_date=end_date,
        min_amount=min_amount,
        max_amount=max_amount,
        active_only=active_only,
        completed_only=completed_only,
        order_by=order_by,
        order_direction=order_direction,
        skip=skip,
        limit=limit
    )
    
    response, status_code = await controller.list_sales(search_criteria)
    
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response)
    
    return response


@sale_router.patch("/{sale_id}/status", summary="Atualizar status da venda", description="Atualiza apenas o status de uma venda")
async def update_sale_status(
    sale_id: UUID,
    status_data: SaleStatusUpdateDto,
    controller: SaleController = Depends(get_sale_controller)
):
    """
    Atualiza o status de uma venda.
    
    - **sale_id**: ID da venda
    - **status**: Novo status (Pendente, Confirmada, Paga, Entregue, Cancelada)
    
    Transições válidas são validadas pela regra de negócio.
    """
    response, status_code = await controller.update_sale_status(sale_id, status_data)
    
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response)
    
    return response


@sale_router.get("/client/{client_id}", summary="Vendas por cliente", description="Lista todas as vendas de um cliente")
async def get_sales_by_client(
    client_id: UUID,
    skip: int = Query(0, description="Registros para pular"),
    limit: int = Query(100, description="Número máximo de registros"),
    order_by: Optional[str] = Query("sale_date", description="Campo para ordenação"),
    order_direction: str = Query("desc", description="Direção da ordenação"),
    controller: SaleController = Depends(get_sale_controller)
):
    """
    Lista vendas de um cliente específico.
    
    - **client_id**: ID do cliente
    - Suporte a paginação e ordenação
    """
    search_criteria = SaleSearchDto(
        skip=skip,
        limit=limit,
        order_by=order_by,
        order_direction=order_direction
    )
    
    response, status_code = await controller.get_sales_by_client(client_id, search_criteria)
    
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response)
    
    return response


@sale_router.get("/employee/{employee_id}", summary="Vendas por funcionário", description="Lista todas as vendas de um funcionário")
async def get_sales_by_employee(
    employee_id: UUID,
    skip: int = Query(0, description="Registros para pular"),
    limit: int = Query(100, description="Número máximo de registros"),
    order_by: Optional[str] = Query("sale_date", description="Campo para ordenação"),
    order_direction: str = Query("desc", description="Direção da ordenação"),
    controller: SaleController = Depends(get_sale_controller)
):
    """
    Lista vendas de um funcionário específico.
    
    - **employee_id**: ID do funcionário
    - Inclui totais de vendas e comissões
    - Suporte a paginação e ordenação
    """
    search_criteria = SaleSearchDto(
        skip=skip,
        limit=limit,
        order_by=order_by,
        order_direction=order_direction
    )
    
    response, status_code = await controller.get_sales_by_employee(employee_id, search_criteria)
    
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response)
    
    return response


@sale_router.get("/analytics/statistics", summary="Estatísticas de vendas", description="Relatório com estatísticas gerais de vendas")
async def get_sales_statistics(
    start_date: Optional[date] = Query(None, description="Data inicial"),
    end_date: Optional[date] = Query(None, description="Data final"),
    controller: SaleController = Depends(get_sale_controller)
):
    """
    Busca estatísticas de vendas.
    
    Retorna:
    - Total de vendas e valores
    - Vendas por status e forma de pagamento
    - Top performers (vendedores)
    - Valores médios e totais de comissão
    
    - **start_date**: Data inicial (opcional)
    - **end_date**: Data final (opcional)
    """
    response, status_code = await controller.get_sales_statistics(start_date, end_date)
    
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response)
    
    return response
