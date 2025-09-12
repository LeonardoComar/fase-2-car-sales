"""
Mock repository para vendas - desenvolvimento/teste.
"""

from typing import List, Optional
from datetime import datetime, date
from src.domain.entities.sale import Sale
from src.domain.ports.sale_repository import SaleRepository
from src.application.dtos.sale_dto import SaleStatisticsResponse
from decimal import Decimal


class MockSaleRepository(SaleRepository):
    """Mock repository para vendas - desenvolvimento/teste."""
    
    def __init__(self):
        self._sales = []
        self._next_id = 1
    
    async def create_sale(self, sale: Sale) -> Sale:
        """Cria uma nova venda (mock)."""
        sale.id = self._next_id
        self._next_id += 1
        self._sales.append(sale)
        return sale
    
    async def get_sale_by_id(self, sale_id: int) -> Optional[Sale]:
        """Busca venda por ID (mock)."""
        for sale in self._sales:
            if sale.id == sale_id:
                return sale
        return None
    
    async def update_sale(self, sale_id: int, sale: Sale) -> Optional[Sale]:
        """Atualiza uma venda (mock)."""
        for i, existing_sale in enumerate(self._sales):
            if existing_sale.id == sale_id:
                sale.id = sale_id
                self._sales[i] = sale
                return sale
        return None
    
    async def update_sale_status(self, sale_id: int, status: str) -> Optional[Sale]:
        """Atualiza o status de uma venda (mock)."""
        for i, existing_sale in enumerate(self._sales):
            if existing_sale.id == sale_id:
                existing_sale.status = status
                return existing_sale
        return None
    
    async def delete_sale(self, sale_id: int) -> bool:
        """Exclui uma venda (mock)."""
        for i, sale in enumerate(self._sales):
            if sale.id == sale_id:
                del self._sales[i]
                return True
        return False
    
    async def get_all_sales(self, skip: int = 0, limit: int = 100, order_by_value: Optional[str] = None) -> List[Sale]:
        """Lista todas as vendas (mock)."""
        return self._sales[skip:skip + limit]
    
    async def get_sales_by_filters(
        self,
        client_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        payment_method: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Sale]:
        """Lista vendas com filtros (mock)."""
        filtered_sales = self._sales.copy()
        
        if client_id:
            filtered_sales = [s for s in filtered_sales if s.client_id == client_id]
        if employee_id:
            filtered_sales = [s for s in filtered_sales if s.employee_id == employee_id]
        if status:
            filtered_sales = [s for s in filtered_sales if s.status == status]
        if payment_method:
            filtered_sales = [s for s in filtered_sales if s.payment_method == payment_method]
        
        return filtered_sales[skip:skip + limit]
    
    async def get_sales_by_client(self, client_id: int, skip: int = 0, limit: int = 100) -> List[Sale]:
        """Busca vendas por cliente (mock)."""
        return await self.get_sales_by_filters(client_id=client_id, skip=skip, limit=limit)
    
    async def get_sales_by_employee(self, employee_id: int, skip: int = 0, limit: int = 100) -> List[Sale]:
        """Busca vendas por funcionário (mock)."""
        return await self.get_sales_by_filters(employee_id=employee_id, skip=skip, limit=limit)
    
    async def get_sales_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Sale]:
        """Busca vendas por status (mock)."""
        return await self.get_sales_by_filters(status=status, skip=skip, limit=limit)
    
    async def get_sales_by_date_range(
        self, 
        start_date: date, 
        end_date: date, 
        skip: int = 0, 
        limit: int = 100,
        order_by_value: Optional[str] = None
    ) -> List[Sale]:
        """Busca vendas por período (mock)."""
        return await self.get_sales_by_filters(
            start_date=start_date, 
            end_date=end_date, 
            skip=skip, 
            limit=limit
        )
    
    async def get_sales_by_payment_method(
        self, 
        payment_method: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Sale]:
        """Busca vendas por método de pagamento (mock)."""
        return await self.get_sales_by_filters(payment_method=payment_method, skip=skip, limit=limit)
    
    async def get_sales_statistics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        employee_id: Optional[int] = None
    ) -> SaleStatisticsResponse:
        """Gera estatísticas de vendas (mock)."""
        # Mock simples
        return SaleStatisticsResponse(
            total_sales=len(self._sales),
            total_revenue=Decimal('100000.00'),
            total_commission=Decimal('5000.00'),
            average_sale_value=Decimal('50000.00'),
            sales_by_status={"Confirmada": 3, "Pendente": 1},
            sales_by_payment_method={"Financiamento": 2, "À vista": 2},
            period_start="",
            period_end=""
        )