"""
Gateway para Vendas - Infrastructure Layer

Implementação simplificada do repositório de vendas.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from src.domain.entities.sale import Sale
from src.domain.ports.sale_repository import SaleRepository
from src.infrastructure.database.models.sale_model import SaleModel
from src.application.dtos.sale_dto import SaleStatisticsResponse
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class SaleGateway(SaleRepository):
    """Gateway simplificado para operações de vendas."""
    
    def __init__(self, session: Session):
        """
        Inicializa o gateway com uma sessão do banco de dados.
        
        Args:
            session: Sessão do SQLAlchemy
        """
        self._session = session
    
    async def create_sale(self, sale: Sale) -> Sale:
        """Cria uma nova venda."""
        try:
            sale_model = SaleModel(
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
                commission_rate=sale.commission_rate
            )
            
            self._session.add(sale_model)
            self._session.commit()
            self._session.refresh(sale_model)
            
            return self._model_to_entity(sale_model)
            
        except Exception as e:
            self._session.rollback()
            logger.error(f"Erro ao criar venda: {str(e)}")
            raise Exception(f"Erro ao criar venda: {str(e)}")
    
    async def get_sale_by_id(self, sale_id: int) -> Optional[Sale]:
        """Busca venda por ID."""
        try:
            sale_model = self._session.query(SaleModel).filter(SaleModel.id == sale_id).first()
            
            if not sale_model:
                return None
                
            return self._model_to_entity(sale_model)
            
        except Exception as e:
            logger.error(f"Erro ao buscar venda por ID: {str(e)}")
            raise Exception(f"Erro ao buscar venda: {str(e)}")
    
    async def update_sale(self, sale_id: int, sale: Sale) -> Optional[Sale]:
        """Atualiza uma venda."""
        try:
            sale_model = self._session.query(SaleModel).filter(SaleModel.id == sale_id).first()
            
            if not sale_model:
                return None
            
            # Atualizar campos
            sale_model.client_id = sale.client_id
            sale_model.employee_id = sale.employee_id
            sale_model.vehicle_id = sale.vehicle_id
            sale_model.total_amount = sale.total_amount
            sale_model.payment_method = sale.payment_method
            sale_model.status = sale.status
            sale_model.sale_date = sale.sale_date
            sale_model.notes = sale.notes
            sale_model.discount_amount = sale.discount_amount
            sale_model.tax_amount = sale.tax_amount
            sale_model.commission_rate = sale.commission_rate
            
            self._session.commit()
            self._session.refresh(sale_model)
            
            return self._model_to_entity(sale_model)
            
        except Exception as e:
            self._session.rollback()
            logger.error(f"Erro ao atualizar venda: {str(e)}")
            raise Exception(f"Erro ao atualizar venda: {str(e)}")
    
    async def delete_sale(self, sale_id: int) -> bool:
        """Exclui uma venda."""
        try:
            sale_model = self._session.query(SaleModel).filter(SaleModel.id == sale_id).first()
            
            if not sale_model:
                return False
            
            self._session.delete(sale_model)
            self._session.commit()
            
            return True
            
        except Exception as e:
            self._session.rollback()
            logger.error(f"Erro ao excluir venda: {str(e)}")
            raise Exception(f"Erro ao excluir venda: {str(e)}")
    
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
        """Lista vendas com filtros."""
        try:
            query = self._session.query(SaleModel)
            
            # Aplicar filtros
            if client_id:
                query = query.filter(SaleModel.client_id == client_id)
            if employee_id:
                query = query.filter(SaleModel.employee_id == employee_id)
            if status:
                query = query.filter(SaleModel.status == status)
            if start_date:
                query = query.filter(SaleModel.sale_date >= start_date)
            if end_date:
                query = query.filter(SaleModel.sale_date <= end_date)
            if payment_method:
                query = query.filter(SaleModel.payment_method == payment_method)
            
            # Paginação e ordenação
            sales = query.order_by(desc(SaleModel.sale_date)).offset(skip).limit(limit).all()
            
            return [self._model_to_entity(sale) for sale in sales]
            
        except Exception as e:
            logger.error(f"Erro ao listar vendas: {str(e)}")
            raise Exception(f"Erro ao listar vendas: {str(e)}")
    
    async def get_sales_by_client(self, client_id: int, skip: int = 0, limit: int = 100) -> List[Sale]:
        """Busca vendas por cliente."""
        return await self.get_sales_by_filters(client_id=client_id, skip=skip, limit=limit)
    
    async def get_sales_by_employee(self, employee_id: int, skip: int = 0, limit: int = 100) -> List[Sale]:
        """Busca vendas por funcionário."""
        return await self.get_sales_by_filters(employee_id=employee_id, skip=skip, limit=limit)
    
    async def get_sales_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Sale]:
        """Busca vendas por status."""
        return await self.get_sales_by_filters(status=status, skip=skip, limit=limit)
    
    async def get_sales_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Sale]:
        """Busca vendas por período."""
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
        """Busca vendas por método de pagamento."""
        return await self.get_sales_by_filters(payment_method=payment_method, skip=skip, limit=limit)
    
    async def get_all_sales(self, skip: int = 0, limit: int = 100, order_by_value: Optional[str] = None) -> List[Sale]:
        """Busca todas as vendas com paginação."""
        try:
            query = self._session.query(SaleModel)
            
            # Aplicar ordenação
            if order_by_value == 'asc':
                query = query.order_by(SaleModel.total_amount.asc())
            elif order_by_value == 'desc':
                query = query.order_by(SaleModel.total_amount.desc())
            else:
                query = query.order_by(desc(SaleModel.sale_date))
            
            # Paginação
            sales = query.offset(skip).limit(limit).all()
            
            return [self._model_to_entity(sale) for sale in sales]
            
        except Exception as e:
            logger.error(f"Erro ao listar todas as vendas: {str(e)}")
            raise Exception(f"Erro ao listar vendas: {str(e)}")
    
    async def update_sale_status(self, sale_id: int, status: str) -> Optional[Sale]:
        """Atualiza apenas o status de uma venda."""
        try:
            sale_model = self._session.query(SaleModel).filter(SaleModel.id == sale_id).first()
            
            if not sale_model:
                return None
            
            sale_model.status = status
            
            self._session.commit()
            self._session.refresh(sale_model)
            
            return self._model_to_entity(sale_model)
            
        except Exception as e:
            self._session.rollback()
            logger.error(f"Erro ao atualizar status da venda: {str(e)}")
            raise Exception(f"Erro ao atualizar status da venda: {str(e)}")
    
    async def get_sales_statistics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        employee_id: Optional[int] = None
    ) -> SaleStatisticsResponse:
        """Gera estatísticas de vendas."""
        try:
            query = self._session.query(SaleModel)
            
            # Aplicar filtros
            if start_date:
                query = query.filter(SaleModel.sale_date >= start_date)
            if end_date:
                query = query.filter(SaleModel.sale_date <= end_date)
            if employee_id:
                query = query.filter(SaleModel.employee_id == employee_id)
            
            sales = query.all()
            
            # Calcular estatísticas
            total_sales = len(sales)
            total_revenue = sum(sale.total_amount for sale in sales)
            total_commission = sum(
                (sale.total_amount * sale.commission_rate / 100) if sale.commission_rate else Decimal('0')
                for sale in sales
            )
            
            average_sale_value = total_revenue / total_sales if total_sales > 0 else Decimal('0')
            
            # Estatísticas por status
            status_stats = {}
            for sale in sales:
                if sale.status not in status_stats:
                    status_stats[sale.status] = 0
                status_stats[sale.status] += 1
            
            # Estatísticas por método de pagamento
            payment_method_stats = {}
            for sale in sales:
                if sale.payment_method not in payment_method_stats:
                    payment_method_stats[sale.payment_method] = 0
                payment_method_stats[sale.payment_method] += 1
            
            return SaleStatisticsResponse(
                total_sales=total_sales,
                total_revenue=total_revenue,
                total_commission=total_commission,
                average_sale_value=average_sale_value,
                sales_by_status=status_stats,
                sales_by_payment_method=payment_method_stats,
                period_start=start_date.isoformat() if start_date else "",
                period_end=end_date.isoformat() if end_date else ""
            )
            
        except Exception as e:
            logger.error(f"Erro ao gerar estatísticas: {str(e)}")
            raise Exception(f"Erro ao gerar estatísticas: {str(e)}")
    
    def _model_to_entity(self, sale_model: SaleModel) -> Sale:
        """Converte modelo SQLAlchemy para entidade de domínio."""
        return Sale(
            id=sale_model.id,
            client_id=sale_model.client_id,
            employee_id=sale_model.employee_id,
            vehicle_id=sale_model.vehicle_id,
            total_amount=sale_model.total_amount,
            payment_method=sale_model.payment_method,
            status=sale_model.status,
            sale_date=sale_model.sale_date,
            notes=sale_model.notes,
            discount_amount=sale_model.discount_amount,
            tax_amount=sale_model.tax_amount,
            commission_rate=sale_model.commission_rate,
            created_at=sale_model.created_at,
            updated_at=sale_model.updated_at
        )