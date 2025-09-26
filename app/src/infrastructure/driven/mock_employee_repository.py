"""
Implementação Mock do EmployeeRepository - Infrastructure Layer

Simula operações de persistência para funcionários em memória.
Útil para testes e desenvolvimento inicial.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela persistência mock de funcionários
- OCP: Extensível para novas operações sem modificar existentes
- LSP: Pode substituir qualquer implementação do repositório
- ISP: Implementa interface específica do repositório
- DIP: Implementa abstração definida no domínio
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio

from src.domain.entities.employee import Employee
from src.domain.entities.address import Address
from src.domain.ports.employee_repository import EmployeeRepository


class MockEmployeeRepository(EmployeeRepository):
    """
    Implementação mock do repositório de funcionários.
    
    Armazena dados em memória com simulação de operações assíncronas.
    Mantém integridade referencial e regras de negócio.
    """
    
    def __init__(self):
        """Inicializa o repositório mock com dados em memória."""
        self._employees: Dict[int, Employee] = {}
        self._addresses: Dict[int, Address] = {}
        self._next_employee_id = 1
        self._next_address_id = 1
        
        # Dados iniciais para demonstração
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Inicializa dados mock para demonstração."""
        # Endereços mock
        address1 = Address(
            id=1,
            street="Rua das Empresas, 123",
            city="São Paulo",
            state="SP",
            zip_code="01234-567",
            country="Brasil",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self._addresses[1] = address1
        
        # Funcionários mock
        employee1 = Employee(
            id=1,
            name="João Silva",
            email="joao.silva@empresa.com",
            phone="(11) 99999-9999",
            cpf="123.456.789-00",
            status="Ativo",
            address_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self._employees[1] = employee1
        
        employee2 = Employee(
            id=2,
            name="Maria Santos",
            email="maria.santos@empresa.com",
            phone="(11) 88888-8888",
            cpf="987.654.321-00",
            status="Ativo",
            address_id=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self._employees[2] = employee2
        
        self._next_employee_id = 3
        self._next_address_id = 2
    
    async def create(self, employee: Employee, address: Optional[Address] = None) -> Employee:
        """
        Cria um novo funcionário no repositório mock.
        
        Args:
            employee: Dados do funcionário a ser criado
            address: Dados do endereço (opcional)
            
        Returns:
            Employee: O funcionário criado com ID gerado
        """
        # Simular latência de rede
        await asyncio.sleep(0.1)
        
        # Verificar se email já existe
        existing_email = await self.find_by_email(employee.email)
        if existing_email:
            raise ValueError(f"Email '{employee.email}' já está em uso")
        
        # Verificar se CPF já existe
        existing_cpf = await self.find_by_cpf(employee.cpf)
        if existing_cpf:
            raise ValueError(f"CPF '{employee.cpf}' já está em uso")
        
        # Criar endereço se fornecido
        address_id = None
        if address:
            address.id = self._next_address_id
            address.created_at = datetime.now()
            address.updated_at = datetime.now()
            self._addresses[self._next_address_id] = address
            address_id = self._next_address_id
            self._next_address_id += 1
        
        # Criar funcionário
        employee.id = self._next_employee_id
        employee.address_id = address_id
        employee.created_at = datetime.now()
        employee.updated_at = datetime.now()
        
        self._employees[self._next_employee_id] = employee
        self._next_employee_id += 1
        
        return employee
    
    async def find_by_id(self, employee_id: int) -> Optional[Employee]:
        """
        Busca um funcionário pelo ID.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            Optional[Employee]: O funcionário encontrado ou None
        """
        # Simular latência de rede
        await asyncio.sleep(0.05)
        
        return self._employees.get(employee_id)
    
    async def find_by_email(self, email: str) -> Optional[Employee]:
        """
        Busca um funcionário pelo email.
        
        Args:
            email: Email do funcionário
            
        Returns:
            Optional[Employee]: O funcionário encontrado ou None
        """
        # Simular latência de rede
        await asyncio.sleep(0.05)
        
        email_lower = email.lower()
        for employee in self._employees.values():
            if employee.email.lower() == email_lower:
                return employee
        return None
    
    async def find_by_cpf(self, cpf: str) -> Optional[Employee]:
        """
        Busca um funcionário pelo CPF.
        
        Args:
            cpf: CPF do funcionário
            
        Returns:
            Optional[Employee]: O funcionário encontrado ou None
        """
        # Simular latência de rede
        await asyncio.sleep(0.05)
        
        for employee in self._employees.values():
            if employee.cpf == cpf:
                return employee
        return None
    
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
        # Simular latência de rede
        await asyncio.sleep(0.1)
        
        if employee_id not in self._employees:
            return None
        
        existing_employee = self._employees[employee_id]
        
        # Verificar se email já existe (se está sendo alterado)
        if employee.email != existing_employee.email:
            existing_email = await self.find_by_email(employee.email)
            if existing_email and existing_email.id != employee_id:
                raise ValueError(f"Email '{employee.email}' já está em uso")
        
        # Verificar se CPF já existe (se está sendo alterado)
        if employee.cpf != existing_employee.cpf:
            existing_cpf = await self.find_by_cpf(employee.cpf)
            if existing_cpf and existing_cpf.id != employee_id:
                raise ValueError(f"CPF '{employee.cpf}' já está em uso")
        
        # Atualizar endereço se fornecido
        address_id = existing_employee.address_id
        if address:
            if address_id:
                # Atualizar endereço existente
                address.id = address_id
                address.updated_at = datetime.now()
                if address.created_at is None:
                    address.created_at = self._addresses[address_id].created_at
                self._addresses[address_id] = address
            else:
                # Criar novo endereço
                address.id = self._next_address_id
                address.created_at = datetime.now()
                address.updated_at = datetime.now()
                self._addresses[self._next_address_id] = address
                address_id = self._next_address_id
                self._next_address_id += 1
        
        # Atualizar funcionário
        employee.id = employee_id
        employee.address_id = address_id
        employee.updated_at = datetime.now()
        employee.created_at = existing_employee.created_at
        
        self._employees[employee_id] = employee
        
        return employee
    
    async def delete(self, employee_id: int) -> bool:
        """
        Remove um funcionário do repositório mock.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        # Simular latência de rede
        await asyncio.sleep(0.1)
        
        if employee_id in self._employees:
            employee = self._employees[employee_id]
            
            # Remover endereço associado se existir
            if employee.address_id and employee.address_id in self._addresses:
                del self._addresses[employee.address_id]
            
            del self._employees[employee_id]
            return True
        
        return False
    
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """
        Busca todos os funcionários com paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            List[Employee]: Lista de funcionários encontrados
        """
        # Simular latência de rede
        await asyncio.sleep(0.05)
        
        all_employees = list(self._employees.values())
        all_employees.sort(key=lambda e: e.id or 0)
        
        return all_employees[skip:skip + limit]
    
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
        # Simular latência de rede
        await asyncio.sleep(0.05)
        
        name_lower = name.lower()
        matching_employees = [
            employee for employee in self._employees.values()
            if name_lower in employee.name.lower()
        ]
        
        matching_employees.sort(key=lambda e: e.id or 0)
        
        return matching_employees[skip:skip + limit]
    
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
        # Simular latência de rede
        await asyncio.sleep(0.05)
        
        matching_employees = [
            employee for employee in self._employees.values()
            if employee.status == status
        ]
        
        matching_employees.sort(key=lambda e: e.id or 0)
        
        return matching_employees[skip:skip + limit]
    
    def get_address_by_id(self, address_id: int) -> Optional[Address]:
        """
        Busca um endereço pelo ID (método auxiliar).
        
        Args:
            address_id: ID do endereço
            
        Returns:
            Optional[Address]: O endereço encontrado ou None
        """
        return self._addresses.get(address_id)
    
    def get_all_data(self) -> Dict[str, Any]:
        """
        Retorna todos os dados armazenados (útil para debug).
        
        Returns:
            Dict: Dicionário com funcionários e endereços
        """
        return {
            "employees": {k: vars(v) for k, v in self._employees.items()},
            "addresses": {k: vars(v) for k, v in self._addresses.items()},
            "next_employee_id": self._next_employee_id,
            "next_address_id": self._next_address_id
        }
