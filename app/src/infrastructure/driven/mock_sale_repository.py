from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from decimal import Decimal
from datetime import datetime, date

from src.domain.entities.sale import Sale
from src.domain.ports.sale_repository import SaleRepository


class MockSaleRepository(SaleRepository):
    """
    Implementação mock do repositório de vendas para desenvolvimento e testes.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    implementa a interface abstrata definida no domínio.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela simulação de persistência de vendas.
    """
    
    def __init__(self):
        # Armazenamento em memória para simulação
        self._sales: Dict[UUID, Sale] = {}
        
        # Dados iniciais para demonstração
        self._seed_initial_data()
    
    def _seed_initial_data(self):
        """Adiciona dados iniciais para demonstração."""
        # IDs fictícios para relações
        client_id = uuid4()
        employee_id = uuid4()
        vehicle_id_1 = uuid4()
        vehicle_id_2 = uuid4()
        
        # Venda 1 - Confirmada
        sale1 = Sale(
            id=uuid4(),
            client_id=client_id,
            employee_id=employee_id,
            vehicle_id=vehicle_id_1,
            total_amount=Decimal("85000.00"),
            payment_method="Financiamento",
            sale_date=date(2024, 1, 15),
            status=Sale.STATUS_CONFIRMADA,
            notes="Cliente interessado em garantia estendida",
            discount_amount=Decimal("5000.00"),
            tax_amount=Decimal("1500.00"),
            commission_rate=Decimal("3.5"),
            created_at=datetime(2024, 1, 15, 10, 30)
        )
        self._sales[sale1.id] = sale1
        
        # Venda 2 - Entregue
        sale2 = Sale(
            id=uuid4(),
            client_id=uuid4(),
            employee_id=employee_id,
            vehicle_id=vehicle_id_2,
            total_amount=Decimal("65000.00"),
            payment_method="À vista",
            sale_date=date(2024, 1, 20),
            status=Sale.STATUS_ENTREGUE,
            notes="Pagamento à vista com desconto",
            discount_amount=Decimal("3000.00"),
            tax_amount=Decimal("1200.00"),
            commission_rate=Decimal("4.0"),
            created_at=datetime(2024, 1, 20, 14, 15)
        )
        self._sales[sale2.id] = sale2
        
        # Venda 3 - Pendente
        sale3 = Sale(
            id=uuid4(),
            client_id=uuid4(),
            employee_id=uuid4(),
            vehicle_id=uuid4(),
            total_amount=Decimal("120000.00"),
            payment_method="Consórcio",
            sale_date=date(2024, 2, 1),
            status=Sale.STATUS_PENDENTE,
            notes="Aguardando aprovação do consórcio",
            discount_amount=Decimal("2000.00"),
            tax_amount=Decimal("2500.00"),
            commission_rate=Decimal("2.5"),
            created_at=datetime(2024, 2, 1, 9, 45)
        )
        self._sales[sale3.id] = sale3
    
    async def save(self, sale: Sale) -> Sale:
        """
        Salva uma venda.
        
        Args:
            sale: Venda a ser salva
            
        Returns:
            Sale: Venda salva com dados atualizados
        """
        # Se não tem ID, gerar um novo
        if sale.id is None:
            sale.id = uuid4()
        
        # Atualizar timestamp
        sale.updated_at = datetime.utcnow()
        
        # Armazenar
        self._sales[sale.id] = sale
        
        return sale
    
    async def find_by_id(self, sale_id: UUID) -> Optional[Sale]:
        """
        Busca uma venda pelo ID.
        
        Args:
            sale_id: ID da venda
            
        Returns:
            Optional[Sale]: A venda encontrada ou None
        """
        return self._sales.get(sale_id)
    
    async def find_by_criteria(self, **kwargs) -> List[Sale]:
        """
        Busca vendas por múltiplos critérios.
        
        Args:
            **kwargs: Critérios de busca
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        sales = list(self._sales.values())
        
        # Aplicar filtros
        sales = self._apply_filters(sales, **kwargs)
        
        # Aplicar ordenação
        sales = self._apply_ordering(sales, kwargs.get('order_by'), kwargs.get('order_direction'))
        
        # Aplicar paginação
        if 'skip' in kwargs and kwargs['skip'] is not None:
            offset = kwargs['skip']
            sales = sales[offset:]
        
        if 'limit' in kwargs and kwargs['limit'] is not None:
            limit = kwargs['limit']
            sales = sales[:limit]
        
        return sales
    
    async def find_by_client(self, client_id: UUID, **kwargs) -> List[Sale]:
        """
        Busca vendas por cliente.
        
        Args:
            client_id: ID do cliente
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        kwargs['client_id'] = client_id
        return await self.find_by_criteria(**kwargs)
    
    async def find_by_employee(self, employee_id: UUID, **kwargs) -> List[Sale]:
        """
        Busca vendas por funcionário.
        
        Args:
            employee_id: ID do funcionário
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        kwargs['employee_id'] = employee_id
        return await self.find_by_criteria(**kwargs)
    
    async def find_by_vehicle(self, vehicle_id: UUID) -> Optional[Sale]:
        """
        Busca venda por veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Optional[Sale]: Venda encontrada ou None
        """
        for sale in self._sales.values():
            if sale.vehicle_id == vehicle_id:
                return sale
        return None
    
    async def find_by_status(self, status: str, **kwargs) -> List[Sale]:
        """
        Busca vendas por status.
        
        Args:
            status: Status das vendas
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        kwargs['status'] = status
        return await self.find_by_criteria(**kwargs)
    
    async def find_by_date_range(self, start_date: date, end_date: date, **kwargs) -> List[Sale]:
        """
        Busca vendas por período.
        
        Args:
            start_date: Data inicial
            end_date: Data final
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        kwargs['start_date'] = start_date
        kwargs['end_date'] = end_date
        return await self.find_by_criteria(**kwargs)
    
    async def find_by_payment_method(self, payment_method: str, **kwargs) -> List[Sale]:
        """
        Busca vendas por forma de pagamento.
        
        Args:
            payment_method: Forma de pagamento
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        kwargs['payment_method'] = payment_method
        return await self.find_by_criteria(**kwargs)
    
    async def delete(self, sale_id: UUID) -> None:
        """
        Remove uma venda.
        
        Args:
            sale_id: ID da venda a ser removida
        """
        if sale_id in self._sales:
            del self._sales[sale_id]
    
    async def exists_by_id(self, sale_id: UUID) -> bool:
        """
        Verifica se existe venda com o ID.
        
        Args:
            sale_id: ID a ser verificado
            
        Returns:
            bool: True se existir venda com o ID
        """
        return sale_id in self._sales
    
    async def exists_by_vehicle(self, vehicle_id: UUID, exclude_id: Optional[UUID] = None) -> bool:
        """
        Verifica se existe venda para o veículo.
        
        Args:
            vehicle_id: ID do veículo
            exclude_id: ID da venda a ser excluída da verificação
            
        Returns:
            bool: True se existir venda para o veículo
        """
        for sale in self._sales.values():
            if sale.vehicle_id == vehicle_id and sale.id != exclude_id:
                return True
        return False
    
    async def count_by_client(self, client_id: UUID) -> int:
        """
        Conta vendas por cliente.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            int: Número de vendas do cliente
        """
        count = 0
        for sale in self._sales.values():
            if sale.client_id == client_id:
                count += 1
        return count
    
    async def count_by_employee(self, employee_id: UUID) -> int:
        """
        Conta vendas por funcionário.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            int: Número de vendas do funcionário
        """
        count = 0
        for sale in self._sales.values():
            if sale.employee_id == employee_id:
                count += 1
        return count
    
    async def count_by_status(self, status: str) -> int:
        """
        Conta vendas por status.
        
        Args:
            status: Status das vendas
            
        Returns:
            int: Número de vendas com o status
        """
        count = 0
        for sale in self._sales.values():
            if sale.status == status:
                count += 1
        return count
    
    async def get_total_sales_amount(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Decimal:
        """
        Calcula valor total de vendas em período.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            Decimal: Valor total das vendas
        """
        total = Decimal('0')
        for sale in self._sales.values():
            if self._sale_in_date_range(sale, start_date, end_date):
                total += sale.total_amount
        return total
    
    async def get_total_commission_amount(self, employee_id: Optional[UUID] = None, 
                                         start_date: Optional[date] = None, 
                                         end_date: Optional[date] = None) -> Decimal:
        """
        Calcula valor total de comissões.
        
        Args:
            employee_id: ID do funcionário (opcional)
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            Decimal: Valor total das comissões
        """
        total = Decimal('0')
        for sale in self._sales.values():
            if employee_id and sale.employee_id != employee_id:
                continue
            if self._sale_in_date_range(sale, start_date, end_date):
                total += sale.commission_amount
        return total
    
    async def get_sales_statistics(self, start_date: Optional[date] = None, 
                                  end_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Busca estatísticas de vendas.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            dict: Estatísticas das vendas
        """
        filtered_sales = [
            sale for sale in self._sales.values()
            if self._sale_in_date_range(sale, start_date, end_date)
        ]
        
        total_sales = len(filtered_sales)
        total_amount = sum(sale.total_amount for sale in filtered_sales)
        average_amount = total_amount / total_sales if total_sales > 0 else Decimal('0')
        total_commission = sum(sale.commission_amount for sale in filtered_sales)
        
        # Vendas por status
        sales_by_status = {}
        for status in Sale.VALID_STATUSES:
            count = sum(1 for sale in filtered_sales if sale.status == status)
            sales_by_status[status] = count
        
        # Vendas por forma de pagamento
        sales_by_payment_method = {}
        for payment_method in Sale.VALID_PAYMENT_METHODS:
            count = sum(1 for sale in filtered_sales if sale.payment_method == payment_method)
            if count > 0:
                sales_by_payment_method[payment_method] = count
        
        return {
            'total_sales': total_sales,
            'total_amount': total_amount,
            'average_sale_amount': average_amount,
            'total_commission': total_commission,
            'sales_by_status': sales_by_status,
            'sales_by_payment_method': sales_by_payment_method
        }
    
    async def get_top_performers(self, start_date: Optional[date] = None, 
                                end_date: Optional[date] = None, 
                                limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca top vendedores por performance.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            limit: Número máximo de resultados
            
        Returns:
            List[Dict]: Lista de vendedores com estatísticas
        """
        filtered_sales = [
            sale for sale in self._sales.values()
            if self._sale_in_date_range(sale, start_date, end_date)
        ]
        
        # Agrupar por funcionário
        employee_stats = {}
        for sale in filtered_sales:
            emp_id = sale.employee_id
            if emp_id not in employee_stats:
                employee_stats[emp_id] = {
                    'employee_id': emp_id,
                    'sales_count': 0,
                    'total_amount': Decimal('0'),
                    'total_commission': Decimal('0')
                }
            
            employee_stats[emp_id]['sales_count'] += 1
            employee_stats[emp_id]['total_amount'] += sale.total_amount
            employee_stats[emp_id]['total_commission'] += sale.commission_amount
        
        # Ordenar por valor total e limitar
        performers = list(employee_stats.values())
        performers.sort(key=lambda x: x['total_amount'], reverse=True)
        
        return performers[:limit]
    
    def _apply_filters(self, sales: List[Sale], **kwargs) -> List[Sale]:
        """Aplica filtros à lista de vendas."""
        result = sales.copy()
        
        # Filtros diretos
        if 'client_id' in kwargs and kwargs['client_id']:
            result = [s for s in result if s.client_id == kwargs['client_id']]
        
        if 'employee_id' in kwargs and kwargs['employee_id']:
            result = [s for s in result if s.employee_id == kwargs['employee_id']]
        
        if 'vehicle_id' in kwargs and kwargs['vehicle_id']:
            result = [s for s in result if s.vehicle_id == kwargs['vehicle_id']]
        
        if 'status' in kwargs and kwargs['status']:
            result = [s for s in result if s.status == kwargs['status']]
        
        if 'payment_method' in kwargs and kwargs['payment_method']:
            result = [s for s in result if s.payment_method == kwargs['payment_method']]
        
        # Filtros de data
        if 'start_date' in kwargs and kwargs['start_date']:
            start_date = kwargs['start_date']
            result = [s for s in result if s.sale_date >= start_date]
        
        if 'end_date' in kwargs and kwargs['end_date']:
            end_date = kwargs['end_date']
            result = [s for s in result if s.sale_date <= end_date]
        
        # Filtros de valor
        if 'min_amount' in kwargs and kwargs['min_amount'] is not None:
            min_amount = kwargs['min_amount']
            result = [s for s in result if s.total_amount >= min_amount]
        
        if 'max_amount' in kwargs and kwargs['max_amount'] is not None:
            max_amount = kwargs['max_amount']
            result = [s for s in result if s.total_amount <= max_amount]
        
        # Filtros especiais
        if 'active_only' in kwargs and kwargs['active_only']:
            result = [s for s in result if s.is_active()]
        
        if 'completed_only' in kwargs and kwargs['completed_only']:
            result = [s for s in result if s.is_completed()]
        
        return result
    
    def _apply_ordering(self, sales: List[Sale], order_by: Optional[str], order_direction: Optional[str]) -> List[Sale]:
        """Aplica ordenação à lista de vendas."""
        if not order_by:
            order_by = 'sale_date'
        
        if not order_direction:
            order_direction = 'desc'
        
        reverse = order_direction.lower() == 'desc'
        
        # Ordenação por campo
        if order_by == 'sale_date':
            sales.sort(key=lambda s: s.sale_date, reverse=reverse)
        elif order_by == 'total_amount':
            sales.sort(key=lambda s: s.total_amount, reverse=reverse)
        elif order_by == 'final_amount':
            sales.sort(key=lambda s: s.calculate_final_amount(), reverse=reverse)
        elif order_by == 'status':
            sales.sort(key=lambda s: s.status, reverse=reverse)
        elif order_by == 'created_at':
            sales.sort(key=lambda s: s.created_at, reverse=reverse)
        
        return sales
    
    def _sale_in_date_range(self, sale: Sale, start_date: Optional[date], end_date: Optional[date]) -> bool:
        """Verifica se venda está no período especificado."""
        if start_date and sale.sale_date < start_date:
            return False
        if end_date and sale.sale_date > end_date:
            return False
        return True
