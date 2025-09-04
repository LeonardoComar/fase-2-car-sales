from pydantic import BaseModel, Field, validator
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


class CarCreateDto(BaseModel):
    """
    DTO para criação de carro.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela transferência de dados de criação.
    """
    # Dados do veículo base (MotorVehicle)
    model: str = Field(..., min_length=1, max_length=100, description="Modelo do veículo")
    year: str = Field(..., min_length=4, max_length=20, description="Ano do veículo")
    mileage: int = Field(..., ge=0, description="Quilometragem do veículo")
    fuel_type: str = Field(..., min_length=1, max_length=20, description="Tipo de combustível")
    color: str = Field(..., min_length=1, max_length=50, description="Cor do veículo")
    city: str = Field(..., min_length=1, max_length=100, description="Cidade onde está o veículo")
    price: Decimal = Field(..., gt=0, description="Preço do veículo (deve ser maior que zero)")
    additional_description: Optional[str] = Field(None, description="Descrição adicional do veículo")
    
    # Dados específicos do carro
    bodywork: str = Field(..., min_length=1, max_length=20, description="Tipo de carroceria")
    transmission: str = Field(..., min_length=1, max_length=20, description="Tipo de transmissão")

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v

    @validator('mileage')
    def validate_mileage(cls, v):
        if v < 0:
            raise ValueError('Quilometragem não pode ser negativa')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "model": "Honda Civic",
                "year": "2020",
                "mileage": 25000,
                "fuel_type": "Flex",
                "color": "Branco",
                "city": "São Paulo",
                "price": "85000.00",
                "additional_description": "Carro em excelente estado de conservação",
                "bodywork": "Sedan",
                "transmission": "Automatica"
            }
        }


class MotorVehicleUpdateDto(BaseModel):
    """
    DTO para atualização de dados do motor vehicle.
    """
    brand: Optional[str] = Field(None, min_length=1, max_length=100, description="Marca do veículo")
    model: Optional[str] = Field(None, min_length=1, max_length=100, description="Modelo do veículo")
    year: Optional[int] = Field(None, ge=1900, le=2030, description="Ano do veículo")
    mileage: Optional[int] = Field(None, ge=0, description="Quilometragem do veículo")
    fuel_type: Optional[str] = Field(None, min_length=1, max_length=20, description="Tipo de combustível")
    engine_power: Optional[str] = Field(None, min_length=1, max_length=50, description="Potência do motor")
    color: Optional[str] = Field(None, min_length=1, max_length=50, description="Cor do veículo")
    status: Optional[str] = Field(None, min_length=1, max_length=20, description="Status do veículo")
    description: Optional[str] = Field(None, description="Descrição do veículo")
    price: Optional[Decimal] = Field(None, gt=0, description="Preço do veículo")

    @validator('price')
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v

    @validator('mileage')
    def validate_mileage(cls, v):
        if v is not None and v < 0:
            raise ValueError('Quilometragem não pode ser negativa')
        return v


class CarUpdateNestedDto(BaseModel):
    """
    DTO para atualização de carro com estrutura aninhada ou flat.
    """
    # Campos específicos do carro
    bodywork: Optional[str] = Field(None, min_length=1, max_length=20, description="Tipo de carroceria")
    transmission: Optional[str] = Field(None, min_length=1, max_length=20, description="Tipo de transmissão")
    
    # Estrutura aninhada (opcional)
    motor_vehicle: Optional[MotorVehicleUpdateDto] = Field(None, description="Dados do veículo motor")
    
    # Campos diretos (para compatibilidade com formato flat)
    model: Optional[str] = Field(None, min_length=1, max_length=100, description="Modelo do veículo")
    year: Optional[int] = Field(None, ge=1900, le=2030, description="Ano do veículo")
    mileage: Optional[int] = Field(None, ge=0, description="Quilometragem do veículo")
    fuel_type: Optional[str] = Field(None, min_length=1, max_length=20, description="Tipo de combustível")
    color: Optional[str] = Field(None, min_length=1, max_length=50, description="Cor do veículo")
    city: Optional[str] = Field(None, min_length=1, max_length=100, description="Cidade")
    price: Optional[Decimal] = Field(None, gt=0, description="Preço do veículo")
    additional_description: Optional[str] = Field(None, description="Descrição adicional")

    @validator('price')
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v

    @validator('mileage')
    def validate_mileage(cls, v):
        if v is not None and v < 0:
            raise ValueError('Quilometragem não pode ser negativa')
        return v


class CarUpdateDto(BaseModel):
    """
    DTO para atualização de carro.
    
    Aplicando o princípio Open/Closed Principle (OCP) - 
    aberto para extensão, fechado para modificação.
    """
    # Dados do veículo base (opcionais para atualização)
    model: Optional[str] = Field(None, min_length=1, max_length=100, description="Modelo do veículo")
    year: Optional[str] = Field(None, min_length=4, max_length=20, description="Ano do veículo")
    mileage: Optional[int] = Field(None, ge=0, description="Quilometragem do veículo")
    fuel_type: Optional[str] = Field(None, min_length=1, max_length=20, description="Tipo de combustível")
    color: Optional[str] = Field(None, min_length=1, max_length=50, description="Cor do veículo")
    city: Optional[str] = Field(None, min_length=1, max_length=100, description="Cidade onde está o veículo")
    price: Optional[Decimal] = Field(None, gt=0, description="Preço do veículo")
    additional_description: Optional[str] = Field(None, description="Descrição adicional do veículo")
    
    # Dados específicos do carro (opcionais para atualização)
    bodywork: Optional[str] = Field(None, min_length=1, max_length=20, description="Tipo de carroceria")
    transmission: Optional[str] = Field(None, min_length=1, max_length=20, description="Tipo de transmissão")

    @validator('price')
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v

    @validator('mileage')
    def validate_mileage(cls, v):
        if v is not None and v < 0:
            raise ValueError('Quilometragem não pode ser negativa')
        return v


class MotorVehicleResponseDto(BaseModel):
    """
    DTO para resposta do veículo motor.
    """
    id: Optional[int] = Field(None, description="ID do veículo motor")
    model: str = Field(..., description="Modelo do veículo")
    year: str = Field(..., description="Ano do veículo")
    mileage: int = Field(..., description="Quilometragem do veículo")
    fuel_type: str = Field(..., description="Tipo de combustível")
    color: str = Field(..., description="Cor do veículo")
    city: str = Field(..., description="Cidade onde está o veículo")
    price: Decimal = Field(..., description="Preço do veículo")
    additional_description: Optional[str] = Field(None, description="Descrição adicional")
    status: str = Field(..., description="Status do veículo")
    created_at: Optional[datetime] = Field(None, description="Data de criação")
    updated_at: Optional[datetime] = Field(None, description="Data de última atualização")

    class Config:
        from_attributes = True


class CarResponseDto(BaseModel):
    """
    DTO para resposta de carro.
    
    Responsável apenas pela apresentação dos dados do carro.
    """
    id: Optional[int] = Field(None, description="ID do carro")
    motor_vehicle: Optional[MotorVehicleResponseDto] = Field(None, description="Dados do veículo motor")
    bodywork: str = Field(..., description="Tipo de carroceria")
    transmission: str = Field(..., description="Tipo de transmissão")
    updated_at: Optional[datetime] = Field(None, description="Data de última atualização")

    class Config:
        from_attributes = True


class CarSearchDto(BaseModel):
    """
    DTO para busca de carros com filtros.
    """
    model: Optional[str] = Field(None, description="Modelo do veículo")
    year: Optional[str] = Field(None, description="Ano do veículo")
    bodywork: Optional[str] = Field(None, description="Tipo de carroceria")
    transmission: Optional[str] = Field(None, description="Tipo de transmissão")
    fuel_type: Optional[str] = Field(None, description="Tipo de combustível")
    city: Optional[str] = Field(None, description="Cidade")
    min_price: Optional[Decimal] = Field(None, ge=0, description="Preço mínimo")
    max_price: Optional[Decimal] = Field(None, ge=0, description="Preço máximo")
    status: Optional[str] = Field(None, description="Status do veículo")
    skip: int = Field(0, ge=0, description="Número de registros para pular")
    limit: int = Field(100, ge=1, le=1000, description="Número máximo de registros")

    @validator('max_price')
    def validate_price_range(cls, v, values):
        if v is not None and 'min_price' in values and values['min_price'] is not None:
            if v < values['min_price']:
                raise ValueError('Preço máximo deve ser maior que o preço mínimo')
        return v


class CarSummaryDto(BaseModel):
    """
    DTO para resumo de carro (listagens).
    """
    id: Optional[int] = Field(None, description="ID do carro")
    model: str = Field(..., description="Modelo do veículo")
    year: str = Field(..., description="Ano do veículo")
    bodywork: str = Field(..., description="Tipo de carroceria")
    transmission: str = Field(..., description="Tipo de transmissão")
    price: Decimal = Field(..., description="Preço do veículo")
    city: str = Field(..., description="Cidade")
    status: str = Field(..., description="Status do veículo")
    mileage: int = Field(..., description="Quilometragem")
    fuel_type: str = Field(..., description="Tipo de combustível")
    color: str = Field(..., description="Cor do veículo")

    class Config:
        from_attributes = True


class CarListResponseDto(BaseModel):
    """
    DTO para resposta de lista de carros.
    """
    cars: List[CarSummaryDto] = Field(..., description="Lista de carros")
    total: int = Field(..., description="Total de carros encontrados")
    skip: int = Field(..., description="Número de registros pulados")
    limit: int = Field(..., description="Limite de registros por página")

    class Config:
        from_attributes = True
