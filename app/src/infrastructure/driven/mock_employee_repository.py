from typing import List, Optional, Dict
from uuid import UUID, uuid4
from decimal import Decimal
from datetime import datetime, date
import re

from src.domain.entities.employee import Employee
from src.domain.ports.employee_repository import EmployeeRepository


class MockEmployeeRepository(EmployeeRepository):
    """
    Implementação mock do repositório de funcionários para desenvolvimento e testes.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    implementa a interface abstrata definida no domínio.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela simulação de persistência de funcionários.
    """
    
    def __init__(self):
        # Armazenamento em memória para simulação
        self._employees: Dict[UUID, Employee] = {}
        self._employee_id_counter = 1
        
        # Dados iniciais para demonstração
        self._seed_initial_data()
    
    def _seed_initial_data(self):
        """Adiciona dados iniciais para demonstração."""
        # Gerente Geral
        manager = Employee(
            id=uuid4(),
            name="Carlos Silva",
            email="carlos.silva@carsales.com",
            phone="+55 11 99999-1001",
            cpf="123.456.789-10",
            birth_date=date(1980, 5, 15),
            position="Gerente Geral",
            department="Administração",
            salary=Decimal("12000.00"),
            hire_date=date(2020, 1, 15),
            manager_id=None,
            employee_id="EMP001",
            address="Rua das Flores, 123",
            city="São Paulo",
            state="SP",
            zip_code="01234-567",
            emergency_contact_name="Maria Silva",
            emergency_contact_phone="+55 11 99999-2001",
            status="active",
            notes="Gerente responsável pela operação geral da concessionária"
        )
        self._employees[manager.id] = manager
        
        # Gerente de Vendas
        sales_manager = Employee(
            id=uuid4(),
            name="Ana Souza",
            email="ana.souza@carsales.com",
            phone="+55 11 99999-1002",
            cpf="234.567.890-21",
            birth_date=date(1985, 8, 22),
            position="Gerente de Vendas",
            department="Vendas",
            salary=Decimal("8500.00"),
            hire_date=date(2021, 3, 10),
            manager_id=manager.id,
            employee_id="EMP002",
            address="Av. Paulista, 456",
            city="São Paulo",
            state="SP",
            zip_code="01310-100",
            emergency_contact_name="João Souza",
            emergency_contact_phone="+55 11 99999-2002",
            status="active",
            notes="Gerente da equipe de vendas"
        )
        self._employees[sales_manager.id] = sales_manager
        
        # Vendedor
        salesperson = Employee(
            id=uuid4(),
            name="Pedro Santos",
            email="pedro.santos@carsales.com",
            phone="+55 11 99999-1003",
            cpf="345.678.901-32",
            birth_date=date(1990, 12, 3),
            position="Vendedor",
            department="Vendas",
            salary=Decimal("4500.00"),
            hire_date=date(2022, 6, 1),
            manager_id=sales_manager.id,
            employee_id="EMP003",
            address="Rua Augusta, 789",
            city="São Paulo",
            state="SP",
            zip_code="01305-000",
            emergency_contact_name="Lucia Santos",
            emergency_contact_phone="+55 11 99999-2003",
            status="active",
            notes="Vendedor especializado em carros populares"
        )
        self._employees[salesperson.id] = salesperson
        
        # Incrementar contador
        self._employee_id_counter = 4
    
    async def save(self, employee: Employee) -> Employee:
        """
        Salva um funcionário.
        
        Args:
            employee: Funcionário a ser salvo
            
        Returns:
            Employee: Funcionário salvo com dados atualizados
        """
        # Se não tem ID, gerar um novo
        if employee.id is None:
            employee.id = uuid4()
        
        # Se não tem employee_id, gerar um novo
        if not employee.employee_id:
            employee.employee_id = f"EMP{self._employee_id_counter:03d}"
            self._employee_id_counter += 1
        
        # Atualizar timestamp
        employee.updated_at = datetime.utcnow()
        
        # Armazenar
        self._employees[employee.id] = employee
        
        return employee
    
    async def find_by_id(self, employee_id: UUID) -> Optional[Employee]:
        """
        Busca funcionário por ID.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
        """
        return self._employees.get(employee_id)
    
    async def find_by_cpf(self, cpf: str) -> Optional[Employee]:
        """
        Busca funcionário por CPF.
        
        Args:
            cpf: CPF do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
        """
        for employee in self._employees.values():
            if employee.cpf == cpf:
                return employee
        return None
    
    async def find_by_email(self, email: str) -> Optional[Employee]:
        """
        Busca funcionário por email.
        
        Args:
            email: Email do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
        """
        for employee in self._employees.values():
            if employee.email.lower() == email.lower():
                return employee
        return None
    
    async def find_by_employee_id(self, employee_id: str) -> Optional[Employee]:
        """
        Busca funcionário por ID interno da empresa.
        
        Args:
            employee_id: ID interno do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
        """
        for employee in self._employees.values():
            if employee.employee_id == employee_id:
                return employee
        return None
    
    async def find_by_criteria(self, **kwargs) -> List[Employee]:
        """
        Busca funcionários por múltiplos critérios.
        
        Returns:
            List[Employee]: Lista de funcionários encontrados
        """
        employees = list(self._employees.values())
        
        # Aplicar filtros
        employees = self._apply_filters(employees, **kwargs)
        
        # Aplicar ordenação
        employees = self._apply_ordering(employees, kwargs.get('order_by'), kwargs.get('order_direction'))
        
        # Aplicar paginação
        if 'offset' in kwargs and kwargs['offset'] is not None:
            offset = kwargs['offset']
            employees = employees[offset:]
        
        if 'limit' in kwargs and kwargs['limit'] is not None:
            limit = kwargs['limit']
            employees = employees[:limit]
        
        return employees
    
    async def find_by_department(self, department: str) -> List[Employee]:
        """
        Busca funcionários por departamento.
        
        Args:
            department: Nome do departamento
            
        Returns:
            List[Employee]: Lista de funcionários do departamento
        """
        result = []
        for employee in self._employees.values():
            if department.lower() in employee.department.lower():
                result.append(employee)
        return result
    
    async def find_by_manager(self, manager_id: UUID) -> List[Employee]:
        """
        Busca funcionários por gerente.
        
        Args:
            manager_id: ID do gerente
            
        Returns:
            List[Employee]: Lista de funcionários subordinados
        """
        result = []
        for employee in self._employees.values():
            if employee.manager_id == manager_id:
                result.append(employee)
        return result
    
    async def find_managers(self) -> List[Employee]:
        """
        Busca todos os gerentes.
        
        Returns:
            List[Employee]: Lista de gerentes
        """
        result = []
        manager_keywords = ['gerente', 'supervisor', 'coordenador', 'diretor', 'manager']
        
        for employee in self._employees.values():
            position_lower = employee.position.lower()
            if any(keyword in position_lower for keyword in manager_keywords):
                result.append(employee)
        
        return result
    
    async def delete(self, employee_id: UUID) -> None:
        """
        Exclui um funcionário.
        
        Args:
            employee_id: ID do funcionário a ser excluído
        """
        if employee_id in self._employees:
            del self._employees[employee_id]
    
    async def exists_by_cpf(self, cpf: str, exclude_id: Optional[UUID] = None) -> bool:
        """
        Verifica se existe funcionário com o CPF.
        
        Args:
            cpf: CPF a ser verificado
            exclude_id: ID a ser excluído da verificação (para atualizações)
            
        Returns:
            bool: True se existir funcionário com o CPF
        """
        for employee in self._employees.values():
            if employee.cpf == cpf and employee.id != exclude_id:
                return True
        return False
    
    async def exists_by_email(self, email: str, exclude_id: Optional[UUID] = None) -> bool:
        """
        Verifica se existe funcionário com o email.
        
        Args:
            email: Email a ser verificado
            exclude_id: ID a ser excluído da verificação (para atualizações)
            
        Returns:
            bool: True se existir funcionário com o email
        """
        for employee in self._employees.values():
            if employee.email.lower() == email.lower() and employee.id != exclude_id:
                return True
        return False
    
    async def exists_by_employee_id(self, employee_id: str, exclude_id: Optional[UUID] = None) -> bool:
        """
        Verifica se existe funcionário com o ID interno.
        
        Args:
            employee_id: ID interno a ser verificado
            exclude_id: ID a ser excluído da verificação (para atualizações)
            
        Returns:
            bool: True se existir funcionário com o ID interno
        """
        for employee in self._employees.values():
            if employee.employee_id == employee_id and employee.id != exclude_id:
                return True
        return False
    
    async def has_subordinates(self, employee_id: UUID) -> bool:
        """
        Verifica se o funcionário tem subordinados.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            bool: True se tiver subordinados
        """
        for employee in self._employees.values():
            if employee.manager_id == employee_id:
                return True
        return False
    
    async def has_associated_sales(self, employee_id: UUID) -> bool:
        """
        Verifica se o funcionário tem vendas associadas.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            bool: True se tiver vendas associadas
        """
        # Simulação - sempre retorna False por enquanto
        return False
    
    async def has_pending_transactions(self, employee_id: UUID) -> bool:
        """
        Verifica se o funcionário tem transações pendentes.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            bool: True se tiver transações pendentes
        """
        # Simulação - sempre retorna False por enquanto
        return False
    
    async def count_by_department(self, department: str) -> int:
        """
        Conta funcionários por departamento.
        
        Args:
            department: Nome do departamento
            
        Returns:
            int: Número de funcionários no departamento
        """
        count = 0
        for employee in self._employees.values():
            if department.lower() in employee.department.lower():
                count += 1
        return count
    
    async def get_department_payroll(self, department: str) -> Decimal:
        """
        Calcula folha de pagamento por departamento.
        
        Args:
            department: Nome do departamento
            
        Returns:
            Decimal: Total da folha do departamento
        """
        total = Decimal('0')
        for employee in self._employees.values():
            if (department.lower() in employee.department.lower() and 
                employee.status == "active"):
                total += employee.salary
        return total
    
    def _apply_filters(self, employees: List[Employee], **kwargs) -> List[Employee]:
        """Aplica filtros à lista de funcionários."""
        result = employees.copy()
        
        # Filtros de texto
        if 'name' in kwargs and kwargs['name']:
            name_filter = kwargs['name'].lower()
            result = [e for e in result if name_filter in e.name.lower()]
        
        if 'email' in kwargs and kwargs['email']:
            email_filter = kwargs['email'].lower()
            result = [e for e in result if email_filter in e.email.lower()]
        
        if 'phone' in kwargs and kwargs['phone']:
            result = [e for e in result if e.phone == kwargs['phone']]
        
        if 'cpf' in kwargs and kwargs['cpf']:
            result = [e for e in result if e.cpf == kwargs['cpf']]
        
        if 'position' in kwargs and kwargs['position']:
            position_filter = kwargs['position'].lower()
            result = [e for e in result if position_filter in e.position.lower()]
        
        if 'department' in kwargs and kwargs['department']:
            dept_filter = kwargs['department'].lower()
            result = [e for e in result if dept_filter in e.department.lower()]
        
        if 'employee_id' in kwargs and kwargs['employee_id']:
            result = [e for e in result if e.employee_id == kwargs['employee_id']]
        
        # Filtros de localização
        if 'city' in kwargs and kwargs['city']:
            city_filter = kwargs['city'].lower()
            result = [e for e in result if city_filter in e.city.lower()]
        
        if 'state' in kwargs and kwargs['state']:
            result = [e for e in result if e.state == kwargs['state']]
        
        if 'zip_code' in kwargs and kwargs['zip_code']:
            result = [e for e in result if e.zip_code == kwargs['zip_code']]
        
        # Filtros hierárquicos
        if 'manager_id' in kwargs and kwargs['manager_id']:
            result = [e for e in result if e.manager_id == kwargs['manager_id']]
        
        # Filtros de status
        if 'status' in kwargs and kwargs['status']:
            result = [e for e in result if e.status == kwargs['status']]
        
        if 'active_only' in kwargs and kwargs['active_only']:
            result = [e for e in result if e.status == "active"]
        
        # Filtros de salário
        if 'min_salary' in kwargs and kwargs['min_salary'] is not None:
            min_sal = kwargs['min_salary']
            result = [e for e in result if e.salary >= min_sal]
        
        if 'max_salary' in kwargs and kwargs['max_salary'] is not None:
            max_sal = kwargs['max_salary']
            result = [e for e in result if e.salary <= max_sal]
        
        # Filtros especiais
        if 'managers_only' in kwargs and kwargs['managers_only']:
            manager_keywords = ['gerente', 'supervisor', 'coordenador', 'diretor', 'manager']
            result = [e for e in result if any(keyword in e.position.lower() for keyword in manager_keywords)]
        
        return result
    
    def _apply_ordering(self, employees: List[Employee], order_by: Optional[str], order_direction: Optional[str]) -> List[Employee]:
        """Aplica ordenação à lista de funcionários."""
        if not order_by:
            order_by = 'name'
        
        if not order_direction:
            order_direction = 'asc'
        
        reverse = order_direction.lower() == 'desc'
        
        # Mapeamento de campos para ordenação
        if order_by == 'name':
            employees.sort(key=lambda e: e.name, reverse=reverse)
        elif order_by == 'email':
            employees.sort(key=lambda e: e.email, reverse=reverse)
        elif order_by == 'position':
            employees.sort(key=lambda e: e.position, reverse=reverse)
        elif order_by == 'department':
            employees.sort(key=lambda e: e.department, reverse=reverse)
        elif order_by == 'salary':
            employees.sort(key=lambda e: e.salary, reverse=reverse)
        elif order_by == 'hire_date':
            employees.sort(key=lambda e: e.hire_date, reverse=reverse)
        elif order_by == 'created_at':
            employees.sort(key=lambda e: e.created_at, reverse=reverse)
        
        return employees
