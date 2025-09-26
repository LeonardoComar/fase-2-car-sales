"""
Gateway para Mensagens - Infrastructure Layer

Implementação do repositório de mensagens usando SQLAlchemy.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from src.domain.entities.message import Message
from src.domain.ports.message_repository import MessageRepository
from src.infrastructure.database.models.message_model import MessageModel
import logging

logger = logging.getLogger(__name__)


class MessageGateway(MessageRepository):
    """Gateway para operações de mensagens."""
    
    def __init__(self, session: Session):
        """
        Inicializa o gateway com uma sessão do banco de dados.
        
        Args:
            session: Sessão do SQLAlchemy
        """
        self._session = session
    
    async def create_message(self, message: Message) -> Message:
        """Cria uma nova mensagem."""
        try:
            message_model = MessageModel(
                name=message.name,
                email=message.email,
                phone=message.phone,
                message=message.message,
                vehicle_id=message.vehicle_id,
                responsible_id=message.responsible_id,
                status=message.status,
                service_start_time=message.service_start_time
            )
            
            self._session.add(message_model)
            self._session.commit()  # Commit para persistir no banco
            self._session.refresh(message_model)  # Refresh para obter dados atualizados
            
            # Converter de volta para entidade de domínio
            return self._model_to_entity(message_model)
            
        except Exception as e:
            logger.error(f"Erro ao criar mensagem: {str(e)}")
            self._session.rollback()
            raise
    
    async def get_message_by_id(self, message_id: int) -> Optional[Message]:
        """Busca uma mensagem por ID."""
        try:
            message_model = self._session.query(MessageModel).filter(
                MessageModel.id == message_id
            ).first()
            
            if not message_model:
                return None
            
            return self._model_to_entity(message_model)
            
        except Exception as e:
            logger.error(f"Erro ao buscar mensagem por ID {message_id}: {str(e)}")
            raise
    
    async def get_all_messages(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by_value: str = "created_at",
        order_direction: str = "desc",
        status: Optional[str] = None,
        responsible_id: Optional[int] = None,
        vehicle_id: Optional[int] = None
    ) -> List[Message]:
        """Busca todas as mensagens com filtros opcionais."""
        try:
            query = self._session.query(MessageModel)
            
            # Aplicar filtros
            if status:
                query = query.filter(MessageModel.status == status)
            
            if responsible_id:
                query = query.filter(MessageModel.responsible_id == responsible_id)
            
            if vehicle_id:
                query = query.filter(MessageModel.vehicle_id == vehicle_id)
            
            # Ordenação
            order_column = getattr(MessageModel, order_by_value, MessageModel.created_at)
            if order_direction.lower() == "desc":
                query = query.order_by(desc(order_column))
            else:
                query = query.order_by(asc(order_column))
            
            # Paginação
            message_models = query.offset(offset).limit(limit).all()
            
            # Converter para entidades de domínio
            return [self._model_to_entity(model) for model in message_models]
            
        except Exception as e:
            logger.error(f"Erro ao buscar mensagens: {str(e)}")
            raise
    
    async def count_messages(
        self,
        status: Optional[str] = None,
        responsible_id: Optional[int] = None,
        vehicle_id: Optional[int] = None
    ) -> int:
        """Conta o número total de mensagens com filtros opcionais."""
        try:
            query = self._session.query(MessageModel)
            
            # Aplicar filtros
            if status:
                query = query.filter(MessageModel.status == status)
            
            if responsible_id:
                query = query.filter(MessageModel.responsible_id == responsible_id)
            
            if vehicle_id:
                query = query.filter(MessageModel.vehicle_id == vehicle_id)
            
            return query.count()
            
        except Exception as e:
            logger.error(f"Erro ao contar mensagens: {str(e)}")
            raise
    
    async def update_message(self, message: Message) -> Message:
        """Atualiza uma mensagem existente."""
        try:
            message_model = self._session.query(MessageModel).filter(
                MessageModel.id == message.id
            ).first()
            
            if not message_model:
                raise ValueError(f"Mensagem com ID {message.id} não encontrada")
            
            # Atualizar campos
            message_model.name = message.name
            message_model.email = message.email
            message_model.phone = message.phone
            message_model.message = message.message
            message_model.vehicle_id = message.vehicle_id
            message_model.responsible_id = message.responsible_id
            message_model.status = message.status
            message_model.service_start_time = message.service_start_time
            message_model.updated_at = datetime.utcnow()
            
            self._session.commit()
            self._session.refresh(message_model)
            
            return self._model_to_entity(message_model)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar mensagem {message.id}: {str(e)}")
            self._session.rollback()
            raise
    
    async def update_message_by_id(self, message_id: int, updates: Dict[str, Any]) -> Message:
        """Atualiza campos específicos de uma mensagem por ID."""
        try:
            message_model = self._session.query(MessageModel).filter(
                MessageModel.id == message_id
            ).first()
            
            if not message_model:
                raise ValueError(f"Mensagem com ID {message_id} não encontrada")
            
            # Aplicar atualizações
            for field, value in updates.items():
                if hasattr(message_model, field):
                    setattr(message_model, field, value)
            
            # Sempre atualizar updated_at
            message_model.updated_at = datetime.utcnow()
            
            self._session.commit()
            self._session.refresh(message_model)
            
            return self._model_to_entity(message_model)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar mensagem {message_id}: {str(e)}")
            self._session.rollback()
            raise
    
    async def delete_message(self, message_id: int) -> bool:
        """Remove uma mensagem do repositório."""
        try:
            message_model = self._session.query(MessageModel).filter(
                MessageModel.id == message_id
            ).first()
            
            if not message_model:
                return False
            
            self._session.delete(message_model)
            self._session.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao deletar mensagem {message_id}: {str(e)}")
            self._session.rollback()
            raise
    
    async def start_service(self, message_id: int, responsible_id: int) -> Message:
        """Inicia o atendimento de uma mensagem."""
        try:
            message_model = self._session.query(MessageModel).filter(
                MessageModel.id == message_id
            ).first()
            
            if not message_model:
                raise ValueError(f"Mensagem com ID {message_id} não encontrada")
            
            if message_model.responsible_id is not None:
                raise ValueError("Mensagem já possui responsável atribuído")
            
            if message_model.status != "Pendente":
                raise ValueError(f"Só é possível iniciar atendimento de mensagens com status 'Pendente'")
            
            # Atualizar campos
            message_model.responsible_id = responsible_id
            message_model.service_start_time = datetime.utcnow()
            message_model.status = "Contato iniciado"
            message_model.updated_at = datetime.utcnow()
            
            self._session.commit()
            self._session.refresh(message_model)
            
            return self._model_to_entity(message_model)
            
        except Exception as e:
            logger.error(f"Erro ao iniciar atendimento da mensagem {message_id}: {str(e)}")
            self._session.rollback()
            raise
    
    async def update_status(self, message_id: int, status: str) -> Message:
        """Atualiza o status de uma mensagem."""
        try:
            message_model = self._session.query(MessageModel).filter(
                MessageModel.id == message_id
            ).first()
            
            if not message_model:
                raise ValueError(f"Mensagem com ID {message_id} não encontrada")
            
            # Validar status
            valid_statuses = ["Pendente", "Contato iniciado", "Finalizado", "Cancelado"]
            if status not in valid_statuses:
                raise ValueError(f"Status deve ser um dos valores: {', '.join(valid_statuses)}")
            
            # Atualizar status
            message_model.status = status
            message_model.updated_at = datetime.utcnow()
            
            self._session.commit()
            self._session.refresh(message_model)
            
            return self._model_to_entity(message_model)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar status da mensagem {message_id}: {str(e)}")
            self._session.rollback()
            raise
    
    def _model_to_entity(self, message_model: MessageModel) -> Message:
        """Converte um modelo SQLAlchemy para entidade de domínio."""
        return Message(
            id=message_model.id,
            name=message_model.name,
            email=message_model.email,
            phone=message_model.phone,
            message=message_model.message,
            vehicle_id=message_model.vehicle_id,
            responsible_id=message_model.responsible_id,
            status=message_model.status,
            service_start_time=message_model.service_start_time,
            created_at=message_model.created_at,
            updated_at=message_model.updated_at
        )
