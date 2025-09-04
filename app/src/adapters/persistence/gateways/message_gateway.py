from typing import List, Optional, Dict, Any
import logging
from uuid import UUID
from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, and_, or_

from src.domain.entities.message import Message
from src.domain.ports.message_repository import MessageRepository
from src.domain.exceptions import MessageNotFoundError, DatabaseError
from src.infrastructure.database.models.message_model import MessageModel

logger = logging.getLogger(__name__)


class MessageGateway(MessageRepository):
    """
    Gateway para persistência de mensagens usando SQLAlchemy.
    
    Implementa o padrão Gateway e Interface Segregation Principle (ISP),
    fornecendo implementação concreta do MessageRepository.
    """

    def __init__(self, db_session: Session):
        """
        Inicializa o gateway com uma sessão de banco de dados.
        
        Args:
            db_session: Sessão SQLAlchemy para operações de banco
        """
        self.db_session = db_session

    async def save(self, message: Message) -> Message:
        """
        Salva uma mensagem no banco de dados.
        
        Args:
            message: Entidade Message a ser salva
            
        Returns:
            Message: Entidade salva com dados atualizados
            
        Raises:
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info(f"Salvando mensagem - ID: {message.id}")
            
            # Verifica se é update ou create
            existing_message = self.db_session.query(MessageModel).filter_by(id=message.id).first()
            
            if existing_message:
                # Update
                existing_message.client_id = message.client_id
                existing_message.employee_id = message.employee_id
                existing_message.subject = message.subject
                existing_message.content = message.content
                existing_message.message_type = message.message_type
                existing_message.priority = message.priority
                existing_message.status = message.status
                existing_message.is_read = message.is_read
                existing_message.client_name = message.client_name
                existing_message.client_email = message.client_email
                existing_message.client_phone = message.client_phone
                existing_message.response = message.response
                existing_message.response_date = message.response_date
                
                message_model = existing_message
            else:
                # Create
                message_model = self._entity_to_model(message)
                self.db_session.add(message_model)
            
            self.db_session.commit()
            self.db_session.refresh(message_model)
            
            logger.info(f"Mensagem salva com sucesso - ID: {message.id}")
            return self._model_to_entity(message_model)
            
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(f"Erro ao salvar mensagem: {str(e)}")
            raise DatabaseError(f"Erro ao salvar mensagem: {str(e)}")

    async def find_by_id(self, message_id: UUID) -> Optional[Message]:
        """
        Busca mensagem por ID.
        
        Args:
            message_id: UUID da mensagem
            
        Returns:
            Optional[Message]: Mensagem encontrada ou None
            
        Raises:
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info(f"Buscando mensagem por ID: {message_id}")
            
            message_model = self.db_session.query(MessageModel).filter_by(id=message_id).first()
            
            if message_model:
                logger.info(f"Mensagem encontrada: {message_model.subject}")
                return self._model_to_entity(message_model)
            
            logger.info(f"Mensagem não encontrada para ID: {message_id}")
            return None
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar mensagem por ID: {str(e)}")
            raise DatabaseError(f"Erro ao buscar mensagem: {str(e)}")

    async def find_by_criteria(self, **kwargs) -> List[Message]:
        """
        Busca mensagens por múltiplos critérios.
        
        Args:
            **kwargs: Critérios de busca
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        try:
            logger.info(f"Buscando mensagens por critérios: {kwargs}")
            
            query = self.db_session.query(MessageModel)
            
            if 'status' in kwargs:
                query = query.filter(MessageModel.status == kwargs['status'])
            
            if 'employee_id' in kwargs:
                query = query.filter(MessageModel.employee_id == kwargs['employee_id'])
                
            if 'client_id' in kwargs:
                query = query.filter(MessageModel.client_id == kwargs['client_id'])
                
            if 'message_type' in kwargs:
                query = query.filter(MessageModel.message_type == kwargs['message_type'])
                
            if 'priority' in kwargs:
                query = query.filter(MessageModel.priority == kwargs['priority'])
                
            if 'is_read' in kwargs:
                query = query.filter(MessageModel.is_read == kwargs['is_read'])
                
            if 'start_date' in kwargs:
                query = query.filter(MessageModel.created_at >= kwargs['start_date'])
                
            if 'end_date' in kwargs:
                query = query.filter(MessageModel.created_at <= kwargs['end_date'])
            
            # Paginação
            if 'skip' in kwargs:
                query = query.offset(kwargs['skip'])
                
            if 'limit' in kwargs:
                query = query.limit(kwargs['limit'])
            
            message_models = query.all()
            messages = [self._model_to_entity(model) for model in message_models]
            
            logger.info(f"Encontradas {len(messages)} mensagens com os critérios aplicados")
            return messages
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar mensagens por critérios: {str(e)}")
            raise DatabaseError(f"Erro ao buscar mensagens: {str(e)}")

    async def find_by_email(self, email: str, **kwargs) -> List[Message]:
        """
        Busca mensagens por email.
        
        Args:
            email: Email do interessado
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        return await self.find_by_criteria(client_email=email, **kwargs)

    async def find_by_responsible(self, responsible_id: UUID, **kwargs) -> List[Message]:
        """
        Busca mensagens por responsável.
        
        Args:
            responsible_id: ID do funcionário responsável
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        return await self.find_by_criteria(employee_id=responsible_id, **kwargs)

    async def find_by_vehicle(self, vehicle_id: UUID, **kwargs) -> List[Message]:
        """
        Busca mensagens por veículo.
        
        Args:
            vehicle_id: ID do veículo
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        # Como não temos campo vehicle_id no MessageModel, retornamos lista vazia
        logger.warning("Vehicle search not implemented in MessageModel")
        return []

    async def find_by_status(self, status: str, **kwargs) -> List[Message]:
        """
        Busca mensagens por status.
        
        Args:
            status: Status das mensagens
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        return await self.find_by_criteria(status=status, **kwargs)

    async def find_by_date_range(self, start_date: date, end_date: date, **kwargs) -> List[Message]:
        """
        Busca mensagens por período.
        
        Args:
            start_date: Data inicial
            end_date: Data final
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        return await self.find_by_criteria(start_date=start_date, end_date=end_date, **kwargs)

    async def find_pending_messages(self, **kwargs) -> List[Message]:
        """
        Busca mensagens pendentes.
        
        Args:
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens pendentes
        """
        return await self.find_by_criteria(status="Pendente", **kwargs)

    async def find_unassigned_messages(self, **kwargs) -> List[Message]:
        """
        Busca mensagens sem responsável atribuído.
        
        Args:
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens sem responsável
        """
        try:
            logger.info("Buscando mensagens não atribuídas")
            
            query = self.db_session.query(MessageModel).filter(MessageModel.employee_id.is_(None))
            
            # Aplicar outros filtros se fornecidos
            if 'skip' in kwargs:
                query = query.offset(kwargs['skip'])
                
            if 'limit' in kwargs:
                query = query.limit(kwargs['limit'])
            
            message_models = query.all()
            messages = [self._model_to_entity(model) for model in message_models]
            
            logger.info(f"Encontradas {len(messages)} mensagens não atribuídas")
            return messages
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar mensagens não atribuídas: {str(e)}")
            raise DatabaseError(f"Erro ao buscar mensagens: {str(e)}")

    async def find_overdue_messages(self, hours_threshold: int = 24, **kwargs) -> List[Message]:
        """
        Busca mensagens em atraso.
        
        Args:
            hours_threshold: Número de horas para considerar em atraso
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens em atraso
        """
        try:
            logger.info(f"Buscando mensagens em atraso (>{hours_threshold}h)")
            
            threshold_date = datetime.now() - timedelta(hours=hours_threshold)
            
            query = self.db_session.query(MessageModel).filter(
                and_(
                    MessageModel.status == "Pendente",
                    MessageModel.created_at <= threshold_date
                )
            )
            
            # Aplicar outros filtros se fornecidos
            if 'skip' in kwargs:
                query = query.offset(kwargs['skip'])
                
            if 'limit' in kwargs:
                query = query.limit(kwargs['limit'])
            
            message_models = query.all()
            messages = [self._model_to_entity(model) for model in message_models]
            
            logger.info(f"Encontradas {len(messages)} mensagens em atraso")
            return messages
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar mensagens em atraso: {str(e)}")
            raise DatabaseError(f"Erro ao buscar mensagens: {str(e)}")

    async def delete(self, message_id: UUID) -> None:
        """
        Remove uma mensagem do banco de dados.
        
        Args:
            message_id: ID da mensagem a ser removida
            
        Raises:
            MessageNotFoundError: Se mensagem não encontrada
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info(f"Removendo mensagem com ID: {message_id}")
            
            message_model = self.db_session.query(MessageModel).filter_by(id=message_id).first()
            if not message_model:
                raise MessageNotFoundError(f"Mensagem com ID {message_id} não encontrada")
            
            self.db_session.delete(message_model)
            self.db_session.commit()
            
            logger.info(f"Mensagem removida com sucesso - ID: {message_id}")
            
        except MessageNotFoundError:
            self.db_session.rollback()
            raise
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(f"Erro ao remover mensagem: {str(e)}")
            raise DatabaseError(f"Erro ao remover mensagem: {str(e)}")

    async def exists_by_id(self, message_id: UUID) -> bool:
        """
        Verifica se existe mensagem com o ID.
        
        Args:
            message_id: ID a ser verificado
            
        Returns:
            bool: True se existir mensagem com o ID
        """
        try:
            count = self.db_session.query(MessageModel).filter_by(id=message_id).count()
            return count > 0
        except SQLAlchemyError as e:
            logger.error(f"Erro ao verificar existência de mensagem: {str(e)}")
            raise DatabaseError(f"Erro ao verificar mensagem: {str(e)}")

    async def count_by_status(self, status: str) -> int:
        """
        Conta mensagens por status.
        
        Args:
            status: Status das mensagens
            
        Returns:
            int: Número de mensagens com o status
        """
        try:
            return self.db_session.query(MessageModel).filter_by(status=status).count()
        except SQLAlchemyError as e:
            logger.error(f"Erro ao contar mensagens por status: {str(e)}")
            raise DatabaseError(f"Erro ao contar mensagens: {str(e)}")

    async def count_by_responsible(self, responsible_id: UUID) -> int:
        """
        Conta mensagens por responsável.
        
        Args:
            responsible_id: ID do funcionário responsável
            
        Returns:
            int: Número de mensagens do responsável
        """
        try:
            return self.db_session.query(MessageModel).filter_by(employee_id=responsible_id).count()
        except SQLAlchemyError as e:
            logger.error(f"Erro ao contar mensagens por responsável: {str(e)}")
            raise DatabaseError(f"Erro ao contar mensagens: {str(e)}")

    async def count_by_vehicle(self, vehicle_id: UUID) -> int:
        """
        Conta mensagens por veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            int: Número de mensagens do veículo
        """
        # Como não temos campo vehicle_id no MessageModel, retornamos 0
        logger.warning("Vehicle count not implemented in MessageModel")
        return 0

    async def count_pending_messages(self) -> int:
        """
        Conta mensagens pendentes.
        
        Returns:
            int: Número de mensagens pendentes
        """
        return await self.count_by_status("Pendente")

    async def count_unassigned_messages(self) -> int:
        """
        Conta mensagens sem responsável.
        
        Returns:
            int: Número de mensagens sem responsável
        """
        try:
            return self.db_session.query(MessageModel).filter(MessageModel.employee_id.is_(None)).count()
        except SQLAlchemyError as e:
            logger.error(f"Erro ao contar mensagens não atribuídas: {str(e)}")
            raise DatabaseError(f"Erro ao contar mensagens: {str(e)}")

    async def get_response_time_statistics(self, start_date: Optional[date] = None, 
                                          end_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Calcula estatísticas de tempo de resposta.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            dict: Estatísticas de tempo de resposta
        """
        try:
            query = self.db_session.query(MessageModel).filter(MessageModel.response_date.isnot(None))
            
            if start_date:
                query = query.filter(MessageModel.created_at >= start_date)
            
            if end_date:
                query = query.filter(MessageModel.created_at <= end_date)
            
            messages = query.all()
            
            if not messages:
                return {
                    'total_responded': 0,
                    'average_response_hours': 0,
                    'min_response_hours': 0,
                    'max_response_hours': 0
                }
            
            response_times = []
            for message in messages:
                if message.response_date and message.created_at:
                    delta = message.response_date - message.created_at
                    hours = delta.total_seconds() / 3600
                    response_times.append(hours)
            
            if response_times:
                avg_time = sum(response_times) / len(response_times)
                min_time = min(response_times)
                max_time = max(response_times)
            else:
                avg_time = min_time = max_time = 0
            
            return {
                'total_responded': len(messages),
                'average_response_hours': avg_time,
                'min_response_hours': min_time,
                'max_response_hours': max_time
            }
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao calcular estatísticas de resposta: {str(e)}")
            raise DatabaseError(f"Erro ao calcular estatísticas: {str(e)}")

    async def get_messages_statistics(self, start_date: Optional[date] = None, 
                                     end_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Busca estatísticas gerais de mensagens.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            dict: Estatísticas das mensagens
        """
        try:
            query = self.db_session.query(MessageModel)
            
            if start_date:
                query = query.filter(MessageModel.created_at >= start_date)
            
            if end_date:
                query = query.filter(MessageModel.created_at <= end_date)
            
            messages = query.all()
            total_messages = len(messages)
            
            # Estatísticas por status
            status_stats = {}
            for message in messages:
                status = message.status
                if status not in status_stats:
                    status_stats[status] = 0
                status_stats[status] += 1
            
            # Estatísticas por prioridade
            priority_stats = {}
            for message in messages:
                priority = message.priority
                if priority not in priority_stats:
                    priority_stats[priority] = 0
                priority_stats[priority] += 1
            
            unread_count = sum(1 for m in messages if not m.is_read)
            unassigned_count = sum(1 for m in messages if m.employee_id is None)
            
            return {
                'total_messages': total_messages,
                'unread_messages': unread_count,
                'unassigned_messages': unassigned_count,
                'status_statistics': status_stats,
                'priority_statistics': priority_stats
            }
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao calcular estatísticas de mensagens: {str(e)}")
            raise DatabaseError(f"Erro ao calcular estatísticas: {str(e)}")

    async def get_top_performers(self, start_date: Optional[date] = None, 
                                end_date: Optional[date] = None, 
                                limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca funcionários com melhor performance no atendimento.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            limit: Número máximo de resultados
            
        Returns:
            List[Dict]: Lista de funcionários com estatísticas
        """
        try:
            query = self.db_session.query(
                MessageModel.employee_id,
                func.count(MessageModel.id).label('total_messages'),
                func.sum(func.case([(MessageModel.status == 'Finalizado', 1)], else_=0)).label('completed_messages')
            ).filter(MessageModel.employee_id.isnot(None)).group_by(MessageModel.employee_id)
            
            if start_date:
                query = query.filter(MessageModel.created_at >= start_date)
            
            if end_date:
                query = query.filter(MessageModel.created_at <= end_date)
            
            results = query.order_by(func.count(MessageModel.id).desc()).limit(limit).all()
            
            performers = []
            for result in results:
                completion_rate = (result.completed_messages / result.total_messages * 100) if result.total_messages > 0 else 0
                performers.append({
                    'employee_id': result.employee_id,
                    'total_messages': result.total_messages,
                    'completed_messages': result.completed_messages or 0,
                    'completion_rate': completion_rate
                })
            
            return performers
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar top performers: {str(e)}")
            raise DatabaseError(f"Erro ao buscar performers: {str(e)}")

    async def get_vehicles_with_most_interest(self, start_date: Optional[date] = None, 
                                            end_date: Optional[date] = None, 
                                            limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca veículos com mais interesse.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            limit: Número máximo de resultados
            
        Returns:
            List[Dict]: Lista de veículos com estatísticas
        """
        # Como não temos campo vehicle_id no MessageModel, retornamos lista vazia
        logger.warning("Vehicle interest statistics not implemented in MessageModel")
        return []

    def _entity_to_model(self, message: Message) -> MessageModel:
        """
        Converte entidade Message para modelo MessageModel.
        
        Args:
            message: Entidade Message
            
        Returns:
            MessageModel: Modelo para persistência
        """
        return MessageModel(
            id=message.id,
            client_id=message.client_id,
            employee_id=message.employee_id,
            subject=message.subject,
            content=message.content,
            message_type=message.message_type,
            priority=message.priority,
            status=message.status,
            is_read=message.is_read,
            client_name=message.client_name,
            client_email=message.client_email,
            client_phone=message.client_phone,
            response=message.response,
            response_date=message.response_date
        )

    def _model_to_entity(self, model: MessageModel) -> Message:
        """
        Converte modelo MessageModel para entidade Message.
        
        Args:
            model: Modelo MessageModel
            
        Returns:
            Message: Entidade de domínio
        """
        return Message(
            id=model.id,
            client_id=model.client_id,
            employee_id=model.employee_id,
            subject=model.subject,
            content=model.content,
            message_type=model.message_type,
            priority=model.priority,
            status=model.status,
            is_read=model.is_read,
            client_name=model.client_name,
            client_email=model.client_email,
            client_phone=model.client_phone,
            response=model.response,
            response_date=model.response_date,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
