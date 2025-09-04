from uuid import UUID

from src.domain.ports.employee_repository import EmployeeRepository
from src.domain.exceptions import NotFoundError, BusinessRuleError


class DeleteEmployeeUseCase:
    """
    Use case para exclusão de funcionários.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela exclusão de funcionários.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração EmployeeRepository, não da implementação.
    """
    
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository
    
    async def execute(self, employee_id: UUID) -> None:
        """
        Executa a exclusão de um funcionário.
        
        Args:
            employee_id: ID do funcionário a ser excluído
            
        Raises:
            NotFoundError: Se o funcionário não for encontrado
            BusinessRuleError: Se o funcionário não puder ser excluído
        """
        try:
            # Buscar funcionário existente
            existing_employee = await self.employee_repository.find_by_id(employee_id)
            if not existing_employee:
                raise NotFoundError("Funcionário", str(employee_id))
            
            # Validar se pode ser excluído
            await self._validate_can_delete(employee_id)
            
            # Excluir do repositório
            await self.employee_repository.delete(employee_id)
            
        except NotFoundError:
            raise
        except BusinessRuleError:
            raise
        except Exception as e:
            raise BusinessRuleError(f"Erro interno durante exclusão do funcionário: {str(e)}")
    
    async def _validate_can_delete(self, employee_id: UUID) -> None:
        """
        Valida se o funcionário pode ser excluído.
        
        Args:
            employee_id: ID do funcionário
            
        Raises:
            BusinessRuleError: Se o funcionário não puder ser excluído
        """
        # Regra: Verificar se funcionário tem subordinados
        has_subordinates = await self.employee_repository.has_subordinates(employee_id)
        if has_subordinates:
            raise BusinessRuleError(
                "Não é possível excluir funcionário que possui subordinados. Realocar equipe primeiro.",
                "employee_has_subordinates"
            )
        
        # Regra: Verificar se funcionário tem vendas associadas
        has_sales = await self.employee_repository.has_associated_sales(employee_id)
        if has_sales:
            raise BusinessRuleError(
                "Não é possível excluir funcionário que possui vendas associadas",
                "employee_has_sales"
            )
        
        # Regra: Verificar se funcionário tem transações pendentes
        has_pending_transactions = await self.employee_repository.has_pending_transactions(employee_id)
        if has_pending_transactions:
            raise BusinessRuleError(
                "Não é possível excluir funcionário que possui transações pendentes",
                "employee_has_pending_transactions"
            )
        
        # Regra: Gerentes ativos requerem aprovação especial
        employee = await self.employee_repository.find_by_id(employee_id)
        if employee and employee.is_manager() and employee.status == "active":
            # Em um cenário real, isso poderia exigir um processo de aprovação
            # Por agora, apenas permitimos a exclusão com um log/aviso
            pass
