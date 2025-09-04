from typing import Optional
from datetime import date

from src.domain.ports.sale_repository import SaleRepository
from src.application.dtos.sale_dto import SalesStatisticsDto


class GetSalesStatisticsUseCase:
    """
    Caso de uso para obter estatísticas de vendas.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pelas estatísticas de vendas.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração SaleRepository.
    """
    
    def __init__(self, sale_repository: SaleRepository):
        self._sale_repository = sale_repository
    
    async def execute(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> SalesStatisticsDto:
        """
        Executa a busca de estatísticas de vendas.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            SalesStatisticsDto: Estatísticas das vendas
        """
        # Buscar estatísticas no repositório
        stats = await self._sale_repository.get_sales_statistics(start_date, end_date)
        
        # Buscar top performers
        top_performers = await self._sale_repository.get_top_performers(start_date, end_date, limit=10)
        
        # Converter para DTO
        return SalesStatisticsDto(
            total_sales=stats.get('total_sales', 0),
            total_amount=stats.get('total_amount', 0),
            average_sale_amount=stats.get('average_sale_amount', 0),
            total_commission=stats.get('total_commission', 0),
            sales_by_status=stats.get('sales_by_status', {}),
            sales_by_payment_method=stats.get('sales_by_payment_method', {}),
            top_performers=top_performers
        )
