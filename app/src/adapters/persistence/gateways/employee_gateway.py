from typing import List, Optional
import logging
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.domain.entities.employee import Employee
from src.domain.ports.employee_repository import EmployeeRepository
from src.domain.exceptions import EmployeeNotFoundError, EmployeeAlreadyExistsError, DatabaseError
from src.infrastructure.database.models.employee_model import EmployeeModel

logger = logging.getLogger(__name__)


class EmployeeGateway(EmployeeRepository):
    """
    Gateway para persistência de funcionários usando SQLAlchemy.
    
    Implementa o padrão Gateway e Interface Segregation Principle (ISP),
    fornecendo implementação concreta do EmployeeRepository.
    """

    def __init__(self, db_session: Session):
        """
        Inicializa o gateway com uma sessão de banco de dados.
        
        Args:
            db_session: Sessão SQLAlchemy para operações de banco
        """
        self.db_session = db_session

    def create(self, employee: Employee) -> Employee:
        """
        Cria um novo funcionário no banco de dados.
        
        Args:
            employee: Entidade Employee a ser criada
            
        Returns:
            Employee: Entidade criada com ID atribuído
            
        Raises:
            EmployeeAlreadyExistsError: Se funcionário com mesmo CPF já existe
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info(f"Criando funcionário com CPF: {employee.cpf}")
            
            # Verifica se já existe funcionário com mesmo CPF
            existing_employee = self.db_session.query(EmployeeModel).filter_by(cpf=employee.cpf).first()
            if existing_employee:
                raise EmployeeAlreadyExistsError(f"Funcionário com CPF {employee.cpf} já existe")
            
            # Converte entidade para modelo
            employee_model = self._entity_to_model(employee)
            
            # Salva no banco
            self.db_session.add(employee_model)
            self.db_session.commit()
            self.db_session.refresh(employee_model)
            
            logger.info(f"Funcionário criado com sucesso - ID: {employee_model.id}")
            
            # Converte modelo para entidade e retorna
            return self._model_to_entity(employee_model)
            
        except EmployeeAlreadyExistsError:
            self.db_session.rollback()
            raise
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(f"Erro ao criar funcionário: {str(e)}")
            raise DatabaseError(f"Erro ao criar funcionário: {str(e)}")

    def get_by_id(self, employee_id: UUID) -> Optional[Employee]:
        """
        Busca funcionário por ID.
        
        Args:
            employee_id: UUID do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
            
        Raises:
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info(f"Buscando funcionário por ID: {employee_id}")
            
            employee_model = self.db_session.query(EmployeeModel).filter_by(id=employee_id).first()
            
            if employee_model:
                logger.info(f"Funcionário encontrado: {employee_model.name}")
                return self._model_to_entity(employee_model)
            
            logger.info(f"Funcionário não encontrado para ID: {employee_id}")
            return None
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar funcionário por ID: {str(e)}")
            raise DatabaseError(f"Erro ao buscar funcionário: {str(e)}")

    def get_by_cpf(self, cpf: str) -> Optional[Employee]:
        """
        Busca funcionário por CPF.
        
        Args:
            cpf: CPF do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
            
        Raises:
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info(f"Buscando funcionário por CPF: {cpf}")
            
            employee_model = self.db_session.query(EmployeeModel).filter_by(cpf=cpf).first()
            
            if employee_model:
                logger.info(f"Funcionário encontrado: {employee_model.name}")
                return self._model_to_entity(employee_model)
            
            logger.info(f"Funcionário não encontrado para CPF: {cpf}")
            return None
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar funcionário por CPF: {str(e)}")
            raise DatabaseError(f"Erro ao buscar funcionário: {str(e)}")

    def get_by_email(self, email: str) -> Optional[Employee]:
        """
        Busca funcionário por email.
        
        Args:
            email: Email do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
            
        Raises:
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info(f"Buscando funcionário por email: {email}")
            
            employee_model = self.db_session.query(EmployeeModel).filter_by(email=email).first()
            
            if employee_model:
                logger.info(f"Funcionário encontrado: {employee_model.name}")
                return self._model_to_entity(employee_model)
            
            logger.info(f"Funcionário não encontrado para email: {email}")
            return None
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar funcionário por email: {str(e)}")
            raise DatabaseError(f"Erro ao buscar funcionário: {str(e)}")

    def update(self, employee: Employee) -> Employee:
        """
        Atualiza um funcionário existente.
        
        Args:
            employee: Entidade Employee com dados atualizados
            
        Returns:
            Employee: Entidade atualizada
            
        Raises:
            EmployeeNotFoundError: Se funcionário não existe
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info(f"Atualizando funcionário com ID: {employee.id}")
            
            # Busca funcionário existente
            employee_model = self.db_session.query(EmployeeModel).filter_by(id=employee.id).first()
            if not employee_model:
                raise EmployeeNotFoundError(f"Funcionário com ID {employee.id} não encontrado")
            
            # Atualiza campos
            employee_model.name = employee.name
            employee_model.email = employee.email
            employee_model.phone = employee.phone
            employee_model.department = employee.department
            employee_model.position = employee.position
            employee_model.salary = employee.salary
            employee_model.hire_date = employee.hire_date
            employee_model.is_active = employee.is_active
            
            # Salva alterações
            self.db_session.commit()
            self.db_session.refresh(employee_model)
            
            logger.info(f"Funcionário atualizado com sucesso - ID: {employee.id}")
            
            return self._model_to_entity(employee_model)
            
        except EmployeeNotFoundError:
            self.db_session.rollback()
            raise
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(f"Erro ao atualizar funcionário: {str(e)}")
            raise DatabaseError(f"Erro ao atualizar funcionário: {str(e)}")

    def delete(self, employee_id: UUID) -> bool:
        """
        Remove um funcionário do banco de dados.
        
        Args:
            employee_id: UUID do funcionário
            
        Returns:
            bool: True se removido com sucesso, False se não encontrado
            
        Raises:
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info(f"Removendo funcionário com ID: {employee_id}")
            
            employee_model = self.db_session.query(EmployeeModel).filter_by(id=employee_id).first()
            if not employee_model:
                logger.info(f"Funcionário não encontrado para remoção - ID: {employee_id}")
                return False
            
            self.db_session.delete(employee_model)
            self.db_session.commit()
            
            logger.info(f"Funcionário removido com sucesso - ID: {employee_id}")
            return True
            
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(f"Erro ao remover funcionário: {str(e)}")
            raise DatabaseError(f"Erro ao remover funcionário: {str(e)}")

    def list_all(self) -> List[Employee]:
        """
        Lista todos os funcionários.
        
        Returns:
            List[Employee]: Lista de todos os funcionários
            
        Raises:
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info("Listando todos os funcionários")
            
            employee_models = self.db_session.query(EmployeeModel).all()
            employees = [self._model_to_entity(model) for model in employee_models]
            
            logger.info(f"Encontrados {len(employees)} funcionários")
            return employees
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar funcionários: {str(e)}")
            raise DatabaseError(f"Erro ao listar funcionários: {str(e)}")

    def search(self, department: Optional[str] = None, position: Optional[str] = None,
               is_active: Optional[bool] = None) -> List[Employee]:
        """
        Busca funcionários com filtros opcionais.
        
        Args:
            department: Filtrar por departamento
            position: Filtrar por cargo
            is_active: Filtrar por status ativo
            
        Returns:
            List[Employee]: Lista de funcionários encontrados
            
        Raises:
            DatabaseError: Se houver erro na operação de banco
        """
        try:
            logger.info(f"Buscando funcionários - Department: {department}, Position: {position}, Active: {is_active}")
            
            query = self.db_session.query(EmployeeModel)
            
            if department:
                query = query.filter(EmployeeModel.department.ilike(f"%{department}%"))
            
            if position:
                query = query.filter(EmployeeModel.position.ilike(f"%{position}%"))
                
            if is_active is not None:
                query = query.filter(EmployeeModel.is_active == is_active)
            
            employee_models = query.all()
            employees = [self._model_to_entity(model) for model in employee_models]
            
            logger.info(f"Encontrados {len(employees)} funcionários com os filtros aplicados")
            return employees
            
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar funcionários com filtros: {str(e)}")
            raise DatabaseError(f"Erro ao buscar funcionários: {str(e)}")

    def _entity_to_model(self, employee: Employee) -> EmployeeModel:
        """
        Converte entidade Employee para modelo EmployeeModel.
        
        Args:
            employee: Entidade Employee
            
        Returns:
            EmployeeModel: Modelo para persistência
        """
        return EmployeeModel(
            id=employee.id,
            name=employee.name,
            email=employee.email,
            cpf=employee.cpf,
            phone=employee.phone,
            department=employee.department,
            position=employee.position,
            salary=employee.salary,
            hire_date=employee.hire_date,
            is_active=employee.is_active
        )

    def _model_to_entity(self, model: EmployeeModel) -> Employee:
        """
        Converte modelo EmployeeModel para entidade Employee.
        
        Args:
            model: Modelo EmployeeModel
            
        Returns:
            Employee: Entidade de domínio
        """
        return Employee(
            id=model.id,
            name=model.name,
            email=model.email,
            cpf=model.cpf,
            phone=model.phone,
            department=model.department,
            position=model.position,
            salary=model.salary,
            hire_date=model.hire_date,
            is_active=model.is_active
        )
