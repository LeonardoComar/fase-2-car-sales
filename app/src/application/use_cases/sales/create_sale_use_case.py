"""
Use Case para Criação de Venda - Application Layer

Responsável por coordenar a criação de vendas aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela criação de vendas
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para criação
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from src.domain.entities.sale import Sale
from src.domain.ports.sale_repository import SaleRepository
from src.application.dtos.sale_dto import CreateSaleRequest, SaleResponse, ClientSummary, EmployeeSummary, VehicleSummary
from decimal import Decimal


class CreateSaleUseCase:
    """
    Use Case para criação de vendas.
    
    Coordena a validação de dados, aplicação de regras de negócio
    e persistência de vendas no sistema.
    """
    
    def __init__(self, sale_repository: SaleRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            sale_repository: Repositório de vendas
        """
        self._sale_repository = sale_repository
    
    async def execute(self, sale_data: CreateSaleRequest) -> SaleResponse:
        """
        Executa a criação de uma venda.
        
        Args:
            sale_data: Dados para criação da venda
            
        Returns:
            SaleResponse: Dados da venda criada
            
        Raises:
            ValueError: Se dados inválidos forem fornecidos
            Exception: Se houver erro na criação
        """
        try:
            # Criar entidade de venda
            sale = Sale.create_sale(
                client_id=sale_data.client_id,
                employee_id=sale_data.employee_id,
                vehicle_id=sale_data.vehicle_id,
                total_amount=sale_data.total_amount,
                payment_method=sale_data.payment_method,
                sale_date=sale_data.sale_date,
                notes=sale_data.notes,
                discount_amount=sale_data.discount_amount or Decimal('0.00'),
                tax_amount=sale_data.tax_amount or Decimal('0.00'),
                commission_rate=sale_data.commission_rate or Decimal('0.00')
            )
            
            # Persistir no repositório
            created_sale = await self._sale_repository.create_sale(sale)
            
            # Converter para DTO de resposta
            return self._convert_to_response_dto(created_sale)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao criar venda: {str(e)}")
    
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
            name="Cliente",  # Placeholder - seria buscado do repositório
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
