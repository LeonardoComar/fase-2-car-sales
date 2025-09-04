from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Literal
from uuid import UUID
import re

from pydantic import BaseModel, EmailStr, field_validator, Field


class EmployeeCreateDto(BaseModel):
    """
    DTO para criação de funcionários.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas por transportar e validar dados de criação de funcionários.
    """
    
    name: str = Field(..., min_length=2, max_length=200, description="Nome completo do funcionário")
    email: EmailStr = Field(..., description="Email do funcionário")
    phone: str = Field(..., min_length=10, max_length=15, description="Telefone do funcionário")
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF do funcionário")
    birth_date: date = Field(..., description="Data de nascimento")
    position: str = Field(..., min_length=2, max_length=100, description="Cargo do funcionário")
    department: str = Field(..., min_length=2, max_length=100, description="Departamento")
    salary: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Salário")
    hire_date: date = Field(..., description="Data de contratação")
    manager_id: Optional[UUID] = Field(None, description="ID do gerente")
    employee_id: Optional[str] = Field(None, min_length=2, max_length=20, description="ID interno do funcionário")
    address: Optional[str] = Field(None, max_length=300, description="Endereço")
    city: Optional[str] = Field(None, min_length=2, max_length=100, description="Cidade")
    state: Optional[str] = Field(None, min_length=2, max_length=2, description="Estado (UF)")
    zip_code: Optional[str] = Field(None, min_length=8, max_length=9, description="CEP")
    emergency_contact_name: Optional[str] = Field(None, max_length=200, description="Nome do contato de emergência")
    emergency_contact_phone: Optional[str] = Field(None, min_length=10, max_length=15, description="Telefone do contato de emergência")
    notes: Optional[str] = Field(None, max_length=1000, description="Observações")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Valida nome do funcionário."""
        if not v or not v.strip():
            raise ValueError("Nome é obrigatório")
        
        # Deve ter pelo menos nome e sobrenome
        if len(v.strip().split()) < 2:
            raise ValueError("Nome deve conter pelo menos nome e sobrenome")
        
        # Verificar caracteres válidos
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-'\.]+$", v):
            raise ValueError("Nome contém caracteres inválidos")
        
        return v.strip().title()
    
    @field_validator('phone', 'emergency_contact_phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Valida formato do telefone."""
        if not v:
            return v
        
        # Remove formatação
        clean_phone = re.sub(r'[^0-9]', '', v)
        
        # Verifica se tem 10 ou 11 dígitos
        if len(clean_phone) not in [10, 11]:
            raise ValueError("Telefone deve ter 10 ou 11 dígitos")
        
        # Verifica se não são todos iguais
        if len(set(clean_phone)) == 1:
            raise ValueError("Telefone inválido")
        
        return clean_phone
    
    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        """Valida CPF brasileiro."""
        if not v:
            raise ValueError("CPF é obrigatório")
        
        # Remove formatação
        cpf = re.sub(r'[^0-9]', '', v)
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        
        # Verifica se não são todos iguais
        if cpf == cpf[0] * 11:
            raise ValueError("CPF inválido")
        
        # Algoritmo de validação do CPF
        def calculate_digit(cpf_digits, weights):
            total = sum(int(digit) * weight for digit, weight in zip(cpf_digits, weights))
            remainder = total % 11
            return 0 if remainder < 2 else 11 - remainder
        
        # Primeiro dígito verificador
        first_digit = calculate_digit(cpf[:9], range(10, 1, -1))
        if int(cpf[9]) != first_digit:
            raise ValueError("CPF inválido")
        
        # Segundo dígito verificador
        second_digit = calculate_digit(cpf[:10], range(11, 1, -1))
        if int(cpf[10]) != second_digit:
            raise ValueError("CPF inválido")
        
        return cpf
    
    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, v: date) -> date:
        """Valida data de nascimento."""
        if not v:
            raise ValueError("Data de nascimento é obrigatória")
        
        # Não pode ser futura
        if v > date.today():
            raise ValueError("Data de nascimento não pode ser futura")
        
        # Idade mínima de 16 anos
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 16:
            raise ValueError("Funcionário deve ter pelo menos 16 anos")
        
        # Idade máxima de 80 anos
        if age > 80:
            raise ValueError("Funcionário não pode ter mais de 80 anos")
        
        return v
    
    @field_validator('hire_date')
    @classmethod
    def validate_hire_date(cls, v: date) -> date:
        """Valida data de contratação."""
        if not v:
            raise ValueError("Data de contratação é obrigatória")
        
        # Não pode ser futura
        if v > date.today():
            raise ValueError("Data de contratação não pode ser futura")
        
        return v
    
    @field_validator('state')
    @classmethod
    def validate_state(cls, v: Optional[str]) -> Optional[str]:
        """Valida UF do estado."""
        if not v:
            return v
        
        valid_states = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
            "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
            "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ]
        
        state_upper = v.upper()
        if state_upper not in valid_states:
            raise ValueError("Estado inválido")
        
        return state_upper
    
    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls, v: Optional[str]) -> Optional[str]:
        """Valida CEP."""
        if not v:
            return v
        
        # Remove formatação
        cep = re.sub(r'[^0-9]', '', v)
        
        # Verifica se tem 8 dígitos
        if len(cep) != 8:
            raise ValueError("CEP deve ter 8 dígitos")
        
        return cep
    
    @field_validator('salary')
    @classmethod
    def validate_salary(cls, v: Decimal) -> Decimal:
        """Valida salário."""
        if v <= 0:
            raise ValueError("Salário deve ser maior que zero")
        
        if v > Decimal('1000000.00'):
            raise ValueError("Salário excede limite máximo")
        
        return v
    
    @field_validator('position')
    @classmethod
    def validate_position(cls, v: str) -> str:
        """Valida cargo."""
        if not v or not v.strip():
            raise ValueError("Cargo é obrigatório")
        
        return v.strip().title()
    
    @field_validator('department')
    @classmethod
    def validate_department(cls, v: str) -> str:
        """Valida departamento."""
        if not v or not v.strip():
            raise ValueError("Departamento é obrigatório")
        
        return v.strip().title()
    
    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }


class EmployeeUpdateDto(BaseModel):
    """
    DTO para atualização de funcionários.
    
    Todos os campos são opcionais para permitir atualizações parciais.
    """
    
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    cpf: Optional[str] = Field(None, min_length=11, max_length=14)
    birth_date: Optional[date] = None
    position: Optional[str] = Field(None, min_length=2, max_length=100)
    department: Optional[str] = Field(None, min_length=2, max_length=100)
    salary: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    manager_id: Optional[UUID] = None
    employee_id: Optional[str] = Field(None, min_length=2, max_length=20)
    address: Optional[str] = Field(None, max_length=300)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=2)
    zip_code: Optional[str] = Field(None, min_length=8, max_length=9)
    emergency_contact_name: Optional[str] = Field(None, max_length=200)
    emergency_contact_phone: Optional[str] = Field(None, min_length=10, max_length=15)
    status: Optional[Literal["active", "inactive", "suspended", "terminated", "on_leave"]] = None
    notes: Optional[str] = Field(None, max_length=1000)
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return EmployeeCreateDto.validate_name(v)
        return v
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return EmployeeCreateDto.validate_phone(v)
        return v
    
    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return EmployeeCreateDto.validate_cpf(v)
        return v
    
    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, v: Optional[date]) -> Optional[date]:
        if v is not None:
            return EmployeeCreateDto.validate_birth_date(v)
        return v
    
    @field_validator('state')
    @classmethod
    def validate_state(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return EmployeeCreateDto.validate_state(v)
        return v
    
    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return EmployeeCreateDto.validate_zip_code(v)
        return v
    
    @field_validator('salary')
    @classmethod
    def validate_salary(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        if v is not None:
            return EmployeeCreateDto.validate_salary(v)
        return v
    
    @field_validator('position')
    @classmethod
    def validate_position(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return EmployeeCreateDto.validate_position(v)
        return v
    
    @field_validator('department')
    @classmethod
    def validate_department(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return EmployeeCreateDto.validate_department(v)
        return v
    
    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }


class EmployeeResponseDto(BaseModel):
    """
    DTO para resposta de funcionários.
    
    Inclui todos os dados do funcionário plus campos calculados.
    """
    
    id: UUID
    name: str
    email: str
    phone: str
    cpf: str
    birth_date: date
    position: str
    department: str
    salary: Decimal
    hire_date: date
    manager_id: Optional[UUID] = None
    employee_id: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    status: str
    notes: Optional[str] = None
    
    # Campos calculados
    age: int
    years_of_service: int
    formatted_cpf: str
    formatted_phone: str
    formatted_zip_code: str
    full_address: str
    display_name: str
    formatted_salary: str
    is_manager: bool
    is_senior: bool
    can_approve_expenses: bool
    needs_performance_review: bool
    
    # Auditoria
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            UUID: str,
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }


class EmployeeSearchDto(BaseModel):
    """
    DTO para busca de funcionários.
    
    Permite filtros avançados e paginação.
    """
    
    # Filtros de texto
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    email: Optional[str] = Field(None, min_length=1, max_length=200)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    cpf: Optional[str] = Field(None, min_length=11, max_length=14)
    position: Optional[str] = Field(None, min_length=1, max_length=100)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    employee_id: Optional[str] = Field(None, min_length=1, max_length=20)
    
    # Filtros de localização
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=2)
    zip_code: Optional[str] = Field(None, min_length=8, max_length=9)
    
    # Filtros hierárquicos
    manager_id: Optional[UUID] = None
    
    # Filtros de status
    status: Optional[Literal["active", "inactive", "suspended", "terminated", "on_leave"]] = None
    active_only: Optional[bool] = None
    
    # Filtros de salário
    min_salary: Optional[Decimal] = Field(None, ge=0)
    max_salary: Optional[Decimal] = Field(None, ge=0)
    
    # Filtros de tempo de serviço
    min_years_service: Optional[int] = Field(None, ge=0, le=60)
    max_years_service: Optional[int] = Field(None, ge=0, le=60)
    
    # Filtros especiais
    managers_only: Optional[bool] = None
    
    # Paginação
    limit: Optional[int] = Field(None, ge=1, le=1000)
    offset: Optional[int] = Field(None, ge=0)
    
    # Ordenação
    order_by: Optional[Literal["name", "email", "position", "department", "salary", "hire_date", "created_at"]] = None
    order_direction: Optional[Literal["asc", "desc"]] = None
    
    @field_validator('phone')
    @classmethod
    def validate_phone_search(cls, v: Optional[str]) -> Optional[str]:
        """Valida telefone para busca."""
        if not v:
            return v
        return re.sub(r'[^0-9]', '', v)
    
    @field_validator('cpf')
    @classmethod
    def validate_cpf_search(cls, v: Optional[str]) -> Optional[str]:
        """Valida CPF para busca."""
        if not v:
            return v
        return re.sub(r'[^0-9]', '', v)
    
    @field_validator('zip_code')
    @classmethod
    def validate_zip_code_search(cls, v: Optional[str]) -> Optional[str]:
        """Valida CEP para busca."""
        if not v:
            return v
        return re.sub(r'[^0-9]', '', v)
    
    @field_validator('state')
    @classmethod
    def validate_state_search(cls, v: Optional[str]) -> Optional[str]:
        """Valida estado para busca."""
        if not v:
            return v
        return v.upper()
    
    class Config:
        from_attributes = True


class EmployeeStatusUpdateDto(BaseModel):
    """
    DTO para atualização de status de funcionário.
    """
    
    status: Literal["active", "inactive", "suspended", "terminated", "on_leave"]
    reason: Optional[str] = Field(None, max_length=500, description="Motivo da mudança de status")
    
    class Config:
        from_attributes = True


class EmployeePromotionDto(BaseModel):
    """
    DTO para promoção de funcionário.
    """
    
    new_position: str = Field(..., min_length=2, max_length=100, description="Nova posição")
    new_salary: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Novo salário")
    new_department: Optional[str] = Field(None, min_length=2, max_length=100, description="Novo departamento")
    effective_date: Optional[date] = Field(None, description="Data efetiva da promoção")
    notes: Optional[str] = Field(None, max_length=500, description="Observações sobre a promoção")
    
    @field_validator('new_position')
    @classmethod
    def validate_new_position(cls, v: str) -> str:
        """Valida nova posição."""
        if not v or not v.strip():
            raise ValueError("Nova posição é obrigatória")
        return v.strip().title()
    
    @field_validator('new_department')
    @classmethod
    def validate_new_department(cls, v: Optional[str]) -> Optional[str]:
        """Valida novo departamento."""
        if v and not v.strip():
            raise ValueError("Novo departamento não pode estar vazio")
        return v.strip().title() if v else None
    
    @field_validator('effective_date')
    @classmethod
    def validate_effective_date(cls, v: Optional[date]) -> Optional[date]:
        """Valida data efetiva."""
        if v and v > date.today():
            raise ValueError("Data efetiva não pode ser futura")
        return v
    
    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
