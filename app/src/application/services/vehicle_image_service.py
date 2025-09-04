"""
Use Cases para VehicleImage - Application Layer

Implementa as regras de negócio para gerenciamento de imagens de veículos.
Aplicando Clean Architecture, os use cases orquestram as operações entre
entidades de domínio, repositórios e serviços externos.

Aplicando princípios SOLID:
- SRP: Cada use case tem uma responsabilidade específica
- OCP: Extensível para novos casos de uso sem modificar existentes
- LSP: Use cases podem ser substituídos sem afetar comportamento
- ISP: Interfaces específicas para cada operação
- DIP: Dependem de abstrações (ports), não de implementações
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID
from datetime import datetime

from ..dtos.vehicle_image_dto import (
    VehicleImageCreateDto,
    VehicleImageUpdateDto,
    VehicleImageResponseDto,
    VehicleImageSearchDto,
    VehicleImageReorderDto,
    VehicleGalleryDto,
    VehicleImageStatisticsDto
)
from ...domain.entities.vehicle_image import VehicleImage
from ...domain.ports.vehicle_image_repository import VehicleImageRepository
from ...domain.services.image_manager import ImageManager


# ==============================================
# INTERFACES DOS USE CASES
# ==============================================

class CreateVehicleImageUseCase(ABC):
    """Interface para criação de imagem de veículo."""
    
    @abstractmethod
    async def execute(self, dto: VehicleImageCreateDto) -> VehicleImageResponseDto:
        """
        Cria uma nova imagem de veículo.
        
        Args:
            dto: Dados para criação da imagem
            
        Returns:
            Dados da imagem criada
            
        Raises:
            ValidationError: Se os dados não são válidos
            BusinessRuleError: Se viola regras de negócio
        """
        pass


class UpdateVehicleImageUseCase(ABC):
    """Interface para atualização de imagem de veículo."""
    
    @abstractmethod
    async def execute(self, image_id: UUID, dto: VehicleImageUpdateDto) -> VehicleImageResponseDto:
        """
        Atualiza uma imagem de veículo.
        
        Args:
            image_id: ID da imagem a ser atualizada
            dto: Dados para atualização
            
        Returns:
            Dados da imagem atualizada
            
        Raises:
            NotFoundError: Se a imagem não existe
            ValidationError: Se os dados não são válidos
            BusinessRuleError: Se viola regras de negócio
        """
        pass


class DeleteVehicleImageUseCase(ABC):
    """Interface para exclusão de imagem de veículo."""
    
    @abstractmethod
    async def execute(self, image_id: UUID) -> bool:
        """
        Exclui uma imagem de veículo.
        
        Args:
            image_id: ID da imagem a ser excluída
            
        Returns:
            True se excluída com sucesso
            
        Raises:
            NotFoundError: Se a imagem não existe
            BusinessRuleError: Se não pode ser excluída
        """
        pass


class GetVehicleImageUseCase(ABC):
    """Interface para obtenção de imagem por ID."""
    
    @abstractmethod
    async def execute(self, image_id: UUID) -> VehicleImageResponseDto:
        """
        Obtém uma imagem por ID.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            Dados da imagem
            
        Raises:
            NotFoundError: Se a imagem não existe
        """
        pass


class SearchVehicleImagesUseCase(ABC):
    """Interface para busca de imagens com filtros."""
    
    @abstractmethod
    async def execute(self, dto: VehicleImageSearchDto) -> Tuple[List[VehicleImageResponseDto], int]:
        """
        Busca imagens com filtros.
        
        Args:
            dto: Critérios de busca
            
        Returns:
            Tupla com lista de imagens e total de registros
        """
        pass


class GetVehicleGalleryUseCase(ABC):
    """Interface para obtenção da galeria de um veículo."""
    
    @abstractmethod
    async def execute(self, vehicle_id: UUID) -> VehicleGalleryDto:
        """
        Obtém a galeria completa de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Galeria com todas as imagens
        """
        pass


class ReorderVehicleImagesUseCase(ABC):
    """Interface para reordenação de imagens."""
    
    @abstractmethod
    async def execute(self, vehicle_id: UUID, dto: VehicleImageReorderDto) -> List[VehicleImageResponseDto]:
        """
        Reordena as imagens de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            dto: Novas posições das imagens
            
        Returns:
            Lista de imagens reordenadas
            
        Raises:
            ValidationError: Se as posições não são válidas
            NotFoundError: Se o veículo ou imagens não existem
        """
        pass


class SetPrimaryImageUseCase(ABC):
    """Interface para definir imagem principal."""
    
    @abstractmethod
    async def execute(self, image_id: UUID) -> VehicleImageResponseDto:
        """
        Define uma imagem como principal do veículo.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            Dados da imagem definida como principal
            
        Raises:
            NotFoundError: Se a imagem não existe
            BusinessRuleError: Se não pode ser definida como principal
        """
        pass


class GenerateThumbnailUseCase(ABC):
    """Interface para geração de miniatura."""
    
    @abstractmethod
    async def execute(self, image_id: UUID) -> VehicleImageResponseDto:
        """
        Gera miniatura para uma imagem.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            Dados da imagem com miniatura
            
        Raises:
            NotFoundError: Se a imagem não existe
            ProcessingError: Se não consegue gerar miniatura
        """
        pass


class GetImageStatisticsUseCase(ABC):
    """Interface para obtenção de estatísticas."""
    
    @abstractmethod
    async def execute(self) -> VehicleImageStatisticsDto:
        """
        Obtém estatísticas das imagens.
        
        Returns:
            Estatísticas completas das imagens
        """
        pass


# ==============================================
# IMPLEMENTAÇÕES DOS USE CASES
# ==============================================

class CreateVehicleImageUseCaseImpl(CreateVehicleImageUseCase):
    """Implementação do caso de uso para criação de imagem."""
    
    def __init__(
        self,
        repository: VehicleImageRepository,
        image_manager: ImageManager
    ):
        self._repository = repository
        self._image_manager = image_manager
    
    async def execute(self, dto: VehicleImageCreateDto) -> VehicleImageResponseDto:
        """Cria uma nova imagem de veículo."""
        
        # Validar se o arquivo existe
        if not await self._image_manager.file_exists(dto.path):
            raise ValueError("Arquivo de imagem não encontrado")
        
        # Se não tem posição definida, usar a próxima disponível
        if dto.position == 1:  # Posição padrão
            next_position = await self._repository.get_next_position(dto.vehicle_id)
            dto.position = next_position
        
        # Verificar se a posição está disponível
        existing_at_position = await self._repository.find_by_vehicle_and_position(
            dto.vehicle_id, dto.position
        )
        if existing_at_position:
            # Ajustar posições existentes
            await self._repository.adjust_positions_for_insertion(
                dto.vehicle_id, dto.position
            )
        
        # Se está definindo como principal, remover principal atual
        if dto.is_primary:
            current_primary = await self._repository.find_primary_by_vehicle(dto.vehicle_id)
            if current_primary:
                current_primary.set_as_secondary()
                await self._repository.save(current_primary)
        
        # Criar a entidade de domínio
        vehicle_image = VehicleImage.create_vehicle_image(
            vehicle_id=dto.vehicle_id,
            filename=dto.filename,
            path=dto.path,
            position=dto.position,
            is_primary=dto.is_primary,
            file_size=dto.file_size,
            width=dto.width,
            height=dto.height,
            mime_type=dto.mime_type
        )
        
        # Salvar no repositório
        saved_image = await self._repository.save(vehicle_image)
        
        # Gerar miniatura se configurado
        if await self._image_manager.should_generate_thumbnail(saved_image.path):
            try:
                thumbnail_path = await self._image_manager.generate_thumbnail(saved_image.path)
                saved_image.set_thumbnail_path(thumbnail_path)
                saved_image = await self._repository.save(saved_image)
            except Exception:
                # Log error, mas não falha a criação
                pass
        
        return self._map_to_response_dto(saved_image)
    
    def _map_to_response_dto(self, image: VehicleImage) -> VehicleImageResponseDto:
        """Mapeia entidade para DTO de resposta."""
        return VehicleImageResponseDto(
            id=image.id,
            vehicle_id=image.vehicle_id,
            filename=image.filename,
            path=image.path,
            thumbnail_path=image.thumbnail_path,
            position=image.position,
            is_primary=image.is_primary,
            file_size=image.file_size,
            width=image.width,
            height=image.height,
            mime_type=image.mime_type,
            uploaded_at=image.uploaded_at,
            updated_at=image.updated_at,
            file_extension=image.get_file_extension(),
            file_size_mb=image.get_file_size_mb(),
            aspect_ratio=image.get_aspect_ratio(),
            is_landscape=image.is_landscape(),
            is_portrait=image.is_portrait(),
            is_square=image.is_square(),
            has_thumbnail=image.has_thumbnail(),
            display_name=image.get_display_name()
        )


class UpdateVehicleImageUseCaseImpl(UpdateVehicleImageUseCase):
    """Implementação do caso de uso para atualização de imagem."""
    
    def __init__(
        self,
        repository: VehicleImageRepository,
        image_manager: ImageManager
    ):
        self._repository = repository
        self._image_manager = image_manager
    
    async def execute(self, image_id: UUID, dto: VehicleImageUpdateDto) -> VehicleImageResponseDto:
        """Atualiza uma imagem de veículo."""
        
        # Buscar a imagem
        image = await self._repository.find_by_id(image_id)
        if not image:
            raise ValueError("Imagem não encontrada")
        
        # Atualizar posição se especificada
        if dto.position is not None and dto.position != image.position:
            # Verificar se a nova posição está disponível
            existing_at_position = await self._repository.find_by_vehicle_and_position(
                image.vehicle_id, dto.position
            )
            
            if existing_at_position and existing_at_position.id != image.id:
                # Trocar posições
                old_position = image.position
                image.update_position(dto.position)
                existing_at_position.update_position(old_position)
                
                await self._repository.save(existing_at_position)
            else:
                image.update_position(dto.position)
        
        # Atualizar status de principal se especificado
        if dto.is_primary is not None:
            if dto.is_primary and not image.is_primary:
                # Remover principal atual
                current_primary = await self._repository.find_primary_by_vehicle(image.vehicle_id)
                if current_primary and current_primary.id != image.id:
                    current_primary.set_as_secondary()
                    await self._repository.save(current_primary)
                
                image.set_as_primary()
            elif not dto.is_primary and image.is_primary:
                image.set_as_secondary()
        
        # Atualizar caminho da miniatura se especificado
        if dto.thumbnail_path is not None:
            image.set_thumbnail_path(dto.thumbnail_path)
        
        # Salvar alterações
        updated_image = await self._repository.save(image)
        
        return self._map_to_response_dto(updated_image)
    
    def _map_to_response_dto(self, image: VehicleImage) -> VehicleImageResponseDto:
        """Mapeia entidade para DTO de resposta."""
        return VehicleImageResponseDto(
            id=image.id,
            vehicle_id=image.vehicle_id,
            filename=image.filename,
            path=image.path,
            thumbnail_path=image.thumbnail_path,
            position=image.position,
            is_primary=image.is_primary,
            file_size=image.file_size,
            width=image.width,
            height=image.height,
            mime_type=image.mime_type,
            uploaded_at=image.uploaded_at,
            updated_at=image.updated_at,
            file_extension=image.get_file_extension(),
            file_size_mb=image.get_file_size_mb(),
            aspect_ratio=image.get_aspect_ratio(),
            is_landscape=image.is_landscape(),
            is_portrait=image.is_portrait(),
            is_square=image.is_square(),
            has_thumbnail=image.has_thumbnail(),
            display_name=image.get_display_name()
        )


class DeleteVehicleImageUseCaseImpl(DeleteVehicleImageUseCase):
    """Implementação do caso de uso para exclusão de imagem."""
    
    def __init__(
        self,
        repository: VehicleImageRepository,
        image_manager: ImageManager
    ):
        self._repository = repository
        self._image_manager = image_manager
    
    async def execute(self, image_id: UUID) -> bool:
        """Exclui uma imagem de veículo."""
        
        # Buscar a imagem
        image = await self._repository.find_by_id(image_id)
        if not image:
            raise ValueError("Imagem não encontrada")
        
        vehicle_id = image.vehicle_id
        position = image.position
        is_primary = image.is_primary
        
        # Excluir arquivos físicos
        try:
            if await self._image_manager.file_exists(image.path):
                await self._image_manager.delete_file(image.path)
            
            if image.thumbnail_path and await self._image_manager.file_exists(image.thumbnail_path):
                await self._image_manager.delete_file(image.thumbnail_path)
        except Exception:
            # Log error, mas continua com a exclusão do registro
            pass
        
        # Excluir do repositório
        success = await self._repository.delete(image_id)
        
        if success:
            # Ajustar posições das imagens restantes
            await self._repository.adjust_positions_after_deletion(vehicle_id, position)
            
            # Se era a imagem principal, definir nova principal
            if is_primary:
                next_primary = await self._repository.find_first_by_vehicle(vehicle_id)
                if next_primary:
                    next_primary.set_as_primary()
                    await self._repository.save(next_primary)
        
        return success


class GetVehicleImageUseCaseImpl(GetVehicleImageUseCase):
    """Implementação do caso de uso para obtenção de imagem."""
    
    def __init__(self, repository: VehicleImageRepository):
        self._repository = repository
    
    async def execute(self, image_id: UUID) -> VehicleImageResponseDto:
        """Obtém uma imagem por ID."""
        
        image = await self._repository.find_by_id(image_id)
        if not image:
            raise ValueError("Imagem não encontrada")
        
        return self._map_to_response_dto(image)
    
    def _map_to_response_dto(self, image: VehicleImage) -> VehicleImageResponseDto:
        """Mapeia entidade para DTO de resposta."""
        return VehicleImageResponseDto(
            id=image.id,
            vehicle_id=image.vehicle_id,
            filename=image.filename,
            path=image.path,
            thumbnail_path=image.thumbnail_path,
            position=image.position,
            is_primary=image.is_primary,
            file_size=image.file_size,
            width=image.width,
            height=image.height,
            mime_type=image.mime_type,
            uploaded_at=image.uploaded_at,
            updated_at=image.updated_at,
            file_extension=image.get_file_extension(),
            file_size_mb=image.get_file_size_mb(),
            aspect_ratio=image.get_aspect_ratio(),
            is_landscape=image.is_landscape(),
            is_portrait=image.is_portrait(),
            is_square=image.is_square(),
            has_thumbnail=image.has_thumbnail(),
            display_name=image.get_display_name()
        )


class SearchVehicleImagesUseCaseImpl(SearchVehicleImagesUseCase):
    """Implementação do caso de uso para busca de imagens."""
    
    def __init__(self, repository: VehicleImageRepository):
        self._repository = repository
    
    async def execute(self, dto: VehicleImageSearchDto) -> Tuple[List[VehicleImageResponseDto], int]:
        """Busca imagens com filtros."""
        
        # Construir filtros do repositório baseado no DTO
        filters = {}
        
        if dto.vehicle_id:
            filters['vehicle_id'] = dto.vehicle_id
        
        if dto.is_primary is not None:
            filters['is_primary'] = dto.is_primary
        
        if dto.position is not None:
            filters['position'] = dto.position
        
        if dto.position_range_start and dto.position_range_end:
            filters['position_range'] = (dto.position_range_start, dto.position_range_end)
        
        if dto.has_thumbnail is not None:
            filters['has_thumbnail'] = dto.has_thumbnail
        
        if dto.min_file_size:
            filters['min_file_size'] = dto.min_file_size
        
        if dto.max_file_size:
            filters['max_file_size'] = dto.max_file_size
        
        if dto.min_width:
            filters['min_width'] = dto.min_width
        
        if dto.min_height:
            filters['min_height'] = dto.min_height
        
        if dto.orientation:
            filters['orientation'] = dto.orientation
        
        # Buscar no repositório
        images, total = await self._repository.find_with_filters(
            filters=filters,
            order_by=dto.order_by,
            order_direction=dto.order_direction,
            skip=dto.skip,
            limit=dto.limit
        )
        
        # Mapear para DTOs
        image_dtos = [self._map_to_response_dto(image) for image in images]
        
        return image_dtos, total
    
    def _map_to_response_dto(self, image: VehicleImage) -> VehicleImageResponseDto:
        """Mapeia entidade para DTO de resposta."""
        return VehicleImageResponseDto(
            id=image.id,
            vehicle_id=image.vehicle_id,
            filename=image.filename,
            path=image.path,
            thumbnail_path=image.thumbnail_path,
            position=image.position,
            is_primary=image.is_primary,
            file_size=image.file_size,
            width=image.width,
            height=image.height,
            mime_type=image.mime_type,
            uploaded_at=image.uploaded_at,
            updated_at=image.updated_at,
            file_extension=image.get_file_extension(),
            file_size_mb=image.get_file_size_mb(),
            aspect_ratio=image.get_aspect_ratio(),
            is_landscape=image.is_landscape(),
            is_portrait=image.is_portrait(),
            is_square=image.is_square(),
            has_thumbnail=image.has_thumbnail(),
            display_name=image.get_display_name()
        )


class GetVehicleGalleryUseCaseImpl(GetVehicleGalleryUseCase):
    """Implementação do caso de uso para obtenção de galeria."""
    
    def __init__(self, repository: VehicleImageRepository):
        self._repository = repository
    
    async def execute(self, vehicle_id: UUID) -> VehicleGalleryDto:
        """Obtém a galeria completa de um veículo."""
        
        # Buscar todas as imagens do veículo
        images = await self._repository.find_by_vehicle_ordered(vehicle_id)
        
        # Buscar imagem principal
        primary_image = None
        for image in images:
            if image.is_primary:
                primary_image = self._map_to_response_dto(image)
                break
        
        # Mapear todas as imagens
        image_dtos = [self._map_to_response_dto(image) for image in images]
        
        # Calcular informações da galeria
        gallery_info = await self._calculate_gallery_info(images)
        
        return VehicleGalleryDto(
            vehicle_id=vehicle_id,
            total_images=len(images),
            primary_image=primary_image,
            images=image_dtos,
            gallery_info=gallery_info
        )
    
    async def _calculate_gallery_info(self, images: List[VehicleImage]) -> Dict[str, Any]:
        """Calcula informações estatísticas da galeria."""
        if not images:
            return {
                "total_size_mb": 0.0,
                "average_size_mb": 0.0,
                "orientations": {"landscape": 0, "portrait": 0, "square": 0}
            }
        
        total_size = sum(img.file_size or 0 for img in images)
        total_size_mb = total_size / (1024 * 1024)
        average_size_mb = total_size_mb / len(images)
        
        orientations = {"landscape": 0, "portrait": 0, "square": 0}
        
        for image in images:
            if image.is_landscape():
                orientations["landscape"] += 1
            elif image.is_portrait():
                orientations["portrait"] += 1
            elif image.is_square():
                orientations["square"] += 1
        
        return {
            "total_size_mb": round(total_size_mb, 2),
            "average_size_mb": round(average_size_mb, 2),
            "orientations": orientations
        }
    
    def _map_to_response_dto(self, image: VehicleImage) -> VehicleImageResponseDto:
        """Mapeia entidade para DTO de resposta."""
        return VehicleImageResponseDto(
            id=image.id,
            vehicle_id=image.vehicle_id,
            filename=image.filename,
            path=image.path,
            thumbnail_path=image.thumbnail_path,
            position=image.position,
            is_primary=image.is_primary,
            file_size=image.file_size,
            width=image.width,
            height=image.height,
            mime_type=image.mime_type,
            uploaded_at=image.uploaded_at,
            updated_at=image.updated_at,
            file_extension=image.get_file_extension(),
            file_size_mb=image.get_file_size_mb(),
            aspect_ratio=image.get_aspect_ratio(),
            is_landscape=image.is_landscape(),
            is_portrait=image.is_portrait(),
            is_square=image.is_square(),
            has_thumbnail=image.has_thumbnail(),
            display_name=image.get_display_name()
        )


class ReorderVehicleImagesUseCaseImpl(ReorderVehicleImagesUseCase):
    """Implementação do caso de uso para reordenação de imagens."""
    
    def __init__(self, repository: VehicleImageRepository):
        self._repository = repository
    
    async def execute(self, vehicle_id: UUID, dto: VehicleImageReorderDto) -> List[VehicleImageResponseDto]:
        """Reordena as imagens de um veículo."""
        
        # Validar que todas as imagens pertencem ao veículo
        for image_id in dto.image_positions.keys():
            image = await self._repository.find_by_id(image_id)
            if not image or image.vehicle_id != vehicle_id:
                raise ValueError(f"Imagem {image_id} não pertence ao veículo {vehicle_id}")
        
        # Aplicar as novas posições
        updated_images = []
        
        for image_id, new_position in dto.image_positions.items():
            image = await self._repository.find_by_id(image_id)
            image.update_position(new_position)
            updated_image = await self._repository.save(image)
            updated_images.append(updated_image)
        
        # Ordenar por posição e retornar
        updated_images.sort(key=lambda img: img.position)
        
        return [self._map_to_response_dto(image) for image in updated_images]
    
    def _map_to_response_dto(self, image: VehicleImage) -> VehicleImageResponseDto:
        """Mapeia entidade para DTO de resposta."""
        return VehicleImageResponseDto(
            id=image.id,
            vehicle_id=image.vehicle_id,
            filename=image.filename,
            path=image.path,
            thumbnail_path=image.thumbnail_path,
            position=image.position,
            is_primary=image.is_primary,
            file_size=image.file_size,
            width=image.width,
            height=image.height,
            mime_type=image.mime_type,
            uploaded_at=image.uploaded_at,
            updated_at=image.updated_at,
            file_extension=image.get_file_extension(),
            file_size_mb=image.get_file_size_mb(),
            aspect_ratio=image.get_aspect_ratio(),
            is_landscape=image.is_landscape(),
            is_portrait=image.is_portrait(),
            is_square=image.is_square(),
            has_thumbnail=image.has_thumbnail(),
            display_name=image.get_display_name()
        )


class SetPrimaryImageUseCaseImpl(SetPrimaryImageUseCase):
    """Implementação do caso de uso para definir imagem principal."""
    
    def __init__(self, repository: VehicleImageRepository):
        self._repository = repository
    
    async def execute(self, image_id: UUID) -> VehicleImageResponseDto:
        """Define uma imagem como principal do veículo."""
        
        # Buscar a imagem
        image = await self._repository.find_by_id(image_id)
        if not image:
            raise ValueError("Imagem não encontrada")
        
        # Se já é principal, não fazer nada
        if image.is_primary:
            return self._map_to_response_dto(image)
        
        # Remover principal atual
        current_primary = await self._repository.find_primary_by_vehicle(image.vehicle_id)
        if current_primary:
            current_primary.set_as_secondary()
            await self._repository.save(current_primary)
        
        # Definir como principal
        image.set_as_primary()
        updated_image = await self._repository.save(image)
        
        return self._map_to_response_dto(updated_image)
    
    def _map_to_response_dto(self, image: VehicleImage) -> VehicleImageResponseDto:
        """Mapeia entidade para DTO de resposta."""
        return VehicleImageResponseDto(
            id=image.id,
            vehicle_id=image.vehicle_id,
            filename=image.filename,
            path=image.path,
            thumbnail_path=image.thumbnail_path,
            position=image.position,
            is_primary=image.is_primary,
            file_size=image.file_size,
            width=image.width,
            height=image.height,
            mime_type=image.mime_type,
            uploaded_at=image.uploaded_at,
            updated_at=image.updated_at,
            file_extension=image.get_file_extension(),
            file_size_mb=image.get_file_size_mb(),
            aspect_ratio=image.get_aspect_ratio(),
            is_landscape=image.is_landscape(),
            is_portrait=image.is_portrait(),
            is_square=image.is_square(),
            has_thumbnail=image.has_thumbnail(),
            display_name=image.get_display_name()
        )


class GenerateThumbnailUseCaseImpl(GenerateThumbnailUseCase):
    """Implementação do caso de uso para geração de miniatura."""
    
    def __init__(
        self,
        repository: VehicleImageRepository,
        image_manager: ImageManager
    ):
        self._repository = repository
        self._image_manager = image_manager
    
    async def execute(self, image_id: UUID) -> VehicleImageResponseDto:
        """Gera miniatura para uma imagem."""
        
        # Buscar a imagem
        image = await self._repository.find_by_id(image_id)
        if not image:
            raise ValueError("Imagem não encontrada")
        
        # Verificar se o arquivo existe
        if not await self._image_manager.file_exists(image.path):
            raise ValueError("Arquivo de imagem não encontrado")
        
        # Gerar miniatura
        try:
            thumbnail_path = await self._image_manager.generate_thumbnail(image.path)
            image.set_thumbnail_path(thumbnail_path)
            updated_image = await self._repository.save(image)
            
            return self._map_to_response_dto(updated_image)
            
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar miniatura: {str(e)}")
    
    def _map_to_response_dto(self, image: VehicleImage) -> VehicleImageResponseDto:
        """Mapeia entidade para DTO de resposta."""
        return VehicleImageResponseDto(
            id=image.id,
            vehicle_id=image.vehicle_id,
            filename=image.filename,
            path=image.path,
            thumbnail_path=image.thumbnail_path,
            position=image.position,
            is_primary=image.is_primary,
            file_size=image.file_size,
            width=image.width,
            height=image.height,
            mime_type=image.mime_type,
            uploaded_at=image.uploaded_at,
            updated_at=image.updated_at,
            file_extension=image.get_file_extension(),
            file_size_mb=image.get_file_size_mb(),
            aspect_ratio=image.get_aspect_ratio(),
            is_landscape=image.is_landscape(),
            is_portrait=image.is_portrait(),
            is_square=image.is_square(),
            has_thumbnail=image.has_thumbnail(),
            display_name=image.get_display_name()
        )


class GetImageStatisticsUseCaseImpl(GetImageStatisticsUseCase):
    """Implementação do caso de uso para obtenção de estatísticas."""
    
    def __init__(self, repository: VehicleImageRepository):
        self._repository = repository
    
    async def execute(self) -> VehicleImageStatisticsDto:
        """Obtém estatísticas das imagens."""
        
        # Obter estatísticas do repositório
        stats = await self._repository.get_statistics()
        
        return VehicleImageStatisticsDto(
            total_images=stats.get('total_images', 0),
            total_size_mb=stats.get('total_size_mb', 0.0),
            average_size_mb=stats.get('average_size_mb', 0.0),
            vehicles_with_images=stats.get('vehicles_with_images', 0),
            vehicles_without_images=stats.get('vehicles_without_images', 0),
            vehicles_without_primary=stats.get('vehicles_without_primary', 0),
            images_without_thumbnails=stats.get('images_without_thumbnails', 0),
            large_images_count=stats.get('large_images_count', 0),
            orphaned_images_count=stats.get('orphaned_images_count', 0),
            images_by_format=stats.get('images_by_format', {}),
            images_by_orientation=stats.get('images_by_orientation', {}),
            size_distribution=stats.get('size_distribution', {})
        )
