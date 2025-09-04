from typing import Optional
from uuid import UUID

from src.domain.entities.sale import Sale
from src.domain.ports.sale_repository import SaleRepository
from src.application.dtos.sale_dto import SaleCreateDto, SaleResponseDto
from src.domain.exceptions import ValidationError


class CreateSaleUseCase:
    """
    Caso de uso para criação de venda.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela criação de vendas.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração SaleRepository.
    """
    
    def __init__(self, sale_repository: SaleRepository):
        self._sale_repository = sale_repository
    
    async def execute(self, sale_data: SaleCreateDto) -> SaleResponseDto:
        """
        Executa a criação de uma venda.
        
        Args:
            sale_data: Dados da venda a ser criada
            
        Returns:
            SaleResponseDto: Dados da venda criada
            
        Raises:
            DomainValidationError: Se dados inválidos
            Exception: Se erro na persistência
        """
        # Verificar se veículo já foi vendido
        if await self._sale_repository.exists_by_vehicle(sale_data.vehicle_id):
            raise ValidationError("Veículo já foi vendido")
        
        # Criar entidade Sale
        sale = Sale.create_sale(
            client_id=sale_data.client_id,
            employee_id=sale_data.employee_id,
            vehicle_id=sale_data.vehicle_id,
            total_amount=sale_data.total_amount,
            payment_method=sale_data.payment_method,
            sale_date=sale_data.sale_date,
            notes=sale_data.notes,
            discount_amount=sale_data.discount_amount or 0,
            tax_amount=sale_data.tax_amount or 0,
            commission_rate=sale_data.commission_rate or 0
        )
        
        # Salvar no repositório
        saved_sale = await self._sale_repository.save(sale)
        
        # Converter para DTO de resposta
        return self._to_response_dto(saved_sale)
    
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
