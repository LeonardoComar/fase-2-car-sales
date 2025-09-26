"""
EmployeeGateway - Infrastructure Layer

Gateway para persistência de funcionários usando SQLAlchemy.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela persistência de funcionários
- OCP: Extensível para novas operações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para operações de funcionários
- DIP: Depende de abstrações (EmployeeRepository) não de implementações
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from src.domain.entities.employee import Employee
from src.domain.entities.address import Address
from src.domain.ports.employee_repository import EmployeeRepository
from src.infrastructure.database.models.employee_model import EmployeeModel
from src.infrastructure.database.models.address_model import AddressModel


class EmployeeGateway(EmployeeRepository):
    """
    Gateway para persistência de funcionários no banco de dados.
    
    Implementa a interface EmployeeRepository usando SQLAlchemy.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa o gateway com uma sessão do banco de dados.
        
        Args:
            session: Sessão SQLAlchemy para operações no banco
        """
        self._session = session
    
    async def create(self, employee: Employee, address: Optional[Address] = None) -> Employee:
        """
        Cria um novo funcionário no banco de dados.
        
        Args:
            employee: Entidade funcionário para criar
            address: Endereço opcional
            
        Returns:
            Employee: Funcionário criado com ID atribuído
        """
        try:
            address_id = None
            
            # Criar endereço primeiro se fornecido
            if address:
                address_model = AddressModel(
                    street=address.street,
                    city=address.city,
                    state=address.state,
                    zip_code=address.zip_code,
                    country=address.country
                )
                
                self._session.add(address_model)
                self._session.flush()  # Para obter o ID sem fazer commit completo
                address_id = address_model.id
            
            # Criar funcionário com o address_id
            employee_model = EmployeeModel(
                name=employee.name,
                email=employee.email,
                phone=employee.phone,
                cpf=employee.cpf,
                status=employee.status,
                address_id=address_id
            )
            
            self._session.add(employee_model)
            self._session.commit()
            self._session.refresh(employee_model)
            
            return self._model_to_entity(employee_model)
            
        except Exception as e:
            self._session.rollback()
            raise Exception(f"Erro ao criar funcionário: {str(e)}")
    
    async def find_by_id(self, employee_id: int) -> Optional[Employee]:
        """
        Busca um funcionário pelo ID.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
        """
        query = self._session.query(EmployeeModel).filter(EmployeeModel.id == employee_id)
        employee_model = query.first()
        
        if not employee_model:
            return None
        
        # Buscar endereço se existir
        address_model = None
        if employee_model.address_id:
            address_model = self._session.query(AddressModel).filter(
                AddressModel.id == employee_model.address_id
            ).first()
        
        return self._model_to_entity(employee_model, address_model)
    
    async def update(self, employee_id: int, employee: Employee, address: Optional[Address] = None) -> Optional[Employee]:
        """
        Atualiza um funcionário no banco de dados.
        
        Args:
            employee_id: ID do funcionário
            employee: Entidade funcionário para atualizar
            address: Endereço opcional
            
        Returns:
            Optional[Employee]: Funcionário atualizado ou None se não encontrado
        """
        try:
            employee_model = self._session.query(EmployeeModel).filter(
                EmployeeModel.id == employee_id
            ).first()
            
            if not employee_model:
                return None
            
            # Atualizar dados do funcionário
            employee_model.name = employee.name
            employee_model.email = employee.email
            employee_model.phone = employee.phone
            employee_model.cpf = employee.cpf
            employee_model.status = employee.status
            
            # Lidar com atualização do endereço
            updated_address_model = None
            if address:
                if employee_model.address_id:
                    # Atualizar endereço existente
                    address_model = self._session.query(AddressModel).filter(
                        AddressModel.id == employee_model.address_id
                    ).first()
                    
                    if address_model:
                        address_model.street = address.street
                        address_model.city = address.city
                        address_model.state = address.state
                        address_model.zip_code = address.zip_code
                        address_model.country = address.country
                        updated_address_model = address_model
                else:
                    # Criar novo endereço
                    address_model = AddressModel(
                        street=address.street,
                        city=address.city,
                        state=address.state,
                        zip_code=address.zip_code,
                        country=address.country
                    )
                    
                    self._session.add(address_model)
                    self._session.flush()  # Para obter o ID
                    employee_model.address_id = address_model.id
                    updated_address_model = address_model
            
            self._session.commit()
            self._session.refresh(employee_model)
            
            return self._model_to_entity(employee_model, updated_address_model)
            
        except Exception as e:
            self._session.rollback()
            raise Exception(f"Erro ao atualizar funcionário: {str(e)}")
    
    async def delete(self, employee_id: int) -> bool:
        """
        Remove um funcionário do banco de dados.
        
        Args:
            employee_id: ID do funcionário
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        employee_model = self._session.query(EmployeeModel).filter(
            EmployeeModel.id == employee_id
        ).first()
        
        if not employee_model:
            return False
        
        self._session.delete(employee_model)
        self._session.commit()
        return True
    
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """
        Lista todos os funcionários com paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Limite de registros para retornar
            
        Returns:
            List[Employee]: Lista de funcionários
        """
        # Query com LEFT JOIN para buscar funcionários e seus endereços
        query = self._session.query(EmployeeModel).offset(skip).limit(limit)
        employee_models = query.all()
        
        employees = []
        for employee_model in employee_models:
            # Buscar endereço se existir
            address_model = None
            if employee_model.address_id:
                address_model = self._session.query(AddressModel).filter(
                    AddressModel.id == employee_model.address_id
                ).first()
            
            employees.append(self._model_to_entity(employee_model, address_model))
        
        return employees
    
    async def find_by_email(self, email: str) -> Optional[Employee]:
        """
        Busca funcionário pelo email.
        
        Args:
            email: Email do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
        """
        employee_model = self._session.query(EmployeeModel).filter(
            EmployeeModel.email == email
        ).first()
        
        if not employee_model:
            return None
            
        # Buscar endereço se existir
        address_model = None
        if employee_model.address_id:
            address_model = self._session.query(AddressModel).filter(
                AddressModel.id == employee_model.address_id
            ).first()
        
        return self._model_to_entity(employee_model, address_model)
    
    async def find_by_cpf(self, cpf: str) -> Optional[Employee]:
        """
        Busca funcionário pelo CPF.
        
        Args:
            cpf: CPF do funcionário
            
        Returns:
            Optional[Employee]: Funcionário encontrado ou None
        """
        employee_model = self._session.query(EmployeeModel).filter(
            EmployeeModel.cpf == cpf
        ).first()
        
        if not employee_model:
            return None
            
        # Buscar endereço se existir
        address_model = None
        if employee_model.address_id:
            address_model = self._session.query(AddressModel).filter(
                AddressModel.id == employee_model.address_id
            ).first()
        
        return self._model_to_entity(employee_model, address_model)
    
    async def find_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Employee]:
        """
        Busca funcionários pelo status.
        
        Args:
            status: Status dos funcionários
            skip: Número de registros para pular
            limit: Limite de registros para retornar
            
        Returns:
            List[Employee]: Lista de funcionários com o status especificado
        """
        query = self._session.query(EmployeeModel).filter(
            EmployeeModel.status == status
        ).offset(skip).limit(limit)
        
        employee_models = query.all()
        
        employees = []
        for employee_model in employee_models:
            # Buscar endereço se existir
            address_model = None
            if employee_model.address_id:
                address_model = self._session.query(AddressModel).filter(
                    AddressModel.id == employee_model.address_id
                ).first()
            
            employees.append(self._model_to_entity(employee_model, address_model))
        
        return employees
    
    async def find_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Employee]:
        """
        Busca funcionários por nome (busca parcial).
        
        Args:
            name: Nome ou parte do nome para buscar
            skip: Número de registros para pular
            limit: Limite de registros para retornar
            
        Returns:
            List[Employee]: Lista de funcionários encontrados
        """
        query = self._session.query(EmployeeModel).filter(
            EmployeeModel.name.ilike(f"%{name}%")
        ).offset(skip).limit(limit)
        
        employee_models = query.all()
        
        employees = []
        for employee_model in employee_models:
            # Buscar endereço se existir
            address_model = None
            if employee_model.address_id:
                address_model = self._session.query(AddressModel).filter(
                    AddressModel.id == employee_model.address_id
                ).first()
            
            employees.append(self._model_to_entity(employee_model, address_model))
        
        return employees
    
    def _model_to_entity(self, model: EmployeeModel, address_model: Optional[AddressModel] = None) -> Employee:
        """
        Converte um modelo SQLAlchemy para entidade de domínio.
        
        Args:
            model: Modelo SQLAlchemy do funcionário
            address_model: Modelo SQLAlchemy do endereço (opcional)
            
        Returns:
            Employee: Entidade de domínio
        """
        employee = Employee(
            id=model.id,
            name=model.name or "",
            email=model.email or "",
            phone=model.phone or "",
            cpf=model.cpf or "",
            status=model.status or "Ativo",
            address_id=model.address_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
        
        # Adicionar informações do endereço se disponível (para uso no use case)
        if address_model:
            employee._address_data = {
                'id': address_model.id,
                'street': address_model.street,
                'city': address_model.city,
                'state': address_model.state,
                'zip_code': address_model.zip_code,
                'country': address_model.country,
                'created_at': address_model.created_at,
                'updated_at': address_model.updated_at
            }
        
        return employee
