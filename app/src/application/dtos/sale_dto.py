from pydantic import BaseModel, Field, validator
from typing import Optional, List
from decimal import Decimal
from datetime import date
from uuid import UUID


class SaleCreateDto(BaseModel):
    """
    DTO para criação de venda.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela validação de dados de criação de venda.
    """
    client_id: UUID = Field(..., description="ID do cliente")
    employee_id: UUID = Field(..., description="ID do funcionário")
    vehicle_id: UUID = Field(..., description="ID do veículo")
    total_amount: Decimal = Field(..., gt=0, description="Valor total da venda")
    payment_method: str = Field(..., min_length=1, max_length=50, description="Forma de pagamento")
    sale_date: date = Field(..., description="Data da venda")
    notes: Optional[str] = Field(None, max_length=1000, description="Observações da venda")
    discount_amount: Optional[Decimal] = Field(Decimal('0.00'), ge=0, description="Valor do desconto")
    tax_amount: Optional[Decimal] = Field(Decimal('0.00'), ge=0, description="Valor dos impostos")
    commission_rate: Optional[Decimal] = Field(Decimal('0.00'), ge=0, le=100, description="Taxa de comissão (%)")

    @validator('payment_method')
    def validate_payment_method(cls, v):
        """Valida forma de pagamento."""
        valid_methods = [
            "À vista", "Cartão de crédito", "Cartão de débito",
            "Financiamento", "Consórcio", "PIX"
        ]
        if v not in valid_methods:
            raise ValueError(f"Forma de pagamento deve ser uma das opções: {', '.join(valid_methods)}")
        return v

    @validator('discount_amount')
    def validate_discount(cls, v, values):
        """Valida desconto."""
        if 'total_amount' in values and v and v > values['total_amount']:
            raise ValueError("Desconto não pode ser maior que o valor total")
        return v

    @validator('sale_date')
    def validate_sale_date(cls, v):
        """Valida data da venda."""
        if v > date.today():
            raise ValueError("Data da venda não pode ser no futuro")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "123e4567-e89b-12d3-a456-426614174000",
                "employee_id": "987fcdeb-51a2-43d1-9f12-123456789abc",
                "vehicle_id": "456e7890-e89b-12d3-a456-426614174111",
                "total_amount": 85000.00,
                "payment_method": "Financiamento",
                "sale_date": "2024-01-15",
                "notes": "Cliente interessado em garantia estendida",
                "discount_amount": 5000.00,
                "tax_amount": 1500.00,
                "commission_rate": 3.5
            }
        }


class SaleUpdateDto(BaseModel):
    """
    DTO para atualização de venda.
    """
    total_amount: Optional[Decimal] = Field(None, gt=0, description="Valor total da venda")
    payment_method: Optional[str] = Field(None, min_length=1, max_length=50, description="Forma de pagamento")
    status: Optional[str] = Field(None, description="Status da venda")
    sale_date: Optional[date] = Field(None, description="Data da venda")
    notes: Optional[str] = Field(None, max_length=1000, description="Observações da venda")
    discount_amount: Optional[Decimal] = Field(None, ge=0, description="Valor do desconto")
    tax_amount: Optional[Decimal] = Field(None, ge=0, description="Valor dos impostos")
    commission_rate: Optional[Decimal] = Field(None, ge=0, le=100, description="Taxa de comissão (%)")

    @validator('payment_method')
    def validate_payment_method(cls, v):
        """Valida forma de pagamento."""
        if v is not None:
            valid_methods = [
                "À vista", "Cartão de crédito", "Cartão de débito",
                "Financiamento", "Consórcio", "PIX"
            ]
            if v not in valid_methods:
                raise ValueError(f"Forma de pagamento deve ser uma das opções: {', '.join(valid_methods)}")
        return v

    @validator('status')
    def validate_status(cls, v):
        """Valida status."""
        if v is not None:
            valid_statuses = ["Pendente", "Confirmada", "Paga", "Entregue", "Cancelada"]
            if v not in valid_statuses:
                raise ValueError(f"Status deve ser um dos valores: {', '.join(valid_statuses)}")
        return v

    @validator('sale_date')
    def validate_sale_date(cls, v):
        """Valida data da venda."""
        if v is not None and v > date.today():
            raise ValueError("Data da venda não pode ser no futuro")
        return v

    @validator('discount_amount')
    def validate_discount(cls, v, values):
        """Valida desconto."""
        if v is not None and 'total_amount' in values and values['total_amount'] and v > values['total_amount']:
            raise ValueError("Desconto não pode ser maior que o valor total")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "total_amount": 90000.00,
                "payment_method": "À vista",
                "status": "Confirmada",
                "discount_amount": 3000.00,
                "notes": "Cliente decidiu por pagamento à vista"
            }
        }


class SaleResponseDto(BaseModel):
    """
    DTO para resposta de venda.
    """
    id: UUID = Field(..., description="ID da venda")
    client_id: UUID = Field(..., description="ID do cliente")
    employee_id: UUID = Field(..., description="ID do funcionário")
    vehicle_id: UUID = Field(..., description="ID do veículo")
    total_amount: Decimal = Field(..., description="Valor total da venda")
    payment_method: str = Field(..., description="Forma de pagamento")
    status: str = Field(..., description="Status da venda")
    sale_date: date = Field(..., description="Data da venda")
    notes: Optional[str] = Field(None, description="Observações da venda")
    discount_amount: Decimal = Field(..., description="Valor do desconto")
    tax_amount: Decimal = Field(..., description="Valor dos impostos")
    commission_rate: Decimal = Field(..., description="Taxa de comissão (%)")
    commission_amount: Decimal = Field(..., description="Valor da comissão")
    final_amount: Decimal = Field(..., description="Valor final (total - desconto + impostos)")
    created_at: str = Field(..., description="Data/hora de criação")
    updated_at: str = Field(..., description="Data/hora da última atualização")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "client_id": "987fcdeb-51a2-43d1-9f12-123456789abc",
                "employee_id": "456e7890-e89b-12d3-a456-426614174111",
                "vehicle_id": "789e0123-e89b-12d3-a456-426614174222",
                "total_amount": 85000.00,
                "payment_method": "Financiamento",
                "status": "Confirmada",
                "sale_date": "2024-01-15",
                "notes": "Cliente interessado em garantia estendida",
                "discount_amount": 5000.00,
                "tax_amount": 1500.00,
                "commission_rate": 3.5,
                "commission_amount": 2800.00,
                "final_amount": 81500.00,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T14:45:00Z"
            }
        }


class SaleSearchDto(BaseModel):
    """
    DTO para busca de vendas.
    """
    client_id: Optional[UUID] = Field(None, description="ID do cliente")
    employee_id: Optional[UUID] = Field(None, description="ID do funcionário")
    vehicle_id: Optional[UUID] = Field(None, description="ID do veículo")
    status: Optional[str] = Field(None, description="Status da venda")
    payment_method: Optional[str] = Field(None, description="Forma de pagamento")
    start_date: Optional[date] = Field(None, description="Data inicial")
    end_date: Optional[date] = Field(None, description="Data final")
    min_amount: Optional[Decimal] = Field(None, ge=0, description="Valor mínimo")
    max_amount: Optional[Decimal] = Field(None, ge=0, description="Valor máximo")
    active_only: Optional[bool] = Field(None, description="Apenas vendas ativas (não canceladas)")
    completed_only: Optional[bool] = Field(None, description="Apenas vendas entregues")
    order_by: Optional[str] = Field(None, description="Campo para ordenação")
    order_direction: Optional[str] = Field("asc", description="Direção da ordenação (asc/desc)")
    skip: Optional[int] = Field(0, ge=0, description="Número de registros para pular")
    limit: Optional[int] = Field(100, ge=1, le=1000, description="Número máximo de registros")

    @validator('status')
    def validate_status(cls, v):
        """Valida status."""
        if v is not None:
            valid_statuses = ["Pendente", "Confirmada", "Paga", "Entregue", "Cancelada"]
            if v not in valid_statuses:
                raise ValueError(f"Status deve ser um dos valores: {', '.join(valid_statuses)}")
        return v

    @validator('payment_method')
    def validate_payment_method(cls, v):
        """Valida forma de pagamento."""
        if v is not None:
            valid_methods = [
                "À vista", "Cartão de crédito", "Cartão de débito",
                "Financiamento", "Consórcio", "PIX"
            ]
            if v not in valid_methods:
                raise ValueError(f"Forma de pagamento deve ser uma das opções: {', '.join(valid_methods)}")
        return v

    @validator('order_by')
    def validate_order_by(cls, v):
        """Valida campo de ordenação."""
        if v is not None:
            valid_fields = ["sale_date", "total_amount", "status", "created_at", "final_amount"]
            if v not in valid_fields:
                raise ValueError(f"Campo de ordenação deve ser um dos valores: {', '.join(valid_fields)}")
        return v

    @validator('order_direction')
    def validate_order_direction(cls, v):
        """Valida direção da ordenação."""
        if v not in ["asc", "desc"]:
            raise ValueError("Direção deve ser 'asc' ou 'desc'")
        return v

    @validator('end_date')
    def validate_date_range(cls, v, values):
        """Valida período de datas."""
        if v is not None and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError("Data final deve ser posterior à data inicial")
        return v

    @validator('max_amount')
    def validate_amount_range(cls, v, values):
        """Valida faixa de valores."""
        if v is not None and 'min_amount' in values and values['min_amount'] and v < values['min_amount']:
            raise ValueError("Valor máximo deve ser maior que o valor mínimo")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "987fcdeb-51a2-43d1-9f12-123456789abc",
                "status": "Confirmada",
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "min_amount": 50000.00,
                "order_by": "sale_date",
                "order_direction": "desc",
                "limit": 50
            }
        }


class SaleStatusUpdateDto(BaseModel):
    """
    DTO para atualização de status de venda.
    """
    status: str = Field(..., description="Novo status da venda")

    @validator('status')
    def validate_status(cls, v):
        """Valida status."""
        valid_statuses = ["Pendente", "Confirmada", "Paga", "Entregue", "Cancelada"]
        if v not in valid_statuses:
            raise ValueError(f"Status deve ser um dos valores: {', '.join(valid_statuses)}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "status": "Confirmada"
            }
        }


class SalesStatisticsDto(BaseModel):
    """
    DTO para estatísticas de vendas.
    """
    total_sales: int = Field(..., description="Número total de vendas")
    total_amount: Decimal = Field(..., description="Valor total das vendas")
    average_sale_amount: Decimal = Field(..., description="Valor médio por venda")
    total_commission: Decimal = Field(..., description="Total de comissões")
    sales_by_status: dict = Field(..., description="Vendas por status")
    sales_by_payment_method: dict = Field(..., description="Vendas por forma de pagamento")
    top_performers: List[dict] = Field(..., description="Top vendedores")

    class Config:
        json_schema_extra = {
            "example": {
                "total_sales": 150,
                "total_amount": 12750000.00,
                "average_sale_amount": 85000.00,
                "total_commission": 446250.00,
                "sales_by_status": {
                    "Pendente": 10,
                    "Confirmada": 25,
                    "Paga": 40,
                    "Entregue": 70,
                    "Cancelada": 5
                },
                "sales_by_payment_method": {
                    "Financiamento": 80,
                    "À vista": 30,
                    "Cartão de crédito": 25,
                    "PIX": 15
                },
                "top_performers": [
                    {
                        "employee_id": "987fcdeb-51a2-43d1-9f12-123456789abc",
                        "sales_count": 25,
                        "total_amount": 2125000.00,
                        "total_commission": 74375.00
                    }
                ]
            }
        }
