from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.connection import get_db_session
import logging

logger = logging.getLogger(__name__)


class UserGateway(UserRepository):
    """
    Gateway de persistência para usuários.
    
    Implementa a interface UserRepository definida no domínio.
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    implementa a abstração definida no domínio.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela persistência de dados de usuários.
    """
    
    def __init__(self):
        pass
    
    async def create_user(self, user: User) -> User:
        """
        Cria um novo usuário no banco de dados.
        
        Args:
            user: Entidade User do domínio
            
        Returns:
            User: Entidade User criada com ID gerado
            
        Raises:
            Exception: Se houver erro na criação
        """
        try:
            with get_db_session() as session:
                # Converter entidade do domínio para modelo de banco
                user_model = UserModel(
                    email=user.email,
                    password=user.password,
                    role=user.role,
                    employee_id=user.employee_id
                )
                
                session.add(user_model)
                session.commit()
                session.refresh(user_model)
                
                # Converter modelo de banco para entidade do domínio
                created_user = self._model_to_entity(user_model)
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(user_model)
                
                logger.info(f"Usuário criado com sucesso. ID: {created_user.id}, Email: {created_user.email}")
                return created_user
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar usuário: {str(e)}")
            raise Exception(f"Erro ao criar usuário: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao criar usuário: {str(e)}")
            raise Exception(f"Erro inesperado ao criar usuário: {str(e)}")
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca um usuário pelo ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Optional[User]: Entidade User encontrada ou None
        """
        try:
            with get_db_session() as session:
                user_model = session.query(UserModel).filter(UserModel.id == user_id).first()
                
                if user_model:
                    # Fazer expunge para desconectar o objeto da sessão
                    session.expunge(user_model)
                    return self._model_to_entity(user_model)
                
                return None
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar usuário por ID {user_id}: {str(e)}")
            raise Exception(f"Erro ao buscar usuário: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar usuário por ID {user_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar usuário: {str(e)}")
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Busca um usuário pelo email.
        
        Args:
            email: Email do usuário
            
        Returns:
            Optional[User]: Entidade User encontrada ou None
        """
        try:
            with get_db_session() as session:
                user_model = session.query(UserModel).filter(UserModel.email == email).first()
                
                if user_model:
                    # Fazer expunge para desconectar o objeto da sessão
                    session.expunge(user_model)
                    return self._model_to_entity(user_model)
                
                return None
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar usuário por email {email}: {str(e)}")
            raise Exception(f"Erro ao buscar usuário: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar usuário por email {email}: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar usuário: {str(e)}")
    
    async def get_all_users(self) -> List[User]:
        """
        Busca todos os usuários.
        
        Returns:
            List[User]: Lista de entidades User
        """
        try:
            with get_db_session() as session:
                user_models = session.query(UserModel).all()
                
                users = []
                for user_model in user_models:
                    session.expunge(user_model)
                    users.append(self._model_to_entity(user_model))
                
                return users
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar todos os usuários: {str(e)}")
            raise Exception(f"Erro ao buscar usuários: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar todos os usuários: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar usuários: {str(e)}")
    
    async def update_user(self, user_id: int, user: User) -> Optional[User]:
        """
        Atualiza um usuário existente.
        
        Args:
            user_id: ID do usuário
            user: Entidade User com dados atualizados
            
        Returns:
            Optional[User]: Entidade User atualizada ou None se não encontrado
        """
        try:
            with get_db_session() as session:
                user_model = session.query(UserModel).filter(UserModel.id == user_id).first()
                
                if not user_model:
                    return None
                
                # Atualizar campos
                user_model.email = user.email
                user_model.password = user.password
                user_model.role = user.role
                user_model.employee_id = user.employee_id
                
                session.commit()
                session.refresh(user_model)
                
                # Converter para entidade do domínio
                updated_user = self._model_to_entity(user_model)
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(user_model)
                
                logger.info(f"Usuário atualizado com sucesso. ID: {updated_user.id}")
                return updated_user
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar usuário {user_id}: {str(e)}")
            raise Exception(f"Erro ao atualizar usuário: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar usuário {user_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao atualizar usuário: {str(e)}")
    
    async def delete_user(self, user_id: int) -> bool:
        """
        Remove um usuário do banco de dados.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        try:
            with get_db_session() as session:
                user_model = session.query(UserModel).filter(UserModel.id == user_id).first()
                
                if not user_model:
                    return False
                
                session.delete(user_model)
                session.commit()
                
                logger.info(f"Usuário removido com sucesso. ID: {user_id}")
                return True
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao remover usuário {user_id}: {str(e)}")
            raise Exception(f"Erro ao remover usuário: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao remover usuário {user_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao remover usuário: {str(e)}")
    
    async def user_exists_by_email(self, email: str) -> bool:
        """
        Verifica se existe um usuário com o email informado.
        
        Args:
            email: Email a ser verificado
            
        Returns:
            bool: True se existir, False caso contrário
        """
        try:
            user = await self.get_user_by_email(email)
            return user is not None
        except Exception as e:
            logger.error(f"Erro ao verificar existência de usuário por email {email}: {str(e)}")
            return False
    
    def _model_to_entity(self, user_model: UserModel) -> User:
        """
        Converte modelo de banco para entidade do domínio.
        
        Args:
            user_model: Modelo SQLAlchemy
            
        Returns:
            User: Entidade do domínio
        """
        return User(
            id=user_model.id,
            email=user_model.email,
            password=user_model.password,
            role=user_model.role,
            employee_id=user_model.employee_id,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )
