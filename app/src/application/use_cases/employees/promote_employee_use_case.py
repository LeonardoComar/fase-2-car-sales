from uuid import UUID

from src.application.dtos.employee_dto import EmployeePromotionDto, EmployeeResponseDto
from src.domain.entities.employee import Employee
from src.domain.ports.employee_repository import EmployeeRepository
from src.domain.exceptions import NotFoundError, BusinessRuleError, ValidationError


class PromoteEmployeeUseCase:
    """
    Use case para promoção de funcionários.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela promoção de funcionários.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração EmployeeRepository, não da implementação.
    """
    
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository
    
    async def execute(self, employee_id: UUID, promotion_data: EmployeePromotionDto) -> EmployeeResponseDto:
        """
        Executa a promoção de um funcionário.
        
        Args:
            employee_id: ID do funcionário
            promotion_data: Dados da promoção
            
        Returns:
            EmployeeResponseDto: Dados do funcionário promovido
            
        Raises:
            NotFoundError: Se o funcionário não for encontrado
            ValidationError: Se os dados da promoção forem inválidos
            BusinessRuleError: Se a promoção não for permitida
        """
        try:
            # Buscar funcionário existente
            existing_employee = await self.employee_repository.find_by_id(employee_id)
            if not existing_employee:
                raise NotFoundError("Funcionário", str(employee_id))
            
            # Validar se a promoção é permitida
            await self._validate_promotion_eligibility(existing_employee)
            
            # Validar dados da promoção
            await self._validate_promotion_data(existing_employee, promotion_data)
            
            # Aplicar promoção
            existing_employee.promote(
                new_position=promotion_data.new_position,
                new_salary=promotion_data.new_salary,
                new_department=promotion_data.new_department
            )
            
            # Adicionar nota sobre promoção
            self._add_promotion_note(existing_employee, promotion_data)
            
            # Salvar no repositório
            saved_employee = await self.employee_repository.save(existing_employee)
            
            # Converter para DTO de resposta
            return self._to_response_dto(saved_employee)
            
        except NotFoundError:
            raise
        except ValidationError:
            raise
        except BusinessRuleError:
            raise
        except Exception as e:
            raise ValidationError(f"Erro interno durante promoção do funcionário: {str(e)}")
    
    async def _validate_promotion_eligibility(self, employee: Employee) -> None:
        """
        Valida se o funcionário é elegível para promoção.
        
        Args:
            employee: Funcionário existente
            
        Raises:
            BusinessRuleError: Se a promoção não for permitida
        """
        # Regra: Funcionário deve estar ativo
        if employee.status != "active":
            raise BusinessRuleError(
                "Apenas funcionários ativos podem ser promovidos",
                "inactive_employee_promotion"
            )
        
        # Regra: Funcionário deve ter pelo menos 6 meses na empresa
        if employee.get_years_of_service() < 0.5:
            raise BusinessRuleError(
                "Funcionário deve ter pelo menos 6 meses na empresa para ser promovido",
                "insufficient_service_time"
            )
        
        # Regra: Verificar se não há avaliações pendentes
        if employee.needs_performance_review():
            # Em um cenário real, verificaríamos se há avaliações recentes
            # Por agora, apenas um aviso
            pass
    
    async def _validate_promotion_data(self, employee: Employee, promotion_data: EmployeePromotionDto) -> None:
        """
        Valida os dados da promoção.
        
        Args:
            employee: Funcionário existente
            promotion_data: Dados da promoção
            
        Raises:
            ValidationError: Se os dados forem inválidos
            BusinessRuleError: Se a promoção for inconsistente
        """
        # Regra: Novo salário deve ser maior que o atual
        if promotion_data.new_salary <= employee.salary:
            raise BusinessRuleError(
                "Promoção deve incluir aumento salarial",
                "promotion_without_salary_increase"
            )
        
        # Regra: Aumento não pode ser excessivo (mais de 100%)
        increase_percentage = (promotion_data.new_salary - employee.salary) / employee.salary
        if increase_percentage > 1.0:
            raise BusinessRuleError(
                "Aumento salarial não pode exceder 100% em uma única promoção",
                "excessive_salary_increase"
            )
        
        # Regra: Nova posição deve ser diferente da atual
        if promotion_data.new_position.lower() == employee.position.lower():
            raise BusinessRuleError(
                "Nova posição deve ser diferente da atual",
                "same_position_promotion"
            )
        
        # Regra: Validar mudança de departamento se aplicável
        if promotion_data.new_department:
            await self._validate_department_change(employee, promotion_data.new_department)
        
        # Regra: Validar consistência da nova posição
        await self._validate_position_consistency(promotion_data)
    
    async def _validate_department_change(self, employee: Employee, new_department: str) -> None:
        """
        Valida mudança de departamento na promoção.
        
        Args:
            employee: Funcionário existente
            new_department: Novo departamento
            
        Raises:
            BusinessRuleError: Se mudança de departamento for inválida
        """
        # Verificar limite do novo departamento
        dept_count = await self.employee_repository.count_by_department(new_department)
        if dept_count >= 100:
            raise BusinessRuleError(
                f"Departamento {new_department} atingiu limite máximo de funcionários",
                "department_limit_exceeded"
            )
        
        # Verificar se funcionário tem subordinados e mudança é para outro departamento
        if (new_department.lower() != employee.department.lower() and 
            await self.employee_repository.has_subordinates(employee.id)):
            raise BusinessRuleError(
                "Funcionário com subordinados precisa de realocação da equipe antes de mudar de departamento",
                "manager_department_change_with_subordinates"
            )
    
    async def _validate_position_consistency(self, promotion_data: EmployeePromotionDto) -> None:
        """
        Valida consistência da nova posição.
        
        Args:
            promotion_data: Dados da promoção
            
        Raises:
            BusinessRuleError: Se posição for inconsistente
        """
        # Buscar funcionários com posição similar para comparação salarial
        similar_employees = await self.employee_repository.find_by_criteria(
            position=promotion_data.new_position,
            department=promotion_data.new_department,
            active_only=True,
            limit=50
        )
        
        if similar_employees:
            salaries = [emp.salary for emp in similar_employees]
            avg_salary = sum(salaries) / len(salaries)
            min_salary = min(salaries)
            max_salary = max(salaries)
            
            # Verificar se salário está muito fora da faixa
            if promotion_data.new_salary < min_salary * 0.8:
                raise BusinessRuleError(
                    f"Salário muito abaixo da faixa para a posição {promotion_data.new_position}",
                    "salary_below_position_range"
                )
            
            if promotion_data.new_salary > max_salary * 1.2:
                # Apenas um aviso - não bloquear promoção
                pass
    
    def _add_promotion_note(self, employee: Employee, promotion_data: EmployeePromotionDto) -> None:
        """
        Adiciona nota sobre promoção.
        
        Args:
            employee: Funcionário
            promotion_data: Dados da promoção
        """
        from datetime import datetime
        
        old_position = employee.position
        old_salary = employee.get_formatted_salary()
        new_salary = f"R$ {promotion_data.new_salary:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        promotion_note = (
            f"PROMOÇÃO em {datetime.now().strftime('%d/%m/%Y')}: "
            f"{old_position} → {promotion_data.new_position}. "
            f"Salário: {old_salary} → {new_salary}"
        )
        
        if promotion_data.new_department:
            promotion_note += f". Departamento: {promotion_data.new_department}"
        
        if promotion_data.notes:
            promotion_note += f". Obs: {promotion_data.notes}"
        
        if employee.notes:
            employee.notes += f"\n{promotion_note}"
        else:
            employee.notes = promotion_note
    
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
