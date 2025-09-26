from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator, ConfigDict


class MotorcycleCreateDto(BaseModel):
    """
    DTO para criação de motocicleta.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pelos dados de criação de motocicleta.
    """
    
    # Dados do MotorVehicle
    model: str = Field(..., min_length=1, max_length=100, description="Modelo da motocicleta")
    year: str = Field(..., min_length=4, max_length=50, description="Ano de fabricação")
    price: float = Field(..., gt=0, description="Preço da motocicleta")
    mileage: int = Field(..., ge=0, description="Quilometragem")
    fuel_type: str = Field(..., description="Tipo de combustível")
    color: str = Field(..., min_length=2, max_length=50, description="Cor da motocicleta")
    city: Optional[str] = Field(None, max_length=100, description="Cidade")
    additional_description: Optional[str] = Field(None, max_length=1000, description="Descrição adicional")
    status: Optional[str] = Field("Ativo", max_length=50, description="Status do veículo")
    
    # Dados específicos da Motorcycle
    starter: Optional[str] = Field(None, max_length=50, description="Tipo de partida")
    fuel_system: Optional[str] = Field(None, max_length=50, description="Sistema de combustível")
    engine_displacement: Optional[int] = Field(None, ge=50, le=2500, description="Cilindrada em cc")
    cooling: Optional[str] = Field(None, max_length=50, description="Sistema de refrigeração")
    style: Optional[str] = Field(None, max_length=50, description="Estilo da motocicleta")
    engine_type: Optional[str] = Field(None, max_length=50, description="Tipo do motor")
    gears: Optional[int] = Field(None, ge=1, le=10, description="Número de marchas")
    front_rear_brake: Optional[str] = Field(None, max_length=100, description="Sistema de freios")
    
    @validator('fuel_type')
    def validate_fuel_type(cls, v):
        valid_fuels = ["Gasolina", "Etanol", "Flex", "Elétrico"]
        if v not in valid_fuels:
            raise ValueError(f"Tipo de combustível deve ser um dos seguintes: {', '.join(valid_fuels)}")
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ["Ativo", "Vendido", "Inativo", "Manutenção"]
            if v not in valid_statuses:
                raise ValueError(f"Status deve ser um dos seguintes: {', '.join(valid_statuses)}")
        return v


class MotorcycleUpdateDto(BaseModel):
    """
    DTO para atualização de motocicleta.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pelos dados de atualização de motocicleta.
    """
    
    # Dados do MotorVehicle (opcionais para atualização)
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
    style: Optional[str] = Field(None, description="Estilo/tipo de motocicleta")
    starter: Optional[str] = Field(None, description="Tipo de partida")
    fuel_system: Optional[str] = Field(None, description="Sistema de combustível")
    engine_displacement: Optional[int] = Field(None, ge=50, le=2500, description="Cilindrada em cc")
    cooling: Optional[str] = Field(None, description="Sistema de arrefecimento")
    engine_type: Optional[str] = Field(None, description="Tipo de motor")
    gears: Optional[int] = Field(None, ge=1, le=7, description="Número de marchas")
    front_rear_brake: Optional[str] = Field(None, description="Sistema de freios")
    
    @validator('fuel_type')
    def validate_fuel_type(cls, v):
        if v is not None:
            valid_fuels = ["Gasolina", "Etanol", "Flex", "Elétrico"]
            if v not in valid_fuels:
                raise ValueError(f"Tipo de combustível deve ser um dos seguintes: {', '.join(valid_fuels)}")
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ["Ativo", "Inativo", "Vendido", "Reservado", "Em Manutenção"]
            if v not in valid_statuses:
                raise ValueError(f"Status deve ser um dos seguintes: {', '.join(valid_statuses)}")
        return v


class MotorVehicleUpdateDto(BaseModel):
    """DTO para atualização de dados do motor vehicle."""
    model: Optional[str] = Field(None, min_length=1, max_length=100, description="Modelo do veículo")
    year: Optional[str] = Field(None, min_length=4, max_length=50, description="Ano do veículo")  # Mudado para str
    mileage: Optional[int] = Field(None, ge=0, description="Quilometragem do veículo")
    fuel_type: Optional[str] = Field(None, min_length=1, max_length=20, description="Tipo de combustível")
    engine_power: Optional[str] = Field(None, min_length=1, max_length=50, description="Potência do motor")
    color: Optional[str] = Field(None, min_length=1, max_length=50, description="Cor do veículo")
    status: Optional[str] = Field(None, min_length=1, max_length=20, description="Status do veículo")
    description: Optional[str] = Field(None, description="Descrição do veículo")
    price: Optional[float] = Field(None, gt=0, description="Preço do veículo")


class MotorcycleUpdateNestedDto(BaseModel):
    """DTO para atualização de motorcycle com estrutura aninhada ou flat."""
    # Campos específicos da motorcycle
    style: Optional[str] = Field(None, description="Estilo/tipo de motocicleta")
    starter: Optional[str] = Field(None, description="Tipo de partida")
    fuel_system: Optional[str] = Field(None, description="Sistema de combustível")
    engine_displacement: Optional[int] = Field(None, ge=50, le=2500, description="Cilindrada em cc")
    cooling: Optional[str] = Field(None, description="Sistema de arrefecimento")
    engine_type: Optional[str] = Field(None, description="Tipo de motor")
    gears: Optional[int] = Field(None, ge=1, le=7, description="Número de marchas")
    front_rear_brake: Optional[str] = Field(None, description="Sistema de freios")
    
    # Estrutura aninhada (opcional)
    motor_vehicle: Optional[MotorVehicleUpdateDto] = Field(None, description="Dados do veículo motor")
    
    # Campos diretos (para compatibilidade com formato flat)
    model: Optional[str] = Field(None, min_length=1, max_length=100, description="Modelo da motocicleta")
    year: Optional[str] = Field(None, min_length=4, max_length=50, description="Ano de fabricação")  # Mudado para str
    price: Optional[float] = Field(None, gt=0, description="Preço da motocicleta")
    mileage: Optional[int] = Field(None, ge=0, description="Quilometragem")
    fuel_type: Optional[str] = Field(None, description="Tipo de combustível")
    engine_power: Optional[str] = Field(None, min_length=1, max_length=20, description="Potência do motor")
    color: Optional[str] = Field(None, min_length=2, max_length=30, description="Cor da motocicleta")
    city: Optional[str] = Field(None, max_length=100, description="Cidade")
    status: Optional[str] = Field(None, description="Status da motocicleta")
    description: Optional[str] = Field(None, max_length=1000, description="Descrição adicional")
    additional_description: Optional[str] = Field(None, max_length=1000, description="Descrição adicional (alias)")


class MotorcycleResponseDto(BaseModel):
    """
    DTO para resposta de motocicleta.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela estrutura de resposta de motocicleta.
    """
    
    id: int
    
    # Dados do MotorVehicle (conforme tabela motor_vehicles)
    model: str
    year: str  # No banco é VARCHAR(50)
    price: float
    mileage: int
    fuel_type: str
    color: str
    city: Optional[str] = None
    additional_description: Optional[str] = None
    status: str
    
    # Dados específicos da Motorcycle (conforme tabela motorcycles)
    starter: Optional[str] = None
    fuel_system: Optional[str] = None
    engine_displacement: Optional[int] = None
    cooling: Optional[str] = None
    style: Optional[str] = None
    engine_type: Optional[str] = None
    gears: Optional[int] = None
    front_rear_brake: Optional[str] = None
    
    # Dados calculados
    display_name: str
    
    # Auditoria
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )


class MotorcycleSummaryDto(BaseModel):
    """
    DTO para resumo de motocicleta.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pelo resumo de dados de motocicleta.
    """
    
    id: int
    model: str
    year: str
    price: float
    mileage: int
    style: Optional[str] = None  # Campo real da tabela motorcycles
    engine_displacement: Optional[int] = None  # Campo real da tabela motorcycles
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
    style: Optional[str] = None
    engine_displacement_min: Optional[int] = Field(None, ge=50)
    engine_displacement_max: Optional[int] = Field(None, le=2500)
    
    # Ordenação
    order_by_price: Optional[str] = Field(None, description="Ordenação por preço (asc/desc)")
    
    # Paginação
    skip: int = Field(0, ge=0, description="Número de registros para pular")
    limit: int = Field(100, ge=1, le=1000, description="Número máximo de registros")
    
    @validator('fuel_type')
    def validate_fuel_type(cls, v):
        if v is not None:
            valid_fuels = ["Gasolina", "Etanol", "Flex", "Elétrico"]
            if v not in valid_fuels:
                raise ValueError(f"Tipo de combustível deve ser um dos seguintes: {', '.join(valid_fuels)}")
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
    skip: int
    limit: int
    
    class Config:
        from_attributes = True
