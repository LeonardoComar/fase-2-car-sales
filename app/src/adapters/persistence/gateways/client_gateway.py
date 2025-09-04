from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.domain.entities.client import Client
from src.domain.ports.client_repository import ClientRepository
from src.infrastructure.database.models.client_model import ClientModel
from src.infrastructure.database.connection import get_db_session
import logging

logger = logging.getLogger(__name__)


class ClientGateway(ClientRepository):
    """
    Gateway de persistência para clientes.
    
    Implementa a interface ClientRepository definida no domínio.
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    implementa a abstração definida no domínio.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela persistência de dados de clientes.
    """
    
    def __init__(self):
        pass
    
    async def save(self, client: Client) -> Client:
        """
        Salva um cliente no banco de dados.
        
        Args:
            client: Entidade Client do domínio
            
        Returns:
            Client: Entidade Client salva com ID gerado
            
        Raises:
            Exception: Se houver erro na criação
        """
        try:
            with get_db_session() as session:
                # Converter entidade do domínio para modelo de banco
                client_model = ClientModel(
                    name=client.name,
                    email=client.email,
                    phone=client.phone,
                    cpf=client.cpf,
                    birth_date=client.birth_date,
                    address=client.address,
                    city=client.city,
                    state=client.state,
                    zip_code=client.zip_code,
                    status=client.status,
                    notes=client.notes
                )
                
                session.add(client_model)
                session.commit()
                session.refresh(client_model)
                
                # Converter modelo de banco para entidade do domínio
                saved_client = self._model_to_entity(client_model)
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(client_model)
                
                logger.info(f"Cliente criado com sucesso. ID: {saved_client.id}, Nome: {saved_client.name}")
                return saved_client
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao salvar cliente: {str(e)}")
            raise Exception(f"Erro ao salvar cliente: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao salvar cliente: {str(e)}")
            raise Exception(f"Erro inesperado ao salvar cliente: {str(e)}")
    
    async def update(self, client: Client) -> Client:
        """
        Atualiza um cliente existente.
        
        Args:
            client: Entidade Client do domínio com dados atualizados
            
        Returns:
            Client: Entidade Client atualizada
        """
        try:
            with get_db_session() as session:
                client_model = session.query(ClientModel).filter(ClientModel.id == client.id).first()
                
                if not client_model:
                    raise Exception(f"Cliente com ID {client.id} não encontrado")
                
                # Atualizar dados
                client_model.name = client.name
                client_model.email = client.email
                client_model.phone = client.phone
                client_model.cpf = client.cpf
                client_model.birth_date = client.birth_date
                client_model.address = client.address
                client_model.city = client.city
                client_model.state = client.state
                client_model.zip_code = client.zip_code
                client_model.status = client.status
                client_model.notes = client.notes
                
                session.commit()
                session.refresh(client_model)
                
                # Converter modelo de banco para entidade do domínio
                updated_client = self._model_to_entity(client_model)
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(client_model)
                
                logger.info(f"Cliente atualizado com sucesso. ID: {updated_client.id}")
                return updated_client
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar cliente: {str(e)}")
            raise Exception(f"Erro ao atualizar cliente: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar cliente: {str(e)}")
            raise Exception(f"Erro inesperado ao atualizar cliente: {str(e)}")
    
    async def find_by_id(self, client_id: int) -> Optional[Client]:
        """
        Busca um cliente pelo ID.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            Optional[Client]: Entidade Client encontrada ou None
        """
        try:
            with get_db_session() as session:
                client_model = session.query(ClientModel).filter(ClientModel.id == client_id).first()
                
                if client_model:
                    # Fazer expunge para desconectar o objeto da sessão
                    session.expunge(client_model)
                    return self._model_to_entity(client_model)
                
                return None
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar cliente por ID {client_id}: {str(e)}")
            raise Exception(f"Erro ao buscar cliente: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar cliente por ID {client_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar cliente: {str(e)}")
    
    async def find_by_cpf(self, cpf: str) -> Optional[Client]:
        """
        Busca um cliente pelo CPF.
        
        Args:
            cpf: CPF do cliente
            
        Returns:
            Optional[Client]: Entidade Client encontrada ou None
        """
        try:
            with get_db_session() as session:
                client_model = session.query(ClientModel).filter(ClientModel.cpf == cpf).first()
                
                if client_model:
                    # Fazer expunge para desconectar o objeto da sessão
                    session.expunge(client_model)
                    return self._model_to_entity(client_model)
                
                return None
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar cliente por CPF {cpf}: {str(e)}")
            raise Exception(f"Erro ao buscar cliente: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar cliente por CPF {cpf}: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar cliente: {str(e)}")
    
    async def find_by_email(self, email: str) -> Optional[Client]:
        """
        Busca um cliente pelo email.
        
        Args:
            email: Email do cliente
            
        Returns:
            Optional[Client]: Entidade Client encontrada ou None
        """
        try:
            with get_db_session() as session:
                client_model = session.query(ClientModel).filter(ClientModel.email == email).first()
                
                if client_model:
                    # Fazer expunge para desconectar o objeto da sessão
                    session.expunge(client_model)
                    return self._model_to_entity(client_model)
                
                return None
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar cliente por email {email}: {str(e)}")
            raise Exception(f"Erro ao buscar cliente: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar cliente por email {email}: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar cliente: {str(e)}")
    
    async def find_all(self, limit: int = 100, offset: int = 0) -> List[Client]:
        """
        Busca todos os clientes com paginação.
        
        Args:
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            List[Client]: Lista de entidades Client
        """
        try:
            with get_db_session() as session:
                client_models = session.query(ClientModel).offset(offset).limit(limit).all()
                
                clients = []
                for client_model in client_models:
                    session.expunge(client_model)
                    clients.append(self._model_to_entity(client_model))
                
                return clients
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar todos os clientes: {str(e)}")
            raise Exception(f"Erro ao buscar clientes: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar todos os clientes: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar clientes: {str(e)}")
    
    async def delete(self, client_id: int) -> bool:
        """
        Remove um cliente pelo ID.
        
        Args:
            client_id: ID do cliente
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        try:
            with get_db_session() as session:
                client_model = session.query(ClientModel).filter(ClientModel.id == client_id).first()
                
                if not client_model:
                    return False
                
                session.delete(client_model)
                session.commit()
                
                logger.info(f"Cliente removido com sucesso. ID: {client_id}")
                return True
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao remover cliente {client_id}: {str(e)}")
            raise Exception(f"Erro ao remover cliente: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao remover cliente {client_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao remover cliente: {str(e)}")
    
    async def search(self, filters: Dict[str, Any], limit: int = 50, offset: int = 0) -> Tuple[List[Client], int]:
        """
        Busca clientes com filtros.
        
        Args:
            filters: Dicionário com filtros
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            Tuple[List[Client], int]: Lista de clientes e total de registros
        """
        try:
            with get_db_session() as session:
                query = session.query(ClientModel)
                
                # Aplicar filtros
                if filters.get('name'):
                    query = query.filter(ClientModel.name.ilike(f"%{filters['name']}%"))
                if filters.get('email'):
                    query = query.filter(ClientModel.email.ilike(f"%{filters['email']}%"))
                if filters.get('cpf'):
                    query = query.filter(ClientModel.cpf == filters['cpf'])
                if filters.get('city'):
                    query = query.filter(ClientModel.city.ilike(f"%{filters['city']}%"))
                if filters.get('state'):
                    query = query.filter(ClientModel.state == filters['state'])
                if filters.get('status'):
                    query = query.filter(ClientModel.status == filters['status'])
                
                # Contar total
                total = query.count()
                
                # Aplicar paginação
                client_models = query.offset(offset).limit(limit).all()
                
                clients = []
                for client_model in client_models:
                    session.expunge(client_model)
                    clients.append(self._model_to_entity(client_model))
                
                return clients, total
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar clientes com filtros: {str(e)}")
            raise Exception(f"Erro ao buscar clientes: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar clientes com filtros: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar clientes: {str(e)}")
    
    async def exists_by_cpf(self, cpf: str) -> bool:
        """
        Verifica se existe um cliente com o CPF informado.
        
        Args:
            cpf: CPF a ser verificado
            
        Returns:
            bool: True se existir, False caso contrário
        """
        try:
            client = await self.find_by_cpf(cpf)
            return client is not None
        except Exception as e:
            logger.error(f"Erro ao verificar existência de cliente por CPF {cpf}: {str(e)}")
            return False
    
    async def exists_by_email(self, email: str) -> bool:
        """
        Verifica se existe um cliente com o email informado.
        
        Args:
            email: Email a ser verificado
            
        Returns:
            bool: True se existir, False caso contrário
        """
        try:
            client = await self.find_by_email(email)
            return client is not None
        except Exception as e:
            logger.error(f"Erro ao verificar existência de cliente por email {email}: {str(e)}")
            return False
    
    def _model_to_entity(self, client_model: ClientModel) -> Client:
        """
        Converte modelo de banco para entidade do domínio.
        
        Args:
            client_model: Modelo SQLAlchemy
            
        Returns:
            Client: Entidade do domínio
        """
        return Client(
            id=client_model.id,
            name=client_model.name,
            email=client_model.email,
            phone=client_model.phone,
            cpf=client_model.cpf,
            birth_date=client_model.birth_date,
            address=client_model.address,
            city=client_model.city,
            state=client_model.state,
            zip_code=client_model.zip_code,
            status=client_model.status,
            notes=client_model.notes,
            created_at=client_model.created_at,
            updated_at=client_model.updated_at
        )
