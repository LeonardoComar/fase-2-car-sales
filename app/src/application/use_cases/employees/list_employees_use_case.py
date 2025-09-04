from typing import List

from src.application.dtos.employee_dto import EmployeeSearchDto, EmployeeResponseDto
from src.domain.entities.employee import Employee
from src.domain.ports.employee_repository import EmployeeRepository
from src.domain.exceptions import ValidationError


class ListEmployeesUseCase:
    """
    Use case para listagem de funcionários com filtros e paginação.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela listagem e busca de funcionários.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração EmployeeRepository, não da implementação.
    """
    
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository
    
    async def execute(self, search_criteria: EmployeeSearchDto) -> List[EmployeeResponseDto]:
        """
        Executa a listagem de funcionários com filtros.
        
        Args:
            search_criteria: Critérios de busca e filtros
            
        Returns:
            List[EmployeeResponseDto]: Lista de funcionários encontrados
            
        Raises:
            ValidationError: Se os critérios de busca forem inválidos
        """
        try:
            # Validar critérios de busca
            self._validate_search_criteria(search_criteria)
            
            # Preparar parâmetros de busca
            search_params = self._prepare_search_params(search_criteria)
            
            # Buscar no repositório
            employees = await self.employee_repository.find_by_criteria(**search_params)
            
            # Converter para DTOs de resposta
            return [self._to_response_dto(employee) for employee in employees]
            
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Erro durante busca de funcionários: {str(e)}")
    
    def _validate_search_criteria(self, search_criteria: EmployeeSearchDto) -> None:
        """
        Valida os critérios de busca.
        
        Args:
            search_criteria: Critérios de busca
            
        Raises:
            ValidationError: Se os critérios forem inválidos
        """
        # Validar limite de resultados
        if search_criteria.limit and search_criteria.limit > 1000:
            raise ValidationError("Limite máximo de 1000 resultados por consulta")
        
        # Validar offset
        if search_criteria.offset and search_criteria.offset < 0:
            raise ValidationError("Offset não pode ser negativo")
        
        # Validar faixa salarial
        if search_criteria.min_salary and search_criteria.min_salary < 0:
            raise ValidationError("Salário mínimo não pode ser negativo")
        
        if search_criteria.max_salary and search_criteria.max_salary < 0:
            raise ValidationError("Salário máximo não pode ser negativo")
        
        if (search_criteria.min_salary and search_criteria.max_salary and 
            search_criteria.min_salary > search_criteria.max_salary):
            raise ValidationError("Salário mínimo não pode ser maior que salário máximo")
        
        # Validar faixa de anos de serviço
        if search_criteria.min_years_service and search_criteria.min_years_service < 0:
            raise ValidationError("Anos mínimos de serviço não podem ser negativos")
        
        if search_criteria.max_years_service and search_criteria.max_years_service < 0:
            raise ValidationError("Anos máximos de serviço não podem ser negativos")
        
        if (search_criteria.min_years_service and search_criteria.max_years_service and 
            search_criteria.min_years_service > search_criteria.max_years_service):
            raise ValidationError("Anos mínimos de serviço não podem ser maiores que anos máximos")
    
    def _prepare_search_params(self, search_criteria: EmployeeSearchDto) -> dict:
        """
        Prepara os parâmetros para busca no repositório.
        
        Args:
            search_criteria: Critérios de busca
            
        Returns:
            dict: Parâmetros preparados para o repositório
        """
        params = {}
        
        # Filtros de texto
        if search_criteria.name:
            params['name'] = search_criteria.name
        
        if search_criteria.email:
            params['email'] = search_criteria.email
        
        if search_criteria.phone:
            params['phone'] = self._clean_phone(search_criteria.phone)
        
        if search_criteria.cpf:
            params['cpf'] = self._clean_cpf(search_criteria.cpf)
        
        if search_criteria.position:
            params['position'] = search_criteria.position
        
        if search_criteria.department:
            params['department'] = search_criteria.department
        
        if search_criteria.employee_id:
            params['employee_id'] = search_criteria.employee_id
        
        # Filtros de localização
        if search_criteria.city:
            params['city'] = search_criteria.city
        
        if search_criteria.state:
            params['state'] = search_criteria.state
        
        if search_criteria.zip_code:
            params['zip_code'] = self._clean_zip_code(search_criteria.zip_code)
        
        # Filtros hierárquicos
        if search_criteria.manager_id:
            params['manager_id'] = search_criteria.manager_id
        
        # Filtros de status
        if search_criteria.status:
            params['status'] = search_criteria.status
        
        if search_criteria.active_only is not None:
            params['active_only'] = search_criteria.active_only
        
        # Filtros de salário
        if search_criteria.min_salary is not None:
            params['min_salary'] = search_criteria.min_salary
        
        if search_criteria.max_salary is not None:
            params['max_salary'] = search_criteria.max_salary
        
        # Filtros de tempo de serviço
        if search_criteria.min_years_service is not None:
            params['min_years_service'] = search_criteria.min_years_service
        
        if search_criteria.max_years_service is not None:
            params['max_years_service'] = search_criteria.max_years_service
        
        # Filtros especiais
        if search_criteria.managers_only is not None:
            params['managers_only'] = search_criteria.managers_only
        
        # Paginação
        if search_criteria.limit is not None:
            params['limit'] = search_criteria.limit
        
        if search_criteria.offset is not None:
            params['offset'] = search_criteria.offset
        
        # Ordenação
        if search_criteria.order_by:
            params['order_by'] = search_criteria.order_by
        
        if search_criteria.order_direction:
            params['order_direction'] = search_criteria.order_direction
        
        return params
    
    def _clean_phone(self, phone: str) -> str:
        """
        Remove formatação do telefone.
        
        Args:
            phone: Telefone com ou sem formatação
            
        Returns:
            str: Telefone apenas com números
        """
        return ''.join(filter(str.isdigit, phone))
    
    def _clean_cpf(self, cpf: str) -> str:
        """
        Remove formatação do CPF.
        
        Args:
            cpf: CPF com ou sem formatação
            
        Returns:
            str: CPF apenas com números
        """
        return ''.join(filter(str.isdigit, cpf))
    
    def _clean_zip_code(self, zip_code: str) -> str:
        """
        Remove formatação do CEP.
        
        Args:
            zip_code: CEP com ou sem formatação
            
        Returns:
            str: CEP apenas com números
        """
        return ''.join(filter(str.isdigit, zip_code))
    
    def _to_response_dto(self, employee: Employee) -> EmployeeResponseDto:
        """
        Converte entidade de domínio para DTO de resposta.
        
        Args:
            employee: Entidade de funcionário
            
        Returns:
            EmployeeResponseDto: DTO de resposta
        """
        return EmployeeResponseDto(
            id=employee.id,
            name=employee.name,
            email=employee.email,
            phone=employee.phone,
            cpf=employee.cpf,
            birth_date=employee.birth_date,
            position=employee.position,
            department=employee.department,
            salary=employee.salary,
            hire_date=employee.hire_date,
            manager_id=employee.manager_id,
            employee_id=employee.employee_id,
            address=employee.address,
            city=employee.city,
            state=employee.state,
            zip_code=employee.zip_code,
            emergency_contact_name=employee.emergency_contact_name,
            emergency_contact_phone=employee.emergency_contact_phone,
            status=employee.status,
            notes=employee.notes,
            # Dados calculados
            age=employee.get_age(),
            years_of_service=employee.get_years_of_service(),
            formatted_cpf=employee.get_formatted_cpf(),
            formatted_phone=employee.get_formatted_phone(),
            formatted_zip_code=employee.get_formatted_zip_code(),
            full_address=employee.get_full_address(),
            display_name=employee.get_display_name(),
            formatted_salary=employee.get_formatted_salary(),
            is_manager=employee.is_manager(),
            is_senior=employee.is_senior(),
            can_approve_expenses=employee.can_approve_expenses(),
            needs_performance_review=employee.needs_performance_review(),
            # Auditoria
            created_at=employee.created_at,
            updated_at=employee.updated_at
        )
