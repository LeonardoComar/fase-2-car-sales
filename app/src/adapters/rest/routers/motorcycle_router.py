"""
Rotas REST para Motorcycles - Adapters Layer

Define os endpoints da API para gerenciamento de motocicletas.
Aplicando padrões REST e Clean Architecture.
"""

from typing import Optional
import logging

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from src.application.dtos.motorcycle_dto import (
    MotorcycleCreateDto, MotorcycleUpdateNestedDto, MotorcycleSearchDto
)
from src.adapters.rest.controllers.motorcycle_controller import MotorcycleController
from src.adapters.rest.dependencies import get_motorcycle_controller

# Setup logging
logger = logging.getLogger(__name__)


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
    motorcycle_id: int,
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
    model: Optional[str] = Query(None, description="Filtrar por modelo"),
    min_price: Optional[float] = Query(None, description="Preço mínimo"),
    max_price: Optional[float] = Query(None, description="Preço máximo"),
    fuel_type: Optional[str] = Query(None, description="Tipo de combustível"),
    status: Optional[str] = Query(None, description="Status do veículo"),
    motorcycle_type: Optional[str] = Query(None, description="Tipo de motocicleta"),
    min_displacement: Optional[int] = Query(None, description="Cilindrada mínima"),
    max_displacement: Optional[int] = Query(None, description="Cilindrada máxima"),
    order_by_price: Optional[str] = Query(None, description="Ordenação por preço (asc/desc)"),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(20, ge=1, le=100, description="Número máximo de registros"),
    controller: MotorcycleController = Depends(get_motorcycle_controller)
) -> JSONResponse:
    """
    Lista motocicletas com filtros opcionais e paginação.
    """
    try:
        logger.info(f"🔍 [MOTORCYCLE_ROUTES] Recebendo requisição para listar motocicletas")
        logger.info(f"🔍 [MOTORCYCLE_ROUTES] Parâmetros: model={model}, min_price={min_price}, max_price={max_price}")
        logger.info(f"🔍 [MOTORCYCLE_ROUTES] Parâmetros: fuel_type={fuel_type}, status={status}, motorcycle_type={motorcycle_type}")
        logger.info(f"🔍 [MOTORCYCLE_ROUTES] Parâmetros: min_displacement={min_displacement}, max_displacement={max_displacement}")
        logger.info(f"🔍 [MOTORCYCLE_ROUTES] Parâmetros: order_by_price={order_by_price}, skip={skip}, limit={limit}")
        
        logger.info("🔍 [MOTORCYCLE_ROUTES] Criando MotorcycleSearchDto...")
        search_dto = MotorcycleSearchDto(
            model=model,
            price_min=min_price,
            price_max=max_price,
            fuel_type=fuel_type,
            status=status,
            style=motorcycle_type,  # Mantém o parâmetro motorcycle_type mas mapeia para style
            engine_displacement_min=min_displacement,
            engine_displacement_max=max_displacement,
            order_by_price=order_by_price,
            skip=skip,
            limit=limit
        )
        logger.info(f"🔍 [MOTORCYCLE_ROUTES] DTO criado com sucesso: {search_dto}")
        
        logger.info("🔍 [MOTORCYCLE_ROUTES] Chamando controller.search_motorcycles...")
        result = await controller.search_motorcycles(search_dto)
        logger.info(f"🔍 [MOTORCYCLE_ROUTES] Controller retornou resultado com sucesso")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ [MOTORCYCLE_ROUTES] Erro na rota list_motorcycles: {str(e)}", exc_info=True)
        raise e


@motorcycle_router.put(
    "/{motorcycle_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizar motocicleta",
    description="Atualiza os dados de uma motocicleta existente"
)
async def update_motorcycle(
    motorcycle_id: int,
    motorcycle_data: MotorcycleUpdateNestedDto,
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
    motorcycle_id: int,
    controller: MotorcycleController = Depends(get_motorcycle_controller)
) -> JSONResponse:
    """Remove uma motocicleta do sistema."""
    return await controller.delete_motorcycle(motorcycle_id)


@motorcycle_router.patch(
    "/{motorcycle_id}/deactivate",
    status_code=status.HTTP_200_OK,
    summary="Desativar motocicleta",
    description="Desativa uma motocicleta (muda status para Inativo)"
)
async def deactivate_motorcycle(
    motorcycle_id: int,
    controller: MotorcycleController = Depends(get_motorcycle_controller)
) -> JSONResponse:
    """Desativa uma motocicleta."""
    return await controller.deactivate_motorcycle(motorcycle_id)


@motorcycle_router.patch(
    "/{motorcycle_id}/activate",
    status_code=status.HTTP_200_OK,
    summary="Ativar motocicleta",
    description="Ativa uma motocicleta (muda status para Ativo)"
)
async def activate_motorcycle(
    motorcycle_id: int,
    controller: MotorcycleController = Depends(get_motorcycle_controller)
) -> JSONResponse:
    """Ativa uma motocicleta."""
    return await controller.activate_motorcycle(motorcycle_id)
