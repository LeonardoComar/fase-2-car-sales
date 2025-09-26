"""
Use Case para Obter Venda por ID - Application Layer

Responsável por buscar vendas por ID aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela busca de vendas
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para busca
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from src.domain.entities.sale import Sale
from src.domain.ports.sale_repository import SaleRepository
from src.application.dtos.sale_dto import SaleResponse, ClientSummary, EmployeeSummary, VehicleSummary
from decimal import Decimal


class GetSaleByIdUseCase:
    """
    Use Case para busca de vendas por ID.
    
    Coordena a busca e conversão de dados de vendas.
    """
    
    def __init__(self, sale_repository: SaleRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            sale_repository: Repositório de vendas
        """
        self._sale_repository = sale_repository
    
    async def execute(self, sale_id: int) -> Optional[SaleResponse]:
        """
        Executa a busca de uma venda por ID.
        
        Args:
            sale_id: ID da venda a ser buscada
            
        Returns:
            Optional[SaleResponse]: Dados da venda ou None se não encontrada
            
        Raises:
            ValueError: Se ID inválido for fornecido
            Exception: Se houver erro na busca
        """
        try:
            if sale_id <= 0:
                raise ValueError("ID da venda deve ser maior que zero")
            
            # Buscar venda no repositório
            sale = await self._sale_repository.get_sale_by_id(sale_id)
            
            if not sale:
                return None
            
            # Converter para DTO de resposta
            return self._convert_to_response_dto(sale)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao buscar venda: {str(e)}")
    
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
