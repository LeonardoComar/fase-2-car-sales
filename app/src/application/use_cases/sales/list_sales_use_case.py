"""
Use Case para Listagem de Vendas - Application Layer

Responsável por listar vendas com filtros seguindo regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela listagem de vendas
- OCP: Extensível para novos filtros sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para listagem
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import List, Optional
from datetime import datetime
from src.domain.entities.sale import Sale
from src.domain.ports.sale_repository import SaleRepository
from src.application.dtos.sale_dto import SaleResponse, ClientSummary, EmployeeSummary, VehicleSummary
from decimal import Decimal


class ListSalesUseCase:
    """
    Use Case para listagem de vendas com filtros.
    
    Coordena a aplicação de filtros e busca de vendas no sistema.
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
        client_id: Optional[int] = None,
        employee_id: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        payment_method: Optional[str] = None,
        order_by_value: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[SaleResponse]:
        """
        Executa a listagem de vendas com filtros opcionais.
        
        Args:
            client_id: Filtro por ID do cliente
            employee_id: Filtro por ID do funcionário
            status: Filtro por status da venda
            start_date: Data inicial para filtro
            end_date: Data final para filtro
            payment_method: Filtro por método de pagamento
            order_by_value: Ordenação por valor - 'asc' ou 'desc'
            skip: Número de registros para pular (paginação)
            limit: Número máximo de registros para retornar
            
        Returns:
            List[SaleResponse]: Lista de vendas encontradas
            
        Raises:
            ValueError: Se parâmetros inválidos forem fornecidos
            Exception: Se houver erro na busca
        """
        try:
            # Validar parâmetros
            if skip < 0:
                raise ValueError("Skip deve ser maior ou igual a zero")
            if limit <= 0 or limit > 1000:
                raise ValueError("Limit deve ser entre 1 e 1000")
            if start_date and end_date and start_date > end_date:
                raise ValueError("Data inicial deve ser anterior à data final")
            
            # Verificar se deve usar get_all_sales ou get_sales_by_filters
            has_filters = any([
                client_id is not None,
                employee_id is not None,
                status is not None,
                start_date is not None,
                end_date is not None,
                payment_method is not None
            ])
            
            if not has_filters and order_by_value:
                # Usar get_all_sales quando só há ordenação sem filtros
                sales = await self._sale_repository.get_all_sales(
                    skip=skip,
                    limit=limit,
                    order_by_value=order_by_value
                )
            else:
                # Buscar vendas com filtros
                sales = await self._sale_repository.get_sales_by_filters(
                    client_id=client_id,
                    employee_id=employee_id,
                    status=status,
                    start_date=start_date,
                    end_date=end_date,
                    payment_method=payment_method,
                    skip=skip,
                    limit=limit
                )
            
            # Converter para DTOs de resposta
            return [self._convert_to_response_dto(sale) for sale in sales]
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao listar vendas: {str(e)}")
    
    async def get_sales_by_client(self, client_id: int, skip: int = 0, limit: int = 100) -> List[SaleResponse]:
        """
        Busca vendas por cliente específico.
        
        Args:
            client_id: ID do cliente
            skip: Número de registros para pular
            limit: Número máximo de registros
            
        Returns:
            List[SaleResponse]: Lista de vendas do cliente
        """
        try:
            if client_id <= 0:
                raise ValueError("ID do cliente deve ser maior que zero")
            
            sales = await self._sale_repository.get_sales_by_client(client_id, skip, limit)
            return [self._convert_to_response_dto(sale) for sale in sales]
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao buscar vendas do cliente: {str(e)}")
    
    async def get_sales_by_employee(self, employee_id: int, skip: int = 0, limit: int = 100) -> List[SaleResponse]:
        """
        Busca vendas por funcionário específico.
        
        Args:
            employee_id: ID do funcionário
            skip: Número de registros para pular
            limit: Número máximo de registros
            
        Returns:
            List[SaleResponse]: Lista de vendas do funcionário
        """
        try:
            if employee_id <= 0:
                raise ValueError("ID do funcionário deve ser maior que zero")
            
            sales = await self._sale_repository.get_sales_by_employee(employee_id, skip, limit)
            return [self._convert_to_response_dto(sale) for sale in sales]
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao buscar vendas do funcionário: {str(e)}")
    
    async def get_sales_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[SaleResponse]:
        """
        Busca vendas por status específico.
        
        Args:
            status: Status da venda
            skip: Número de registros para pular
            limit: Número máximo de registros
            
        Returns:
            List[SaleResponse]: Lista de vendas com o status
        """
        try:
            if not status or not status.strip():
                raise ValueError("Status não pode ser vazio")
            
            sales = await self._sale_repository.get_sales_by_status(status, skip, limit)
            return [self._convert_to_response_dto(sale) for sale in sales]
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao buscar vendas por status: {str(e)}")
    
    def _convert_to_response_dto(self, sale: Sale) -> SaleResponse:
        """
        Converte entidade Sale para DTO de resposta.
        
        Args:
            sale: Entidade da venda
            
        Returns:
            SaleResponse: DTO de resposta
        """
        # Criar resumos das entidades relacionadas (dados simplificados)
        client_summary = ClientSummary(
            id=sale.client_id,
            name="Cliente",  # Placeholder
            email="cliente@email.com",  # Placeholder
            cpf="000.000.000-00"  # Placeholder
        )
        
        employee_summary = EmployeeSummary(
            id=sale.employee_id,
            name="Funcionário",  # Placeholder
            email="funcionario@empresa.com"  # Placeholder
        )
        
        vehicle_summary = VehicleSummary(
            id=sale.vehicle_id,
            model="Veículo",  # Placeholder
            year="2023",  # Placeholder
            color="Cor",  # Placeholder
            price=Decimal('0.00')  # Placeholder
        )
        
        return SaleResponse(
            id=sale.id,
            client=client_summary,
            employee=employee_summary,
            vehicle=vehicle_summary,
            total_amount=sale.total_amount,
            payment_method=sale.payment_method,
            status=sale.status,
            sale_date=sale.sale_date.isoformat(),
            notes=sale.notes,
            discount_amount=sale.discount_amount,
            tax_amount=sale.tax_amount,
            commission_rate=sale.commission_rate,
            commission_amount=sale.commission_amount,
            final_amount=sale.calculate_final_amount(),
            created_at=sale.created_at.isoformat() if sale.created_at else "",
            updated_at=sale.updated_at.isoformat() if sale.updated_at else ""
        )
