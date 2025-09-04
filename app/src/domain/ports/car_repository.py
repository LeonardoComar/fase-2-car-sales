from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.car import Car


class CarRepository(ABC):
    """
    Interface para repositório de carros.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    define a abstração que as implementações devem seguir.
    
    Aplicando o princípio Interface Segregation Principle (ISP) - 
    interface específica para operações de carro.
    """
    
    @abstractmethod
    async def save(self, car: Car) -> Car:
        """
        Salva um carro.
        
        Args:
            car: Entidade de carro a ser salva
            
        Returns:
            Car: Entidade de carro salva com ID atualizado
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, car_id: int) -> Optional[Car]:
        """
        Busca um carro por ID.
        
        Args:
            car_id: ID do carro
            
        Returns:
            Optional[Car]: Carro encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Car]:
        """
        Busca todos os carros com paginação.
        
        Args:
            skip: Número de registros a pular
            limit: Limite de registros
            
        Returns:
            List[Car]: Lista de carros
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
        transmission: Optional[str] = None,
        bodywork: Optional[str] = None,
        status: Optional[str] = None,
        available_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Car]:
        """
        Busca carros por critérios específicos.
        
        Args:
            Vários critérios de busca opcionais
            
        Returns:
            List[Car]: Lista de carros que atendem os critérios
        """
        pass
    
    @abstractmethod
    async def update(self, car: Car) -> Car:
        """
        Atualiza um carro existente.
        
        Args:
            car: Entidade de carro a ser atualizada
            
        Returns:
            Car: Entidade de carro atualizada
        """
        pass
    
    @abstractmethod
    async def delete(self, car_id: int) -> bool:
        """
        Exclui um carro.
        
        Args:
            car_id: ID do carro a ser excluído
            
        Returns:
            bool: True se excluído com sucesso
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
        transmission: Optional[str] = None,
        bodywork: Optional[str] = None,
        status: Optional[str] = None,
        available_only: bool = False
    ) -> int:
        """
        Conta carros por critérios específicos.
        
        Args:
            Vários critérios de busca opcionais
            
        Returns:
            int: Número de carros que atendem os critérios
        """
        pass
    
    @abstractmethod
    async def search_cars(
        self,
        model: str = None,
        year: str = None,
        bodywork: str = None,
        transmission: str = None,
        fuel_type: str = None,
        city: str = None,
        min_price: float = None,
        max_price: float = None,
        status: str = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Car]:
        """
        Busca carros por critérios específicos.
        
        Args:
            model: Modelo do carro
            year: Ano do carro
            bodywork: Tipo de carroceria
            transmission: Tipo de transmissão
            fuel_type: Tipo de combustível
            city: Cidade
            min_price: Preço mínimo
            max_price: Preço máximo
            status: Status do veículo
            skip: Número de registros para pular
            limit: Limite de registros
            
        Returns:
            Lista de carros que correspondem aos critérios
        """
        pass
