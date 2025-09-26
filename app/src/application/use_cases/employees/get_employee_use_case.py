"""
Use Case para Obter Funcionário - Application Layer

Responsável por buscar funcionários por ID aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela busca de funcionários
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para busca
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from src.domain.entities.employee import Employee
from src.domain.ports.employee_repository import EmployeeRepository
from src.application.dtos.employee_dto import EmployeeResponseDto
from src.application.dtos.address_dto import AddressResponseDto


class GetEmployeeUseCase:
    """
    Use Case para busca de funcionários por ID.
    
    Coordena a busca e conversão de dados de funcionários.
    """
    
    def __init__(self, employee_repository: EmployeeRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            employee_repository: Repositório de funcionários
        """
        self._employee_repository = employee_repository
    
    async def execute(self, employee_id: int) -> Optional[EmployeeResponseDto]:
        """
        Executa a busca de um funcionário por ID.
        
        Args:
            employee_id: ID do funcionário a ser buscado
            
        Returns:
            Optional[EmployeeResponseDto]: Dados do funcionário ou None se não encontrado
            
        Raises:
            ValueError: Se ID inválido for fornecido
            Exception: Se houver erro na busca
        """
        try:
            if employee_id <= 0:
                raise ValueError("ID do funcionário deve ser maior que zero")
            
            # Buscar funcionário no repositório
            employee = await self._employee_repository.find_by_id(employee_id)
            
            if not employee:
                return None
            
            # Verificar se há dados de endereço anexados
            address = None
            if hasattr(employee, '_address_data') and employee._address_data:
                from src.domain.entities.address import Address
                from datetime import datetime
                
                addr_data = employee._address_data
                address = Address(
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
            return self._convert_to_response_dto(employee, address)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao buscar funcionário: {str(e)}")
    
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
