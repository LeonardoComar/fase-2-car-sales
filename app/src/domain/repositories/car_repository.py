from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.car import Car


class CarRepository(ABC):
    """
    Interface do repositório de carros no domínio.
    
    Define as operações que devem ser implementadas pela infraestrutura.
    Seguindo o princípio Dependency Inversion Principle (DIP) do SOLID.
    """
    
    @abstractmethod
    async def create_car(self, car: Car) -> Car:
        """
        Cria um novo carro no banco de dados.
        
        Args:
            car: Dados do carro a ser criado
            
        Returns:
            Car: O carro criado com ID gerado
            
        Raises:
            Exception: Se houver erro na criação
        """
        pass
    
    @abstractmethod
    async def get_car_by_id(self, car_id: int) -> Optional[Car]:
        """
        Busca um carro pelo ID.
        
        Args:
            car_id: ID do carro
            
        Returns:
            Optional[Car]: O carro encontrado ou None
        """
        pass
    
    @abstractmethod
    async def get_all_cars(self, skip: int = 0, limit: int = 100) -> List[Car]:
        """
        Busca todos os carros com paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            List[Car]: Lista de carros
        """
        pass
    
    @abstractmethod
    async def get_cars_by_bodywork(self, bodywork: str) -> List[Car]:
        """
        Busca carros por tipo de carroceria.
        
        Args:
            bodywork: Tipo de carroceria
            
        Returns:
            List[Car]: Lista de carros com a carroceria especificada
        """
        pass
    
    @abstractmethod
    async def get_cars_by_transmission(self, transmission: str) -> List[Car]:
        """
        Busca carros por tipo de transmissão.
        
        Args:
            transmission: Tipo de transmissão
            
        Returns:
            List[Car]: Lista de carros com a transmissão especificada
        """
        pass
    
    @abstractmethod
    async def get_cars_by_price_range(self, min_price: float, max_price: float) -> List[Car]:
        """
        Busca carros por faixa de preço.
        
        Args:
            min_price: Preço mínimo
            max_price: Preço máximo
            
        Returns:
            List[Car]: Lista de carros na faixa de preço
        """
        pass
    
    @abstractmethod
    async def get_cars_by_city(self, city: str) -> List[Car]:
        """
        Busca carros por cidade.
        
        Args:
            city: Nome da cidade
            
        Returns:
            List[Car]: Lista de carros na cidade especificada
        """
        pass
    
    @abstractmethod
    async def get_available_cars(self) -> List[Car]:
        """
        Busca carros disponíveis para venda.
        
        Returns:
            List[Car]: Lista de carros disponíveis
        """
        pass
    
    @abstractmethod
    async def update_car(self, car_id: int, car: Car) -> Optional[Car]:
        """
        Atualiza um carro existente.
        
        Args:
            car_id: ID do carro
            car: Dados atualizados do carro
            
        Returns:
            Optional[Car]: O carro atualizado ou None se não encontrado
        """
        pass
    
    @abstractmethod
    async def delete_car(self, car_id: int) -> bool:
        """
        Remove um carro do banco de dados.
        
        Args:
            car_id: ID do carro
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        pass
    
    @abstractmethod
    async def search_cars(
        self, 
        model: Optional[str] = None,
        year: Optional[str] = None,
        bodywork: Optional[str] = None,
        transmission: Optional[str] = None,
        fuel_type: Optional[str] = None,
        city: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Car]:
        """
        Busca carros com filtros múltiplos.
        
        Args:
            model: Modelo do veículo (opcional)
            year: Ano do veículo (opcional)
            bodywork: Tipo de carroceria (opcional)
            transmission: Tipo de transmissão (opcional)
            fuel_type: Tipo de combustível (opcional)
            city: Cidade (opcional)
            min_price: Preço mínimo (opcional)
            max_price: Preço máximo (opcional)
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            List[Car]: Lista de carros que atendem aos critérios
        """
        pass
    async def get_car_by_id(self, car_id: int) -> Optional[Car]:
        """
        Busca um carro pelo ID.
        
        Args:
            car_id: ID do carro
            
        Returns:
            Optional[Car]: O carro encontrado ou None
        """
        pass
    
    @abstractmethod
    async def get_car_by_vehicle_id(self, vehicle_id: int) -> Optional[Car]:
        """
        Busca um carro pelo ID do veículo motor.
        
        Args:
            vehicle_id: ID do veículo motor
            
        Returns:
            Optional[Car]: O carro encontrado ou None
        """
        pass
    
    @abstractmethod
    async def get_all_cars(self) -> List[Car]:
        """
        Busca todos os carros.
        
        Returns:
            List[Car]: Lista de todos os carros
        """
        pass
    
    @abstractmethod
    async def get_cars_by_bodywork(self, bodywork: str) -> List[Car]:
        """
        Busca carros por tipo de carroceria.
        
        Args:
            bodywork: Tipo de carroceria
            
        Returns:
            List[Car]: Lista de carros com a carroceria especificada
        """
        pass
    
    @abstractmethod
    async def get_cars_by_transmission(self, transmission: str) -> List[Car]:
        """
        Busca carros por tipo de transmissão.
        
        Args:
            transmission: Tipo de transmissão
            
        Returns:
            List[Car]: Lista de carros com a transmissão especificada
        """
        pass
    
    @abstractmethod
    async def update_car(self, car_id: int, car: Car) -> Optional[Car]:
        """
        Atualiza um carro existente.
        
        Args:
            car_id: ID do carro
            car: Dados atualizados do carro
            
        Returns:
            Optional[Car]: O carro atualizado ou None se não encontrado
        """
        pass
    
    @abstractmethod
    async def delete_car(self, car_id: int) -> bool:
        """
        Remove um carro do banco de dados.
        
        Args:
            car_id: ID do carro
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        pass
