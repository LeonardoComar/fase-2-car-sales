from typing import List, Optional, Dict, Any
import logging
from uuid import UUID
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, and_

from src.domain.entities.sale import Sale
from src.domain.ports.sale_repository import SaleRepository
from src.domain.exceptions import SaleNotFoundError, DatabaseError
from src.infrastructure.database.models.sale_model import SaleModel

logger = logging.getLogger(__name__)


class SaleGateway(SaleRepository):
    """
    Gateway para persistência de vendas usando SQLAlchemy.
    
    Implementa o padrão Gateway e Interface Segregation Principle (ISP),
    fornecendo implementação concreta do SaleRepository.
    """

    def __init__(self, db_session: Session):
        """
        Inicializa o gateway com uma sessão de banco de dados.
        
        Args:
            db_session: Sessão SQLAlchemy para operações de banco
        """
        self.db_session = db_session

    async def save(self, sale: Sale) -> Sale:
        """
        Salva uma venda no banco de dados.
        
        Args:
            sale: Entidade Sale a ser salva
            
        Returns:
            Sale: Entidade salva com dados atualizados
            
        Raises:
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info(f"Salvando venda - ID: {sale.id}")
            
            # Verifica se é update ou create
            existing_sale = self.db_session.query(SaleModel).filter_by(id=sale.id).first()
            
            if existing_sale:
                # Update
                existing_sale.client_id = sale.client_id
                existing_sale.employee_id = sale.employee_id
                existing_sale.vehicle_id = sale.vehicle_id
                existing_sale.sale_date = sale.sale_date
                existing_sale.sale_price = sale.total_amount
                existing_sale.discount = sale.discount_amount
                existing_sale.final_price = sale.total_amount - sale.discount_amount
                existing_sale.payment_method = sale.payment_method
                existing_sale.status = sale.status
                existing_sale.notes = sale.notes
                
                sale_model = existing_sale
            else:
                # Create
                sale_model = self._entity_to_model(sale)
                self.db_session.add(sale_model)
            
            self.db_session.commit()
            self.db_session.refresh(sale_model)
            
            logger.info(f"Venda salva com sucesso - ID: {sale.id}")
            return self._model_to_entity(sale_model)
            
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(f"Erro ao salvar venda: {str(e)}")
            raise DatabaseError(f"Erro ao salvar venda: {str(e)}")

    async def find_by_id(self, sale_id: UUID) -> Optional[Sale]:
        """
        Busca venda por ID.
        
        Args:
            sale_id: UUID da venda
            
        Returns:
            Optional[Sale]: Venda encontrada ou None
            
        Raises:
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info(f"Buscando venda por ID: {sale_id}")
            
            sale_model = self.db_session.query(SaleModel).filter_by(id=sale_id).first()
            
            if sale_model:
                logger.info(f"Venda encontrada: {sale_model.id}")
                return self._model_to_entity(sale_model)
            
            logger.info(f"Venda não encontrada para ID: {sale_id}")
            return None
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar venda por ID: {str(e)}")
            raise DatabaseError(f"Erro ao buscar venda: {str(e)}")

    async def find_by_criteria(self, **kwargs) -> List[Sale]:
        """
        Busca vendas por múltiplos critérios.
        
        Args:
            **kwargs: Critérios de busca
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        try:
            logger.info(f"Buscando vendas por critérios: {kwargs}")
            
            query = self.db_session.query(SaleModel)
            
            if 'client_id' in kwargs:
                query = query.filter(SaleModel.client_id == kwargs['client_id'])
            
            if 'employee_id' in kwargs:
                query = query.filter(SaleModel.employee_id == kwargs['employee_id'])
                
            if 'status' in kwargs:
                query = query.filter(SaleModel.status == kwargs['status'])
                
            if 'payment_method' in kwargs:
                query = query.filter(SaleModel.payment_method == kwargs['payment_method'])
                
            if 'start_date' in kwargs:
                query = query.filter(SaleModel.sale_date >= kwargs['start_date'])
                
            if 'end_date' in kwargs:
                query = query.filter(SaleModel.sale_date <= kwargs['end_date'])
            
            # Paginação
            if 'skip' in kwargs:
                query = query.offset(kwargs['skip'])
                
            if 'limit' in kwargs:
                query = query.limit(kwargs['limit'])
            
            sale_models = query.all()
            sales = [self._model_to_entity(model) for model in sale_models]
            
            logger.info(f"Encontradas {len(sales)} vendas com os critérios aplicados")
            return sales
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar vendas por critérios: {str(e)}")
            raise DatabaseError(f"Erro ao buscar vendas: {str(e)}")

    async def find_by_client(self, client_id: UUID, **kwargs) -> List[Sale]:
        """
        Busca vendas por cliente.
        
        Args:
            client_id: ID do cliente
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        return await self.find_by_criteria(client_id=client_id, **kwargs)

    async def find_by_employee(self, employee_id: UUID, **kwargs) -> List[Sale]:
        """
        Busca vendas por funcionário.
        
        Args:
            employee_id: ID do funcionário
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        return await self.find_by_criteria(employee_id=employee_id, **kwargs)

    async def find_by_vehicle(self, vehicle_id: UUID) -> Optional[Sale]:
        """
        Busca venda por veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Optional[Sale]: Venda encontrada ou None
        """
        try:
            logger.info(f"Buscando venda por veículo: {vehicle_id}")
            
            sale_model = self.db_session.query(SaleModel).filter_by(vehicle_id=vehicle_id).first()
            
            if sale_model:
                logger.info(f"Venda encontrada para veículo: {vehicle_id}")
                return self._model_to_entity(sale_model)
            
            return None
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar venda por veículo: {str(e)}")
            raise DatabaseError(f"Erro ao buscar venda: {str(e)}")

    async def find_by_status(self, status: str, **kwargs) -> List[Sale]:
        """
        Busca vendas por status.
        
        Args:
            status: Status das vendas
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        return await self.find_by_criteria(status=status, **kwargs)

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
        return await self.find_by_criteria(start_date=start_date, end_date=end_date, **kwargs)

    async def find_by_payment_method(self, payment_method: str, **kwargs) -> List[Sale]:
        """
        Busca vendas por forma de pagamento.
        
        Args:
            payment_method: Forma de pagamento
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Sale]: Lista de vendas encontradas
        """
        return await self.find_by_criteria(payment_method=payment_method, **kwargs)

    async def delete(self, sale_id: UUID) -> None:
        """
        Remove uma venda do banco de dados.
        
        Args:
            sale_id: ID da venda a ser removida
            
        Raises:
            SaleNotFoundError: Se venda não encontrada
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info(f"Removendo venda com ID: {sale_id}")
            
            sale_model = self.db_session.query(SaleModel).filter_by(id=sale_id).first()
            if not sale_model:
                raise SaleNotFoundError(f"Venda com ID {sale_id} não encontrada")
            
            self.db_session.delete(sale_model)
            self.db_session.commit()
            
            logger.info(f"Venda removida com sucesso - ID: {sale_id}")
            
        except SaleNotFoundError:
            self.db_session.rollback()
            raise
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(f"Erro ao remover venda: {str(e)}")
            raise DatabaseError(f"Erro ao remover venda: {str(e)}")

    async def exists_by_id(self, sale_id: UUID) -> bool:
        """
        Verifica se existe venda com o ID.
        
        Args:
            sale_id: ID a ser verificado
            
        Returns:
            bool: True se existir venda com o ID
        """
        try:
            count = self.db_session.query(SaleModel).filter_by(id=sale_id).count()
            return count > 0
        except SQLAlchemyError as e:
            logger.error(f"Erro ao verificar existência de venda: {str(e)}")
            raise DatabaseError(f"Erro ao verificar venda: {str(e)}")

    async def exists_by_vehicle(self, vehicle_id: UUID, exclude_id: Optional[UUID] = None) -> bool:
        """
        Verifica se existe venda para o veículo.
        
        Args:
            vehicle_id: ID do veículo
            exclude_id: ID da venda a ser excluída da verificação
            
        Returns:
            bool: True se existir venda para o veículo
        """
        try:
            query = self.db_session.query(SaleModel).filter_by(vehicle_id=vehicle_id)
            
            if exclude_id:
                query = query.filter(SaleModel.id != exclude_id)
            
            count = query.count()
            return count > 0
        except SQLAlchemyError as e:
            logger.error(f"Erro ao verificar venda por veículo: {str(e)}")
            raise DatabaseError(f"Erro ao verificar venda: {str(e)}")

    async def count_by_client(self, client_id: UUID) -> int:
        """
        Conta vendas por cliente.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            int: Número de vendas do cliente
        """
        try:
            return self.db_session.query(SaleModel).filter_by(client_id=client_id).count()
        except SQLAlchemyError as e:
            logger.error(f"Erro ao contar vendas por cliente: {str(e)}")
            raise DatabaseError(f"Erro ao contar vendas: {str(e)}")

    async def count_by_employee(self, employee_id: UUID) -> int:
        """
        Conta vendas por funcionário.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            int: Número de vendas do funcionário
        """
        try:
            return self.db_session.query(SaleModel).filter_by(employee_id=employee_id).count()
        except SQLAlchemyError as e:
            logger.error(f"Erro ao contar vendas por funcionário: {str(e)}")
            raise DatabaseError(f"Erro ao contar vendas: {str(e)}")

    async def count_by_status(self, status: str) -> int:
        """
        Conta vendas por status.
        
        Args:
            status: Status das vendas
            
        Returns:
            int: Número de vendas com o status
        """
        try:
            return self.db_session.query(SaleModel).filter_by(status=status).count()
        except SQLAlchemyError as e:
            logger.error(f"Erro ao contar vendas por status: {str(e)}")
            raise DatabaseError(f"Erro ao contar vendas: {str(e)}")

    async def get_total_sales_amount(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Decimal:
        """
        Calcula valor total de vendas em período.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            Decimal: Valor total das vendas
        """
        try:
            query = self.db_session.query(func.sum(SaleModel.final_price))
            
            if start_date:
                query = query.filter(SaleModel.sale_date >= start_date)
            
            if end_date:
                query = query.filter(SaleModel.sale_date <= end_date)
            
            result = query.scalar()
            return Decimal(str(result)) if result else Decimal('0.00')
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao calcular total de vendas: {str(e)}")
            raise DatabaseError(f"Erro ao calcular vendas: {str(e)}")

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
        try:
            # Como não temos campo de comissão no modelo, calculamos 5% do valor final
            query = self.db_session.query(func.sum(SaleModel.final_price * 0.05))
            
            if employee_id:
                query = query.filter(SaleModel.employee_id == employee_id)
            
            if start_date:
                query = query.filter(SaleModel.sale_date >= start_date)
            
            if end_date:
                query = query.filter(SaleModel.sale_date <= end_date)
            
            result = query.scalar()
            return Decimal(str(result)) if result else Decimal('0.00')
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao calcular comissões: {str(e)}")
            raise DatabaseError(f"Erro ao calcular comissões: {str(e)}")

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
        try:
            query = self.db_session.query(SaleModel)
            
            if start_date:
                query = query.filter(SaleModel.sale_date >= start_date)
            
            if end_date:
                query = query.filter(SaleModel.sale_date <= end_date)
            
            sales = query.all()
            
            total_sales = len(sales)
            total_amount = sum(sale.final_price for sale in sales)
            average_amount = total_amount / total_sales if total_sales > 0 else 0
            
            # Estatísticas por status
            status_stats = {}
            for sale in sales:
                status = sale.status
                if status not in status_stats:
                    status_stats[status] = {'count': 0, 'amount': Decimal('0.00')}
                status_stats[status]['count'] += 1
                status_stats[status]['amount'] += sale.final_price
            
            return {
                'total_sales': total_sales,
                'total_amount': total_amount,
                'average_amount': average_amount,
                'status_statistics': status_stats
            }
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao calcular estatísticas: {str(e)}")
            raise DatabaseError(f"Erro ao calcular estatísticas: {str(e)}")

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
        try:
            query = self.db_session.query(
                SaleModel.employee_id,
                func.count(SaleModel.id).label('total_sales'),
                func.sum(SaleModel.final_price).label('total_amount')
            ).group_by(SaleModel.employee_id)
            
            if start_date:
                query = query.filter(SaleModel.sale_date >= start_date)
            
            if end_date:
                query = query.filter(SaleModel.sale_date <= end_date)
            
            results = query.order_by(func.sum(SaleModel.final_price).desc()).limit(limit).all()
            
            performers = []
            for result in results:
                performers.append({
                    'employee_id': result.employee_id,
                    'total_sales': result.total_sales,
                    'total_amount': result.total_amount
                })
            
            return performers
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar top performers: {str(e)}")
            raise DatabaseError(f"Erro ao buscar performers: {str(e)}")

    def _entity_to_model(self, sale: Sale) -> SaleModel:
        """
        Converte entidade Sale para modelo SaleModel.
        
        Args:
            sale: Entidade Sale
            
        Returns:
            SaleModel: Modelo para persistência
        """
        return SaleModel(
            id=sale.id,
            client_id=sale.client_id,
            employee_id=sale.employee_id,
            vehicle_id=sale.vehicle_id,
            vehicle_type="unknown",  # Seria necessário determinar o tipo
            sale_date=sale.sale_date,
            sale_price=sale.total_amount,
            discount=sale.discount_amount,
            final_price=sale.total_amount - sale.discount_amount,
            payment_method=sale.payment_method,
            installments=1,  # Valor padrão
            status=sale.status,
            notes=sale.notes
        )

    def _model_to_entity(self, model: SaleModel) -> Sale:
        """
        Converte modelo SaleModel para entidade Sale.
        
        Args:
            model: Modelo SaleModel
            
        Returns:
            Sale: Entidade de domínio
        """
        return Sale(
            id=model.id,
            client_id=model.client_id,
            employee_id=model.employee_id,
            vehicle_id=model.vehicle_id,
            total_amount=model.sale_price,
            payment_method=model.payment_method,
            sale_date=model.sale_date,
            status=model.status,
            notes=model.notes,
            discount_amount=model.discount or Decimal('0.00'),
            tax_amount=Decimal('0.00'),  # Não temos no modelo
            commission_rate=Decimal('0.05'),  # Padrão 5%
            created_at=model.created_at,
            updated_at=model.updated_at
        )
