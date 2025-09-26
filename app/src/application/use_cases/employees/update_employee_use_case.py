"""
Use Case para Atualização de Funcionário - Application Layer

Responsável por atualizar funcionários aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela atualização de funcionários
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para atualização
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from src.domain.entities.employee import Employee
from src.domain.entities.address import Address
from src.domain.ports.employee_repository import EmployeeRepository
from src.application.dtos.employee_dto import UpdateEmployeeDto, EmployeeResponseDto
from src.application.dtos.address_dto import AddressResponseDto


class UpdateEmployeeUseCase:
    """
    Use Case para atualização de funcionários.
    
    Coordena a validação de dados, aplicação de regras de negócio
    e atualização de funcionários no sistema.
    """
    
    def __init__(self, employee_repository: EmployeeRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            employee_repository: Repositório de funcionários
        """
        self._employee_repository = employee_repository
    
    async def execute(self, employee_id: int, employee_data: UpdateEmployeeDto) -> Optional[EmployeeResponseDto]:
        """
        Executa a atualização de um funcionário.
        
        Args:
            employee_id: ID do funcionário a ser atualizado
            employee_data: Dados para atualização do funcionário
            
        Returns:
            Optional[EmployeeResponseDto]: Dados do funcionário atualizado ou None se não encontrado
            
        Raises:
            ValueError: Se dados inválidos forem fornecidos
            Exception: Se houver erro na atualização
        """
        try:
            if employee_id <= 0:
                raise ValueError("ID do funcionário deve ser maior que zero")
            
            # Buscar funcionário existente
            existing_employee = await self._employee_repository.find_by_id(employee_id)
            if not existing_employee:
                return None
            
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
            
            # Criar cópia do funcionário para atualização
            updated_employee = Employee(
                id=existing_employee.id,
                name=existing_employee.name,
                email=existing_employee.email,
                phone=existing_employee.phone,
                cpf=existing_employee.cpf,
                status=existing_employee.status,
                address_id=existing_employee.address_id,
                created_at=existing_employee.created_at,
                updated_at=existing_employee.updated_at
            )
            
            # Aplicar atualizações apenas aos campos fornecidos
            updated_employee.update_fields(
                name=employee_data.name,
                email=employee_data.email,
                phone=employee_data.phone,
                cpf=employee_data.cpf,
                status=employee_data.status
            )
            
            # Persistir no repositório
            result_employee = await self._employee_repository.update(employee_id, updated_employee, address)
            
            if not result_employee:
                return None
            
            # Verificar se há dados de endereço anexados
            updated_address = None
            if hasattr(result_employee, '_address_data') and result_employee._address_data:
                from datetime import datetime
                
                addr_data = result_employee._address_data
                updated_address = Address(
                    id=addr_data['id'],
                    street=addr_data['street'],
                    city=addr_data['city'],
                    state=addr_data['state'],
                    zip_code=addr_data['zip_code'],
                    country=addr_data['country'],
                    created_at=addr_data['created_at'],
                    updated_at=addr_data['updated_at']
                )
            
            # Converter para DTO de resposta
            return self._convert_to_response_dto(result_employee, updated_address)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao atualizar funcionário: {str(e)}")
    
    def _convert_to_response_dto(self, employee: Employee, address = None) -> EmployeeResponseDto:
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
