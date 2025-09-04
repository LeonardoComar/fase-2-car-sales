from uuid import UUID

from src.domain.ports.sale_repository import SaleRepository
from src.domain.exceptions import ValidationError


class DeleteSaleUseCase:
    """
    Caso de uso para exclusão de venda.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela exclusão de vendas.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração SaleRepository.
    """
    
    def __init__(self, sale_repository: SaleRepository):
        self._sale_repository = sale_repository
    
    async def execute(self, sale_id: UUID) -> bool:
        """
        Executa a exclusão de uma venda.
        
        Args:
            sale_id: ID da venda a ser excluída
            
        Returns:
            bool: True se excluída com sucesso, False se não encontrada
            
        Raises:
            ValidationError: Se venda não pode ser excluída
        """
        # Buscar venda existente
        sale = await self._sale_repository.find_by_id(sale_id)
        if not sale:
            return False
        
        # Verificar se venda pode ser excluída
        if sale.status in [sale.STATUS_PAGA, sale.STATUS_ENTREGUE]:
            raise ValidationError("Vendas pagas ou entregues não podem ser excluídas")
        
        # Excluir do repositório
        await self._sale_repository.delete(sale_id)
        return True
