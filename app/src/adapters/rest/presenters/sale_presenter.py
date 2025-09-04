from typing import List

from src.domain.entities.sale import Sale
from src.application.dtos.sale_dto import SaleResponseDto, SalesStatisticsDto


class SalePresenter:
    """
    Apresentador para formatação de respostas de vendas.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela formatação de dados de resposta.
    
    Aplicando o princípio Open/Closed Principle (OCP) - 
    pode ser estendido para novos formatos sem modificar código existente.
    """
    
    def present_sale(self, sale_dto: SaleResponseDto) -> dict:
        """
        Apresenta uma venda formatada.
        
        Args:
            sale_dto: DTO da venda
            
        Returns:
            dict: Venda formatada para resposta
        """
        return {
            "id": str(sale_dto.id),
            "client_id": str(sale_dto.client_id),
            "employee_id": str(sale_dto.employee_id),
            "vehicle_id": str(sale_dto.vehicle_id),
            "total_amount": float(sale_dto.total_amount),
            "payment_method": sale_dto.payment_method,
            "status": sale_dto.status,
            "sale_date": sale_dto.sale_date.isoformat(),
            "notes": sale_dto.notes,
            "discount_amount": float(sale_dto.discount_amount),
            "tax_amount": float(sale_dto.tax_amount),
            "commission_rate": float(sale_dto.commission_rate),
            "commission_amount": float(sale_dto.commission_amount),
            "final_amount": float(sale_dto.final_amount),
            "created_at": sale_dto.created_at,
            "updated_at": sale_dto.updated_at
        }
    
    def present_sale_list(self, sales_dto: List[SaleResponseDto]) -> dict:
        """
        Apresenta lista de vendas formatada.
        
        Args:
            sales_dto: Lista de DTOs de vendas
            
        Returns:
            dict: Lista formatada para resposta
        """
        return {
            "sales": [self.present_sale(sale) for sale in sales_dto],
            "total": len(sales_dto)
        }
    
    def present_sale_created(self, sale_dto: SaleResponseDto) -> dict:
        """
        Apresenta venda criada com sucesso.
        
        Args:
            sale_dto: DTO da venda criada
            
        Returns:
            dict: Resposta de sucesso formatada
        """
        return {
            "message": "Venda criada com sucesso",
            "sale": self.present_sale(sale_dto)
        }
    
    def present_sale_updated(self, sale_dto: SaleResponseDto) -> dict:
        """
        Apresenta venda atualizada com sucesso.
        
        Args:
            sale_dto: DTO da venda atualizada
            
        Returns:
            dict: Resposta de sucesso formatada
        """
        return {
            "message": "Venda atualizada com sucesso",
            "sale": self.present_sale(sale_dto)
        }
    
    def present_sale_status_updated(self, sale_dto: SaleResponseDto) -> dict:
        """
        Apresenta status da venda atualizado com sucesso.
        
        Args:
            sale_dto: DTO da venda com status atualizado
            
        Returns:
            dict: Resposta de sucesso formatada
        """
        return {
            "message": f"Status da venda atualizado para '{sale_dto.status}' com sucesso",
            "sale": self.present_sale(sale_dto)
        }
    
    def present_sale_deleted(self) -> dict:
        """
        Apresenta venda excluída com sucesso.
        
        Returns:
            dict: Resposta de sucesso formatada
        """
        return {
            "message": "Venda excluída com sucesso"
        }
    
    def present_sale_not_found(self) -> dict:
        """
        Apresenta resposta de venda não encontrada.
        
        Returns:
            dict: Resposta de erro formatada
        """
        return {
            "error": "Venda não encontrada"
        }
    
    def present_sales_statistics(self, stats_dto: SalesStatisticsDto) -> dict:
        """
        Apresenta estatísticas de vendas formatadas.
        
        Args:
            stats_dto: DTO de estatísticas
            
        Returns:
            dict: Estatísticas formatadas para resposta
        """
        return {
            "statistics": {
                "total_sales": stats_dto.total_sales,
                "total_amount": float(stats_dto.total_amount),
                "average_sale_amount": float(stats_dto.average_sale_amount),
                "total_commission": float(stats_dto.total_commission),
                "sales_by_status": stats_dto.sales_by_status,
                "sales_by_payment_method": stats_dto.sales_by_payment_method,
                "top_performers": [
                    {
                        "employee_id": str(performer["employee_id"]),
                        "sales_count": performer["sales_count"],
                        "total_amount": float(performer["total_amount"]),
                        "total_commission": float(performer["total_commission"])
                    }
                    for performer in stats_dto.top_performers
                ]
            }
        }
    
    def present_sales_by_client(self, sales_dto: List[SaleResponseDto], client_id: str) -> dict:
        """
        Apresenta vendas por cliente formatadas.
        
        Args:
            sales_dto: Lista de DTOs de vendas
            client_id: ID do cliente
            
        Returns:
            dict: Vendas por cliente formatadas
        """
        return {
            "client_id": client_id,
            "sales": [self.present_sale(sale) for sale in sales_dto],
            "total_sales": len(sales_dto),
            "total_amount": sum(float(sale.total_amount) for sale in sales_dto)
        }
    
    def present_sales_by_employee(self, sales_dto: List[SaleResponseDto], employee_id: str) -> dict:
        """
        Apresenta vendas por funcionário formatadas.
        
        Args:
            sales_dto: Lista de DTOs de vendas
            employee_id: ID do funcionário
            
        Returns:
            dict: Vendas por funcionário formatadas
        """
        return {
            "employee_id": employee_id,
            "sales": [self.present_sale(sale) for sale in sales_dto],
            "total_sales": len(sales_dto),
            "total_amount": sum(float(sale.total_amount) for sale in sales_dto),
            "total_commission": sum(float(sale.commission_amount) for sale in sales_dto)
        }
    
    def present_validation_error(self, error_details: str) -> dict:
        """
        Apresenta erro de validação formatado.
        
        Args:
            error_details: Detalhes do erro
            
        Returns:
            dict: Erro formatado para resposta
        """
        return {
            "error": "Dados inválidos",
            "details": error_details
        }
    
    def present_business_error(self, error_message: str) -> dict:
        """
        Apresenta erro de negócio formatado.
        
        Args:
            error_message: Mensagem do erro
            
        Returns:
            dict: Erro formatado para resposta
        """
        return {
            "error": error_message
        }
