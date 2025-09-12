"""
Entidade Sale - Domain Layer

Entidade que representa uma venda no domínio da aplicação.

Aplicando princípios SOLID:
- SRP: Responsável apenas por representar e validar dados de vendas
- OCP: Extensível para novas funcionalidades sem modificar código existente
- LSP: Pode ser substituída por especializações
- ISP: Interface específica e coesa
- DIP: Não depende de detalhes de implementação
"""

from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class Sale:
    """
    Entidade Sale que representa uma venda no domínio da aplicação.
    """
    
    # Status possíveis para vendas
    STATUS_PENDENTE = "Pendente"
    STATUS_CONFIRMADA = "Confirmada"
    STATUS_PAGA = "Paga"
    STATUS_ENTREGUE = "Entregue"
    STATUS_CANCELADA = "Cancelada"
    
    VALID_STATUSES = [STATUS_PENDENTE, STATUS_CONFIRMADA, STATUS_PAGA, STATUS_ENTREGUE, STATUS_CANCELADA]

    # Formas de pagamento possíveis
    PAYMENT_A_VISTA = "À vista"
    PAYMENT_CARTAO_CREDITO = "Cartão de crédito"
    PAYMENT_CARTAO_DEBITO = "Cartão de débito"
    PAYMENT_FINANCIAMENTO = "Financiamento"
    PAYMENT_CONSORCIO = "Consórcio"
    PAYMENT_PIX = "PIX"
    
    VALID_PAYMENT_METHODS = [
        PAYMENT_A_VISTA, PAYMENT_CARTAO_CREDITO, PAYMENT_CARTAO_DEBITO,
        PAYMENT_FINANCIAMENTO, PAYMENT_CONSORCIO, PAYMENT_PIX
    ]

    def __init__(
        self,
        client_id: int,
        employee_id: int,
        vehicle_id: int,
        total_amount: Decimal,
        payment_method: str,
        sale_date: date,
        status: str = STATUS_PENDENTE,
        notes: Optional[str] = None,
        discount_amount: Decimal = Decimal('0.00'),
        tax_amount: Decimal = Decimal('0.00'),
        commission_rate: Decimal = Decimal('0.00'),
        commission_amount: Decimal = Decimal('0.00'),
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Inicializa uma nova instância de Sale.
        
        Args:
            client_id: ID do cliente
            employee_id: ID do funcionário
            vehicle_id: ID do veículo
            total_amount: Valor total da venda
            payment_method: Forma de pagamento
            sale_date: Data da venda
            status: Status da venda
            notes: Observações da venda (opcional)
            discount_amount: Valor do desconto
            tax_amount: Valor dos impostos
            commission_rate: Taxa de comissão
            commission_amount: Valor da comissão
            id: ID da venda (opcional, para entidades já persistidas)
            created_at: Data de criação (opcional)
            updated_at: Data de atualização (opcional)
        """
        self.id = id
        self.client_id = client_id
        self.employee_id = employee_id
        self.vehicle_id = vehicle_id
        self.total_amount = total_amount
        self.payment_method = payment_method
        self.status = status
        self.sale_date = sale_date
        self.notes = notes
        self.discount_amount = discount_amount
        self.tax_amount = tax_amount
        self.commission_rate = commission_rate
        self.commission_amount = commission_amount
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_sale(
        cls,
        client_id: int,
        employee_id: int,
        vehicle_id: int,
        total_amount: Decimal,
        payment_method: str,
        sale_date: date,
        notes: Optional[str] = None,
        discount_amount: Decimal = Decimal('0.00'),
        tax_amount: Decimal = Decimal('0.00'),
        commission_rate: Decimal = Decimal('0.00')
    ) -> 'Sale':
        """
        Método de classe para criar uma venda.
        
        Args:
            client_id: ID do cliente
            employee_id: ID do funcionário
            vehicle_id: ID do veículo
            total_amount: Valor total da venda
            payment_method: Forma de pagamento
            sale_date: Data da venda
            notes: Observações da venda (opcional)
            discount_amount: Valor do desconto
            tax_amount: Valor dos impostos
            commission_rate: Taxa de comissão
            
        Returns:
            Sale: Nova instância de Sale
        """
        # Calcular comissão automaticamente
        commission_amount = (total_amount - discount_amount) * (commission_rate / 100)
        
        return cls(
            client_id=client_id,
            employee_id=employee_id,
            vehicle_id=vehicle_id,
            total_amount=total_amount,
            payment_method=payment_method,
            sale_date=sale_date,
            status=cls.STATUS_PENDENTE,
            notes=notes,
            discount_amount=discount_amount,
            tax_amount=tax_amount,
            commission_rate=commission_rate,
            commission_amount=commission_amount
        )

    def update_fields(
        self,
        total_amount: Optional[Decimal] = None,
        payment_method: Optional[str] = None,
        status: Optional[str] = None,
        sale_date: Optional[date] = None,
        notes: Optional[str] = None,
        discount_amount: Optional[Decimal] = None,
        tax_amount: Optional[Decimal] = None,
        commission_rate: Optional[Decimal] = None
    ):
        """
        Atualiza os campos da venda.
        
        Args:
            total_amount: Valor total da venda (opcional)
            payment_method: Forma de pagamento (opcional)
            status: Status da venda (opcional)
            sale_date: Data da venda (opcional)
            notes: Observações da venda (opcional)
            discount_amount: Valor do desconto (opcional)
            tax_amount: Valor dos impostos (opcional)
            commission_rate: Taxa de comissão (opcional)
        """
        if total_amount is not None:
            self.total_amount = total_amount
        if payment_method is not None:
            self.payment_method = payment_method
        if status is not None:
            self.status = status
        if sale_date is not None:
            self.sale_date = sale_date
        if notes is not None:
            self.notes = notes
        if discount_amount is not None:
            self.discount_amount = discount_amount
        if tax_amount is not None:
            self.tax_amount = tax_amount
        if commission_rate is not None:
            self.commission_rate = commission_rate
            # Recalcular comissão
            self.commission_amount = (self.total_amount - self.discount_amount) * (self.commission_rate / 100)

    def confirm_sale(self):
        """Confirma a venda."""
        self.status = self.STATUS_CONFIRMADA

    def mark_as_paid(self):
        """Marca a venda como paga."""
        self.status = self.STATUS_PAGA

    def mark_as_delivered(self):
        """Marca a venda como entregue."""
        self.status = self.STATUS_ENTREGUE

    def cancel_sale(self):
        """Cancela a venda."""
        self.status = self.STATUS_CANCELADA

    def calculate_final_amount(self) -> Decimal:
        """
        Calcula o valor final da venda (total - desconto + impostos).
        
        Returns:
            Decimal: Valor final da venda
        """
        return self.total_amount - self.discount_amount + self.tax_amount

    def is_active(self) -> bool:
        """
        Verifica se a venda está ativa (não cancelada).
        
        Returns:
            bool: True se a venda está ativa
        """
        return self.status != self.STATUS_CANCELADA

    def is_completed(self) -> bool:
        """
        Verifica se a venda foi completada (entregue).
        
        Returns:
            bool: True se a venda foi completada
        """
        return self.status == self.STATUS_ENTREGUE

    @classmethod
    def is_valid_status(cls, status: str) -> bool:
        """
        Verifica se o status é válido.
        
        Args:
            status: Status a ser validado
            
        Returns:
            bool: True se o status é válido
        """
        return status in cls.VALID_STATUSES

    @classmethod
    def is_valid_payment_method(cls, payment_method: str) -> bool:
        """
        Verifica se a forma de pagamento é válida.
        
        Args:
            payment_method: Forma de pagamento a ser validada
            
        Returns:
            bool: True se a forma de pagamento é válida
        """
        return payment_method in cls.VALID_PAYMENT_METHODS

    def __repr__(self):
        return f"<Sale(id={self.id}, client_id={self.client_id}, total={self.total_amount}, status='{self.status}')>"
