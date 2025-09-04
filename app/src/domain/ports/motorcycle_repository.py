from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.motorcycle import Motorcycle


class MotorcycleRepository(ABC):
    """
    Interface para repositório de motocicletas.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    define a abstração que as implementações devem seguir.
    
    Aplicando o princípio Interface Segregation Principle (ISP) - 
    interface específica para operações de motocicleta.
    """
    
    @abstractmethod
    async def save(self, motorcycle: Motorcycle) -> Motorcycle:
        """
        Salva uma motocicleta.
        
        Args:
            motorcycle: Entidade de motocicleta a ser salva
            
        Returns:
            Motorcycle: Entidade de motocicleta salva com ID atualizado
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, motorcycle_id: int) -> Optional[Motorcycle]:
        """
        Busca uma motocicleta por ID.
        
        Args:
            motorcycle_id: ID da motocicleta
            
        Returns:
            Optional[Motorcycle]: Motocicleta encontrada ou None
        """
        pass
    
    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Motorcycle]:
        """
        Busca todas as motocicletas com paginação.
        
        Args:
            skip: Número de registros a pular
            limit: Limite de registros
            
        Returns:
            List[Motorcycle]: Lista de motocicletas
        """
        pass
    
    @abstractmethod
    async def find_by_criteria(
        self,
        brand: Optional[str] = None,
        model: Optional[str] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        mileage_max: Optional[int] = None,
        fuel_type: Optional[str] = None,
        motorcycle_type: Optional[str] = None,
        cylinder_capacity_min: Optional[int] = None,
        cylinder_capacity_max: Optional[int] = None,
        has_abs: Optional[bool] = None,
        has_traction_control: Optional[bool] = None,
        status: Optional[str] = None,
        available_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Motorcycle]:
        """
        Busca motocicletas por critérios específicos.
        
        Args:
            Vários critérios de busca opcionais
            
        Returns:
            List[Motorcycle]: Lista de motocicletas que atendem os critérios
        """
        pass
    
    @abstractmethod
    async def update(self, motorcycle: Motorcycle) -> Motorcycle:
        """
        Atualiza uma motocicleta existente.
        
        Args:
            motorcycle: Entidade de motocicleta a ser atualizada
            
        Returns:
            Motorcycle: Entidade de motocicleta atualizada
        """
        pass
    
    @abstractmethod
    async def delete(self, motorcycle_id: int) -> bool:
        """
        Exclui uma motocicleta.
        
        Args:
            motorcycle_id: ID da motocicleta a ser excluída
            
        Returns:
            bool: True se excluída com sucesso
        """
        pass
    
    @abstractmethod
    async def count_by_criteria(
        self,
        brand: Optional[str] = None,
        model: Optional[str] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        mileage_max: Optional[int] = None,
        fuel_type: Optional[str] = None,
        motorcycle_type: Optional[str] = None,
        cylinder_capacity_min: Optional[int] = None,
        cylinder_capacity_max: Optional[int] = None,
        has_abs: Optional[bool] = None,
        has_traction_control: Optional[bool] = None,
        status: Optional[str] = None,
        available_only: bool = False
    ) -> int:
        """
        Conta motocicletas por critérios específicos.
        
        Args:
            Vários critérios de busca opcionais
            
        Returns:
            int: Número de motocicletas que atendem os critérios
        """
        pass
