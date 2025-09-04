"""
Rotas para gerenciamento de imagens de veículos.
Implements REST endpoints following Postman collection patterns.
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List

from src.adapters.rest.dependencies import get_vehicle_image_controller

vehicle_image_router = APIRouter()


# ===== CAR IMAGE ROUTES =====

@vehicle_image_router.post("/cars/{vehicle_id}/images", status_code=status.HTTP_201_CREATED)
async def upload_car_images(
    vehicle_id: int,
    files: List[UploadFile] = File(...),
    controller=Depends(get_vehicle_image_controller)
):
    """
    Upload de imagens para um carro.
    Seguindo padrão: POST /api/vehicles/cars/{car_id}/images
    """
    try:
        uploaded_images = []
        for file in files:
            allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
            if file.content_type not in allowed_types:
                raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    detail=f"Tipo de arquivo não suportado: {file.content_type}"
                )
            
            result = await controller.upload_image(
                vehicle_id=vehicle_id,
                image_file=file,
                vehicle_type="car"
            )
            uploaded_images.append(result)
        
        return {
            "message": f"{len(uploaded_images)} imagens carregadas com sucesso",
            "images": uploaded_images
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao carregar imagens"
        )


@vehicle_image_router.get("/cars/{vehicle_id}/images")
async def get_car_images(
    vehicle_id: int,
    controller=Depends(get_vehicle_image_controller)
):
    """
    Lista todas as imagens de um carro.
    Seguindo padrão: GET /api/vehicles/cars/{car_id}/images
    """
    try:
        images = await controller.get_vehicle_images(vehicle_id, "car")
        return {
            "vehicle_id": vehicle_id,
            "vehicle_type": "car",
            "images": images,
            "total_count": len(images)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao buscar imagens"
        )


@vehicle_image_router.delete("/cars/{vehicle_id}/images/{image_id}")
async def delete_car_image(
    vehicle_id: int,
    image_id: int,
    controller=Depends(get_vehicle_image_controller)
):
    """
    Remove uma imagem de carro.
    Seguindo padrão: DELETE /api/vehicles/cars/{car_id}/images/{image_id}
    """
    try:
        await controller.delete_image(image_id, vehicle_id)
        return {
            "message": "Imagem removida com sucesso",
            "image_id": image_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao remover imagem"
        )


@vehicle_image_router.patch("/cars/{vehicle_id}/images/primary")
async def set_car_primary_image(
    vehicle_id: int,
    image_data: dict,
    controller=Depends(get_vehicle_image_controller)
):
    """
    Define uma imagem como principal para um carro.
    Seguindo padrão: PATCH /api/vehicles/cars/{car_id}/images/primary
    """
    try:
        image_id = image_data.get("image_id")
        await controller.set_primary_image(vehicle_id, image_id)
        return {
            "message": "Imagem definida como principal com sucesso",
            "vehicle_id": vehicle_id,
            "primary_image_id": image_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao definir imagem principal"
        )


@vehicle_image_router.patch("/cars/{vehicle_id}/images/reorder")
async def reorder_car_images(
    vehicle_id: int,
    reorder_data: dict,
    controller=Depends(get_vehicle_image_controller)
):
    """
    Reordena as imagens de um carro.
    Seguindo padrão: PATCH /api/vehicles/cars/{car_id}/images/reorder
    """
    try:
        image_positions = reorder_data.get("image_positions", [])
        await controller.reorder_images(vehicle_id, image_positions)
        return {
            "message": "Imagens reordenadas com sucesso",
            "vehicle_id": vehicle_id,
            "reordered_count": len(image_positions)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao reordenar imagens"
        )


# ===== MOTORCYCLE IMAGE ROUTES =====

@vehicle_image_router.post("/motorcycles/{vehicle_id}/images", status_code=status.HTTP_201_CREATED)
async def upload_motorcycle_images(
    vehicle_id: int,
    files: List[UploadFile] = File(...),
    controller=Depends(get_vehicle_image_controller)
):
    """
    Upload de imagens para uma motocicleta.
    Seguindo padrão: POST /api/vehicles/motorcycles/{motorcycle_id}/images
    """
    try:
        uploaded_images = []
        for file in files:
            allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
            if file.content_type not in allowed_types:
                raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    detail=f"Tipo de arquivo não suportado: {file.content_type}"
                )
            
            result = await controller.upload_image(
                vehicle_id=vehicle_id,
                image_file=file,
                vehicle_type="motorcycle"
            )
            uploaded_images.append(result)
        
        return {
            "message": f"{len(uploaded_images)} imagens carregadas com sucesso",
            "images": uploaded_images
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao carregar imagens"
        )


@vehicle_image_router.get("/motorcycles/{vehicle_id}/images")
async def get_motorcycle_images(
    vehicle_id: int,
    controller=Depends(get_vehicle_image_controller)
):
    """
    Lista todas as imagens de uma motocicleta.
    Seguindo padrão: GET /api/vehicles/motorcycles/{motorcycle_id}/images
    """
    try:
        images = await controller.get_vehicle_images(vehicle_id, "motorcycle")
        return {
            "vehicle_id": vehicle_id,
            "vehicle_type": "motorcycle",
            "images": images,
            "total_count": len(images)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao buscar imagens"
        )


@vehicle_image_router.delete("/motorcycles/{vehicle_id}/images/{image_id}")
async def delete_motorcycle_image(
    vehicle_id: int,
    image_id: int,
    controller=Depends(get_vehicle_image_controller)
):
    """
    Remove uma imagem de motocicleta.
    Seguindo padrão: DELETE /api/vehicles/motorcycles/{motorcycle_id}/images/{image_id}
    """
    try:
        await controller.delete_image(image_id, vehicle_id)
        return {
            "message": "Imagem removida com sucesso",
            "image_id": image_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao remover imagem"
        )


@vehicle_image_router.patch("/motorcycles/{vehicle_id}/images/primary")
async def set_motorcycle_primary_image(
    vehicle_id: int,
    image_data: dict,
    controller=Depends(get_vehicle_image_controller)
):
    """
    Define uma imagem como principal para uma motocicleta.
    Seguindo padrão: PATCH /api/vehicles/motorcycles/{motorcycle_id}/images/primary
    """
    try:
        image_id = image_data.get("image_id")
        await controller.set_primary_image(vehicle_id, image_id)
        return {
            "message": "Imagem definida como principal com sucesso",
            "vehicle_id": vehicle_id,
            "primary_image_id": image_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao definir imagem principal"
        )


@vehicle_image_router.patch("/motorcycles/{vehicle_id}/images/reorder")
async def reorder_motorcycle_images(
    vehicle_id: int,
    reorder_data: dict,
    controller=Depends(get_vehicle_image_controller)
):
    """
    Reordena as imagens de uma motocicleta.
    Seguindo padrão: PATCH /api/vehicles/motorcycles/{motorcycle_id}/images/reorder
    """
    try:
        image_positions = reorder_data.get("image_positions", [])
        await controller.reorder_images(vehicle_id, image_positions)
        return {
            "message": "Imagens reordenadas com sucesso",
            "vehicle_id": vehicle_id,
            "reordered_count": len(image_positions)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao reordenar imagens"
        )
