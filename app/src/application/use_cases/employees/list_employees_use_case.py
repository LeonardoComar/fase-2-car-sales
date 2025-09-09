"""
Use Case para Listar Funcionários - Application Layer

Responsável por listar funcionários com filtros e paginação.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela listagem de funcionários
- OCP: Extensível para novos filtros sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para listagem
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import List, Optional
from src.domain.entities.employee import Employee
from src.domain.ports.employee_repository import EmployeeRepository
from src.application.dtos.employee_dto import EmployeeListDto


class ListEmployeesUseCase:
    """
    Use Case para listagem de funcionários com filtros.
    
    Coordena a busca de funcionários aplicando filtros e paginação.
    """
    
    def __init__(self, employee_repository: EmployeeRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            employee_repository: Repositório de funcionários
        """
        self._employee_repository = employee_repository
    
    async def execute(self, skip: int = 0, limit: int = 100, 
                     name: Optional[str] = None, cpf: Optional[str] = None,
                     status: Optional[str] = None) -> List[EmployeeListDto]:
        """
        Executa a listagem de funcionários com filtros.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar
            name: Nome ou parte do nome para filtrar (opcional)
            cpf: CPF exato para buscar (opcional)
            status: Status para filtrar (opcional)
            
        Returns:
            List[EmployeeListDto]: Lista de funcionários
            
        Raises:
            ValueError: Se parâmetros inválidos forem fornecidos
            Exception: Se houver erro na busca
        """
        try:
            # Validar parâmetros
            if skip < 0:
                raise ValueError("Skip deve ser maior ou igual a zero")
            if limit <= 0 or limit > 500:
                raise ValueError("Limit deve estar entre 1 e 500")
            
            # Validar que apenas um tipo de busca seja usado
            search_params = [name, cpf]
            provided_params = [param for param in search_params if param is not None]
            if len(provided_params) > 1:
                raise ValueError("Não é possível usar name e cpf simultaneamente")
            
            employees = []
            
            # Aplicar filtros específicos
            if cpf:
                # Busca por CPF exato
                employee = await self._employee_repository.find_by_cpf(cpf)
                if employee:
                    # Aplicar filtro de status se fornecido
                    if not status or employee.status == status:
                        employees = [employee]
                
            elif name:
                # Busca por nome
                employees = await self._employee_repository.find_by_name(name, skip, limit)
                # Aplicar filtro de status se fornecido
                if status:
                    employees = [emp for emp in employees if emp.status == status]
                
            elif status:
                # Busca por status
                employees = await self._employee_repository.find_by_status(status, skip, limit)
                
            else:
                # Busca todos
                employees = await self._employee_repository.find_all(skip, limit)
            
            # Converter para DTO de listagem
            return [self._convert_to_list_dto(employee) for employee in employees]
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao listar funcionários: {str(e)}")
    
    def _convert_to_list_dto(self, employee: Employee) -> EmployeeListDto:
        """
        Converte entidade Employee para DTO de listagem.
        
        Args:
            employee: Entidade do funcionário
            
        Returns:
            EmployeeListDto: DTO de listagem
        """
        # Buscar cidade do endereço se existir
        city = None
        if employee.address_id and hasattr(self._employee_repository, 'get_address_by_id'):
            address = self._employee_repository.get_address_by_id(employee.address_id)
            if address:
                city = address.city
        
        return EmployeeListDto(
            id=employee.id,
            name=employee.name,
            email=employee.email,
            phone=employee.phone,
            cpf=employee.cpf,
            status=employee.status,
            city=city
        )
