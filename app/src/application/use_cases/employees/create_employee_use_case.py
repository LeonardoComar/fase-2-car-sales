"""
Use Case para Criação de Funcionário - Application Layer

Responsável por coordenar a criação de funcionários aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela criação de funcionários
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para criação
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from src.domain.entities.employee import Employee
from src.domain.entities.address import Address
from src.domain.ports.employee_repository import EmployeeRepository
from src.application.dtos.employee_dto import CreateEmployeeDto, EmployeeResponseDto
from src.application.dtos.address_dto import AddressResponseDto


class CreateEmployeeUseCase:
    """
    Use Case para criação de funcionários.
    
    Coordena a validação de dados, aplicação de regras de negócio
    e persistência de funcionários no sistema.
    """
    
    def __init__(self, employee_repository: EmployeeRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            employee_repository: Repositório de funcionários
        """
        self._employee_repository = employee_repository
    
    async def execute(self, employee_data: CreateEmployeeDto) -> EmployeeResponseDto:
        """
        Executa a criação de um funcionário.
        
        Args:
            employee_data: Dados para criação do funcionário
            
        Returns:
            EmployeeResponseDto: Dados do funcionário criado
            
        Raises:
            ValueError: Se dados inválidos forem fornecidos
            Exception: Se houver erro na criação
        """
        try:
            # Criar entidade de endereço se dados forem fornecidos
            address = None
            if any([employee_data.street, employee_data.city, employee_data.state, 
                   employee_data.zip_code, employee_data.country]):
                address = Address(
                    street=employee_data.street or "",
                    city=employee_data.city or "",
                    state=employee_data.state or "",
                    zip_code=employee_data.zip_code or "",
                    country=employee_data.country or "Brasil"
                )
            
            # Criar entidade de funcionário
            employee = Employee.create_employee(
                name=employee_data.name,
                email=employee_data.email,
                cpf=employee_data.cpf,
                phone=employee_data.phone
            )
            
            # Persistir no repositório
            created_employee = await self._employee_repository.create(employee, address)
            
            # Se foi criado um endereço, buscar as informações completas
            created_address = None
            if created_employee.address_id and address:
                # Usar os dados do endereço criado com o ID retornado
                # Aqui poderíamos buscar do banco, mas como acabamos de criar, 
                # vamos usar os dados que temos e adicionar as informações que faltam
                from datetime import datetime
                created_address = Address(
                    id=created_employee.address_id,
                    street=address.street,
                    city=address.city,
                    state=address.state,
                    zip_code=address.zip_code,
                    country=address.country,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
            
            # Converter para DTO de resposta
            return self._convert_to_response_dto(created_employee, created_address)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao criar funcionário: {str(e)}")
    
    def _convert_to_response_dto(self, employee: Employee, address: Optional[Address] = None) -> EmployeeResponseDto:
        """
        Converte entidade Employee para DTO de resposta.
        
        Args:
            employee: Entidade do funcionário
            address: Entidade do endereço (opcional)
            
        Returns:
            EmployeeResponseDto: DTO de resposta
        """
        address_dto = None
        if address:
            address_dto = AddressResponseDto(
                id=address.id,
                street=address.street,
                city=address.city,
                state=address.state,
                zip_code=address.zip_code,
                country=address.country,
                created_at=address.created_at.isoformat() if address.created_at else None,
                updated_at=address.updated_at.isoformat() if address.updated_at else None,
                full_address=address.get_full_address()
            )
        
        return EmployeeResponseDto(
            id=employee.id,
            name=employee.name,
            email=employee.email,
            phone=employee.phone,
            cpf=employee.cpf,
            status=employee.status,
            address=address_dto,
            created_at=employee.created_at.isoformat() if employee.created_at else None,
            updated_at=employee.updated_at.isoformat() if employee.updated_at else None
        )
