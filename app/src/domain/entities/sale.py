from typing import Optional
from decimal import Decimal
from datetime import date, datetime
from uuid import UUID, uuid4

from src.domain.exceptions import ValidationError


class Sale:
    """
    Entidade Sale que representa uma venda na concessionária.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pelas regras de negócio relacionadas a vendas.
    
    Aplicando o princípio Open/Closed Principle (OCP) - 
    pode ser estendida sem modificar código existente.
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
        client_id: UUID,
        employee_id: UUID,
        vehicle_id: UUID,
        total_amount: Decimal,
        payment_method: str,
        sale_date: date,
        id: Optional[UUID] = None,
        status: str = STATUS_PENDENTE,
        notes: Optional[str] = None,
        discount_amount: Decimal = Decimal('0.00'),
        tax_amount: Decimal = Decimal('0.00'),
        commission_rate: Decimal = Decimal('0.00'),
        commission_amount: Optional[Decimal] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id or uuid4()
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
        
        # Calcular comissão se não fornecida
        if commission_amount is None:
            self.commission_amount = self._calculate_commission()
        else:
            self.commission_amount = commission_amount
            
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        
        # Validar dados
        self._validate()
    
    @classmethod
    def create_sale(
        cls,
        client_id: UUID,
        employee_id: UUID,
        vehicle_id: UUID,
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
            notes: Observações opcionais
            discount_amount: Valor do desconto
            tax_amount: Valor dos impostos
            commission_rate: Taxa de comissão (%)
            
        Returns:
            Sale: Nova instância da venda
            
        Raises:
            ValidationError: Se dados inválidos
        """
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
            commission_rate=commission_rate
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
    ) -> None:
        """
        Atualiza os campos da venda.
        
        Args:
            total_amount: Novo valor total
            payment_method: Nova forma de pagamento
            status: Novo status
            sale_date: Nova data da venda
            notes: Novas observações
            discount_amount: Novo valor do desconto
            tax_amount: Novo valor dos impostos
            commission_rate: Nova taxa de comissão
            
        Raises:
            ValidationError: Se dados inválidos
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
            # Recalcular comissão quando taxa muda
            self.commission_amount = self._calculate_commission()
        
        self.updated_at = datetime.utcnow()
        self._validate()
    
    def confirm_sale(self) -> None:
        """
        Confirma a venda.
        
        Raises:
            ValidationError: Se venda não pode ser confirmada
        """
        if self.status != self.STATUS_PENDENTE:
            raise ValidationError("Apenas vendas pendentes podem ser confirmadas")
        
        self.status = self.STATUS_CONFIRMADA
        self.updated_at = datetime.utcnow()
    
    def mark_as_paid(self) -> None:
        """
        Marca a venda como paga.
        
        Raises:
            ValidationError: Se venda não pode ser marcada como paga
        """
        if self.status not in [self.STATUS_CONFIRMADA, self.STATUS_PENDENTE]:
            raise ValidationError("Apenas vendas confirmadas ou pendentes podem ser marcadas como pagas")
        
        self.status = self.STATUS_PAGA
        self.updated_at = datetime.utcnow()
    
    def mark_as_delivered(self) -> None:
        """
        Marca a venda como entregue.
        
        Raises:
            ValidationError: Se venda não pode ser entregue
        """
        if self.status != self.STATUS_PAGA:
            raise ValidationError("Apenas vendas pagas podem ser marcadas como entregues")
        
        self.status = self.STATUS_ENTREGUE
        self.updated_at = datetime.utcnow()
    
    def cancel_sale(self) -> None:
        """
        Cancela a venda.
        
        Raises:
            ValidationError: Se venda não pode ser cancelada
        """
        if self.status == self.STATUS_ENTREGUE:
            raise ValidationError("Vendas entregues não podem ser canceladas")
        
        self.status = self.STATUS_CANCELADA
        self.updated_at = datetime.utcnow()
    
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
            bool: True se ativa, False se cancelada
        """
        return self.status != self.STATUS_CANCELADA
    
    def is_completed(self) -> bool:
        """
        Verifica se a venda foi completada (entregue).
        
        Returns:
            bool: True se completada, False caso contrário
        """
        return self.status == self.STATUS_ENTREGUE
    
    def _calculate_commission(self) -> Decimal:
        """
        Calcula o valor da comissão.
        
        Returns:
            Decimal: Valor da comissão
        """
        base_amount = self.total_amount - self.discount_amount
        return base_amount * (self.commission_rate / 100)
    
    def _validate(self) -> None:
        """
        Valida os dados da venda.
        
        Raises:
            ValidationError: Se dados inválidos
        """
        # Validar valores monetários
        if self.total_amount <= 0:
            raise ValidationError("Valor total deve ser maior que zero")
        
        if self.discount_amount < 0:
            raise ValidationError("Desconto não pode ser negativo")
        
        if self.discount_amount > self.total_amount:
            raise ValidationError("Desconto não pode ser maior que o valor total")
        
        if self.tax_amount < 0:
            raise ValidationError("Valor do imposto não pode ser negativo")
        
        if self.commission_rate < 0 or self.commission_rate > 100:
            raise ValidationError("Taxa de comissão deve estar entre 0 e 100%")
        
        # Validar status
        if not self.is_valid_status(self.status):
            raise ValidationError(f"Status inválido: {self.status}")
        
        # Validar forma de pagamento
        if not self.is_valid_payment_method(self.payment_method):
            raise ValidationError(f"Forma de pagamento inválida: {self.payment_method}")
        
        # Validar observações
        if self.notes and len(self.notes) > 1000:
            raise ValidationError("Observações não podem ter mais de 1000 caracteres")
        
        # Validar data da venda
        if self.sale_date > date.today():
            raise ValidationError("Data da venda não pode ser no futuro")
    
    @classmethod
    def is_valid_status(cls, status: str) -> bool:
        """
        Verifica se o status é válido.
        
        Args:
            status: Status a ser verificado
            
        Returns:
            bool: True se válido, False caso contrário
        """
        return status in cls.VALID_STATUSES
    
    @classmethod
    def is_valid_payment_method(cls, payment_method: str) -> bool:
        """
        Verifica se a forma de pagamento é válida.
        
        Args:
            payment_method: Forma de pagamento a ser verificada
            
        Returns:
            bool: True se válida, False caso contrário
        """
        return payment_method in cls.VALID_PAYMENT_METHODS
    
    def __repr__(self):
        return f"<Sale(id={self.id}, client_id={self.client_id}, total={self.total_amount}, status='{self.status}')>"
    
    def __str__(self):
        return f"Venda {self.id}: {self.total_amount} ({self.status})"
