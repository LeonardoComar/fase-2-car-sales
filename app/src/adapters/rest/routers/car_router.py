"""
Rotas REST para Cars - Adapters Layer

Define os endpoints da API para gerenciamento de carros.
Aplicando padrões REST e Clean Architecture.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from src.application.dtos.car_dto import (
    CarCreateDto, CarUpdateNestedDto, CarSearchDto
)
from src.adapters.rest.controllers.car_controller import CarController
from src.adapters.rest.dependencies import get_car_controller


# Criar router para carros
car_router = APIRouter(
    tags=["Cars"],
    responses={
        404: {"description": "Carro não encontrado"},
        422: {"description": "Regra de negócio violada"},
        500: {"description": "Erro interno do servidor"}
    }
)


@car_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Criar carro",
    description="Cria um novo carro no sistema"
)
async def create_car(
    car_data: CarCreateDto,
    controller: CarController = Depends(get_car_controller)
) -> JSONResponse:
    """
    Cria um novo carro.
    
    - **model**: Modelo do carro
    - **year**: Ano de fabricação
    - **price**: Preço de venda
    - **mileage**: Quilometragem
    - **fuel_type**: Tipo de combustível
    - **color**: Cor do veículo
    - **bodywork**: Tipo de carroceria
    - **transmission**: Tipo de transmissão
    """
    return await controller.create_car(car_data)


@car_router.get(
    "/{car_id}",
    status_code=status.HTTP_200_OK,
    summary="Buscar carro por ID",
    description="Busca um carro específico pelo ID"
)
async def get_car_by_id(
    car_id: int,
    controller: CarController = Depends(get_car_controller)
) -> JSONResponse:
    """
    Busca um carro pelo ID.
    
    - **car_id**: ID único do carro (int)
    """
    return await controller.get_car_by_id(car_id)


@car_router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Listar carros",
    description="Lista carros com filtros e paginação"
)
async def list_cars(
    model: Optional[str] = Query(None, description="Filtrar por modelo"),
    year: Optional[str] = Query(None, description="Ano do veículo"),
    min_price: Optional[float] = Query(None, description="Preço mínimo"),
    max_price: Optional[float] = Query(None, description="Preço máximo"),
    fuel_type: Optional[str] = Query(None, description="Tipo de combustível"),
    color: Optional[str] = Query(None, description="Cor"),
    bodywork: Optional[str] = Query(None, description="Carroceria"),
    transmission: Optional[str] = Query(None, description="Transmissão"),
    city: Optional[str] = Query(None, description="Cidade"),
    status: Optional[str] = Query(None, description="Status do veículo"),
    order_by_price: Optional[str] = Query(None, description="Ordenação por preço (asc/desc)"),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(20, ge=1, le=100, description="Número máximo de registros"),
    controller: CarController = Depends(get_car_controller)
) -> JSONResponse:
    """
    Lista carros com filtros opcionais e paginação.
    """
    search_dto = CarSearchDto(
        model=model,
        year=year,
        min_price=min_price,
        max_price=max_price,
        fuel_type=fuel_type,
        color=color,
        bodywork=bodywork,
        transmission=transmission,
        city=city,
        status=status,
        order_by_price=order_by_price,
        skip=skip,
        limit=limit
    )
    return await controller.search_cars(search_dto)


@car_router.put(
    "/{car_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizar carro",
    description="Atualiza os dados de um carro existente"
)
async def update_car(
    car_id: int,
    car_data: CarUpdateNestedDto,
    controller: CarController = Depends(get_car_controller)
) -> JSONResponse:
    """Atualiza os dados de um carro."""
    return await controller.update_car(car_id, car_data)


@car_router.delete(
    "/{car_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar carro",
    description="Remove um carro do sistema"
)
async def delete_car(
    car_id: int,
    controller: CarController = Depends(get_car_controller)
) -> JSONResponse:
    """Remove um carro do sistema."""
    return await controller.delete_car(car_id)


@car_router.patch(
    "/{car_id}/deactivate",
    status_code=status.HTTP_200_OK,
    summary="Desativar carro",
    description="Desativa um carro (muda status para Inativo)"
)
async def deactivate_car(
    car_id: int,
    controller: CarController = Depends(get_car_controller)
) -> JSONResponse:
    """Desativa um carro."""
    return await controller.deactivate_car(car_id)


@car_router.patch(
    "/{car_id}/activate",
    status_code=status.HTTP_200_OK,
    summary="Ativar carro",
    description="Ativa um carro (muda status para Ativo)"
)
async def activate_car(
    car_id: int,
    controller: CarController = Depends(get_car_controller)
) -> JSONResponse:
    """Ativa um carro."""
    return await controller.activate_car(car_id)
