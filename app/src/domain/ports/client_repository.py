from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.client import Client
from src.domain.entities.address import Address


class ClientRepository(ABC):
    """
    Interface (porta) para o repositório de clientes.
    Define as operações que devem ser implementadas pela infraestrutura.
    """
    
    @abstractmethod
    async def create(self, client: Client, address: Optional[Address] = None) -> Client:
        """
        Cria um novo cliente no banco de dados.
        
        Args:
            client: Dados do cliente a ser criado
            address: Dados do endereço (opcional)
            
        Returns:
            Client: O cliente criado com ID gerado
            
        Raises:
            Exception: Se houver erro na criação
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, client_id: int) -> Optional[Client]:
        """
        Busca um cliente pelo ID.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Optional[Client]: O cliente encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Client]:
        """
        Busca um cliente pelo email.
        
        Args:
            email: Email do cliente
            
        Returns:
            Optional[Client]: O cliente encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_cpf(self, cpf: str) -> Optional[Client]:
        """
        Busca um cliente pelo CPF.
        
        Args:
            cpf: CPF do cliente
            
        Returns:
            Optional[Client]: O cliente encontrado ou None
        """
        pass
    
    @abstractmethod
    async def update(self, client_id: int, client: Client, address: Optional[Address] = None) -> Optional[Client]:
        """
        Atualiza um cliente existente.
        
        Args:
            client_id: ID do cliente
            client: Dados atualizados do cliente
            address: Dados atualizados do endereço (opcional)
            
        Returns:
            Optional[Client]: O cliente atualizado ou None se não encontrado
        """
        pass
    
    @abstractmethod
    async def delete(self, client_id: int) -> bool:
        """
        Remove um cliente do banco de dados.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        pass
    
    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Client]:
        """
        Busca todos os clientes com paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            List[Client]: Lista de clientes encontrados
        """
        pass
    
    @abstractmethod
    async def find_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """
        Busca clientes por nome (busca parcial).
        
        Args:
            name: Nome ou parte do nome para buscar
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            List[Client]: Lista de clientes encontrados
        """
        pass
    
    @abstractmethod
    async def get_address_by_id(self, address_id: int) -> Optional[Address]:
        """
        Busca um endereço pelo ID.
        
        Args:
            address_id: ID do endereço
            
        Returns:
            Optional[Address]: O endereço encontrado ou None
        """
        pass
