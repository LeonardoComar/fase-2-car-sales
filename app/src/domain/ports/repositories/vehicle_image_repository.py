from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.vehicle_image import VehicleImage


class VehicleImageRepository(ABC):
    """
    Interface do repositório para VehicleImage.
    
    Define os contratos que devem ser implementados pelos adaptadores de persistência.
    Aplicando o princípio Dependency Inversion Principle (DIP) do SOLID.
    """
    
    @abstractmethod
    def create(self, vehicle_image: VehicleImage) -> VehicleImage:
        """
        Cria uma nova imagem de veículo.
        
        Args:
            vehicle_image: A imagem de veículo a ser criada
            
        Returns:
            VehicleImage: A imagem criada com ID atribuído
        """
        pass
    
    @abstractmethod
    def get_by_id(self, vehicle_image_id: int) -> Optional[VehicleImage]:
        """
        Busca uma imagem de veículo por ID.
        
        Args:
            vehicle_image_id: ID da imagem
            
        Returns:
            Optional[VehicleImage]: A imagem encontrada ou None
        """
        pass
    
    @abstractmethod
    def get_by_vehicle_id(self, vehicle_id: int) -> List[VehicleImage]:
        """
        Busca todas as imagens de um veículo específico.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            List[VehicleImage]: Lista de imagens do veículo
        """
        pass
    
    @abstractmethod
    def get_primary_by_vehicle_id(self, vehicle_id: int) -> Optional[VehicleImage]:
        """
        Busca a imagem principal de um veículo específico.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Optional[VehicleImage]: A imagem principal ou None
        """
        pass
    
    @abstractmethod
    def update(self, vehicle_image: VehicleImage) -> VehicleImage:
        """
        Atualiza uma imagem de veículo existente.
        
        Args:
            vehicle_image: A imagem com os dados atualizados
            
        Returns:
            VehicleImage: A imagem atualizada
        """
        pass
    
    @abstractmethod
    def delete(self, vehicle_image_id: int) -> bool:
        """
        Remove uma imagem de veículo.
        
        Args:
            vehicle_image_id: ID da imagem a ser removida
            
        Returns:
            bool: True se removida com sucesso, False caso contrário
        """
        pass
    
    @abstractmethod
    def exists(self, vehicle_image_id: int) -> bool:
        """
        Verifica se uma imagem existe.
        
        Args:
            vehicle_image_id: ID da imagem
            
        Returns:
            bool: True se existe, False caso contrário
        """
        pass
    
    @abstractmethod
    def count_by_vehicle_id(self, vehicle_id: int) -> int:
        """
        Conta quantas imagens um veículo possui.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            int: Número de imagens do veículo
        """
        pass
    
    @abstractmethod
    def get_next_position(self, vehicle_id: int) -> int:
        """
        Retorna a próxima posição disponível para uma nova imagem.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            int: Próxima posição disponível
        """
        pass
    
    @abstractmethod
    def update_positions_after_delete(self, vehicle_id: int, deleted_position: int) -> None:
        """
        Reorganiza as posições das imagens após uma exclusão.
        
        Args:
            vehicle_id: ID do veículo
            deleted_position: Posição da imagem que foi deletada
        """
        pass
