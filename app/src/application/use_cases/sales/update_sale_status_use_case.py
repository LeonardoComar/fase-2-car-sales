from typing import Optional
from uuid import UUID

from src.domain.entities.sale import Sale
from src.domain.ports.sale_repository import SaleRepository
from src.application.dtos.sale_dto import SaleStatusUpdateDto, SaleResponseDto
from src.domain.exceptions import ValidationError


class UpdateSaleStatusUseCase:
    """
    Caso de uso para atualização de status de venda.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela atualização de status de vendas.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração SaleRepository.
    """
    
    def __init__(self, sale_repository: SaleRepository):
        self._sale_repository = sale_repository
    
    async def execute(self, sale_id: UUID, status_data: SaleStatusUpdateDto) -> Optional[SaleResponseDto]:
        """
        Executa a atualização de status de uma venda.
        
        Args:
            sale_id: ID da venda
            status_data: Dados do novo status
            
        Returns:
            Optional[SaleResponseDto]: Dados da venda atualizada ou None se não encontrada
            
        Raises:
            ValidationError: Se transição de status inválida
        """
        # Buscar venda existente
        sale = await self._sale_repository.find_by_id(sale_id)
        if not sale:
            return None
        
        # Aplicar transição de status usando métodos de domínio
        new_status = status_data.status
        
        if new_status == Sale.STATUS_CONFIRMADA:
            sale.confirm_sale()
        elif new_status == Sale.STATUS_PAGA:
            sale.mark_as_paid()
        elif new_status == Sale.STATUS_ENTREGUE:
            sale.mark_as_delivered()
        elif new_status == Sale.STATUS_CANCELADA:
            sale.cancel_sale()
        elif new_status == Sale.STATUS_PENDENTE:
            # Volta para pendente só é permitida de confirmada
            if sale.status != Sale.STATUS_CONFIRMADA:
                raise ValidationError("Só é possível voltar para pendente a partir de confirmada")
            sale.status = Sale.STATUS_PENDENTE
            sale.updated_at = sale.updated_at.__class__.utcnow()
        else:
            raise ValidationError(f"Status inválido: {new_status}")
        
        # Salvar no repositório
        updated_sale = await self._sale_repository.save(sale)
        
        # Converter para DTO de resposta
        return self._to_response_dto(updated_sale)
    
    def _to_response_dto(self, sale: Sale) -> SaleResponseDto:
        """Converte entidade Sale para DTO de resposta."""
        return SaleResponseDto(
            id=sale.id,
            client_id=sale.client_id,
            employee_id=sale.employee_id,
            vehicle_id=sale.vehicle_id,
            total_amount=sale.total_amount,
            payment_method=sale.payment_method,
            status=sale.status,
            sale_date=sale.sale_date,
            notes=sale.notes,
            discount_amount=sale.discount_amount,
            tax_amount=sale.tax_amount,
            commission_rate=sale.commission_rate,
            commission_amount=sale.commission_amount,
            final_amount=sale.calculate_final_amount(),
            created_at=sale.created_at.isoformat(),
            updated_at=sale.updated_at.isoformat()
        )
