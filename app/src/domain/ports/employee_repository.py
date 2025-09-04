from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from decimal import Decimal

from src.domain.entities.employee import Employee


class EmployeeRepository(ABC):
    """
    Interface do repositório de funcionários.
    
    Aplicando o princípio Interface Segregation Principle (ISP) - 
    interface específica para operações de funcionários.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    abstração que será implementada pela camada de infraestrutura.
    """
    
    @abstractmethod
    async def save(self, employee: Employee) -> Employee:
        """
        Salva um funcionário.
        
        Args:
            employee: Funcionário a ser salvo
            
        Returns:
            Employee: Funcionário salvo com dados atualizados
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, employee_id: UUID) -> Optional[Employee]:
        """
        Busca funcionário por ID.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_cpf(self, cpf: str) -> Optional[Employee]:
        """
        Busca funcionário por CPF.
        
        Args:
            cpf: CPF do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Employee]:
        """
        Busca funcionário por email.
        
        Args:
            email: Email do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_employee_id(self, employee_id: str) -> Optional[Employee]:
        """
        Busca funcionário por ID interno da empresa.
        
        Args:
            employee_id: ID interno do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_criteria(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        cpf: Optional[str] = None,
        position: Optional[str] = None,
        department: Optional[str] = None,
        manager_id: Optional[UUID] = None,
        employee_id: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        status: Optional[str] = None,
        active_only: Optional[bool] = None,
        min_salary: Optional[Decimal] = None,
        max_salary: Optional[Decimal] = None,
        min_years_service: Optional[int] = None,
        max_years_service: Optional[int] = None,
        managers_only: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        order_direction: Optional[str] = None
    ) -> List[Employee]:
        """
        Busca funcionários por múltiplos critérios.
        
        Args:
            name: Nome do funcionário (busca parcial)
            email: Email do funcionário (busca parcial)
            phone: Telefone do funcionário
            cpf: CPF do funcionário
            position: Cargo do funcionário (busca parcial)
            department: Departamento do funcionário
            manager_id: ID do gerente
            employee_id: ID interno do funcionário
            city: Cidade do funcionário
            state: Estado do funcionário
            zip_code: CEP do funcionário
            status: Status do funcionário
            active_only: Se deve retornar apenas funcionários ativos
            min_salary: Salário mínimo
            max_salary: Salário máximo
            min_years_service: Anos mínimos de serviço
            max_years_service: Anos máximos de serviço
            managers_only: Se deve retornar apenas gerentes
            limit: Limite de resultados
            offset: Deslocamento para paginação
            order_by: Campo para ordenação
            order_direction: Direção da ordenação (asc/desc)
            
        Returns:
            List[Employee]: Lista de funcionários encontrados
        """
        pass
    
    @abstractmethod
    async def find_by_department(self, department: str) -> List[Employee]:
        """
        Busca funcionários por departamento.
        
        Args:
            department: Nome do departamento
            
        Returns:
            List[Employee]: Lista de funcionários do departamento
        """
        pass
    
    @abstractmethod
    async def find_by_manager(self, manager_id: UUID) -> List[Employee]:
        """
        Busca funcionários por gerente.
        
        Args:
            manager_id: ID do gerente
            
        Returns:
            List[Employee]: Lista de funcionários subordinados
        """
        pass
    
    @abstractmethod
    async def find_managers(self) -> List[Employee]:
        """
        Busca todos os gerentes.
        
        Returns:
            List[Employee]: Lista de gerentes
        """
        pass
    
    @abstractmethod
    async def delete(self, employee_id: UUID) -> None:
        """
        Exclui um funcionário.
        
        Args:
            employee_id: ID do funcionário a ser excluído
        """
        pass
    
    @abstractmethod
    async def exists_by_cpf(self, cpf: str, exclude_id: Optional[UUID] = None) -> bool:
        """
        Verifica se existe funcionário com o CPF.
        
        Args:
            cpf: CPF a ser verificado
            exclude_id: ID a ser excluído da verificação (para atualizações)
            
        Returns:
            bool: True se existir funcionário com o CPF
        """
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: str, exclude_id: Optional[UUID] = None) -> bool:
        """
        Verifica se existe funcionário com o email.
        
        Args:
            email: Email a ser verificado
            exclude_id: ID a ser excluído da verificação (para atualizações)
            
        Returns:
            bool: True se existir funcionário com o email
        """
        pass
    
    @abstractmethod
    async def exists_by_employee_id(self, employee_id: str, exclude_id: Optional[UUID] = None) -> bool:
        """
        Verifica se existe funcionário com o ID interno.
        
        Args:
            employee_id: ID interno a ser verificado
            exclude_id: ID a ser excluído da verificação (para atualizações)
            
        Returns:
            bool: True se existir funcionário com o ID interno
        """
        pass
    
    @abstractmethod
    async def has_subordinates(self, employee_id: UUID) -> bool:
        """
        Verifica se o funcionário tem subordinados.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            bool: True se tiver subordinados
        """
        pass
    
    @abstractmethod
    async def has_associated_sales(self, employee_id: UUID) -> bool:
        """
        Verifica se o funcionário tem vendas associadas.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            bool: True se tiver vendas associadas
        """
        pass
    
    @abstractmethod
    async def has_pending_transactions(self, employee_id: UUID) -> bool:
        """
        Verifica se o funcionário tem transações pendentes.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            bool: True se tiver transações pendentes
        """
        pass
    
    @abstractmethod
    async def count_by_department(self, department: str) -> int:
        """
        Conta funcionários por departamento.
        
        Args:
            department: Nome do departamento
            
        Returns:
            int: Número de funcionários no departamento
        """
        pass
    
    @abstractmethod
    async def get_department_payroll(self, department: str) -> Decimal:
        """
        Calcula folha de pagamento por departamento.
        
        Args:
            department: Nome do departamento
            
        Returns:
            Decimal: Total da folha do departamento
        """
        pass
