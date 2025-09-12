"""
SaleGateway - Infrastructure Layer

Gateway de persistência para vendas.

Implementa a interface SaleRepository definida no domínio.
Aplicando o princípio Dependency Inversion Principle (DIP) - 
implementa a abstração definida no domínio.

Aplicando o princípio Single Responsibility Principle (SRP) - 
responsável apenas pela persistência de dados de vendas.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_, desc, asc
from src.domain.entities.sale import Sale
from src.domain.ports.sale_repository import SaleRepository
from src.infrastructure.database.models.sale_model import SaleModel
from src.infrastructure.database.models.client_model import ClientModel
from src.infrastructure.database.models.motor_vehicle_model import MotorVehicleModel
from src.infrastructure.database.connection import get_db_session
from datetime import date
import logging

logger = logging.getLogger(__name__)


class SaleGateway(SaleRepository):
    """
    Gateway de persistência para vendas.
    
    Implementa a interface SaleRepository definida no domínio.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa o gateway com uma sessão do banco de dados.
        
        Args:
            session: Sessão do SQLAlchemy
        """
        self._session = session
    
    def _apply_value_ordering(self, query, order_by_value: Optional[str]):
        """
        Aplica ordenação por valor total da venda.
        
        Args:
            query: Query do SQLAlchemy
            order_by_value: 'asc' para crescente, 'desc' para decrescente
            
        Returns:
            Query com ordenação aplicada
        """
        if order_by_value == 'desc':
            return query.order_by(desc(SaleModel.total_amount))
        elif order_by_value == 'asc':
            return query.order_by(asc(SaleModel.total_amount))
        return query

    async def create_sale(self, sale: Sale) -> Sale:
        """
        Cria uma nova venda no banco de dados.
        
        Args:
            sale: Entidade da venda a ser criada
            
        Returns:
            Sale: Venda criada
        """
        try:
            with get_db_session() as session:
                # Converter entidade do domínio para modelo de banco
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
                    commission_rate=sale.commission_rate,
                    commission_amount=sale.commission_amount
                )
                
                session.add(sale_model)
                session.commit()
                session.refresh(sale_model)
                
                # Converter modelo de banco para entidade do domínio
                created_sale = self._model_to_entity(sale_model)
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(sale_model)
                
                logger.info(f"Venda criada com sucesso. ID: {created_sale.id}")
                return created_sale
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar venda: {str(e)}")
            raise Exception(f"Erro ao criar venda: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao criar venda: {str(e)}")
            raise Exception(f"Erro inesperado ao criar venda: {str(e)}")

    async def get_sale_by_id(self, sale_id: int) -> Optional[Sale]:
        """
        Busca uma venda pelo ID.
        
        Args:
            sale_id: ID da venda
            
        Returns:
            Optional[Sale]: Venda encontrada ou None
        """
        try:
            with get_db_session() as session:
                sale_model = session.query(SaleModel).filter(SaleModel.id == sale_id).first()
                
                if sale_model:
                    # Fazer expunge para desconectar o objeto da sessão
                    session.expunge(sale_model)
                    return self._model_to_entity(sale_model)
                
                return None
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar venda por ID {sale_id}: {str(e)}")
            raise Exception(f"Erro ao buscar venda: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar venda por ID {sale_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar venda: {str(e)}")

    async def update_sale(self, sale_id: int, sale: Sale) -> Optional[Sale]:
        """
        Atualiza uma venda existente.
        
        Args:
            sale_id: ID da venda
            sale: Dados atualizados da venda
            
        Returns:
            Optional[Sale]: Venda atualizada
        """
        try:
            with get_db_session() as session:
                sale_model = session.query(SaleModel).filter(SaleModel.id == sale_id).first()
                
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
                sale_model.commission_amount = sale.commission_amount
                
                session.commit()
                session.refresh(sale_model)
                
                # Converter para entidade do domínio
                updated_sale = self._model_to_entity(sale_model)
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(sale_model)
                
                logger.info(f"Venda atualizada com sucesso. ID: {updated_sale.id}")
                return updated_sale
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar venda {sale_id}: {str(e)}")
            raise Exception(f"Erro ao atualizar venda: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar venda {sale_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao atualizar venda: {str(e)}")

    async def update_sale_status(self, sale_id: int, status: str) -> Optional[Sale]:
        """
        Atualiza apenas o status de uma venda.
        
        Args:
            sale_id: ID da venda
            status: Novo status
            
        Returns:
            Optional[Sale]: Venda atualizada ou None se não encontrada
        """
        try:
            with get_db_session() as session:
                sale_model = session.query(SaleModel).filter(SaleModel.id == sale_id).first()
                
                if not sale_model:
                    return None
                
                # Atualizar apenas o status
                sale_model.status = status
                
                session.commit()
                session.refresh(sale_model)
                
                # Converter para entidade do domínio
                updated_sale = self._model_to_entity(sale_model)
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(sale_model)
                
                logger.info(f"Status da venda atualizado com sucesso. ID: {updated_sale.id}, Status: {status}")
                return updated_sale
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar status da venda {sale_id}: {str(e)}")
            raise Exception(f"Erro ao atualizar status da venda: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar status da venda {sale_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao atualizar status da venda: {str(e)}")

    async def delete_sale(self, sale_id: int) -> bool:
        """
        Remove uma venda.
        
        Args:
            sale_id: ID da venda
            
        Returns:
            bool: True se removida com sucesso, False se não encontrada
        """
        try:
            with get_db_session() as session:
                sale_model = session.query(SaleModel).filter(SaleModel.id == sale_id).first()
                
                if not sale_model:
                    return False
                
                session.delete(sale_model)
                session.commit()
                
                logger.info(f"Venda removida com sucesso. ID: {sale_id}")
                return True
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao remover venda {sale_id}: {str(e)}")
            raise Exception(f"Erro ao remover venda: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao remover venda {sale_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao remover venda: {str(e)}")

    async def get_all_sales(self, skip: int = 0, limit: int = 100, order_by_value: Optional[str] = None) -> List[Sale]:
        """
        Lista todas as vendas com paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            order_by_value: Ordenação por valor - 'asc' ou 'desc' (opcional)
            
        Returns:
            List[Sale]: Lista de vendas
        """
        try:
            with get_db_session() as session:
                query = session.query(SaleModel)
                query = self._apply_value_ordering(query, order_by_value)
                
                sale_models = query.offset(skip).limit(limit).all()
                
                # Fazer expunge para desconectar os objetos da sessão
                for sale_model in sale_models:
                    session.expunge(sale_model)
                
                return [self._model_to_entity(sale_model) for sale_model in sale_models]
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar vendas: {str(e)}")
            raise Exception(f"Erro ao listar vendas: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao listar vendas: {str(e)}")
            raise Exception(f"Erro inesperado ao listar vendas: {str(e)}")

    async def get_sales_by_client(self, client_id: int, skip: int = 0, limit: int = 100, order_by_value: Optional[str] = None) -> List[Sale]:
        """
        Lista vendas por cliente.
        
        Args:
            client_id: ID do cliente
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            order_by_value: Ordenação por valor - 'asc' ou 'desc' (opcional)
            
        Returns:
            List[Sale]: Lista de vendas do cliente
        """
        try:
            with get_db_session() as session:
                query = session.query(SaleModel).filter(SaleModel.client_id == client_id)
                query = self._apply_value_ordering(query, order_by_value)
                
                sale_models = query.offset(skip).limit(limit).all()
                
                # Fazer expunge para desconectar os objetos da sessão
                for sale_model in sale_models:
                    session.expunge(sale_model)
                
                return [self._model_to_entity(sale_model) for sale_model in sale_models]
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar vendas do cliente {client_id}: {str(e)}")
            raise Exception(f"Erro ao listar vendas do cliente: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao listar vendas do cliente {client_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao listar vendas do cliente: {str(e)}")

    async def get_sales_by_employee(self, employee_id: int, skip: int = 0, limit: int = 100, order_by_value: Optional[str] = None) -> List[Sale]:
        """
        Lista vendas por funcionário.
        
        Args:
            employee_id: ID do funcionário
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            order_by_value: Ordenação por valor - 'asc' ou 'desc' (opcional)
            
        Returns:
            List[Sale]: Lista de vendas do funcionário
        """
        try:
            with get_db_session() as session:
                query = session.query(SaleModel).filter(SaleModel.employee_id == employee_id)
                query = self._apply_value_ordering(query, order_by_value)
                
                sale_models = query.offset(skip).limit(limit).all()
                
                # Fazer expunge para desconectar os objetos da sessão
                for sale_model in sale_models:
                    session.expunge(sale_model)
                
                return [self._model_to_entity(sale_model) for sale_model in sale_models]
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar vendas do funcionário {employee_id}: {str(e)}")
            raise Exception(f"Erro ao listar vendas do funcionário: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao listar vendas do funcionário {employee_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao listar vendas do funcionário: {str(e)}")

    async def get_sales_by_status(self, status: str, skip: int = 0, limit: int = 100, order_by_value: Optional[str] = None) -> List[Sale]:
        """
        Lista vendas por status.
        
        Args:
            status: Status das vendas
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            order_by_value: Ordenação por valor - 'asc' ou 'desc' (opcional)
            
        Returns:
            List[Sale]: Lista de vendas com o status especificado
        """
        try:
            with get_db_session() as session:
                query = session.query(SaleModel).filter(SaleModel.status == status)
                query = self._apply_value_ordering(query, order_by_value)
                
                sale_models = query.offset(skip).limit(limit).all()
                
                # Fazer expunge para desconectar os objetos da sessão
                for sale_model in sale_models:
                    session.expunge(sale_model)
                
                return [self._model_to_entity(sale_model) for sale_model in sale_models]
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar vendas com status {status}: {str(e)}")
            raise Exception(f"Erro ao listar vendas por status: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao listar vendas com status {status}: {str(e)}")
            raise Exception(f"Erro inesperado ao listar vendas por status: {str(e)}")

    async def get_sales_by_payment_method(self, payment_method: str, skip: int = 0, limit: int = 100, order_by_value: Optional[str] = None) -> List[Sale]:
        """
        Lista vendas por forma de pagamento.
        
        Args:
            payment_method: Forma de pagamento
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            order_by_value: Ordenação por valor - 'asc' ou 'desc' (opcional)
            
        Returns:
            List[Sale]: Lista de vendas com a forma de pagamento especificada
        """
        try:
            with get_db_session() as session:
                query = session.query(SaleModel).filter(SaleModel.payment_method == payment_method)
                query = self._apply_value_ordering(query, order_by_value)
                
                sale_models = query.offset(skip).limit(limit).all()
                
                # Fazer expunge para desconectar os objetos da sessão
                for sale_model in sale_models:
                    session.expunge(sale_model)
                
                return [self._model_to_entity(sale_model) for sale_model in sale_models]
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar vendas com forma de pagamento {payment_method}: {str(e)}")
            raise Exception(f"Erro ao listar vendas por forma de pagamento: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao listar vendas com forma de pagamento {payment_method}: {str(e)}")
            raise Exception(f"Erro inesperado ao listar vendas por forma de pagamento: {str(e)}")

    async def get_sales_by_date_range(self, start_date: date, end_date: date, skip: int = 0, limit: int = 100, order_by_value: Optional[str] = None) -> List[Sale]:
        """
        Lista vendas em um período de datas.
        
        Args:
            start_date: Data inicial
            end_date: Data final
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            order_by_value: Ordenação por valor - 'asc' ou 'desc' (opcional)
            
        Returns:
            List[Sale]: Lista de vendas no período especificado
        """
        try:
            with get_db_session() as session:
                query = session.query(SaleModel).filter(
                    and_(SaleModel.sale_date >= start_date, SaleModel.sale_date <= end_date)
                )
                query = self._apply_value_ordering(query, order_by_value)
                
                sale_models = query.offset(skip).limit(limit).all()
                
                # Fazer expunge para desconectar os objetos da sessão
                for sale_model in sale_models:
                    session.expunge(sale_model)
                
                return [self._model_to_entity(sale_model) for sale_model in sale_models]
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar vendas no período {start_date} a {end_date}: {str(e)}")
            raise Exception(f"Erro ao listar vendas por período: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao listar vendas no período {start_date} a {end_date}: {str(e)}")
            raise Exception(f"Erro inesperado ao listar vendas por período: {str(e)}")

    async def get_sales_statistics(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> dict:
        """
        Busca estatísticas de vendas.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            dict: Estatísticas das vendas
        """
        try:
            with get_db_session() as session:
                query = session.query(SaleModel)
                
                if start_date and end_date:
                    query = query.filter(
                        and_(SaleModel.sale_date >= start_date, SaleModel.sale_date <= end_date)
                    )
                
                sales = query.all()
                
                total_sales = len(sales)
                total_amount = sum(sale.total_amount for sale in sales)
                total_discount = sum(sale.discount_amount for sale in sales)
                total_tax = sum(sale.tax_amount for sale in sales)
                total_commission = sum(sale.commission_amount for sale in sales)
                
                # Estatísticas por status
                status_stats = {}
                for sale in sales:
                    status = sale.status
                    if status not in status_stats:
                        status_stats[status] = {'count': 0, 'total_amount': 0}
                    status_stats[status]['count'] += 1
                    status_stats[status]['total_amount'] += float(sale.total_amount)
                
                return {
                    'total_sales': total_sales,
                    'total_amount': float(total_amount),
                    'total_discount': float(total_discount),
                    'total_tax': float(total_tax),
                    'total_commission': float(total_commission),
                    'status_statistics': status_stats,
                    'period': {
                        'start_date': start_date.isoformat() if start_date else None,
                        'end_date': end_date.isoformat() if end_date else None
                    }
                }
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar estatísticas de vendas: {str(e)}")
            raise Exception(f"Erro ao buscar estatísticas de vendas: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar estatísticas de vendas: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar estatísticas de vendas: {str(e)}")

    def _model_to_entity(self, sale_model: SaleModel) -> Sale:
        """
        Converte modelo de banco para entidade do domínio.
        
        Args:
            sale_model: Modelo SQLAlchemy
            
        Returns:
            Sale: Entidade do domínio
        """
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
            commission_amount=sale_model.commission_amount,
            created_at=sale_model.created_at,
            updated_at=sale_model.updated_at
        )
