"""
Rotas REST para Motorcycles - Adapters Layer

Define os endpoints da API para gerenciamento de motocicletas.
Aplicando padrões REST e Clean Architecture.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from src.application.dtos.motorcycle_dto import (
    MotorcycleCreateDto, MotorcycleUpdateDto, MotorcycleSearchDto
)
from src.adapters.rest.controllers.motorcycle_controller import MotorcycleController
from src.adapters.rest.dependencies import get_motorcycle_controller


# Criar router para motocicletas
motorcycle_router = APIRouter(
    tags=["Motorcycles"],
    responses={
        404: {"description": "Motocicleta não encontrada"},
        422: {"description": "Regra de negócio violada"},
        500: {"description": "Erro interno do servidor"}
    }
)


@motorcycle_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Criar motocicleta",
    description="Cria uma nova motocicleta no sistema"
)
async def create_motorcycle(
    motorcycle_data: MotorcycleCreateDto,
    controller: MotorcycleController = Depends(get_motorcycle_controller)
) -> JSONResponse:
    """
    Cria uma nova motocicleta.
    
    - **brand**: Marca da motocicleta
    - **model**: Modelo da motocicleta
    - **year**: Ano de fabricação
    - **price**: Preço de venda
    - **mileage**: Quilometragem
    - **fuel_type**: Tipo de combustível
    - **color**: Cor do veículo
    - **starter**: Tipo de partida
    - **fuel_system**: Sistema de combustível
    - **engine_displacement**: Cilindrada do motor
    - **cooling**: Sistema de arrefecimento
    - **style**: Estilo da moto
    - **engine_type**: Tipo de motor
    - **gears**: Número de marchas
    - **front_rear_brake**: Sistema de freios
    """
    return await controller.create_motorcycle(motorcycle_data)


@motorcycle_router.get(
    "/{motorcycle_id}",
    status_code=status.HTTP_200_OK,
    summary="Buscar motocicleta por ID",
    description="Busca uma motocicleta específica pelo ID"
)
async def get_motorcycle_by_id(
    motorcycle_id: UUID,
    controller: MotorcycleController = Depends(get_motorcycle_controller)
) -> JSONResponse:
    """
    Busca uma motocicleta pelo ID.
    
    - **motorcycle_id**: ID único da motocicleta (UUID)
    """
    return await controller.get_motorcycle_by_id(motorcycle_id)


@motorcycle_router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Listar motocicletas",
    description="Lista motocicletas com filtros e paginação"
)
async def list_motorcycles(
    brand: Optional[str] = Query(None, description="Filtrar por marca"),
    model: Optional[str] = Query(None, description="Filtrar por modelo"),
    min_year: Optional[int] = Query(None, description="Ano mínimo"),
    max_year: Optional[int] = Query(None, description="Ano máximo"),
    min_price: Optional[float] = Query(None, description="Preço mínimo"),
    max_price: Optional[float] = Query(None, description="Preço máximo"),
    fuel_type: Optional[str] = Query(None, description="Tipo de combustível"),
    color: Optional[str] = Query(None, description="Cor"),
    style: Optional[str] = Query(None, description="Estilo"),
    min_displacement: Optional[int] = Query(None, description="Cilindrada mínima"),
    max_displacement: Optional[int] = Query(None, description="Cilindrada máxima"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Tamanho da página"),
    controller: MotorcycleController = Depends(get_motorcycle_controller)
) -> JSONResponse:
    """
    Lista motocicletas com filtros opcionais e paginação.
    """
    search_dto = MotorcycleSearchDto(
        brand=brand,
        model=model,
        min_year=min_year,
        max_year=max_year,
        min_price=min_price,
        max_price=max_price,
        fuel_type=fuel_type,
        color=color,
        style=style,
        min_displacement=min_displacement,
        max_displacement=max_displacement,
        page=page,
        page_size=page_size
    )
    return await controller.search_motorcycles(search_dto)


@motorcycle_router.put(
    "/{motorcycle_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizar motocicleta",
    description="Atualiza os dados de uma motocicleta existente"
)
async def update_motorcycle(
    motorcycle_id: UUID,
    motorcycle_data: MotorcycleUpdateDto,
    controller: MotorcycleController = Depends(get_motorcycle_controller)
) -> JSONResponse:
    """Atualiza os dados de uma motocicleta."""
    return await controller.update_motorcycle(motorcycle_id, motorcycle_data)


@motorcycle_router.delete(
    "/{motorcycle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar motocicleta",
    description="Remove uma motocicleta do sistema"
)
async def delete_motorcycle(
    motorcycle_id: UUID,
    controller: MotorcycleController = Depends(get_motorcycle_controller)
) -> JSONResponse:
    """Remove uma motocicleta do sistema."""
    return await controller.delete_motorcycle(motorcycle_id)
