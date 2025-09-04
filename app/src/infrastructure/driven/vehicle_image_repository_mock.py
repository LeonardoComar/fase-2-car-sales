"""
Implementação Mock do VehicleImageRepository - Infrastructure Layer

Simula operações de persistência para imagens de veículos em memória.
Útil para testes e desenvolvimento inicial.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela persistência mock de imagens
- OCP: Extensível para novas operações sem modificar existentes
- LSP: Pode substituir qualquer implementação do repositório
- ISP: Implementa interface específica do repositório
- DIP: Implementa abstração definida no domínio
"""

from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID, uuid4
from datetime import datetime
import asyncio
from collections import defaultdict

from ...domain.entities.vehicle_image import VehicleImage
from ...domain.ports.vehicle_image_repository import VehicleImageRepository


class VehicleImageRepositoryMock(VehicleImageRepository):
    """
    Implementação mock do repositório de imagens de veículos.
    
    Armazena dados em memória com simulação de operações assíncronas.
    Mantém integridade referencial e regras de negócio.
    """
    
    def __init__(self):
        """Inicializa o repositório com dados em memória."""
        self._images: Dict[UUID, VehicleImage] = {}
        self._vehicle_images: Dict[UUID, List[UUID]] = defaultdict(list)
        self._next_id = 1
        
        # Simular algumas imagens para desenvolvimento
        self._seed_data()
    
    def _seed_data(self):
        """Popula dados iniciais para desenvolvimento."""
        # Simular alguns veículos e suas imagens
        vehicle_ids = [uuid4() for _ in range(3)]
        
        for i, vehicle_id in enumerate(vehicle_ids):
            # Criar 2-4 imagens por veículo
            num_images = 2 + i
            
            for j in range(num_images):
                image = VehicleImage.create_vehicle_image(
                    vehicle_id=vehicle_id,
                    filename=f"vehicle_{i+1}_image_{j+1}.jpg",
                    path=f"/uploads/vehicles/{vehicle_id}/vehicle_{i+1}_image_{j+1}.jpg",
                    position=j + 1,
                    is_primary=(j == 0),  # Primeira é principal
                    file_size=1024000 + j * 500000,
                    width=1920,
                    height=1080,
                    mime_type="image/jpeg"
                )
                
                # Definir thumbnail para algumas imagens
                if j < 2:
                    image.set_thumbnail_path(
                        f"/uploads/thumbnails/{vehicle_id}/vehicle_{i+1}_image_{j+1}_thumb.jpg"
                    )
                
                self._images[image.id] = image
                self._vehicle_images[vehicle_id].append(image.id)
    
    async def save(self, image: VehicleImage) -> VehicleImage:
        """
        Salva uma imagem no repositório.
        
        Args:
            image: Imagem a ser salva
            
        Returns:
            Imagem salva com timestamps atualizados
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        # Atualizar timestamp
        if image.id not in self._images:
            image.uploaded_at = datetime.now()
        image.updated_at = datetime.now()
        
        # Salvar
        self._images[image.id] = image
        
        # Atualizar índice por veículo
        if image.id not in self._vehicle_images[image.vehicle_id]:
            self._vehicle_images[image.vehicle_id].append(image.id)
        
        return image
    
    async def find_by_id(self, image_id: UUID) -> Optional[VehicleImage]:
        """
        Busca uma imagem por ID.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            Imagem encontrada ou None
        """
        await asyncio.sleep(0.01)  # Simular latência
        return self._images.get(image_id)
    
    async def find_by_vehicle(self, vehicle_id: UUID) -> List[VehicleImage]:
        """
        Busca todas as imagens de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Lista de imagens do veículo
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        image_ids = self._vehicle_images.get(vehicle_id, [])
        images = [self._images[img_id] for img_id in image_ids if img_id in self._images]
        
        return images
    
    async def find_by_vehicle_ordered(self, vehicle_id: UUID) -> List[VehicleImage]:
        """
        Busca imagens de um veículo ordenadas por posição.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Lista de imagens ordenadas por posição
        """
        images = await self.find_by_vehicle(vehicle_id)
        return sorted(images, key=lambda img: img.position)
    
    async def find_by_vehicle_and_position(
        self, 
        vehicle_id: UUID, 
        position: int
    ) -> Optional[VehicleImage]:
        """
        Busca imagem por veículo e posição.
        
        Args:
            vehicle_id: ID do veículo
            position: Posição da imagem
            
        Returns:
            Imagem na posição especificada ou None
        """
        images = await self.find_by_vehicle(vehicle_id)
        
        for image in images:
            if image.position == position:
                return image
        
        return None
    
    async def find_primary_by_vehicle(self, vehicle_id: UUID) -> Optional[VehicleImage]:
        """
        Busca a imagem principal de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Imagem principal ou None
        """
        images = await self.find_by_vehicle(vehicle_id)
        
        for image in images:
            if image.is_primary:
                return image
        
        return None
    
    async def find_first_by_vehicle(self, vehicle_id: UUID) -> Optional[VehicleImage]:
        """
        Busca a primeira imagem de um veículo (posição 1).
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Primeira imagem ou None
        """
        return await self.find_by_vehicle_and_position(vehicle_id, 1)
    
    async def find_without_thumbnails(self) -> List[VehicleImage]:
        """
        Busca imagens sem miniatura.
        
        Returns:
            Lista de imagens sem miniatura
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        images_without_thumbnails = []
        
        for image in self._images.values():
            if not image.has_thumbnail():
                images_without_thumbnails.append(image)
        
        return images_without_thumbnails
    
    async def find_large_images(self, size_threshold: int = 5242880) -> List[VehicleImage]:
        """
        Busca imagens grandes (acima do threshold).
        
        Args:
            size_threshold: Tamanho limite em bytes (padrão: 5MB)
            
        Returns:
            Lista de imagens grandes
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        large_images = []
        
        for image in self._images.values():
            if image.file_size and image.file_size > size_threshold:
                large_images.append(image)
        
        return large_images
    
    async def find_orphaned_images(self, existing_vehicle_ids: List[UUID]) -> List[VehicleImage]:
        """
        Busca imagens órfãs (veículos que não existem mais).
        
        Args:
            existing_vehicle_ids: Lista de IDs de veículos que existem
            
        Returns:
            Lista de imagens órfãs
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        orphaned_images = []
        
        for image in self._images.values():
            if image.vehicle_id not in existing_vehicle_ids:
                orphaned_images.append(image)
        
        return orphaned_images
    
    async def find_with_filters(
        self,
        filters: Dict[str, Any],
        order_by: str = "position",
        order_direction: str = "asc",
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[VehicleImage], int]:
        """
        Busca imagens com filtros e paginação.
        
        Args:
            filters: Filtros a aplicar
            order_by: Campo para ordenação
            order_direction: Direção da ordenação
            skip: Registros a pular
            limit: Limite de registros
            
        Returns:
            Tupla com lista de imagens e total
        """
        await asyncio.sleep(0.02)  # Simular latência de query complexa
        
        # Aplicar filtros
        filtered_images = list(self._images.values())
        
        if 'vehicle_id' in filters:
            filtered_images = [
                img for img in filtered_images 
                if img.vehicle_id == filters['vehicle_id']
            ]
        
        if 'is_primary' in filters:
            filtered_images = [
                img for img in filtered_images 
                if img.is_primary == filters['is_primary']
            ]
        
        if 'position' in filters:
            filtered_images = [
                img for img in filtered_images 
                if img.position == filters['position']
            ]
        
        if 'position_range' in filters:
            start, end = filters['position_range']
            filtered_images = [
                img for img in filtered_images 
                if start <= img.position <= end
            ]
        
        if 'has_thumbnail' in filters:
            filtered_images = [
                img for img in filtered_images 
                if img.has_thumbnail() == filters['has_thumbnail']
            ]
        
        if 'min_file_size' in filters:
            filtered_images = [
                img for img in filtered_images 
                if img.file_size and img.file_size >= filters['min_file_size']
            ]
        
        if 'max_file_size' in filters:
            filtered_images = [
                img for img in filtered_images 
                if img.file_size and img.file_size <= filters['max_file_size']
            ]
        
        if 'min_width' in filters:
            filtered_images = [
                img for img in filtered_images 
                if img.width and img.width >= filters['min_width']
            ]
        
        if 'min_height' in filters:
            filtered_images = [
                img for img in filtered_images 
                if img.height and img.height >= filters['min_height']
            ]
        
        if 'orientation' in filters:
            orientation = filters['orientation']
            filtered_images = [
                img for img in filtered_images 
                if (
                    (orientation == 'landscape' and img.is_landscape()) or
                    (orientation == 'portrait' and img.is_portrait()) or
                    (orientation == 'square' and img.is_square())
                )
            ]
        
        total = len(filtered_images)
        
        # Aplicar ordenação
        if order_by == "position":
            filtered_images.sort(key=lambda img: img.position, reverse=(order_direction == "desc"))
        elif order_by == "uploaded_at":
            filtered_images.sort(key=lambda img: img.uploaded_at, reverse=(order_direction == "desc"))
        elif order_by == "updated_at":
            filtered_images.sort(key=lambda img: img.updated_at, reverse=(order_direction == "desc"))
        elif order_by == "filename":
            filtered_images.sort(key=lambda img: img.filename, reverse=(order_direction == "desc"))
        elif order_by == "file_size":
            filtered_images.sort(key=lambda img: img.file_size or 0, reverse=(order_direction == "desc"))
        elif order_by == "width":
            filtered_images.sort(key=lambda img: img.width or 0, reverse=(order_direction == "desc"))
        elif order_by == "height":
            filtered_images.sort(key=lambda img: img.height or 0, reverse=(order_direction == "desc"))
        
        # Aplicar paginação
        paginated_images = filtered_images[skip:skip + limit]
        
        return paginated_images, total
    
    async def count_by_vehicle(self, vehicle_id: UUID) -> int:
        """
        Conta imagens de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Número de imagens
        """
        images = await self.find_by_vehicle(vehicle_id)
        return len(images)
    
    async def get_next_position(self, vehicle_id: UUID) -> int:
        """
        Obtém a próxima posição disponível para um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Próxima posição disponível
        """
        images = await self.find_by_vehicle_ordered(vehicle_id)
        
        if not images:
            return 1
        
        return images[-1].position + 1
    
    async def adjust_positions_for_insertion(self, vehicle_id: UUID, position: int) -> None:
        """
        Ajusta posições para inserção de nova imagem.
        
        Args:
            vehicle_id: ID do veículo
            position: Posição onde será inserida a nova imagem
        """
        images = await self.find_by_vehicle(vehicle_id)
        
        for image in images:
            if image.position >= position:
                image.update_position(image.position + 1)
                await self.save(image)
    
    async def adjust_positions_after_deletion(self, vehicle_id: UUID, deleted_position: int) -> None:
        """
        Ajusta posições após exclusão de imagem.
        
        Args:
            vehicle_id: ID do veículo
            deleted_position: Posição da imagem excluída
        """
        images = await self.find_by_vehicle(vehicle_id)
        
        for image in images:
            if image.position > deleted_position:
                image.update_position(image.position - 1)
                await self.save(image)
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas das imagens.
        
        Returns:
            Dicionário com estatísticas
        """
        await asyncio.sleep(0.05)  # Simular query complexa
        
        total_images = len(self._images)
        total_size = sum(img.file_size or 0 for img in self._images.values())
        total_size_mb = total_size / (1024 * 1024)
        average_size_mb = total_size_mb / total_images if total_images > 0 else 0
        
        # Contar veículos
        vehicles_with_images = len(self._vehicle_images)
        vehicles_without_images = 0  # Simular - seria calculado via join
        
        # Contar veículos sem imagem principal
        vehicles_without_primary = 0
        for vehicle_id in self._vehicle_images:
            primary = await self.find_primary_by_vehicle(vehicle_id)
            if not primary:
                vehicles_without_primary += 1
        
        # Contar imagens sem miniatura
        images_without_thumbnails = len(await self.find_without_thumbnails())
        
        # Contar imagens grandes
        large_images_count = len(await self.find_large_images())
        
        # Simular órfãs (seria calculado via join com tabela de veículos)
        orphaned_images_count = 0
        
        # Distribuição por formato
        images_by_format = defaultdict(int)
        for image in self._images.values():
            extension = image.get_file_extension()
            images_by_format[extension] += 1
        
        # Distribuição por orientação
        images_by_orientation = {"landscape": 0, "portrait": 0, "square": 0}
        for image in self._images.values():
            if image.is_landscape():
                images_by_orientation["landscape"] += 1
            elif image.is_portrait():
                images_by_orientation["portrait"] += 1
            elif image.is_square():
                images_by_orientation["square"] += 1
        
        # Distribuição por tamanho
        size_distribution = {"< 1MB": 0, "1-3MB": 0, "3-5MB": 0, "> 5MB": 0}
        for image in self._images.values():
            if image.file_size:
                size_mb = image.file_size / (1024 * 1024)
                if size_mb < 1:
                    size_distribution["< 1MB"] += 1
                elif size_mb < 3:
                    size_distribution["1-3MB"] += 1
                elif size_mb < 5:
                    size_distribution["3-5MB"] += 1
                else:
                    size_distribution["> 5MB"] += 1
        
        return {
            "total_images": total_images,
            "total_size_mb": round(total_size_mb, 2),
            "average_size_mb": round(average_size_mb, 2),
            "vehicles_with_images": vehicles_with_images,
            "vehicles_without_images": vehicles_without_images,
            "vehicles_without_primary": vehicles_without_primary,
            "images_without_thumbnails": images_without_thumbnails,
            "large_images_count": large_images_count,
            "orphaned_images_count": orphaned_images_count,
            "images_by_format": dict(images_by_format),
            "images_by_orientation": images_by_orientation,
            "size_distribution": size_distribution
        }
    
    async def delete(self, image_id: UUID) -> bool:
        """
        Exclui uma imagem.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            True se excluída com sucesso
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        if image_id not in self._images:
            return False
        
        image = self._images[image_id]
        vehicle_id = image.vehicle_id
        
        # Remover da lista do veículo
        if image_id in self._vehicle_images[vehicle_id]:
            self._vehicle_images[vehicle_id].remove(image_id)
        
        # Se não há mais imagens, remover entrada do veículo
        if not self._vehicle_images[vehicle_id]:
            del self._vehicle_images[vehicle_id]
        
        # Remover imagem
        del self._images[image_id]
        
        return True
    
    async def exists(self, image_id: UUID) -> bool:
        """
        Verifica se uma imagem existe.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            True se existe
        """
        await asyncio.sleep(0.01)  # Simular latência
        return image_id in self._images
    
    async def bulk_update_positions(self, position_updates: Dict[UUID, int]) -> None:
        """
        Atualiza posições de múltiplas imagens.
        
        Args:
            position_updates: Mapeamento de ID para nova posição
        """
        await asyncio.sleep(0.02)  # Simular operação em lote
        
        for image_id, new_position in position_updates.items():
            if image_id in self._images:
                self._images[image_id].update_position(new_position)
                self._images[image_id].updated_at = datetime.now()
    
    async def cleanup_orphaned_images(self, existing_vehicle_ids: List[UUID]) -> int:
        """
        Remove imagens órfãs.
        
        Args:
            existing_vehicle_ids: IDs de veículos que existem
            
        Returns:
            Número de imagens removidas
        """
        await asyncio.sleep(0.03)  # Simular operação de limpeza
        
        orphaned_images = await self.find_orphaned_images(existing_vehicle_ids)
        
        removed_count = 0
        for image in orphaned_images:
            if await self.delete(image.id):
                removed_count += 1
        
        return removed_count
