from typing import List

from src.domain.entities.sale import Sale
from src.domain.ports.sale_repository import SaleRepository
from src.application.dtos.sale_dto import SaleSearchDto, SaleResponseDto


class ListSalesUseCase:
    """
    Caso de uso para listagem de vendas.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela listagem de vendas.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração SaleRepository.
    """
    
    def __init__(self, sale_repository: SaleRepository):
        self._sale_repository = sale_repository
    
    async def execute(self, search_criteria: SaleSearchDto) -> List[SaleResponseDto]:
        """
        Executa a busca de vendas com critérios.
        
        Args:
            search_criteria: Critérios de busca
            
        Returns:
            List[SaleResponseDto]: Lista de vendas encontradas
        """
        # Preparar critérios de busca
        criteria = {}
        
        if search_criteria.client_id:
            criteria['client_id'] = search_criteria.client_id
        
        if search_criteria.employee_id:
            criteria['employee_id'] = search_criteria.employee_id
        
        if search_criteria.vehicle_id:
            criteria['vehicle_id'] = search_criteria.vehicle_id
        
        if search_criteria.status:
            criteria['status'] = search_criteria.status
        
        if search_criteria.payment_method:
            criteria['payment_method'] = search_criteria.payment_method
        
        if search_criteria.start_date:
            criteria['start_date'] = search_criteria.start_date
        
        if search_criteria.end_date:
            criteria['end_date'] = search_criteria.end_date
        
        if search_criteria.min_amount:
            criteria['min_amount'] = search_criteria.min_amount
        
        if search_criteria.max_amount:
            criteria['max_amount'] = search_criteria.max_amount
        
        if search_criteria.active_only:
            criteria['active_only'] = search_criteria.active_only
        
        if search_criteria.completed_only:
            criteria['completed_only'] = search_criteria.completed_only
        
        # Parâmetros de paginação e ordenação
        criteria['skip'] = search_criteria.skip or 0
        criteria['limit'] = search_criteria.limit or 100
        criteria['order_by'] = search_criteria.order_by
        criteria['order_direction'] = search_criteria.order_direction
        
        # Buscar vendas no repositório
        sales = await self._sale_repository.find_by_criteria(**criteria)
        
        # Converter para DTOs de resposta
        return [self._to_response_dto(sale) for sale in sales]
    
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
