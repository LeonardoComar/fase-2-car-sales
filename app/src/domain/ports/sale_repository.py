from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import date
from decimal import Decimal

from src.domain.entities.sale import Sale


class SaleRepository(ABC):
    """
    Interface para o repositório de vendas.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    define contrato independente de implementação específica.
    
    Aplicando o princípio Interface Segregation Principle (ISP) - 
    interface focada nas operações de vendas.
    """

    @abstractmethod
    async def save(self, sale: Sale) -> Sale:
        """
        Salva uma venda.
        
        Args:
            sale: Venda a ser salva
            
        Returns:
            Sale: Venda salva com dados atualizados
            
        Raises:
            Exception: Se houver erro na operação
        """
        pass

    @abstractmethod
    async def find_by_id(self, sale_id: UUID) -> Optional[Sale]:
        """
        Busca uma venda pelo ID.
        
        Args:
            sale_id: ID da venda
            
        Returns:
            Optional[Sale]: A venda encontrada ou None
        """
        pass

    @abstractmethod
    async def find_by_criteria(self, **kwargs) -> List[Sale]:
        """
        Busca vendas por múltiplos critérios.
        
        Args:
            **kwargs: Critérios de busca (client_id, employee_id, status, etc.)
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        pass

    @abstractmethod
    async def find_by_client(self, client_id: UUID, **kwargs) -> List[Sale]:
        """
        Busca vendas por cliente.
        
        Args:
            client_id: ID do cliente
            **kwargs: Parâmetros adicionais (skip, limit, order_by, etc.)
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        pass

    @abstractmethod
    async def find_by_employee(self, employee_id: UUID, **kwargs) -> List[Sale]:
        """
        Busca vendas por funcionário.
        
        Args:
            employee_id: ID do funcionário
            **kwargs: Parâmetros adicionais (skip, limit, order_by, etc.)
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        pass

    @abstractmethod
    async def find_by_vehicle(self, vehicle_id: UUID) -> Optional[Sale]:
        """
        Busca venda por veículo (assumindo 1:1).
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Optional[Sale]: Venda encontrada ou None
        """
        pass

    @abstractmethod
    async def find_by_status(self, status: str, **kwargs) -> List[Sale]:
        """
        Busca vendas por status.
        
        Args:
            status: Status das vendas
            **kwargs: Parâmetros adicionais (skip, limit, order_by, etc.)
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        pass

    @abstractmethod
    async def find_by_date_range(self, start_date: date, end_date: date, **kwargs) -> List[Sale]:
        """
        Busca vendas por período.
        
        Args:
            start_date: Data inicial
            end_date: Data final
            **kwargs: Parâmetros adicionais (skip, limit, order_by, etc.)
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        pass

    @abstractmethod
    async def find_by_payment_method(self, payment_method: str, **kwargs) -> List[Sale]:
        """
        Busca vendas por forma de pagamento.
        
        Args:
            payment_method: Forma de pagamento
            **kwargs: Parâmetros adicionais (skip, limit, order_by, etc.)
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        pass

    @abstractmethod
    async def delete(self, sale_id: UUID) -> None:
        """
        Remove uma venda.
        
        Args:
            sale_id: ID da venda a ser removida
            
        Raises:
            Exception: Se venda não encontrada ou erro na operação
        """
        pass

    @abstractmethod
    async def exists_by_id(self, sale_id: UUID) -> bool:
        """
        Verifica se existe venda com o ID.
        
        Args:
            sale_id: ID a ser verificado
            
        Returns:
            bool: True se existir venda com o ID
        """
        pass

    @abstractmethod
    async def exists_by_vehicle(self, vehicle_id: UUID, exclude_id: Optional[UUID] = None) -> bool:
        """
        Verifica se existe venda para o veículo.
        
        Args:
            vehicle_id: ID do veículo
            exclude_id: ID da venda a ser excluída da verificação
            
        Returns:
            bool: True se existir venda para o veículo
        """
        pass

    @abstractmethod
    async def count_by_client(self, client_id: UUID) -> int:
        """
        Conta vendas por cliente.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            int: Número de vendas do cliente
        """
        pass

    @abstractmethod
    async def count_by_employee(self, employee_id: UUID) -> int:
        """
        Conta vendas por funcionário.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            int: Número de vendas do funcionário
        """
        pass

    @abstractmethod
    async def count_by_status(self, status: str) -> int:
        """
        Conta vendas por status.
        
        Args:
            status: Status das vendas
            
        Returns:
            int: Número de vendas com o status
        """
        pass

    @abstractmethod
    async def get_total_sales_amount(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Decimal:
        """
        Calcula valor total de vendas em período.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            Decimal: Valor total das vendas
        """
        pass

    @abstractmethod
    async def get_total_commission_amount(self, employee_id: Optional[UUID] = None, 
                                         start_date: Optional[date] = None, 
                                         end_date: Optional[date] = None) -> Decimal:
        """
        Calcula valor total de comissões.
        
        Args:
            employee_id: ID do funcionário (opcional, para filtrar)
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            Decimal: Valor total das comissões
        """
        pass

    @abstractmethod
    async def get_sales_statistics(self, start_date: Optional[date] = None, 
                                  end_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Busca estatísticas de vendas.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            dict: Estatísticas das vendas (total, média, por status, etc.)
        """
        pass

    @abstractmethod
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
        pass
