from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.client import Client


class ClientRepository(ABC):
    """
    Interface para repositório de clientes.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    define a abstração que as implementações devem seguir.
    
    Aplicando o princípio Interface Segregation Principle (ISP) - 
    interface específica para operações de cliente.
    """
    
    @abstractmethod
    async def save(self, client: Client) -> Client:
        """
        Salva um cliente.
        
        Args:
            client: Entidade de cliente a ser salva
            
        Returns:
            Client: Entidade de cliente salva com ID atualizado
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, client_id: int) -> Optional[Client]:
        """
        Busca um cliente por ID.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Optional[Client]: Cliente encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_cpf(self, cpf: str) -> Optional[Client]:
        """
        Busca um cliente por CPF.
        
        Args:
            cpf: CPF do cliente
            
        Returns:
            Optional[Client]: Cliente encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Client]:
        """
        Busca um cliente por email.
        
        Args:
            email: Email do cliente
            
        Returns:
            Optional[Client]: Cliente encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Client]:
        """
        Busca todos os clientes com paginação.
        
        Args:
            skip: Número de registros a pular
            limit: Limite de registros
            
        Returns:
            List[Client]: Lista de clientes
        """
        pass
    
    @abstractmethod
    async def find_by_criteria(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        cpf: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        status: Optional[str] = None,
        age_min: Optional[int] = None,
        age_max: Optional[int] = None,
        active_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Client]:
        """
        Busca clientes por critérios específicos.
        
        Args:
            Vários critérios de busca opcionais
            
        Returns:
            List[Client]: Lista de clientes que atendem os critérios
        """
        pass
    
    @abstractmethod
    async def update(self, client: Client) -> Client:
        """
        Atualiza um cliente existente.
        
        Args:
            client: Entidade de cliente a ser atualizada
            
        Returns:
            Client: Entidade de cliente atualizada
        """
        pass
    
    @abstractmethod
    async def delete(self, client_id: int) -> bool:
        """
        Exclui um cliente.
        
        Args:
            client_id: ID do cliente a ser excluído
            
        Returns:
            bool: True se excluído com sucesso
        """
        pass
    
    @abstractmethod
    async def count_by_criteria(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        cpf: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        status: Optional[str] = None,
        age_min: Optional[int] = None,
        age_max: Optional[int] = None,
        active_only: bool = False
    ) -> int:
        """
        Conta clientes por critérios específicos.
        
        Args:
            Vários critérios de busca opcionais
            
        Returns:
            int: Número de clientes que atendem os critérios
        """
        pass
    
    @abstractmethod
    async def exists_by_cpf(self, cpf: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica se já existe um cliente com o CPF informado.
        
        Args:
            cpf: CPF a ser verificado
            exclude_id: ID do cliente a ser excluído da verificação (para updates)
            
        Returns:
            bool: True se já existe
        """
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica se já existe um cliente com o email informado.
        
        Args:
            email: Email a ser verificado
            exclude_id: ID do cliente a ser excluído da verificação (para updates)
            
        Returns:
            bool: True se já existe
        """
        pass
