from typing import Optional
from uuid import UUID

from src.domain.entities.sale import Sale
from src.domain.ports.sale_repository import SaleRepository
from src.application.dtos.sale_dto import SaleUpdateDto, SaleResponseDto
from src.domain.exceptions import ValidationError


class UpdateSaleUseCase:
    """
    Caso de uso para atualização de venda.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela atualização de vendas.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração SaleRepository.
    """
    
    def __init__(self, sale_repository: SaleRepository):
        self._sale_repository = sale_repository
    
    async def execute(self, sale_id: UUID, sale_data: SaleUpdateDto) -> Optional[SaleResponseDto]:
        """
        Executa a atualização de uma venda.
        
        Args:
            sale_id: ID da venda a ser atualizada
            sale_data: Dados de atualização
            
        Returns:
            Optional[SaleResponseDto]: Dados da venda atualizada ou None se não encontrada
            
        Raises:
            ValidationError: Se dados inválidos ou operação não permitida
        """
        # Buscar venda existente
        sale = await self._sale_repository.find_by_id(sale_id)
        if not sale:
            return None
        
        # Verificar se venda pode ser atualizada
        if sale.status == Sale.STATUS_CANCELADA:
            raise ValidationError("Vendas canceladas não podem ser atualizadas")
        
        if sale.status == Sale.STATUS_ENTREGUE:
            raise ValidationError("Vendas entregues não podem ser atualizadas")
        
        # Aplicar atualizações
        update_data = {}
        
        if sale_data.total_amount is not None:
            update_data['total_amount'] = sale_data.total_amount
        
        if sale_data.payment_method is not None:
            update_data['payment_method'] = sale_data.payment_method
        
        if sale_data.status is not None:
            update_data['status'] = sale_data.status
        
        if sale_data.sale_date is not None:
            update_data['sale_date'] = sale_data.sale_date
        
        if sale_data.notes is not None:
            update_data['notes'] = sale_data.notes
        
        if sale_data.discount_amount is not None:
            update_data['discount_amount'] = sale_data.discount_amount
        
        if sale_data.tax_amount is not None:
            update_data['tax_amount'] = sale_data.tax_amount
        
        if sale_data.commission_rate is not None:
            update_data['commission_rate'] = sale_data.commission_rate
        
        # Aplicar atualizações na entidade
        if update_data:
            sale.update_fields(**update_data)
        
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
