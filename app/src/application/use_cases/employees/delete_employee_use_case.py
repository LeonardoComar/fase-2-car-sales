"""
Use Case para Exclusão de Funcionário - Application Layer

Responsável por excluir funcionários aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela exclusão de funcionários
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para exclusão
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from src.domain.ports.employee_repository import EmployeeRepository


class DeleteEmployeeUseCase:
    """
    Use Case para exclusão de funcionários.
    
    Coordena a validação e exclusão de funcionários do sistema.
    """
    
    def __init__(self, employee_repository: EmployeeRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            employee_repository: Repositório de funcionários
        """
        self._employee_repository = employee_repository
    
    async def execute(self, employee_id: int) -> bool:
        """
        Executa a exclusão de um funcionário.
        
        Args:
            employee_id: ID do funcionário a ser excluído
            
        Returns:
            bool: True se excluído com sucesso, False se não encontrado
            
        Raises:
            ValueError: Se ID inválido for fornecido
            Exception: Se houver erro na exclusão
        """
        try:
            if employee_id <= 0:
                raise ValueError("ID do funcionário deve ser maior que zero")
            
            # Verificar se funcionário existe
            existing_employee = await self._employee_repository.find_by_id(employee_id)
            if not existing_employee:
                return False
            
            # Excluir funcionário
            return await self._employee_repository.delete(employee_id)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao excluir funcionário: {str(e)}")
