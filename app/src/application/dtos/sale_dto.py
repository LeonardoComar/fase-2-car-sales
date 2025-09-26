from pydantic import BaseModel, Field, validator
from typing import Optional, List
from decimal import Decimal
from datetime import date


class CreateSaleRequest(BaseModel):
    """
    DTO para requisição de criação de venda.
    """
    client_id: int = Field(..., gt=0, description="ID do cliente")
    employee_id: int = Field(..., gt=0, description="ID do funcionário")
    vehicle_id: int = Field(..., gt=0, description="ID do veículo")
    total_amount: Decimal = Field(..., gt=0, description="Valor total da venda")
    payment_method: str = Field(..., description="Forma de pagamento")
    sale_date: date = Field(..., description="Data da venda")
    notes: Optional[str] = Field(None, max_length=1000, description="Observações da venda")
    discount_amount: Optional[Decimal] = Field(Decimal('0.00'), ge=0, description="Valor do desconto")
    tax_amount: Optional[Decimal] = Field(Decimal('0.00'), ge=0, description="Valor dos impostos")
    commission_rate: Optional[Decimal] = Field(Decimal('0.00'), ge=0, le=100, description="Taxa de comissão (%)")

    @validator('payment_method')
    def validate_payment_method(cls, v):
        valid_methods = ["À vista", "Cartão de crédito", "Cartão de débito", "Financiamento", "Consórcio", "PIX"]
        if v not in valid_methods:
            raise ValueError(f'Forma de pagamento deve ser uma das opções: {", ".join(valid_methods)}')
        return v

    @validator('discount_amount')
    def validate_discount(cls, v, values):
        if 'total_amount' in values and v and v > values['total_amount']:
            raise ValueError('Desconto não pode ser maior que o valor total')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "client_id": 1,
                "employee_id": 1,
                "vehicle_id": 1,
                "total_amount": 85000.00,
                "payment_method": "Financiamento",
                "sale_date": "2024-01-15",
                "notes": "Cliente interessado em garantia estendida",
                "discount_amount": 5000.00,
                "tax_amount": 1500.00,
                "commission_rate": 3.5
            }
        }


class UpdateSaleRequest(BaseModel):
    """
    DTO para requisição de atualização de venda.
    """
    total_amount: Optional[Decimal] = Field(None, gt=0, description="Valor total da venda")
    payment_method: Optional[str] = Field(None, description="Forma de pagamento")
    status: Optional[str] = Field(None, description="Status da venda")
    sale_date: Optional[date] = Field(None, description="Data da venda")
    notes: Optional[str] = Field(None, max_length=1000, description="Observações da venda")
    discount_amount: Optional[Decimal] = Field(None, ge=0, description="Valor do desconto")
    tax_amount: Optional[Decimal] = Field(None, ge=0, description="Valor dos impostos")
    commission_rate: Optional[Decimal] = Field(None, ge=0, le=100, description="Taxa de comissão (%)")

    @validator('payment_method')
    def validate_payment_method(cls, v):
        if v is not None:
            valid_methods = ["À vista", "Cartão de crédito", "Cartão de débito", "Financiamento", "Consórcio", "PIX"]
            if v not in valid_methods:
                raise ValueError(f'Forma de pagamento deve ser uma das opções: {", ".join(valid_methods)}')
        return v

    @validator('status')
    def validate_status(cls, v):
        if v is not None:
            valid_statuses = ["Pendente", "Confirmada", "Paga", "Entregue", "Cancelada"]
            if v not in valid_statuses:
                raise ValueError(f'Status deve ser um dos valores: {", ".join(valid_statuses)}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "total_amount": 87000.00,
                "payment_method": "À vista",
                "status": "Confirmada",
                "notes": "Pagamento à vista confirmado",
                "discount_amount": 7000.00,
                "commission_rate": 4.0
            }
        }


class UpdateSaleStatusRequest(BaseModel):
    """
    DTO para requisição de atualização de status da venda.
    """
    status: str = Field(..., description="Novo status da venda")

    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ["Pendente", "Confirmada", "Paga", "Entregue", "Cancelada"]
        if v not in valid_statuses:
            raise ValueError(f'Status deve ser um dos valores: {", ".join(valid_statuses)}')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "status": "Paga"
            }
        }


class ClientSummary(BaseModel):
    """
    DTO para resumo do cliente na resposta de venda.
    """
    id: int
    name: str
    email: str
    cpf: str

    class Config:
        from_attributes = True


class EmployeeSummary(BaseModel):
    """
    DTO para resumo do funcionário na resposta de venda.
    """
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class VehicleSummary(BaseModel):
    """
    DTO para resumo do veículo na resposta de venda.
    """
    id: int
    model: str
    year: str
    color: str
    price: Decimal

    class Config:
        from_attributes = True


class SaleResponse(BaseModel):
    """
    DTO para resposta da criação/consulta de venda.
    """
    id: int
    client: ClientSummary
    employee: EmployeeSummary
    vehicle: VehicleSummary
    total_amount: Decimal
    payment_method: str
    status: str
    sale_date: str
    notes: Optional[str]
    discount_amount: Decimal
    tax_amount: Decimal
    commission_rate: Decimal
    commission_amount: Decimal
    final_amount: Decimal
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "client": {
                    "id": 1,
                    "name": "João Silva",
                    "email": "joao@email.com",
                    "cpf": "123.456.789-00"
                },
                "employee": {
                    "id": 1,
                    "name": "Maria Santos",
                    "email": "maria@empresa.com"
                },
                "vehicle": {
                    "id": 1,
                    "model": "Civic",
                    "year": "2023",
                    "color": "Preto",
                    "price": "85000.00"
                },
                "total_amount": 85000.00,
                "payment_method": "Financiamento",
                "status": "Confirmada",
                "sale_date": "2024-01-15",
                "notes": "Venda com garantia estendida",
                "discount_amount": 5000.00,
                "tax_amount": 1500.00,
                "commission_rate": 3.5,
                "commission_amount": 2800.00,
                "final_amount": 81500.00,
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            }
        }


class SaleListResponse(BaseModel):
    """
    DTO para resposta de um item na listagem de vendas.
    """
    id: int
    client_name: str
    employee_name: str
    vehicle_model: str
    total_amount: Decimal
    payment_method: str
    status: str
    sale_date: str
    final_amount: Decimal

    class Config:
        from_attributes = True


class SalesListResponse(BaseModel):
    """
    DTO para resposta da listagem de vendas com paginação.
    """
    sales: List[SaleListResponse]
    total: int
    skip: int = Field(default=0, description="Número de registros pulados")
    limit: int = Field(default=100, description="Limite de registros")

    class Config:
        from_attributes = True


class SaleStatisticsResponse(BaseModel):
    """
    DTO para resposta de estatísticas de vendas.
    """
    total_sales: int = Field(..., description="Total de vendas")
    total_revenue: Decimal = Field(..., description="Receita total")
    total_commission: Decimal = Field(..., description="Comissão total")
    average_sale_value: Decimal = Field(..., description="Valor médio das vendas")
    sales_by_status: dict = Field(..., description="Vendas por status")
    sales_by_payment_method: dict = Field(..., description="Vendas por método de pagamento")
    period_start: str = Field("", description="Data inicial do período")
    period_end: str = Field("", description="Data final do período")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "total_sales": 25,
                "total_revenue": 1250000.00,
                "total_commission": 43750.00,
                "average_sale_value": 50000.00,
                "sales_by_status": {
                    "Confirmada": 20,
                    "Pendente": 3,
                    "Cancelada": 2
                },
                "sales_by_payment_method": {
                    "Financiamento": 15,
                    "À vista": 8,
                    "Cartão de crédito": 2
                },
                "period_start": "2024-01-01",
                "period_end": "2024-01-31"
            }
        }
