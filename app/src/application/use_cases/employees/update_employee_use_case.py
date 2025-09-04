from uuid import UUID

from src.application.dtos.employee_dto import EmployeeUpdateDto, EmployeeResponseDto
from src.domain.entities.employee import Employee
from src.domain.ports.employee_repository import EmployeeRepository
from src.domain.exceptions import ValidationError, BusinessRuleError, NotFoundError, DuplicateError


class UpdateEmployeeUseCase:
    """
    Use case para atualização de funcionários.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela atualização de funcionários.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração EmployeeRepository, não da implementação.
    """
    
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository
    
    async def execute(self, employee_id: UUID, employee_data: EmployeeUpdateDto) -> EmployeeResponseDto:
        """
        Executa a atualização de um funcionário.
        
        Args:
            employee_id: ID do funcionário a ser atualizado
            employee_data: Dados para atualização
            
        Returns:
            EmployeeResponseDto: Dados do funcionário atualizado
            
        Raises:
            NotFoundError: Se o funcionário não for encontrado
            ValidationError: Se os dados não forem válidos
            BusinessRuleError: Se as regras de negócio não forem atendidas
            DuplicateError: Se houver conflito com CPF, email ou ID interno
        """
        try:
            # Buscar funcionário existente
            existing_employee = await self.employee_repository.find_by_id(employee_id)
            if not existing_employee:
                raise NotFoundError("Funcionário", str(employee_id))
            
            # Validar mudanças de campos únicos
            await self._validate_unique_fields(existing_employee, employee_data)
            
            # Validar se gerente existe (se fornecido)
            if employee_data.manager_id:
                await self._validate_manager_exists(employee_data.manager_id, employee_id)
            
            # Aplicar atualizações
            updated_employee = self._apply_updates(existing_employee, employee_data)
            
            # Validações adicionais de negócio
            await self._validate_business_rules(updated_employee, employee_data)
            
            # Salvar no repositório
            saved_employee = await self.employee_repository.save(updated_employee)
            
            # Converter para DTO de resposta
            return self._to_response_dto(saved_employee)
            
        except NotFoundError:
            raise
        except ValidationError:
            raise
        except BusinessRuleError:
            raise
        except DuplicateError:
            raise
        except Exception as e:
            raise ValidationError(f"Erro interno durante atualização do funcionário: {str(e)}")
    
    async def _validate_unique_fields(self, existing_employee: Employee, employee_data: EmployeeUpdateDto) -> None:
        """
        Valida se os campos únicos não conflitam com outros funcionários.
        
        Args:
            existing_employee: Funcionário existente
            employee_data: Dados de atualização
            
        Raises:
            DuplicateError: Se houver conflito
        """
        # Validar CPF se foi alterado
        if employee_data.cpf and employee_data.cpf != existing_employee.cpf:
            if await self.employee_repository.exists_by_cpf(employee_data.cpf, existing_employee.id):
                raise DuplicateError("Funcionário", "CPF", employee_data.cpf)
        
        # Validar email se foi alterado
        if employee_data.email and employee_data.email != existing_employee.email:
            if await self.employee_repository.exists_by_email(employee_data.email, existing_employee.id):
                raise DuplicateError("Funcionário", "email", employee_data.email)
        
        # Validar ID interno se foi alterado
        if (employee_data.employee_id and 
            employee_data.employee_id != existing_employee.employee_id):
            if await self.employee_repository.exists_by_employee_id(employee_data.employee_id, existing_employee.id):
                raise DuplicateError("Funcionário", "ID interno", employee_data.employee_id)
    
    async def _validate_manager_exists(self, manager_id: UUID, employee_id: UUID) -> None:
        """
        Valida se o gerente existe e não é o próprio funcionário.
        
        Args:
            manager_id: ID do gerente
            employee_id: ID do funcionário sendo atualizado
            
        Raises:
            ValidationError: Se gerente não existir ou for inválido
        """
        if manager_id == employee_id:
            raise ValidationError("Funcionário não pode ser gerente de si mesmo")
        
        manager = await self.employee_repository.find_by_id(manager_id)
        if not manager:
            raise ValidationError(f"Gerente com ID {manager_id} não encontrado")
        
        if manager.status != "active":
            raise ValidationError("Gerente deve estar ativo")
    
    def _apply_updates(self, existing_employee: Employee, employee_data: EmployeeUpdateDto) -> Employee:
        """
        Aplica as atualizações ao funcionário existente.
        
        Args:
            existing_employee: Funcionário existente
            employee_data: Dados de atualização
            
        Returns:
            Employee: Funcionário atualizado
        """
        # Preparar dados para atualização
        update_data = {}
        
        if employee_data.name is not None:
            update_data['name'] = employee_data.name
        
        if employee_data.email is not None:
            update_data['email'] = employee_data.email
        
        if employee_data.phone is not None:
            update_data['phone'] = employee_data.phone
        
        if employee_data.cpf is not None:
            update_data['cpf'] = employee_data.cpf
        
        if employee_data.birth_date is not None:
            update_data['birth_date'] = employee_data.birth_date
        
        if employee_data.position is not None:
            update_data['position'] = employee_data.position
        
        if employee_data.department is not None:
            update_data['department'] = employee_data.department
        
        if employee_data.salary is not None:
            update_data['salary'] = employee_data.salary
        
        if employee_data.manager_id is not None:
            update_data['manager_id'] = employee_data.manager_id
        
        if employee_data.employee_id is not None:
            update_data['employee_id'] = employee_data.employee_id
        
        if employee_data.address is not None:
            update_data['address'] = employee_data.address
        
        if employee_data.city is not None:
            update_data['city'] = employee_data.city
        
        if employee_data.state is not None:
            update_data['state'] = employee_data.state
        
        if employee_data.zip_code is not None:
            update_data['zip_code'] = employee_data.zip_code
        
        if employee_data.emergency_contact_name is not None:
            update_data['emergency_contact_name'] = employee_data.emergency_contact_name
        
        if employee_data.emergency_contact_phone is not None:
            update_data['emergency_contact_phone'] = employee_data.emergency_contact_phone
        
        if employee_data.status is not None:
            update_data['status'] = employee_data.status
        
        if employee_data.notes is not None:
            update_data['notes'] = employee_data.notes
        
        # Atualizar funcionário
        existing_employee.update(**update_data)
        
        return existing_employee
    
    async def _validate_business_rules(self, employee: Employee, employee_data: EmployeeUpdateDto) -> None:
        """
        Valida regras de negócio específicas para atualização.
        
        Args:
            employee: Entidade de funcionário a ser validada
            employee_data: Dados de atualização
            
        Raises:
            BusinessRuleError: Se alguma regra de negócio for violada
        """
        # Regra: Funcionário inativo não pode ter certas atualizações críticas
        if employee.status == "inactive":
            critical_fields = ['position', 'department', 'salary', 'manager_id']
            if any(getattr(employee_data, field) is not None for field in critical_fields):
                raise BusinessRuleError(
                    "Funcionário inativo não pode ter atualizações em campos críticos",
                    "inactive_employee_critical_update"
                )
        
        # Regra: Validar mudança de salário
        if employee_data.salary and employee_data.salary != employee.salary:
            await self._validate_salary_change(employee, employee_data.salary)
        
        # Regra: Validar mudança de departamento
        if employee_data.department and employee_data.department != employee.department:
            await self._validate_department_change(employee, employee_data.department)
        
        # Regra: Validar padrões regionais se endereço foi alterado
        if any([employee_data.address, employee_data.city, employee_data.state, employee_data.zip_code]):
            await self._validate_regional_patterns(employee)
    
    async def _validate_salary_change(self, employee: Employee, new_salary) -> None:
        """
        Valida mudança de salário.
        
        Args:
            employee: Funcionário existente
            new_salary: Novo salário
            
        Raises:
            BusinessRuleError: Se mudança de salário for inválida
        """
        # Regra: Redução salarial significativa requer aprovação especial
        reduction_percentage = (employee.salary - new_salary) / employee.salary
        if reduction_percentage > 0.2:  # Mais de 20% de redução
            raise BusinessRuleError(
                "Redução salarial superior a 20% requer aprovação especial",
                "significant_salary_reduction"
            )
        
        # Regra: Aumento salarial muito alto requer aprovação
        increase_percentage = (new_salary - employee.salary) / employee.salary
        if increase_percentage > 0.5:  # Mais de 50% de aumento
            # Em um cenário real, isso poderia exigir aprovação especial
            pass
    
    async def _validate_department_change(self, employee: Employee, new_department: str) -> None:
        """
        Valida mudança de departamento.
        
        Args:
            employee: Funcionário existente
            new_department: Novo departamento
            
        Raises:
            BusinessRuleError: Se mudança de departamento for inválida
        """
        # Verificar se funcionário tem subordinados
        if await self.employee_repository.has_subordinates(employee.id):
            raise BusinessRuleError(
                "Funcionário com subordinados não pode mudar de departamento sem realocação da equipe",
                "manager_department_change_restricted"
            )
        
        # Verificar limite do novo departamento
        dept_count = await self.employee_repository.count_by_department(new_department)
        if dept_count >= 100:
            raise BusinessRuleError(
                f"Departamento {new_department} atingiu limite máximo de funcionários",
                "department_limit_exceeded"
            )
    
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
