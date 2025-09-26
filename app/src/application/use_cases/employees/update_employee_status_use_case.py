"""
Use Case para Atualização de Status de Funcionário - Application Layer

Responsável por ativar/desativar funcionários aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela atualização de status de funcionários
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para atualização de status
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from src.domain.entities.employee import Employee
from src.domain.ports.employee_repository import EmployeeRepository
from src.application.dtos.employee_dto import EmployeeResponseDto
from src.application.dtos.address_dto import AddressDto


class UpdateEmployeeStatusUseCase:
    """
    Use Case para atualização de status de funcionários.
    
    Coordena a validação e atualização do status de funcionários.
    """
    
    def __init__(self, employee_repository: EmployeeRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            employee_repository: Repositório de funcionários
        """
        self._employee_repository = employee_repository
    
    async def execute(self, employee_id: int, status: str) -> Optional[EmployeeResponseDto]:
        """
        Executa a atualização de status de um funcionário.
        
        Args:
            employee_id: ID do funcionário
            status: Novo status (Ativo/Inativo)
            
        Returns:
            Optional[EmployeeResponseDto]: Dados do funcionário atualizado ou None se não encontrado
            
        Raises:
            ValueError: Se dados inválidos forem fornecidos
            Exception: Se houver erro na atualização
        """
        try:
            if employee_id <= 0:
                raise ValueError("ID do funcionário deve ser maior que zero")
            
            if not Employee.is_valid_status(status):
                raise ValueError(f"Status inválido. Deve ser um de: {', '.join(Employee.VALID_STATUSES)}")
            
            # Buscar funcionário existente
            existing_employee = await self._employee_repository.find_by_id(employee_id)
            if not existing_employee:
                return None
            
            # Atualizar status
            existing_employee.status = status
            
            # Persistir no repositório
            updated_employee = await self._employee_repository.update(employee_id, existing_employee)
            
            if not updated_employee:
                return None
            
            # Buscar endereço se existir
            address = None
            if updated_employee.address_id and hasattr(self._employee_repository, 'get_address_by_id'):
                address = self._employee_repository.get_address_by_id(updated_employee.address_id)
            
            # Converter para DTO de resposta
            return self._convert_to_response_dto(updated_employee, address)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao atualizar status do funcionário: {str(e)}")
    
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
            address_dto = AddressDto(
                id=address.id,
                street=address.street,
                city=address.city,
                state=address.state,
                zip_code=address.zip_code,
                country=address.country
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
