"""
Address Repository Interface - Domain Layer

Interface para operações de persistência de endereços
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.address import Address


class AddressRepository(ABC):
    """
    Interface do repositório de endereços.
    
    Define as operações que devem ser implementadas pela infraestrutura.
    Seguindo o princípio Dependency Inversion Principle (DIP) do SOLID.
    """
    
    @abstractmethod
    async def create(self, address: Address) -> Address:
        """
        Cria um novo endereço.
        
        Args:
            address: Endereço a ser criado
            
        Returns:
            Address: Endereço criado com ID
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, address_id: UUID) -> Optional[Address]:
        """
        Busca endereço por ID.
        
        Args:
            address_id: ID do endereço
            
        Returns:
            Optional[Address]: Endereço encontrado ou None
        """
        pass
    
    @abstractmethod
    async def list_all(self, limit: int = 100, offset: int = 0) -> List[Address]:
        """
        Lista todos os endereços.
        
        Args:
            limit: Número máximo de resultados
            offset: Número de registros para pular
            
        Returns:
            List[Address]: Lista de endereços
        """
        pass
    
    @abstractmethod
    async def search_by_city(self, city: str) -> List[Address]:
        """
        Busca endereços por cidade.
        
        Args:
            city: Nome da cidade
            
        Returns:
            List[Address]: Endereços da cidade
        """
        pass
    
    @abstractmethod
    async def search_by_state(self, state: str) -> List[Address]:
        """
        Busca endereços por estado.
        
        Args:
            state: Nome do estado
            
        Returns:
            List[Address]: Endereços do estado
        """
        pass
    
    @abstractmethod
    async def search_by_zip_code(self, zip_code: str) -> List[Address]:
        """
        Busca endereços por CEP.
        
        Args:
            zip_code: CEP a buscar
            
        Returns:
            List[Address]: Endereços com o CEP
        """
        pass
    
    @abstractmethod
    async def update(self, address: Address) -> Address:
        """
        Atualiza um endereço.
        
        Args:
            address: Endereço com dados atualizados
            
        Returns:
            Address: Endereço atualizado
        """
        pass
    
    @abstractmethod
    async def delete(self, address_id: UUID) -> bool:
        """
        Remove um endereço.
        
        Args:
            address_id: ID do endereço a ser removido
            
        Returns:
            bool: True se removido com sucesso
        """
        pass
