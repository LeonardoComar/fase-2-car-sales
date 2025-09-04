from uuid import UUID

from src.application.dtos.employee_dto import EmployeeStatusUpdateDto, EmployeeResponseDto
from src.domain.entities.employee import Employee
from src.domain.ports.employee_repository import EmployeeRepository
from src.domain.exceptions import NotFoundError, BusinessRuleError, ValidationError


class UpdateEmployeeStatusUseCase:
    """
    Use case para atualização de status de funcionários.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela atualização de status de funcionários.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração EmployeeRepository, não da implementação.
    """
    
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository
    
    async def execute(self, employee_id: UUID, status_data: EmployeeStatusUpdateDto) -> EmployeeResponseDto:
        """
        Executa a atualização de status de um funcionário.
        
        Args:
            employee_id: ID do funcionário
            status_data: Dados de atualização de status
            
        Returns:
            EmployeeResponseDto: Dados do funcionário com status atualizado
            
        Raises:
            NotFoundError: Se o funcionário não for encontrado
            ValidationError: Se o status for inválido
            BusinessRuleError: Se a mudança de status não for permitida
        """
        try:
            # Buscar funcionário existente
            existing_employee = await self.employee_repository.find_by_id(employee_id)
            if not existing_employee:
                raise NotFoundError("Funcionário", str(employee_id))
            
            # Validar se a mudança de status é permitida
            await self._validate_status_change(existing_employee, status_data.status)
            
            # Atualizar status
            existing_employee.update_status(status_data.status)
            
            # Adicionar nota sobre mudança se fornecida
            if status_data.reason:
                self._add_status_change_note(existing_employee, status_data.status, status_data.reason)
            
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
            raise ValidationError(f"Erro interno durante atualização de status: {str(e)}")
    
    async def _validate_status_change(self, employee: Employee, new_status: str) -> None:
        """
        Valida se a mudança de status é permitida.
        
        Args:
            employee: Funcionário existente
            new_status: Novo status
            
        Raises:
            BusinessRuleError: Se a mudança não for permitida
        """
        current_status = employee.status
        
        # Regra: Não permitir mudança desnecessária
        if current_status == new_status:
            raise BusinessRuleError(
                f"Funcionário já possui status '{new_status}'",
                "status_unchanged"
            )
        
        # Regra: Funcionário terminado não pode voltar a ativo facilmente
        if current_status == "terminated" and new_status == "active":
            raise BusinessRuleError(
                "Funcionário terminado requer processo especial de recontratação",
                "terminated_reactivation_restricted"
            )
        
        # Regra: Verificar se funcionário tem subordinados antes de inativar/suspender
        if new_status in ["inactive", "suspended", "terminated", "on_leave"]:
            has_subordinates = await self.employee_repository.has_subordinates(employee.id)
            if has_subordinates:
                if new_status == "terminated":
                    raise BusinessRuleError(
                        "Funcionário com subordinados não pode ser terminado sem realocação da equipe",
                        "manager_termination_with_subordinates"
                    )
                elif new_status in ["suspended", "on_leave"]:
                    # Para suspensão ou licença, apenas um aviso (pode ser temporário)
                    pass
                else:  # inactive
                    raise BusinessRuleError(
                        "Funcionário com subordinados não pode ser inativado sem realocação da equipe",
                        "manager_inactivation_with_subordinates"
                    )
        
        # Regra: Verificar transações pendentes
        if new_status in ["inactive", "terminated"]:
            has_pending_transactions = await self.employee_repository.has_pending_transactions(employee.id)
            if has_pending_transactions:
                raise BusinessRuleError(
                    "Não é possível alterar status de funcionário com transações pendentes",
                    "employee_has_pending_transactions"
                )
        
        # Regra: Validar transições específicas
        await self._validate_specific_transitions(employee, current_status, new_status)
    
    async def _validate_specific_transitions(self, employee: Employee, current_status: str, new_status: str) -> None:
        """
        Valida transições específicas de status.
        
        Args:
            employee: Funcionário
            current_status: Status atual
            new_status: Novo status
            
        Raises:
            BusinessRuleError: Se transição for inválida
        """
        # Regra: Funcionário suspenso só pode ir para ativo, terminado ou licença
        if current_status == "suspended":
            valid_transitions = ["active", "terminated", "on_leave"]
            if new_status not in valid_transitions:
                raise BusinessRuleError(
                    f"Funcionário suspenso só pode transicionar para: {', '.join(valid_transitions)}",
                    "invalid_suspended_transition"
                )
        
        # Regra: Funcionário em licença só pode voltar a ativo ou ser terminado
        if current_status == "on_leave":
            valid_transitions = ["active", "terminated"]
            if new_status not in valid_transitions:
                raise BusinessRuleError(
                    f"Funcionário em licença só pode transicionar para: {', '.join(valid_transitions)}",
                    "invalid_leave_transition"
                )
        
        # Regra: Funcionário inativo pode ir para qualquer status exceto licença diretamente
        if current_status == "inactive" and new_status == "on_leave":
            raise BusinessRuleError(
                "Funcionário inativo deve ser reativado antes de entrar em licença",
                "inactive_to_leave_invalid"
            )
        
        # Regra: Validar se mudança para gerente é apropriada
        if (new_status == "active" and employee.is_manager() and 
            current_status in ["suspended", "on_leave"]):
            # Gerente voltando ao ativo - verificar se ainda tem equipe
            has_subordinates = await self.employee_repository.has_subordinates(employee.id)
            if has_subordinates and current_status == "suspended":
                # Gerente suspenso com equipe ainda ativa - pode precisar de avaliação
                pass
    
    def _add_status_change_note(self, employee: Employee, new_status: str, reason: str) -> None:
        """
        Adiciona nota sobre mudança de status.
        
        Args:
            employee: Funcionário
            new_status: Novo status
            reason: Motivo da mudança
        """
        from datetime import datetime
        
        status_translation = {
            "active": "Ativo",
            "inactive": "Inativo", 
            "suspended": "Suspenso",
            "terminated": "Terminado",
            "on_leave": "Em Licença"
        }
        
        status_note = (
            f"STATUS alterado para '{status_translation.get(new_status, new_status)}' "
            f"em {datetime.now().strftime('%d/%m/%Y %H:%M')}. "
            f"Motivo: {reason}"
        )
        
        if employee.notes:
            employee.notes += f"\n{status_note}"
        else:
            employee.notes = status_note
    
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
