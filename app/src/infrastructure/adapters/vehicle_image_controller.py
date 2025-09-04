"""
Controllers REST para VehicleImage - Adapters Layer

Implementa os endpoints da API para gerenciamento de imagens de veículos.
Aplica padrões REST e Clean Architecture, delegando para use cases.

Aplicando princípios SOLID:
- SRP: Cada controller tem responsabilidade específica
- OCP: Extensível para novos endpoints sem modificar existentes
- LSP: Controllers podem ser substituídos sem afetar comportamento
- ISP: Interfaces específicas para cada operação
- DIP: Dependem de abstrações (use cases), não de implementações
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile, Form
from fastapi.responses import JSONResponse

from ...application.dtos.vehicle_image_dto import (
    VehicleImageCreateDto,
    VehicleImageUpdateDto,
    VehicleImageResponseDto,
    VehicleImageSearchDto,
    VehicleImageReorderDto,
    VehicleGalleryDto,
    VehicleImageStatisticsDto
)
from ...application.services.vehicle_image_service import (
    CreateVehicleImageUseCase,
    UpdateVehicleImageUseCase,
    DeleteVehicleImageUseCase,
    GetVehicleImageUseCase,
    SearchVehicleImagesUseCase,
    GetVehicleGalleryUseCase,
    ReorderVehicleImagesUseCase,
    SetPrimaryImageUseCase,
    GenerateThumbnailUseCase,
    GetImageStatisticsUseCase
)


class VehicleImageController:
    """
    Controller para operações de imagens de veículos.
    
    Centraliza todos os endpoints relacionados ao gerenciamento
    de imagens, aplicando validações e tratamento de erros.
    """
    
    def __init__(
        self,
        create_use_case: CreateVehicleImageUseCase,
        update_use_case: UpdateVehicleImageUseCase,
        delete_use_case: DeleteVehicleImageUseCase,
        get_use_case: GetVehicleImageUseCase,
        search_use_case: SearchVehicleImagesUseCase,
        gallery_use_case: GetVehicleGalleryUseCase,
        reorder_use_case: ReorderVehicleImagesUseCase,
        set_primary_use_case: SetPrimaryImageUseCase,
        generate_thumbnail_use_case: GenerateThumbnailUseCase,
        statistics_use_case: GetImageStatisticsUseCase
    ):
        self._create_use_case = create_use_case
        self._update_use_case = update_use_case
        self._delete_use_case = delete_use_case
        self._get_use_case = get_use_case
        self._search_use_case = search_use_case
        self._gallery_use_case = gallery_use_case
        self._reorder_use_case = reorder_use_case
        self._set_primary_use_case = set_primary_use_case
        self._generate_thumbnail_use_case = generate_thumbnail_use_case
        self._statistics_use_case = statistics_use_case
    
    async def upload_image(
        self,
        vehicle_id: UUID,
        file: UploadFile = File(...),
        position: Optional[int] = Form(None),
        is_primary: bool = Form(False)
    ) -> VehicleImageResponseDto:
        """
        Upload de uma nova imagem para um veículo.
        
        Args:
            vehicle_id: ID do veículo
            file: Arquivo de imagem
            position: Posição na galeria (opcional)
            is_primary: Se é a imagem principal
            
        Returns:
            Dados da imagem criada
            
        Raises:
            HTTPException: Se dados inválidos ou erro no upload
        """
        try:
            # Validar tipo do arquivo
            if not file.content_type or not file.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Arquivo deve ser uma imagem"
                )
            
            # Validar tamanho
            file_size = 0
            content = await file.read()
            file_size = len(content)
            
            if file_size > 10 * 1024 * 1024:  # 10MB
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="Arquivo muito grande. Máximo: 10MB"
                )
            
            await file.seek(0)  # Reset file pointer
            
            # Gerar nome único para o arquivo
            import os
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{file.filename}"
            
            # Definir caminho de armazenamento
            storage_path = f"/uploads/vehicles/{vehicle_id}/{filename}"
            
            # Criar DTO para criação
            create_dto = VehicleImageCreateDto(
                vehicle_id=vehicle_id,
                filename=filename,
                path=storage_path,
                position=position or 1,
                is_primary=is_primary,
                file_size=file_size,
                mime_type=file.content_type
            )
            
            # Salvar arquivo físico (seria implementado no ImageManager)
            # Por agora, apenas simular o salvamento
            
            # Executar use case
            result = await self._create_use_case.execute(create_dto)
            
            return result
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno no upload da imagem"
            )
    
    async def create_image(self, dto: VehicleImageCreateDto) -> VehicleImageResponseDto:
        """
        Cria uma nova imagem de veículo.
        
        Args:
            dto: Dados da imagem
            
        Returns:
            Dados da imagem criada
        """
        try:
            return await self._create_use_case.execute(dto)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na criação da imagem"
            )
    
    async def update_image(
        self, 
        image_id: UUID, 
        dto: VehicleImageUpdateDto
    ) -> VehicleImageResponseDto:
        """
        Atualiza uma imagem de veículo.
        
        Args:
            image_id: ID da imagem
            dto: Dados para atualização
            
        Returns:
            Dados da imagem atualizada
        """
        try:
            return await self._update_use_case.execute(image_id, dto)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na atualização da imagem"
            )
    
    async def delete_image(self, image_id: UUID) -> Dict[str, Any]:
        """
        Exclui uma imagem de veículo.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            Confirmação da exclusão
        """
        try:
            success = await self._delete_use_case.execute(image_id)
            
            if success:
                return {
                    "message": "Imagem excluída com sucesso",
                    "image_id": str(image_id)
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Imagem não encontrada"
                )
                
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na exclusão da imagem"
            )
    
    async def get_image(self, image_id: UUID) -> VehicleImageResponseDto:
        """
        Obtém uma imagem por ID.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            Dados da imagem
        """
        try:
            return await self._get_use_case.execute(image_id)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na obtenção da imagem"
            )
    
    async def search_images(self, dto: VehicleImageSearchDto) -> Dict[str, Any]:
        """
        Busca imagens com filtros.
        
        Args:
            dto: Critérios de busca
            
        Returns:
            Lista de imagens e metadados de paginação
        """
        try:
            images, total = await self._search_use_case.execute(dto)
            
            return {
                "images": images,
                "pagination": {
                    "total": total,
                    "skip": dto.skip,
                    "limit": dto.limit,
                    "has_next": (dto.skip + dto.limit) < total,
                    "has_previous": dto.skip > 0
                }
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na busca de imagens"
            )
    
    async def get_vehicle_gallery(self, vehicle_id: UUID) -> VehicleGalleryDto:
        """
        Obtém a galeria completa de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Galeria com todas as imagens
        """
        try:
            return await self._gallery_use_case.execute(vehicle_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na obtenção da galeria"
            )
    
    async def reorder_images(
        self, 
        vehicle_id: UUID, 
        dto: VehicleImageReorderDto
    ) -> List[VehicleImageResponseDto]:
        """
        Reordena as imagens de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            dto: Novas posições das imagens
            
        Returns:
            Lista de imagens reordenadas
        """
        try:
            return await self._reorder_use_case.execute(vehicle_id, dto)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na reordenação das imagens"
            )
    
    async def set_primary_image(self, image_id: UUID) -> VehicleImageResponseDto:
        """
        Define uma imagem como principal do veículo.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            Dados da imagem definida como principal
        """
        try:
            return await self._set_primary_use_case.execute(image_id)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na definição da imagem principal"
            )
    
    async def generate_thumbnail(self, image_id: UUID) -> VehicleImageResponseDto:
        """
        Gera miniatura para uma imagem.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            Dados da imagem com miniatura
        """
        try:
            return await self._generate_thumbnail_use_case.execute(image_id)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except RuntimeError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na geração da miniatura"
            )
    
    async def get_statistics(self) -> VehicleImageStatisticsDto:
        """
        Obtém estatísticas das imagens.
        
        Returns:
            Estatísticas completas das imagens
        """
        try:
            return await self._statistics_use_case.execute()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno na obtenção das estatísticas"
            )


def create_vehicle_image_router(
    create_use_case: CreateVehicleImageUseCase,
    update_use_case: UpdateVehicleImageUseCase,
    delete_use_case: DeleteVehicleImageUseCase,
    get_use_case: GetVehicleImageUseCase,
    search_use_case: SearchVehicleImagesUseCase,
    gallery_use_case: GetVehicleGalleryUseCase,
    reorder_use_case: ReorderVehicleImagesUseCase,
    set_primary_use_case: SetPrimaryImageUseCase,
    generate_thumbnail_use_case: GenerateThumbnailUseCase,
    statistics_use_case: GetImageStatisticsUseCase
) -> APIRouter:
    """
    Factory para criar o router de imagens de veículos.
    
    Args:
        *_use_case: Injeção de dependência dos use cases
        
    Returns:
        Router configurado com todos os endpoints
    """
    
    router = APIRouter(prefix="/vehicle-images", tags=["Vehicle Images"])
    
    controller = VehicleImageController(
        create_use_case=create_use_case,
        update_use_case=update_use_case,
        delete_use_case=delete_use_case,
        get_use_case=get_use_case,
        search_use_case=search_use_case,
        gallery_use_case=gallery_use_case,
        reorder_use_case=reorder_use_case,
        set_primary_use_case=set_primary_use_case,
        generate_thumbnail_use_case=generate_thumbnail_use_case,
        statistics_use_case=statistics_use_case
    )
    
    @router.post("/upload/{vehicle_id}", 
                response_model=VehicleImageResponseDto,
                status_code=status.HTTP_201_CREATED)
    async def upload_vehicle_image(
        vehicle_id: UUID,
        file: UploadFile = File(...),
        position: Optional[int] = Form(None),
        is_primary: bool = Form(False)
    ):
        """Upload de nova imagem para um veículo."""
        return await controller.upload_image(vehicle_id, file, position, is_primary)
    
    @router.post("/", 
                response_model=VehicleImageResponseDto,
                status_code=status.HTTP_201_CREATED)
    async def create_vehicle_image(dto: VehicleImageCreateDto):
        """Cria uma nova imagem de veículo."""
        return await controller.create_image(dto)
    
    @router.put("/{image_id}", response_model=VehicleImageResponseDto)
    async def update_vehicle_image(image_id: UUID, dto: VehicleImageUpdateDto):
        """Atualiza uma imagem de veículo."""
        return await controller.update_image(image_id, dto)
    
    @router.delete("/{image_id}")
    async def delete_vehicle_image(image_id: UUID):
        """Exclui uma imagem de veículo."""
        return await controller.delete_image(image_id)
    
    @router.get("/{image_id}", response_model=VehicleImageResponseDto)
    async def get_vehicle_image(image_id: UUID):
        """Obtém uma imagem por ID."""
        return await controller.get_image(image_id)
    
    @router.post("/search")
    async def search_vehicle_images(dto: VehicleImageSearchDto):
        """Busca imagens com filtros."""
        return await controller.search_images(dto)
    
    @router.get("/vehicle/{vehicle_id}/gallery", response_model=VehicleGalleryDto)
    async def get_vehicle_gallery(vehicle_id: UUID):
        """Obtém a galeria completa de um veículo."""
        return await controller.get_vehicle_gallery(vehicle_id)
    
    @router.put("/vehicle/{vehicle_id}/reorder", 
               response_model=List[VehicleImageResponseDto])
    async def reorder_vehicle_images(vehicle_id: UUID, dto: VehicleImageReorderDto):
        """Reordena as imagens de um veículo."""
        return await controller.reorder_images(vehicle_id, dto)
    
    @router.patch("/{image_id}/set-primary", response_model=VehicleImageResponseDto)
    async def set_primary_image(image_id: UUID):
        """Define uma imagem como principal do veículo."""
        return await controller.set_primary_image(image_id)
    
    @router.patch("/{image_id}/generate-thumbnail", 
                 response_model=VehicleImageResponseDto)
    async def generate_thumbnail(image_id: UUID):
        """Gera miniatura para uma imagem."""
        return await controller.generate_thumbnail(image_id)
    
    @router.get("/statistics", response_model=VehicleImageStatisticsDto)
    async def get_image_statistics():
        """Obtém estatísticas das imagens."""
        return await controller.get_statistics()
    
    return router


# ==============================================
# PRESENTERS
# ==============================================

class VehicleImagePresenter:
    """
    Presenter para formatação de respostas de imagens.
    
    Aplica formatações específicas para diferentes contextos
    de apresentação dos dados.
    """
    
    @staticmethod
    def format_image_response(image: VehicleImageResponseDto) -> Dict[str, Any]:
        """
        Formata resposta de imagem com campos computados.
        
        Args:
            image: DTO da imagem
            
        Returns:
            Dados formatados para resposta
        """
        return {
            "id": str(image.id),
            "vehicle_id": str(image.vehicle_id),
            "filename": image.filename,
            "path": image.path,
            "thumbnail_path": image.thumbnail_path,
            "position": image.position,
            "is_primary": image.is_primary,
            "file_info": {
                "size_mb": image.file_size_mb,
                "dimensions": f"{image.width}x{image.height}" if image.width and image.height else None,
                "aspect_ratio": image.aspect_ratio,
                "orientation": (
                    "landscape" if image.is_landscape else
                    "portrait" if image.is_portrait else
                    "square" if image.is_square else
                    "unknown"
                ),
                "format": image.file_extension,
                "mime_type": image.mime_type
            },
            "status": {
                "has_thumbnail": image.has_thumbnail,
                "display_name": image.display_name
            },
            "timestamps": {
                "uploaded_at": image.uploaded_at.isoformat(),
                "updated_at": image.updated_at.isoformat()
            }
        }
    
    @staticmethod
    def format_gallery_response(gallery: VehicleGalleryDto) -> Dict[str, Any]:
        """
        Formata resposta de galeria com organização visual.
        
        Args:
            gallery: DTO da galeria
            
        Returns:
            Dados formatados para galeria
        """
        return {
            "vehicle_id": str(gallery.vehicle_id),
            "summary": {
                "total_images": gallery.total_images,
                "has_primary": gallery.primary_image is not None,
                "gallery_info": gallery.gallery_info
            },
            "primary_image": (
                VehicleImagePresenter.format_image_response(gallery.primary_image)
                if gallery.primary_image else None
            ),
            "images": [
                VehicleImagePresenter.format_image_response(img)
                for img in gallery.images
            ],
            "organization": {
                "by_position": {
                    str(img.position): VehicleImagePresenter.format_image_response(img)
                    for img in gallery.images
                },
                "primary_first": sorted(
                    gallery.images,
                    key=lambda x: (not x.is_primary, x.position)
                )
            }
        }
    
    @staticmethod
    def format_statistics_response(stats: VehicleImageStatisticsDto) -> Dict[str, Any]:
        """
        Formata resposta de estatísticas com visualização clara.
        
        Args:
            stats: DTO das estatísticas
            
        Returns:
            Dados formatados para estatísticas
        """
        return {
            "overview": {
                "total_images": stats.total_images,
                "total_storage_mb": stats.total_size_mb,
                "average_image_size_mb": stats.average_size_mb
            },
            "coverage": {
                "vehicles_with_images": stats.vehicles_with_images,
                "vehicles_without_images": stats.vehicles_without_images,
                "coverage_percentage": (
                    round(stats.vehicles_with_images / 
                         (stats.vehicles_with_images + stats.vehicles_without_images) * 100, 2)
                    if (stats.vehicles_with_images + stats.vehicles_without_images) > 0 else 0
                )
            },
            "quality": {
                "vehicles_without_primary": stats.vehicles_without_primary,
                "images_without_thumbnails": stats.images_without_thumbnails,
                "large_images_count": stats.large_images_count,
                "orphaned_images_count": stats.orphaned_images_count
            },
            "distributions": {
                "by_format": stats.images_by_format,
                "by_orientation": stats.images_by_orientation,
                "by_size": stats.size_distribution
            },
            "recommendations": VehicleImagePresenter._generate_recommendations(stats)
        }
    
    @staticmethod
    def _generate_recommendations(stats: VehicleImageStatisticsDto) -> List[str]:
        """Gera recomendações baseadas nas estatísticas."""
        recommendations = []
        
        if stats.vehicles_without_primary > 0:
            recommendations.append(
                f"Definir imagem principal para {stats.vehicles_without_primary} veículos"
            )
        
        if stats.images_without_thumbnails > 0:
            recommendations.append(
                f"Gerar miniaturas para {stats.images_without_thumbnails} imagens"
            )
        
        if stats.large_images_count > 0:
            recommendations.append(
                f"Otimizar {stats.large_images_count} imagens grandes para melhor performance"
            )
        
        if stats.orphaned_images_count > 0:
            recommendations.append(
                f"Revisar {stats.orphaned_images_count} imagens órfãs"
            )
        
        coverage_percentage = (
            stats.vehicles_with_images / 
            (stats.vehicles_with_images + stats.vehicles_without_images) * 100
            if (stats.vehicles_with_images + stats.vehicles_without_images) > 0 else 0
        )
        
        if coverage_percentage < 80:
            recommendations.append(
                "Adicionar imagens aos veículos sem fotos para melhor apresentação"
            )
        
        return recommendations
