"""
Router para VehicleImages - Interface Layer

Define as rotas HTTP para operações relacionadas a imagens de veículos.

Aplicando princípios SOLID:
- SRP: Responsável apenas por definir rotas de imagens de veículos
- OCP: Extensível para novas rotas sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para rotas de imagens de veículos
- DIP: Depende de abstrações (controllers) não de implementações
"""

from typing import Optional
from fastapi import APIRouter, Depends, Path, Body, UploadFile, File, Form, HTTPException
from src.adapters.rest.controllers.vehicle_image_controller import VehicleImageController
from src.adapters.rest.dependencies import get_vehicle_image_controller
from src.application.dtos.vehicle_image_dto import (
    VehicleImageCreateDTO,
    VehicleImageUpdateDTO,
    VehicleImageResponseDTO,
    VehicleImageListResponseDTO,
    VehicleImageUploadResponseDTO
)

# Criar o router diretamente
vehicle_image_router = APIRouter()

@vehicle_image_router.post(
    "/cars/{car_id}/images",
    response_model=VehicleImageUploadResponseDTO,
    status_code=201,
    summary="Adicionar imagem ao carro",
    description="Faz upload de uma imagem para um carro específico.",
    responses={
        201: {"description": "Imagem criada com sucesso"},
        400: {"description": "Arquivo inválido ou ID do carro inválido"},
        422: {"description": "Regra de negócio violada"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def add_car_image(
    car_id: int = Path(..., gt=0, description="ID do carro"),
    file: Optional[UploadFile] = File(None, description="Arquivo de imagem"),
    files: Optional[UploadFile] = File(None, description="Arquivo de imagem (alternativo)"),
    position: Optional[int] = Form(None, description="Posição da imagem"),
    is_primary: bool = Form(False, description="Se é a imagem principal"),
    controller: VehicleImageController = Depends(get_vehicle_image_controller)
) -> VehicleImageUploadResponseDTO:
    """Faz upload de uma imagem para o carro especificado."""
    
    # Verificar qual campo foi usado
    upload_file = file or files
    
    if not upload_file:
        raise HTTPException(
            status_code=400,
            detail="É necessário enviar um arquivo de imagem no campo 'file' ou 'files'"
        )
    
    # Usar o serviço de imagens para processar o upload
    from src.application.services.vehicle_image_service import VehicleImageService
    image_service = VehicleImageService()
    
    # Processar e salvar a imagem
    filename, file_path, thumbnail_path = await image_service.process_and_save_image(upload_file, car_id)
    
    # Criar DTO com os dados
    from src.application.dtos.vehicle_image_dto import VehicleImageCreateDTO
    image_data = VehicleImageCreateDTO(
        vehicle_id=car_id,
        filename=filename,
        path=file_path,
        thumbnail_path=thumbnail_path,
        position=position,
        is_primary=is_primary
    )
    
    return await controller.create_vehicle_image(image_data)

@vehicle_image_router.post(
    "/motorcycles/{motorcycle_id}/images",
    response_model=VehicleImageUploadResponseDTO,
    status_code=201,
    summary="Adicionar imagem à motocicleta",
    description="Faz upload de uma imagem para uma motocicleta específica.",
    responses={
        201: {"description": "Imagem criada com sucesso"},
        400: {"description": "Arquivo inválido ou ID da motocicleta inválido"},
        422: {"description": "Regra de negócio violada"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def add_motorcycle_image(
    motorcycle_id: int = Path(..., gt=0, description="ID da motocicleta"),
    file: Optional[UploadFile] = File(None, description="Arquivo de imagem"),
    files: Optional[UploadFile] = File(None, description="Arquivo de imagem (alternativo)"),
    position: Optional[int] = Form(None, description="Posição da imagem"),
    is_primary: bool = Form(False, description="Se é a imagem principal"),
    controller: VehicleImageController = Depends(get_vehicle_image_controller)
) -> VehicleImageUploadResponseDTO:
    """Faz upload de uma imagem para a motocicleta especificada."""
    
    # Verificar qual campo foi usado
    upload_file = file or files
    
    if not upload_file:
        raise HTTPException(
            status_code=400,
            detail="É necessário enviar um arquivo de imagem no campo 'file' ou 'files'"
        )
    
    # Usar o serviço de imagens para processar o upload
    from src.application.services.vehicle_image_service import VehicleImageService
    image_service = VehicleImageService()
    
    # Processar e salvar a imagem - usando "motorcycles" como tipo de veículo
    filename, file_path, thumbnail_path = await image_service.process_and_save_image(upload_file, motorcycle_id, vehicle_type="motorcycles")
    
    # Criar DTO com os dados
    from src.application.dtos.vehicle_image_dto import VehicleImageCreateDTO
    image_data = VehicleImageCreateDTO(
        vehicle_id=motorcycle_id,
        filename=filename,
        path=file_path,
        thumbnail_path=thumbnail_path,
        position=position,
        is_primary=is_primary
    )
    
    return await controller.create_vehicle_image(image_data)

@vehicle_image_router.get(
    "/images/{image_id}",
    response_model=VehicleImageResponseDTO,
    summary="Buscar imagem por ID",
    description="Busca uma imagem específica pelo seu ID.",
    responses={
        200: {"description": "Imagem encontrada"},
        404: {"description": "Imagem não encontrada"},
        400: {"description": "ID inválido"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def get_image_by_id(
    image_id: int = Path(..., gt=0, description="ID da imagem"),
    controller: VehicleImageController = Depends(get_vehicle_image_controller)
) -> VehicleImageResponseDTO:
    """Busca uma imagem por ID."""
    return await controller.get_vehicle_image_by_id(image_id)

@vehicle_image_router.get(
    "/cars/{car_id}/images",
    response_model=VehicleImageListResponseDTO,
    summary="Listar imagens do carro",
    description="Lista todas as imagens de um carro específico, ordenadas por posição.",
    responses={
        200: {"description": "Lista de imagens retornada com sucesso"},
        400: {"description": "ID do carro inválido"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def list_car_images(
    car_id: int = Path(..., gt=0, description="ID do carro"),
    controller: VehicleImageController = Depends(get_vehicle_image_controller)
) -> VehicleImageListResponseDTO:
    """Lista todas as imagens de um carro específico."""
    return await controller.get_vehicle_images(car_id)

@vehicle_image_router.get(
    "/cars/{car_id}/images/primary",
    response_model=Optional[VehicleImageResponseDTO],
    summary="Buscar imagem principal do carro",
    description="Busca a imagem principal de um carro específico.",
    responses={
        200: {"description": "Imagem principal encontrada ou nenhuma imagem principal"},
        400: {"description": "ID do carro inválido"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def get_car_primary_image(
    car_id: int = Path(..., gt=0, description="ID do carro"),
    controller: VehicleImageController = Depends(get_vehicle_image_controller)
) -> Optional[VehicleImageResponseDTO]:
    """Busca a imagem principal de um carro específico."""
    return await controller.get_primary_vehicle_image(car_id)

@vehicle_image_router.patch(
    "/images/{image_id}",
    response_model=VehicleImageResponseDTO,
    summary="Atualizar imagem",
    description="Atualiza propriedades de uma imagem existente (posição, status principal).",
    responses={
        200: {"description": "Imagem atualizada com sucesso"},
        404: {"description": "Imagem não encontrada"},
        400: {"description": "Dados inválidos"},
        422: {"description": "Regra de negócio violada"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def update_image(
    image_id: int = Path(..., gt=0, description="ID da imagem"),
    update_data: VehicleImageUpdateDTO = Body(..., description="Dados para atualização"),
    controller: VehicleImageController = Depends(get_vehicle_image_controller)
) -> VehicleImageResponseDTO:
    """Atualiza uma imagem."""
    return await controller.update_vehicle_image(image_id, update_data)

@vehicle_image_router.patch(
    "/images/{image_id}/set-primary",
    response_model=VehicleImageResponseDTO,
    summary="Definir como imagem principal",
    description="Define uma imagem como principal, removendo o status principal de outras imagens do mesmo carro.",
    responses={
        200: {"description": "Imagem definida como principal com sucesso"},
        404: {"description": "Imagem não encontrada"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def set_image_as_primary(
    image_id: int = Path(..., gt=0, description="ID da imagem"),
    controller: VehicleImageController = Depends(get_vehicle_image_controller)
) -> VehicleImageResponseDTO:
    """Define uma imagem como principal."""
    return await controller.set_primary_image(image_id)

@vehicle_image_router.delete(
    "/images/{image_id}",
    summary="Remover imagem",
    description="Remove uma imagem de carro. Se a imagem for principal, automaticamente define outra como principal.",
    responses={
        200: {"description": "Imagem removida com sucesso"},
        404: {"description": "Imagem não encontrada"},
        422: {"description": "Não é possível remover a única imagem do carro"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def delete_image(
    image_id: int = Path(..., gt=0, description="ID da imagem"),
    controller: VehicleImageController = Depends(get_vehicle_image_controller)
) -> dict:
    """Remove uma imagem."""
    return await controller.delete_vehicle_image(image_id)
