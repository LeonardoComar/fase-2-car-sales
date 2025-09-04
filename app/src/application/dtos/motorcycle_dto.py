from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator


class MotorcycleCreateDto(BaseModel):
    """
    DTO para criação de motocicleta.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pelos dados de criação de motocicleta.
    """
    
    # Dados do MotorVehicle
    brand: str = Field(..., min_length=2, max_length=50, description="Marca da motocicleta")
    model: str = Field(..., min_length=1, max_length=100, description="Modelo da motocicleta")
    year: int = Field(..., ge=1900, le=2030, description="Ano de fabricação")
    price: float = Field(..., gt=0, description="Preço da motocicleta")
    mileage: int = Field(..., ge=0, description="Quilometragem")
    fuel_type: str = Field(..., description="Tipo de combustível")
    engine_power: str = Field(..., min_length=1, max_length=20, description="Potência do motor")
    color: str = Field(..., min_length=2, max_length=30, description="Cor da motocicleta")
    description: Optional[str] = Field(None, max_length=1000, description="Descrição adicional")
    
    # Dados específicos da Motorcycle
    motorcycle_type: str = Field(..., description="Tipo de motocicleta")
    cylinder_capacity: int = Field(..., ge=50, le=2500, description="Cilindrada em cc")
    has_abs: bool = Field(False, description="Possui ABS")
    has_traction_control: bool = Field(False, description="Possui controle de tração")
    seat_height: Optional[int] = Field(None, ge=60, le=120, description="Altura do assento em cm")
    dry_weight: Optional[int] = Field(None, ge=50, le=500, description="Peso seco em kg")
    fuel_capacity: Optional[float] = Field(None, ge=1, le=50, description="Capacidade do tanque em litros")
    
    @validator('fuel_type')
    def validate_fuel_type(cls, v):
        valid_fuels = ["Gasolina", "Etanol", "Flex", "Elétrico"]
        if v not in valid_fuels:
            raise ValueError(f"Tipo de combustível deve ser um dos seguintes: {', '.join(valid_fuels)}")
        return v
    
    @validator('motorcycle_type')
    def validate_motorcycle_type(cls, v):
        valid_types = ["Street", "Sport", "Cruiser", "Adventure", "Touring", "Scooter", "Custom", "Trail"]
        if v not in valid_types:
            raise ValueError(f"Tipo de motocicleta deve ser um dos seguintes: {', '.join(valid_types)}")
        return v


class MotorcycleUpdateDto(BaseModel):
    """
    DTO para atualização de motocicleta.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pelos dados de atualização de motocicleta.
    """
    
    # Dados do MotorVehicle (opcionais para atualização)
    brand: Optional[str] = Field(None, min_length=2, max_length=50, description="Marca da motocicleta")
    model: Optional[str] = Field(None, min_length=1, max_length=100, description="Modelo da motocicleta")
    year: Optional[int] = Field(None, ge=1900, le=2030, description="Ano de fabricação")
    price: Optional[float] = Field(None, gt=0, description="Preço da motocicleta")
    mileage: Optional[int] = Field(None, ge=0, description="Quilometragem")
    fuel_type: Optional[str] = Field(None, description="Tipo de combustível")
    engine_power: Optional[str] = Field(None, min_length=1, max_length=20, description="Potência do motor")
    color: Optional[str] = Field(None, min_length=2, max_length=30, description="Cor da motocicleta")
    status: Optional[str] = Field(None, description="Status da motocicleta")
    description: Optional[str] = Field(None, max_length=1000, description="Descrição adicional")
    
    # Dados específicos da Motorcycle (opcionais para atualização)
    motorcycle_type: Optional[str] = Field(None, description="Tipo de motocicleta")
    cylinder_capacity: Optional[int] = Field(None, ge=50, le=2500, description="Cilindrada em cc")
    has_abs: Optional[bool] = Field(None, description="Possui ABS")
    has_traction_control: Optional[bool] = Field(None, description="Possui controle de tração")
    seat_height: Optional[int] = Field(None, ge=60, le=120, description="Altura do assento em cm")
    dry_weight: Optional[int] = Field(None, ge=50, le=500, description="Peso seco em kg")
    fuel_capacity: Optional[float] = Field(None, ge=1, le=50, description="Capacidade do tanque em litros")
    
    @validator('fuel_type')
    def validate_fuel_type(cls, v):
        if v is not None:
            valid_fuels = ["Gasolina", "Etanol", "Flex", "Elétrico"]
            if v not in valid_fuels:
                raise ValueError(f"Tipo de combustível deve ser um dos seguintes: {', '.join(valid_fuels)}")
        return v
    
    @validator('motorcycle_type')
    def validate_motorcycle_type(cls, v):
        if v is not None:
            valid_types = ["Street", "Sport", "Cruiser", "Adventure", "Touring", "Scooter", "Custom", "Trail"]
            if v not in valid_types:
                raise ValueError(f"Tipo de motocicleta deve ser um dos seguintes: {', '.join(valid_types)}")
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ["Ativo", "Inativo", "Vendido", "Reservado", "Em Manutenção"]
            if v not in valid_statuses:
                raise ValueError(f"Status deve ser um dos seguintes: {', '.join(valid_statuses)}")
        return v


class MotorcycleResponseDto(BaseModel):
    """
    DTO para resposta de motocicleta.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela estrutura de resposta de motocicleta.
    """
    
    id: int
    
    # Dados do MotorVehicle
    brand: str
    model: str
    year: int
    price: float
    mileage: int
    fuel_type: str
    engine_power: str
    color: str
    status: str
    description: Optional[str] = None
    
    # Dados específicos da Motorcycle
    motorcycle_type: str
    cylinder_capacity: int
    has_abs: bool
    has_traction_control: bool
    seat_height: Optional[int] = None
    dry_weight: Optional[int] = None
    fuel_capacity: Optional[float] = None
    
    # Dados calculados
    is_high_performance: bool = False
    power_to_weight_ratio: Optional[float] = None
    display_name: str
    
    # Auditoria
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MotorcycleSummaryDto(BaseModel):
    """
    DTO para resumo de motocicleta.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pelo resumo de dados de motocicleta.
    """
    
    id: int
    brand: str
    model: str
    year: int
    price: float
    mileage: int
    motorcycle_type: str
    cylinder_capacity: int
    status: str
    
    class Config:
        from_attributes = True


class MotorcycleSearchDto(BaseModel):
    """
    DTO para critérios de busca de motocicletas.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pelos critérios de busca de motocicletas.
    """
    
    # Filtros do MotorVehicle
    brand: Optional[str] = None
    model: Optional[str] = None
    year_min: Optional[int] = Field(None, ge=1900)
    year_max: Optional[int] = Field(None, le=2030)
    price_min: Optional[float] = Field(None, ge=0)
    price_max: Optional[float] = Field(None, ge=0)
    mileage_max: Optional[int] = Field(None, ge=0)
    fuel_type: Optional[str] = None
    status: Optional[str] = None
    available_only: bool = False
    
    # Filtros específicos da Motorcycle
    motorcycle_type: Optional[str] = None
    cylinder_capacity_min: Optional[int] = Field(None, ge=50)
    cylinder_capacity_max: Optional[int] = Field(None, le=2500)
    has_abs: Optional[bool] = None
    has_traction_control: Optional[bool] = None
    
    # Paginação
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)
    
    @validator('fuel_type')
    def validate_fuel_type(cls, v):
        if v is not None:
            valid_fuels = ["Gasolina", "Etanol", "Flex", "Elétrico"]
            if v not in valid_fuels:
                raise ValueError(f"Tipo de combustível deve ser um dos seguintes: {', '.join(valid_fuels)}")
        return v
    
    @validator('motorcycle_type')
    def validate_motorcycle_type(cls, v):
        if v is not None:
            valid_types = ["Street", "Sport", "Cruiser", "Adventure", "Touring", "Scooter", "Custom", "Trail"]
            if v not in valid_types:
                raise ValueError(f"Tipo de motocicleta deve ser um dos seguintes: {', '.join(valid_types)}")
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ["Ativo", "Inativo", "Vendido", "Reservado", "Em Manutenção"]
            if v not in valid_statuses:
                raise ValueError(f"Status deve ser um dos seguintes: {', '.join(valid_statuses)}")
        return v


class MotorcycleListResponseDto(BaseModel):
    """
    DTO para resposta de lista de motocicletas.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela estrutura de resposta de listas de motocicletas.
    """
    
    motorcycles: List[MotorcycleResponseDto]
    total: int
    page: int
    size: int
    total_pages: int
    
    class Config:
        from_attributes = True
