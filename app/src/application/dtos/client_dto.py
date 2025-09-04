from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel, Field, validator, EmailStr


class ClientCreateDto(BaseModel):
    """
    DTO para criação de cliente.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pelos dados de criação de cliente.
    """
    
    name: str = Field(..., min_length=2, max_length=100, description="Nome completo do cliente")
    email: EmailStr = Field(..., description="Email do cliente")
    phone: str = Field(..., min_length=10, max_length=15, description="Telefone do cliente")
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF do cliente")
    birth_date: date = Field(..., description="Data de nascimento")
    address: str = Field(..., min_length=5, max_length=200, description="Endereço completo")
    city: str = Field(..., min_length=2, max_length=100, description="Cidade")
    state: str = Field(..., min_length=2, max_length=2, description="Estado (sigla)")
    zip_code: str = Field(..., min_length=8, max_length=9, description="CEP")
    notes: Optional[str] = Field(None, max_length=1000, description="Observações adicionais")
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        if v >= date.today():
            raise ValueError("Data de nascimento deve ser anterior à data atual")
        
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        
        if age < 18:
            raise ValueError("Cliente deve ser maior de idade")
        
        if age > 120:
            raise ValueError("Data de nascimento inválida")
        
        return v
    
    @validator('state')
    def validate_state(cls, v):
        valid_states = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
            "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
            "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ]
        if v.upper() not in valid_states:
            raise ValueError(f"Estado deve ser uma sigla válida: {', '.join(valid_states)}")
        return v.upper()
    
    @validator('cpf')
    def validate_cpf_format(cls, v):
        import re
        # Remove caracteres não numéricos
        cpf_digits = re.sub(r'[^\d]', '', v)
        if len(cpf_digits) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        return cpf_digits
    
    @validator('zip_code')
    def validate_zip_code_format(cls, v):
        import re
        # Remove caracteres não numéricos
        zip_digits = re.sub(r'[^\d]', '', v)
        if len(zip_digits) != 8:
            raise ValueError("CEP deve ter 8 dígitos")
        return zip_digits
    
    @validator('phone')
    def validate_phone_format(cls, v):
        import re
        # Remove caracteres não numéricos
        phone_digits = re.sub(r'[^\d]', '', v)
        if len(phone_digits) < 10 or len(phone_digits) > 11:
            raise ValueError("Telefone deve ter 10 ou 11 dígitos")
        return phone_digits


class ClientUpdateDto(BaseModel):
    """
    DTO para atualização de cliente.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pelos dados de atualização de cliente.
    """
    
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Nome completo do cliente")
    email: Optional[EmailStr] = Field(None, description="Email do cliente")
    phone: Optional[str] = Field(None, min_length=10, max_length=15, description="Telefone do cliente")
    address: Optional[str] = Field(None, min_length=5, max_length=200, description="Endereço completo")
    city: Optional[str] = Field(None, min_length=2, max_length=100, description="Cidade")
    state: Optional[str] = Field(None, min_length=2, max_length=2, description="Estado (sigla)")
    zip_code: Optional[str] = Field(None, min_length=8, max_length=9, description="CEP")
    status: Optional[str] = Field(None, description="Status do cliente")
    notes: Optional[str] = Field(None, max_length=1000, description="Observações adicionais")
    
    @validator('state')
    def validate_state(cls, v):
        if v is not None:
            valid_states = [
                "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
                "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
                "RS", "RO", "RR", "SC", "SP", "SE", "TO"
            ]
            if v.upper() not in valid_states:
                raise ValueError(f"Estado deve ser uma sigla válida: {', '.join(valid_states)}")
            return v.upper()
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ["Ativo", "Inativo", "Bloqueado"]
            if v not in valid_statuses:
                raise ValueError(f"Status deve ser um dos seguintes: {', '.join(valid_statuses)}")
        return v
    
    @validator('zip_code')
    def validate_zip_code_format(cls, v):
        if v is not None:
            import re
            # Remove caracteres não numéricos
            zip_digits = re.sub(r'[^\d]', '', v)
            if len(zip_digits) != 8:
                raise ValueError("CEP deve ter 8 dígitos")
            return zip_digits
        return v
    
    @validator('phone')
    def validate_phone_format(cls, v):
        if v is not None:
            import re
            # Remove caracteres não numéricos
            phone_digits = re.sub(r'[^\d]', '', v)
            if len(phone_digits) < 10 or len(phone_digits) > 11:
                raise ValueError("Telefone deve ter 10 ou 11 dígitos")
            return phone_digits
        return v


class ClientResponseDto(BaseModel):
    """
    DTO para resposta de cliente.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela estrutura de resposta de cliente.
    """
    
    id: int
    name: str
    email: str
    phone: str
    cpf: str
    birth_date: date
    address: str
    city: str
    state: str
    zip_code: str
    status: str
    notes: Optional[str] = None
    
    # Dados calculados
    age: int
    formatted_cpf: str
    formatted_phone: str
    formatted_zip_code: str
    full_address: str
    display_name: str
    is_vip: bool
    can_make_purchase: bool
    
    # Auditoria
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ClientSummaryDto(BaseModel):
    """
    DTO para resumo de cliente.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pelo resumo de dados de cliente.
    """
    
    id: int
    name: str
    email: str
    phone: str
    city: str
    state: str
    status: str
    age: int
    is_vip: bool
    
    class Config:
        from_attributes = True


class ClientSearchDto(BaseModel):
    """
    DTO para critérios de busca de clientes.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pelos critérios de busca de clientes.
    """
    
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    cpf: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    status: Optional[str] = None
    age_min: Optional[int] = Field(None, ge=18, le=120)
    age_max: Optional[int] = Field(None, ge=18, le=120)
    active_only: bool = False
    
    # Paginação
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)
    
    @validator('state')
    def validate_state(cls, v):
        if v is not None:
            valid_states = [
                "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
                "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
                "RS", "RO", "RR", "SC", "SP", "SE", "TO"
            ]
            if v.upper() not in valid_states:
                raise ValueError(f"Estado deve ser uma sigla válida: {', '.join(valid_states)}")
            return v.upper()
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ["Ativo", "Inativo", "Bloqueado"]
            if v not in valid_statuses:
                raise ValueError(f"Status deve ser um dos seguintes: {', '.join(valid_statuses)}")
        return v
    
    @validator('cpf')
    def validate_cpf_format(cls, v):
        if v is not None:
            import re
            # Remove caracteres não numéricos
            cpf_digits = re.sub(r'[^\d]', '', v)
            if len(cpf_digits) != 11:
                raise ValueError("CPF deve ter 11 dígitos")
            return cpf_digits
        return v
    
    @validator('phone')
    def validate_phone_format(cls, v):
        if v is not None:
            import re
            # Remove caracteres não numéricos
            phone_digits = re.sub(r'[^\d]', '', v)
            if len(phone_digits) < 10 or len(phone_digits) > 11:
                raise ValueError("Telefone deve ter 10 ou 11 dígitos")
            return phone_digits
        return v


class ClientListResponseDto(BaseModel):
    """
    DTO para resposta de lista de clientes.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela estrutura de resposta de listas de clientes.
    """
    
    clients: List[ClientResponseDto]
    total: int
    page: int
    size: int
    total_pages: int
    
    class Config:
        from_attributes = True


class ClientStatusUpdateDto(BaseModel):
    """
    DTO para atualização de status de cliente.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela estrutura de dados para atualizações de status.
    """
    
    status: str = Field(..., description="Novo status do cliente")
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['active', 'inactive', 'blocked', 'pending']
        if v not in valid_statuses:
            raise ValueError(f'Status deve ser um dos seguintes: {", ".join(valid_statuses)}')
        return v
    
    class Config:
        from_attributes = True
