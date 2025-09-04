from typing import Optional
from uuid import UUID

from src.domain.entities.sale import Sale
from src.domain.ports.sale_repository import SaleRepository
from src.application.dtos.sale_dto import SaleResponseDto
from src.domain.exceptions import ValidationError


class GetSaleByIdUseCase:
    """
    Caso de uso para buscar venda por ID.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela busca de venda por ID.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração SaleRepository.
    """
    
    def __init__(self, sale_repository: SaleRepository):
        self._sale_repository = sale_repository
    
    async def execute(self, sale_id: UUID) -> Optional[SaleResponseDto]:
        """
        Executa a busca de uma venda por ID.
        
        Args:
            sale_id: ID da venda
            
        Returns:
            Optional[SaleResponseDto]: Dados da venda encontrada ou None
        """
        # Buscar venda no repositório
        sale = await self._sale_repository.find_by_id(sale_id)
        
        if not sale:
            return None
        
        # Converter para DTO de resposta
        return self._to_response_dto(sale)
    
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
