from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import uuid4, UUID

from src.domain.exceptions import ValidationError, BusinessRuleError


class Employee:
    """
    Entidade de domínio para funcionários.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas por encapsular a lógica de negócio de funcionários.
    
    Aplicando Domain-Driven Design (DDD) - entidade rica com comportamentos
    e regras de negócio encapsuladas.
    """
    
    def __init__(
        self,
        id: UUID,
        name: str,
        email: str,
        phone: str,
        cpf: str,
        birth_date: date,
        position: str,
        department: str,
        salary: Decimal,
        hire_date: date,
        manager_id: Optional[UUID] = None,
        employee_id: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        emergency_contact_name: Optional[str] = None,
        emergency_contact_phone: Optional[str] = None,
        status: str = "active",
        notes: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.cpf = cpf
        self.birth_date = birth_date
        self.position = position
        self.department = department
        self.salary = salary
        self.hire_date = hire_date
        self.manager_id = manager_id
        self.employee_id = employee_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_phone = emergency_contact_phone
        self.status = status
        self.notes = notes
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    @classmethod
    def create_employee(
        cls,
        name: str,
        email: str,
        phone: str,
        cpf: str,
        birth_date: date,
        position: str,
        department: str,
        salary: Decimal,
        hire_date: date,
        manager_id: Optional[UUID] = None,
        employee_id: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        emergency_contact_name: Optional[str] = None,
        emergency_contact_phone: Optional[str] = None,
        notes: Optional[str] = None
    ) -> "Employee":
        """
        Factory method para criar um novo funcionário com todas as validações.
        
        Aplicando o princípio de encapsulamento e factory pattern.
        """
        # Gerar ID único
        employee_uuid = uuid4()
        
        # Criar instância
        employee = cls(
            id=employee_uuid,
            name=name,
            email=email,
            phone=phone,
            cpf=cpf,
            birth_date=birth_date,
            position=position,
            department=department,
            salary=salary,
            hire_date=hire_date,
            manager_id=manager_id,
            employee_id=employee_id,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_phone=emergency_contact_phone,
            notes=notes
        )
        
        # Validar após criação
        employee._validate()
        
        return employee
    
    def update(self, **kwargs) -> None:
        """
        Atualiza os dados do funcionário.
        
        Args:
            **kwargs: Campos a serem atualizados
        """
        updatable_fields = {
            'name', 'email', 'phone', 'cpf', 'birth_date', 'position', 
            'department', 'salary', 'manager_id', 'employee_id', 'address',
            'city', 'state', 'zip_code', 'emergency_contact_name', 
            'emergency_contact_phone', 'status', 'notes'
        }
        
        for field, value in kwargs.items():
            if field in updatable_fields:
                setattr(self, field, value)
        
        self.updated_at = datetime.now()
        self._validate()
    
    def update_status(self, new_status: str) -> None:
        """
        Atualiza o status do funcionário.
        
        Args:
            new_status: Novo status
        """
        self.status = new_status
        self.updated_at = datetime.now()
        self._validate_status()
    
    def promote(self, new_position: str, new_salary: Decimal, new_department: str = None) -> None:
        """
        Promove o funcionário.
        
        Args:
            new_position: Nova posição
            new_salary: Novo salário
            new_department: Novo departamento (opcional)
        """
        if new_salary <= self.salary:
            raise BusinessRuleError("Nova posição deve ter salário maior que o atual")
        
        self.position = new_position
        self.salary = new_salary
        
        if new_department:
            self.department = new_department
        
        self.updated_at = datetime.now()
        self._validate()
    
    def _validate(self) -> None:
        """
        Valida todos os dados do funcionário.
        
        Raises:
            ValidationError: Se algum dado for inválido
            BusinessRuleError: Se alguma regra de negócio for violada
        """
        self._validate_required_fields()
        self._validate_formats()
        self._validate_business_rules()
        self._validate_status()
    
    def _validate_required_fields(self) -> None:
        """
        Valida campos obrigatórios.
        
        Raises:
            ValidationError: Se algum campo obrigatório estiver vazio
        """
        required_fields = {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'cpf': self.cpf,
            'birth_date': self.birth_date,
            'position': self.position,
            'department': self.department,
            'salary': self.salary,
            'hire_date': self.hire_date
        }
        
        for field_name, field_value in required_fields.items():
            if not field_value or (isinstance(field_value, str) and not field_value.strip()):
                raise ValidationError(f"Campo {field_name} é obrigatório")
    
    def _validate_formats(self) -> None:
        """
        Valida formatos dos campos.
        
        Raises:
            ValidationError: Se algum formato for inválido
        """
        # Validar CPF
        if not self._is_valid_cpf(self.cpf):
            raise ValidationError("CPF inválido")
        
        # Validar email
        if '@' not in self.email or '.' not in self.email:
            raise ValidationError("Email inválido")
        
        # Validar telefone
        clean_phone = ''.join(filter(str.isdigit, self.phone))
        if len(clean_phone) not in [10, 11]:
            raise ValidationError("Telefone deve ter 10 ou 11 dígitos")
        
        # Validar CEP se fornecido
        if self.zip_code:
            clean_cep = ''.join(filter(str.isdigit, self.zip_code))
            if len(clean_cep) != 8:
                raise ValidationError("CEP deve ter 8 dígitos")
        
        # Validar estado se fornecido
        if self.state:
            valid_states = [
                "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
                "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
                "RS", "RO", "RR", "SC", "SP", "SE", "TO"
            ]
            if self.state.upper() not in valid_states:
                raise ValidationError("Estado inválido")
        
        # Validar ID do funcionário se fornecido
        if self.employee_id and len(self.employee_id.strip()) < 2:
            raise ValidationError("ID do funcionário deve ter pelo menos 2 caracteres")
    
    def _validate_business_rules(self) -> None:
        """
        Valida regras de negócio.
        
        Raises:
            BusinessRuleError: Se alguma regra for violada
        """
        # Regra: Funcionário deve ter pelo menos 16 anos
        age = self.get_age()
        if age < 16:
            raise BusinessRuleError("Funcionário deve ter pelo menos 16 anos")
        
        # Regra: Funcionário não pode ter mais de 80 anos
        if age > 80:
            raise BusinessRuleError("Funcionário não pode ter mais de 80 anos")
        
        # Regra: Data de contratação não pode ser futura
        if self.hire_date > date.today():
            raise BusinessRuleError("Data de contratação não pode ser futura")
        
        # Regra: Data de contratação não pode ser antes do nascimento
        hire_age = self.hire_date.year - self.birth_date.year
        if self.hire_date.month < self.birth_date.month or \
           (self.hire_date.month == self.birth_date.month and self.hire_date.day < self.birth_date.day):
            hire_age -= 1
        
        if hire_age < 14:
            raise BusinessRuleError("Funcionário deve ter pelo menos 14 anos na data de contratação")
        
        # Regra: Salário deve ser positivo
        if self.salary <= 0:
            raise BusinessRuleError("Salário deve ser maior que zero")
        
        # Regra: Salário não pode ser excessivamente alto (limite de segurança)
        if self.salary > Decimal('1000000.00'):
            raise BusinessRuleError("Salário excede limite máximo permitido")
        
        # Regra: Nome deve ter pelo menos 2 palavras
        if len(self.name.strip().split()) < 2:
            raise BusinessRuleError("Nome deve conter pelo menos nome e sobrenome")
    
    def _validate_status(self) -> None:
        """
        Valida o status do funcionário.
        
        Raises:
            ValidationError: Se o status for inválido
        """
        valid_statuses = ["active", "inactive", "suspended", "terminated", "on_leave"]
        
        if self.status not in valid_statuses:
            raise ValidationError(f"Status inválido. Status válidos: {', '.join(valid_statuses)}")
    
    def _is_valid_cpf(self, cpf: str) -> bool:
        """
        Valida CPF usando o algoritmo oficial brasileiro.
        
        Args:
            cpf: CPF a ser validado
            
        Returns:
            bool: True se CPF for válido
        """
        # Remove formatação
        cpf = ''.join(filter(str.isdigit, cpf))
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se não são todos iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Cálculo do primeiro dígito verificador
        sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum1 % 11)
        if digit1 >= 10:
            digit1 = 0
        
        # Cálculo do segundo dígito verificador
        sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum2 % 11)
        if digit2 >= 10:
            digit2 = 0
        
        # Verifica se os dígitos conferem
        return cpf[-2:] == f"{digit1}{digit2}"
    
    # Métodos de formatação e apresentação
    
    def get_age(self) -> int:
        """
        Calcula a idade do funcionário.
        
        Returns:
            int: Idade em anos
        """
        today = date.today()
        age = today.year - self.birth_date.year
        
        if today.month < self.birth_date.month or \
           (today.month == self.birth_date.month and today.day < self.birth_date.day):
            age -= 1
        
        return age
    
    def get_years_of_service(self) -> int:
        """
        Calcula os anos de serviço.
        
        Returns:
            int: Anos de serviço
        """
        today = date.today()
        years = today.year - self.hire_date.year
        
        if today.month < self.hire_date.month or \
           (today.month == self.hire_date.month and today.day < self.hire_date.day):
            years -= 1
        
        return max(0, years)
    
    def get_formatted_cpf(self) -> str:
        """
        Retorna CPF formatado.
        
        Returns:
            str: CPF no formato XXX.XXX.XXX-XX
        """
        cpf = ''.join(filter(str.isdigit, self.cpf))
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    def get_formatted_phone(self) -> str:
        """
        Retorna telefone formatado.
        
        Returns:
            str: Telefone formatado
        """
        phone = ''.join(filter(str.isdigit, self.phone))
        
        if len(phone) == 11:
            return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
        elif len(phone) == 10:
            return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
        else:
            return self.phone
    
    def get_formatted_zip_code(self) -> str:
        """
        Retorna CEP formatado.
        
        Returns:
            str: CEP no formato XXXXX-XXX
        """
        if not self.zip_code:
            return ""
        
        cep = ''.join(filter(str.isdigit, self.zip_code))
        if len(cep) == 8:
            return f"{cep[:5]}-{cep[5:]}"
        return self.zip_code
    
    def get_full_address(self) -> str:
        """
        Retorna endereço completo formatado.
        
        Returns:
            str: Endereço completo
        """
        parts = []
        
        if self.address:
            parts.append(self.address)
        
        if self.city and self.state:
            parts.append(f"{self.city}/{self.state}")
        elif self.city:
            parts.append(self.city)
        elif self.state:
            parts.append(self.state)
        
        if self.zip_code:
            parts.append(f"CEP: {self.get_formatted_zip_code()}")
        
        return ", ".join(parts)
    
    def get_display_name(self) -> str:
        """
        Retorna nome para exibição.
        
        Returns:
            str: Nome formatado para exibição
        """
        if self.employee_id:
            return f"{self.name} (ID: {self.employee_id})"
        return self.name
    
    def get_formatted_salary(self) -> str:
        """
        Retorna salário formatado em moeda brasileira.
        
        Returns:
            str: Salário formatado
        """
        return f"R$ {self.salary:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def is_manager(self) -> bool:
        """
        Verifica se o funcionário é gerente.
        
        Returns:
            bool: True se for gerente
        """
        manager_positions = ["gerente", "supervisor", "coordenador", "diretor", "manager"]
        return any(pos in self.position.lower() for pos in manager_positions)
    
    def is_senior(self) -> bool:
        """
        Verifica se o funcionário é sênior (5+ anos de empresa).
        
        Returns:
            bool: True se for sênior
        """
        return self.get_years_of_service() >= 5
    
    def can_approve_expenses(self) -> bool:
        """
        Verifica se pode aprovar despesas.
        
        Returns:
            bool: True se puder aprovar despesas
        """
        return (self.is_manager() and 
                self.status == "active" and 
                self.get_years_of_service() >= 1)
    
    def needs_performance_review(self) -> bool:
        """
        Verifica se precisa de avaliação de desempenho.
        
        Returns:
            bool: True se precisar de avaliação
        """
        # Funcionários ativos com 1+ ano precisam de avaliação anual
        return (self.status == "active" and 
                self.get_years_of_service() >= 1)
    
    def __str__(self) -> str:
        return f"Employee(id={self.id}, name='{self.name}', position='{self.position}')"
    
    def __repr__(self) -> str:
        return self.__str__()
