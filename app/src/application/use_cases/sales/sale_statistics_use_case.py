"""
Use Case para Estatísticas de Vendas - Application Layer

Responsável por gerar estatísticas de vendas seguindo regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas por estatísticas de vendas
- OCP: Extensível para novas métricas sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para estatísticas
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from datetime import datetime
from src.domain.ports.sale_repository import SaleRepository
from src.application.dtos.sale_dto import SaleStatisticsResponse


class SaleStatisticsUseCase:
    """
    Use Case para geração de estatísticas de vendas.
    
    Coordena a busca e cálculo de métricas relacionadas às vendas.
    """
    
    def __init__(self, sale_repository: SaleRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            sale_repository: Repositório de vendas
        """
        self._sale_repository = sale_repository
    
    async def execute(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        employee_id: Optional[int] = None
    ) -> SaleStatisticsResponse:
        """
        Executa a geração de estatísticas de vendas.
        
        Args:
            start_date: Data inicial para filtro
            end_date: Data final para filtro
            employee_id: Filtro por funcionário específico
            
        Returns:
            SaleStatisticsResponse: Estatísticas das vendas
            
        Raises:
            ValueError: Se parâmetros inválidos forem fornecidos
            Exception: Se houver erro na geração das estatísticas
        """
        try:
            # Validar parâmetros
            if start_date and end_date and start_date > end_date:
                raise ValueError("Data inicial deve ser anterior à data final")
            if employee_id is not None and employee_id <= 0:
                raise ValueError("ID do funcionário deve ser maior que zero")
            
            # Buscar estatísticas no repositório
            statistics = await self._sale_repository.get_sales_statistics(
                start_date=start_date,
                end_date=end_date,
                employee_id=employee_id
            )
            
            return statistics
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao gerar estatísticas de vendas: {str(e)}")
    
    async def get_monthly_statistics(self, year: int, month: int) -> SaleStatisticsResponse:
        """
        Busca estatísticas de um mês específico.
        
        Args:
            year: Ano
            month: Mês (1-12)
            
        Returns:
            SaleStatisticsResponse: Estatísticas do mês
        """
        try:
            if year < 1900 or year > 2100:
                raise ValueError("Ano deve estar entre 1900 e 2100")
            if month < 1 or month > 12:
                raise ValueError("Mês deve estar entre 1 e 12")
            
            # Calcular primeiro e último dia do mês
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            
            return await self.execute(start_date=start_date, end_date=end_date)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao buscar estatísticas mensais: {str(e)}")
    
    async def get_employee_statistics(self, employee_id: int, year: Optional[int] = None) -> SaleStatisticsResponse:
        """
        Busca estatísticas de um funcionário específico.
        
        Args:
            employee_id: ID do funcionário
            year: Ano para filtro (opcional)
            
        Returns:
            SaleStatisticsResponse: Estatísticas do funcionário
        """
        try:
            if employee_id <= 0:
                raise ValueError("ID do funcionário deve ser maior que zero")
            
            start_date = None
            end_date = None
            
            if year:
                if year < 1900 or year > 2100:
                    raise ValueError("Ano deve estar entre 1900 e 2100")
                start_date = datetime(year, 1, 1)
                end_date = datetime(year + 1, 1, 1)
            
            return await self.execute(
                start_date=start_date,
                end_date=end_date,
                employee_id=employee_id
            )
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao buscar estatísticas do funcionário: {str(e)}")
