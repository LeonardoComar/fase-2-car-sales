"""
Interface do repositório de imagens de veículos - Domain Layer

Define o contrato para persistência de imagens de veículos seguindo o princípio
Dependency Inversion Principle (DIP) da arquitetura limpa.

A interface pertence ao domínio e as implementações concretas
ficam na camada de infraestrutura.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID

from src.domain.entities.vehicle_image import VehicleImage


class VehicleImageRepository(ABC):
    """
    Interface abstrata para repositório de imagens de veículos.
    
    Define todas as operações de persistência necessárias
    para o domínio de imagens de veículos, incluindo CRUD,
    operações de galeria e gerenciamento de arquivos.
    
    Aplicando o princípio Interface Segregation Principle (ISP) -
    interface coesa com métodos relacionados apenas a imagens de veículos.
    """
    
    @abstractmethod
    async def save(self, vehicle_image: VehicleImage) -> VehicleImage:
        """
        Salva uma imagem de veículo (create ou update).
        
        Args:
            vehicle_image: Imagem a ser salva
            
        Returns:
            VehicleImage: Imagem salva com dados atualizados
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, image_id: UUID) -> Optional[VehicleImage]:
        """
        Busca uma imagem pelo ID.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            Optional[VehicleImage]: A imagem encontrada ou None
        """
        pass
    
    @abstractmethod
    async def find_by_vehicle(self, vehicle_id: UUID, **kwargs) -> List[VehicleImage]:
        """
        Busca todas as imagens de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            **kwargs: Parâmetros adicionais (order_by, limit, etc.)
            
        Returns:
            List[VehicleImage]: Lista de imagens do veículo
        """
        pass
    
    @abstractmethod
    async def find_primary_by_vehicle(self, vehicle_id: UUID) -> Optional[VehicleImage]:
        """
        Busca a imagem principal de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Optional[VehicleImage]: Imagem principal ou None se não encontrada
        """
        pass
    
    @abstractmethod
    async def find_by_position(self, vehicle_id: UUID, position: int) -> Optional[VehicleImage]:
        """
        Busca imagem por posição específica.
        
        Args:
            vehicle_id: ID do veículo
            position: Posição da imagem
            
        Returns:
            Optional[VehicleImage]: Imagem na posição ou None
        """
        pass
    
    @abstractmethod
    async def find_by_filename(self, vehicle_id: UUID, filename: str) -> Optional[VehicleImage]:
        """
        Busca imagem por nome de arquivo.
        
        Args:
            vehicle_id: ID do veículo
            filename: Nome do arquivo
            
        Returns:
            Optional[VehicleImage]: Imagem encontrada ou None
        """
        pass
    
    @abstractmethod
    async def find_by_criteria(self, **kwargs) -> List[VehicleImage]:
        """
        Busca imagens por múltiplos critérios.
        
        Args:
            **kwargs: Critérios de busca (vehicle_id, is_primary, position_range, etc.)
            
        Returns:
            List[VehicleImage]: Lista de imagens encontradas
        """
        pass
    
    @abstractmethod
    async def delete(self, image_id: UUID) -> None:
        """
        Remove uma imagem.
        
        Args:
            image_id: ID da imagem a ser removida
        """
        pass
    
    @abstractmethod
    async def delete_by_vehicle(self, vehicle_id: UUID) -> int:
        """
        Remove todas as imagens de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            int: Número de imagens removidas
        """
        pass
    
    @abstractmethod
    async def exists_by_id(self, image_id: UUID) -> bool:
        """
        Verifica se existe imagem com o ID.
        
        Args:
            image_id: ID a ser verificado
            
        Returns:
            bool: True se existir imagem com o ID
        """
        pass
    
    @abstractmethod
    async def exists_by_filename(self, vehicle_id: UUID, filename: str, 
                                exclude_id: Optional[UUID] = None) -> bool:
        """
        Verifica se existe imagem com o nome de arquivo.
        
        Args:
            vehicle_id: ID do veículo
            filename: Nome do arquivo
            exclude_id: ID da imagem a ser excluída da verificação
            
        Returns:
            bool: True se existir imagem com o nome
        """
        pass
    
    @abstractmethod
    async def exists_by_position(self, vehicle_id: UUID, position: int, 
                               exclude_id: Optional[UUID] = None) -> bool:
        """
        Verifica se existe imagem na posição.
        
        Args:
            vehicle_id: ID do veículo
            position: Posição a ser verificada
            exclude_id: ID da imagem a ser excluída da verificação
            
        Returns:
            bool: True se existir imagem na posição
        """
        pass
    
    @abstractmethod
    async def count_by_vehicle(self, vehicle_id: UUID) -> int:
        """
        Conta imagens de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            int: Número de imagens do veículo
        """
        pass
    
    @abstractmethod
    async def get_next_position(self, vehicle_id: UUID) -> int:
        """
        Obtém a próxima posição disponível para uma imagem.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            int: Próxima posição disponível
        """
        pass
    
    @abstractmethod
    async def reorder_positions(self, vehicle_id: UUID, image_positions: Dict[UUID, int]) -> None:
        """
        Reordena posições das imagens de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            image_positions: Mapeamento de ID da imagem para nova posição
        """
        pass
    
    @abstractmethod
    async def set_primary_image(self, vehicle_id: UUID, image_id: UUID) -> None:
        """
        Define uma imagem como principal, removendo o status das outras.
        
        Args:
            vehicle_id: ID do veículo
            image_id: ID da imagem a ser definida como principal
        """
        pass
    
    @abstractmethod
    async def remove_primary_status(self, vehicle_id: UUID) -> None:
        """
        Remove o status de imagem principal de todas as imagens do veículo.
        
        Args:
            vehicle_id: ID do veículo
        """
        pass
    
    @abstractmethod
    async def get_gallery_info(self, vehicle_id: UUID) -> Dict[str, Any]:
        """
        Obtém informações da galeria de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            dict: Informações da galeria (total, principal, posições, etc.)
        """
        pass
    
    @abstractmethod
    async def get_storage_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas de armazenamento.
        
        Returns:
            dict: Estatísticas (total de imagens, tamanho total, etc.)
        """
        pass
    
    @abstractmethod
    async def find_orphaned_images(self) -> List[VehicleImage]:
        """
        Busca imagens órfãs (sem veículo correspondente).
        
        Returns:
            List[VehicleImage]: Lista de imagens órfãs
        """
        pass
    
    @abstractmethod
    async def find_images_without_thumbnails(self) -> List[VehicleImage]:
        """
        Busca imagens sem miniatura.
        
        Returns:
            List[VehicleImage]: Lista de imagens sem miniatura
        """
        pass
    
    @abstractmethod
    async def find_large_images(self, size_threshold_mb: float = 5.0) -> List[VehicleImage]:
        """
        Busca imagens grandes acima do threshold.
        
        Args:
            size_threshold_mb: Threshold de tamanho em MB
            
        Returns:
            List[VehicleImage]: Lista de imagens grandes
        """
        pass
    
    @abstractmethod
    async def get_vehicles_without_images(self) -> List[UUID]:
        """
        Busca veículos sem imagens.
        
        Returns:
            List[UUID]: Lista de IDs de veículos sem imagens
        """
        pass
    
    @abstractmethod
    async def get_vehicles_without_primary_image(self) -> List[UUID]:
        """
        Busca veículos sem imagem principal.
        
        Returns:
            List[UUID]: Lista de IDs de veículos sem imagem principal
        """
        pass
