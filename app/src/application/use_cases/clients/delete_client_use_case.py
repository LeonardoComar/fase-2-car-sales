from uuid import UUID

from src.domain.ports.client_repository import ClientRepository
from src.domain.exceptions import NotFoundError, BusinessRuleError


class DeleteClientUseCase:
    """
    Use case para exclusão de clientes.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela exclusão de clientes.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração ClientRepository, não da implementação.
    """
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    async def execute(self, client_id: UUID) -> None:
        """
        Executa a exclusão de um cliente.
        
        Args:
            client_id: ID do cliente a ser excluído
            
        Raises:
            NotFoundError: Se o cliente não for encontrado
            BusinessRuleError: Se o cliente não puder ser excluído
        """
        try:
            # Buscar cliente existente
            existing_client = await self.client_repository.find_by_id(client_id)
            if not existing_client:
                raise NotFoundError("Cliente", str(client_id))
            
            # Validar se pode ser excluído
            await self._validate_can_delete(client_id)
            
            # Excluir do repositório
            await self.client_repository.delete(client_id)
            
        except NotFoundError:
            raise
        except BusinessRuleError:
            raise
        except Exception as e:
            raise BusinessRuleError(f"Erro interno durante exclusão do cliente: {str(e)}")
    
    async def _validate_can_delete(self, client_id: UUID) -> None:
        """
        Valida se o cliente pode ser excluído.
        
        Args:
            client_id: ID do cliente
            
        Raises:
            BusinessRuleError: Se o cliente não puder ser excluído
        """
        # Regra: Verificar se cliente tem vendas associadas
        has_sales = await self.client_repository.has_associated_sales(client_id)
        if has_sales:
            raise BusinessRuleError(
                "Não é possível excluir cliente que possui vendas associadas",
                "client_has_sales"
            )
        
        # Regra: Verificar se cliente tem transações pendentes
        has_pending_transactions = await self.client_repository.has_pending_transactions(client_id)
        if has_pending_transactions:
            raise BusinessRuleError(
                "Não é possível excluir cliente que possui transações pendentes",
                "client_has_pending_transactions"
            )
        
        # Regra: Clientes VIP requerem aprovação especial
        client = await self.client_repository.find_by_id(client_id)
        if client and client.is_vip():
            # Em um cenário real, isso poderia exigir um processo de aprovação
            # Por agora, apenas permitimos a exclusão com um log/aviso
            pass
