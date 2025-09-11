from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.domain.entities.client import Client
from src.domain.entities.address import Address
from src.domain.ports.client_repository import ClientRepository
from src.infrastructure.database.models.client_model import ClientModel
from src.infrastructure.database.models.address_model import AddressModel
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
    
    async def create(self, client: Client, address: Optional[Address] = None) -> Client:
        """
        Cria um novo cliente no banco de dados.
        
        Args:
            client: Entidade Client do domínio
            address: Dados do endereço (opcional)
            
        Returns:
            Client: Entidade Client criada com ID gerado
            
        Raises:
            Exception: Se houver erro na criação
        """
        try:
            with get_db_session() as session:
                address_id = None
                
                # Criar endereço se fornecido
                if address:
                    address_model = AddressModel(
                        street=address.street,
                        city=address.city,
                        state=address.state,
                        zip_code=address.zip_code,
                        country=address.country
                    )
                    session.add(address_model)
                    session.flush()  # Para obter o ID do endereço
                    address_id = address_model.id
                
                # Converter entidade do domínio para modelo de banco
                client_model = ClientModel(
                    name=client.name,
                    email=client.email,
                    phone=client.phone,
                    cpf=client.cpf,
                    address_id=address_id
                )
                
                session.add(client_model)
                session.commit()
                session.refresh(client_model)
                
                # Converter modelo de banco para entidade do domínio
                created_client = self._model_to_entity(client_model)
                
                # Se o endereço foi criado, atualizar a entidade Client com o address_id
                if address_id:
                    created_client.address_id = address_id
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(client_model)
                
                logger.info(f"Cliente criado com sucesso. ID: {created_client.id}, Nome: {created_client.name}")
                return created_client
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar cliente: {str(e)}")
            raise Exception(f"Erro ao criar cliente: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao criar cliente: {str(e)}")
            raise Exception(f"Erro inesperado ao criar cliente: {str(e)}")
    
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
    
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Client]:
        """
        Busca todos os clientes com paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            List[Client]: Lista de entidades Client
        """
        try:
            with get_db_session() as session:
                client_models = session.query(ClientModel).offset(skip).limit(limit).all()
                
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
    
    async def find_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Client]:
        """
        Busca clientes por nome (busca parcial).
        
        Args:
            name: Nome ou parte do nome para buscar
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            
        Returns:
            List[Client]: Lista de clientes encontrados
        """
        try:
            with get_db_session() as session:
                client_models = session.query(ClientModel).filter(
                    ClientModel.name.ilike(f"%{name}%")
                ).offset(skip).limit(limit).all()
                
                clients = []
                for client_model in client_models:
                    session.expunge(client_model)
                    clients.append(self._model_to_entity(client_model))
                
                return clients
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar clientes por nome {name}: {str(e)}")
            raise Exception(f"Erro ao buscar clientes: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar clientes por nome {name}: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar clientes: {str(e)}")
    
    async def update(self, client_id: int, client: Client, address: Optional[Address] = None) -> Optional[Client]:
        """
        Atualiza um cliente existente.
        
        Args:
            client_id: ID do cliente
            client: Entidade Client com dados atualizados
            address: Dados atualizados do endereço (opcional)
            
        Returns:
            Optional[Client]: Entidade Client atualizada ou None se não encontrado
        """
        try:
            with get_db_session() as session:
                client_model = session.query(ClientModel).filter(ClientModel.id == client_id).first()
                
                if not client_model:
                    return None
                
                # Atualizar endereço se fornecido
                address_id = client_model.address_id
                if address:
                    if address_id:
                        # Atualizar endereço existente
                        address_model = session.query(AddressModel).filter(AddressModel.id == address_id).first()
                        if address_model:
                            address_model.street = address.street
                            address_model.city = address.city
                            address_model.state = address.state
                            address_model.zip_code = address.zip_code
                            address_model.country = address.country
                    else:
                        # Criar novo endereço
                        address_model = AddressModel(
                            street=address.street,
                            city=address.city,
                            state=address.state,
                            zip_code=address.zip_code,
                            country=address.country
                        )
                        session.add(address_model)
                        session.flush()  # Para obter o ID do endereço
                        address_id = address_model.id
                
                # Atualizar campos do cliente
                client_model.name = client.name
                client_model.email = client.email
                client_model.phone = client.phone
                client_model.cpf = client.cpf
                client_model.address_id = address_id
                
                session.commit()
                session.refresh(client_model)
                
                # Converter para entidade do domínio
                updated_client = self._model_to_entity(client_model)
                
                # Fazer expunge para desconectar o objeto da sessão
                session.expunge(client_model)
                
                logger.info(f"Cliente atualizado com sucesso. ID: {updated_client.id}")
                return updated_client
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar cliente {client_id}: {str(e)}")
            raise Exception(f"Erro ao atualizar cliente: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao atualizar cliente {client_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao atualizar cliente: {str(e)}")
    
    async def delete(self, client_id: int) -> bool:
        """
        Remove um cliente do banco de dados.
        
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
            address_id=client_model.address_id,
            created_at=client_model.created_at,
            updated_at=client_model.updated_at
        )
    
    async def get_address_by_id(self, address_id: int) -> Optional[Address]:
        """
        Busca um endereço pelo ID.
        
        Args:
            address_id: ID do endereço
            
        Returns:
            Optional[Address]: Entidade Address encontrada ou None
        """
        try:
            with get_db_session() as session:
                address_model = session.query(AddressModel).filter(AddressModel.id == address_id).first()
                
                if address_model:
                    # Fazer expunge para desconectar o objeto da sessão
                    session.expunge(address_model)
                    return self._address_model_to_entity(address_model)
                
                return None
                
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar endereço por ID {address_id}: {str(e)}")
            raise Exception(f"Erro ao buscar endereço: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar endereço por ID {address_id}: {str(e)}")
            raise Exception(f"Erro inesperado ao buscar endereço: {str(e)}")
    
    def _address_model_to_entity(self, address_model: AddressModel) -> Address:
        """
        Converte modelo de endereço para entidade do domínio.
        
        Args:
            address_model: Modelo SQLAlchemy do endereço
            
        Returns:
            Address: Entidade do domínio
        """
        return Address(
            id=address_model.id,
            street=address_model.street,
            city=address_model.city,
            state=address_model.state,
            zip_code=address_model.zip_code,
            country=address_model.country,
            created_at=address_model.created_at,
            updated_at=address_model.updated_at
        )
