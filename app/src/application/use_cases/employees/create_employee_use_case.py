from src.application.dtos.employee_dto import EmployeeCreateDto, EmployeeResponseDto
from src.domain.entities.employee import Employee
from src.domain.ports.employee_repository import EmployeeRepository
from src.domain.exceptions import ValidationError, BusinessRuleError, DuplicateError


class CreateEmployeeUseCase:
    """
    Use case para criação de funcionários.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela criação de funcionários.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração EmployeeRepository, não da implementação.
    """
    
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository
    
    async def execute(self, employee_data: EmployeeCreateDto) -> EmployeeResponseDto:
        """
        Executa a criação de um novo funcionário.
        
        Args:
            employee_data: Dados do funcionário a ser criado
            
        Returns:
            EmployeeResponseDto: Dados do funcionário criado
            
        Raises:
            ValidationError: Se os dados não forem válidos
            BusinessRuleError: Se as regras de negócio não forem atendidas
            DuplicateError: Se já existir funcionário com CPF, email ou ID interno
        """
        try:
            # Validar se CPF já existe
            await self._validate_unique_cpf(employee_data.cpf)
            
            # Validar se email já existe
            await self._validate_unique_email(employee_data.email)
            
            # Validar se ID interno já existe (se fornecido)
            if employee_data.employee_id:
                await self._validate_unique_employee_id(employee_data.employee_id)
            
            # Validar se gerente existe (se fornecido)
            if employee_data.manager_id:
                await self._validate_manager_exists(employee_data.manager_id)
            
            # Criar a entidade de domínio
            employee = Employee.create_employee(
                name=employee_data.name,
                email=employee_data.email,
                phone=employee_data.phone,
                cpf=employee_data.cpf,
                birth_date=employee_data.birth_date,
                position=employee_data.position,
                department=employee_data.department,
                salary=employee_data.salary,
                hire_date=employee_data.hire_date,
                manager_id=employee_data.manager_id,
                employee_id=employee_data.employee_id,
                address=employee_data.address,
                city=employee_data.city,
                state=employee_data.state,
                zip_code=employee_data.zip_code,
                emergency_contact_name=employee_data.emergency_contact_name,
                emergency_contact_phone=employee_data.emergency_contact_phone,
                notes=employee_data.notes
            )
            
            # Validações adicionais de negócio
            await self._validate_business_rules(employee)
            
            # Salvar no repositório
            saved_employee = await self.employee_repository.save(employee)
            
            # Converter para DTO de resposta
            return self._to_response_dto(saved_employee)
            
        except ValidationError:
            raise
        except BusinessRuleError:
            raise
        except DuplicateError:
            raise
        except Exception as e:
            raise ValidationError(f"Erro interno durante criação do funcionário: {str(e)}")
    
    async def _validate_unique_cpf(self, cpf: str) -> None:
        """
        Valida se o CPF é único.
        
        Args:
            cpf: CPF a ser validado
            
        Raises:
            DuplicateError: Se CPF já existir
        """
        if await self.employee_repository.exists_by_cpf(cpf):
            raise DuplicateError("Funcionário", "CPF", cpf)
    
    async def _validate_unique_email(self, email: str) -> None:
        """
        Valida se o email é único.
        
        Args:
            email: Email a ser validado
            
        Raises:
            DuplicateError: Se email já existir
        """
        if await self.employee_repository.exists_by_email(email):
            raise DuplicateError("Funcionário", "email", email)
    
    async def _validate_unique_employee_id(self, employee_id: str) -> None:
        """
        Valida se o ID interno é único.
        
        Args:
            employee_id: ID interno a ser validado
            
        Raises:
            DuplicateError: Se ID interno já existir
        """
        if await self.employee_repository.exists_by_employee_id(employee_id):
            raise DuplicateError("Funcionário", "ID interno", employee_id)
    
    async def _validate_manager_exists(self, manager_id) -> None:
        """
        Valida se o gerente existe.
        
        Args:
            manager_id: ID do gerente
            
        Raises:
            ValidationError: Se gerente não existir
        """
        manager = await self.employee_repository.find_by_id(manager_id)
        if not manager:
            raise ValidationError(f"Gerente com ID {manager_id} não encontrado")
        
        if manager.status != "active":
            raise ValidationError("Gerente deve estar ativo")
    
    async def _validate_business_rules(self, employee: Employee) -> None:
        """
        Valida regras de negócio específicas para criação.
        
        Args:
            employee: Entidade de funcionário a ser validada
            
        Raises:
            BusinessRuleError: Se alguma regra de negócio for violada
        """
        # Regra: Verificar limite de funcionários por departamento
        dept_count = await self.employee_repository.count_by_department(employee.department)
        if dept_count >= 100:
            raise BusinessRuleError(
                f"Departamento {employee.department} atingiu limite máximo de funcionários",
                "department_limit_exceeded"
            )
        
        # Regra: Validar consistência salarial por cargo
        await self._validate_salary_consistency(employee)
        
        # Regra: Validar padrões regionais
        await self._validate_regional_patterns(employee)
    
    async def _validate_salary_consistency(self, employee: Employee) -> None:
        """
        Valida consistência salarial por cargo.
        
        Args:
            employee: Entidade de funcionário
            
        Raises:
            BusinessRuleError: Se salário for inconsistente
        """
        # Buscar funcionários com mesmo cargo para comparação
        similar_employees = await self.employee_repository.find_by_criteria(
            position=employee.position,
            department=employee.department,
            active_only=True,
            limit=50
        )
        
        if similar_employees:
            salaries = [emp.salary for emp in similar_employees]
            avg_salary = sum(salaries) / len(salaries)
            
            # Verificar se salário está muito acima da média (mais de 50%)
            if employee.salary > avg_salary * 1.5:
                # Apenas um aviso - não bloquear criação
                pass
    
    async def _validate_regional_patterns(self, employee: Employee) -> None:
        """
        Valida padrões regionais específicos.
        
        Args:
            employee: Entidade de funcionário
            
        Raises:
            BusinessRuleError: Se houver inconsistência regional
        """
        # Regra: Validar CEP com estado (se ambos fornecidos)
        if employee.zip_code and employee.state:
            cep_prefix = employee.zip_code[:2]
            state_cep_map = {
                "SP": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"],
                "RJ": ["20", "21", "22", "23", "24", "25", "26", "27", "28"],
                "MG": ["30", "31", "32", "33", "34", "35", "36", "37", "38", "39"],
                # Adicionar mais estados conforme necessário
            }
            
            if employee.state in state_cep_map:
                valid_prefixes = state_cep_map[employee.state]
                if cep_prefix not in valid_prefixes:
                    raise BusinessRuleError(
                        f"CEP {employee.get_formatted_zip_code()} não é válido para o estado {employee.state}",
                        "invalid_cep_state_combination"
                    )
    
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
