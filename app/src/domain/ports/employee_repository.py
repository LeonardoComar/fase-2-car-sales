from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.employee import Employee
from src.domain.entities.address import Address


class EmployeeRepository(ABC):
    """
    Interface (porta) para o repositório de funcionários.
    Define as operações que devem ser implementadas pela infraestrutura.
    """
    
    @abstractmethod
    async def create(self, employee: Employee, address: Optional[Address] = None) -> Employee:
        """
        Cria um novo funcionário no banco de dados.
        
        Args:
            employee: Dados do funcionário a ser criado
            address: Dados do endereço (opcional)
            
        Returns:
            Employee: O funcionário criado com ID gerado
            
        Raises:
            Exception: Se houver erro na criação
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, employee_id: int) -> Optional[Employee]:
        """
        Busca um funcionário pelo ID.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            Optional[Employee]: O funcionário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Employee]:
        """
        Busca um funcionário pelo email.
        
        Args:
            email: Email do funcionário
            
        Returns:
            Optional[Employee]: O funcionário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_cpf(self, cpf: str) -> Optional[Employee]:
        """
        Busca um funcionário pelo CPF.
        
        Args:
            cpf: CPF do funcionário
            
        Returns:
            Optional[Employee]: O funcionário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def update(self, employee_id: int, employee: Employee, address: Optional[Address] = None) -> Optional[Employee]:
        """
        Atualiza um funcionário existente.
        
        Args:
            employee_id: ID do funcionário
            employee: Dados atualizados do funcionário
            address: Dados atualizados do endereço (opcional)
            
        Returns:
            Optional[Employee]: O funcionário atualizado ou None se não encontrado
        """
        pass
    
    @abstractmethod
    async def delete(self, employee_id: int) -> bool:
        """
        Remove um funcionário do banco de dados.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        pass
    
    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """
        Busca todos os funcionários com paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            List[Employee]: Lista de funcionários encontrados
        """
        pass
    
    @abstractmethod
    async def find_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Employee]:
        """
        Busca funcionários por nome (busca parcial).
        
        Args:
            name: Nome ou parte do nome para buscar
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            List[Employee]: Lista de funcionários encontrados
        """
        pass
    
    @abstractmethod
    async def find_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Employee]:
        """
        Busca funcionários por status.
        
        Args:
            status: Status dos funcionários (Ativo/Inativo)
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            List[Employee]: Lista de funcionários encontrados
        """
        pass
