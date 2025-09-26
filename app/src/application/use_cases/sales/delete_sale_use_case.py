"""
Use Case para Exclusão de Venda - Application Layer

Responsável por deletar vendas seguindo regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela exclusão de vendas
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para exclusão
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from src.domain.ports.sale_repository import SaleRepository


class DeleteSaleUseCase:
    """
    Use Case para exclusão de vendas.
    
    Coordena a validação de dados, aplicação de regras de negócio
    e remoção de vendas do sistema.
    """
    
    def __init__(self, sale_repository: SaleRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            sale_repository: Repositório de vendas
        """
        self._sale_repository = sale_repository
    
    async def execute(self, sale_id: int) -> bool:
        """
        Executa a exclusão de uma venda.
        
        Args:
            sale_id: ID da venda a ser excluída
            
        Returns:
            bool: True se excluída com sucesso, False se não encontrada
            
        Raises:
            ValueError: Se ID inválido for fornecido
            Exception: Se houver erro na exclusão
        """
        try:
            if sale_id <= 0:
                raise ValueError("ID da venda deve ser maior que zero")
            
            # Verificar se a venda existe
            existing_sale = await self._sale_repository.get_sale_by_id(sale_id)
            if not existing_sale:
                return False
            
            # Executar exclusão
            result = await self._sale_repository.delete_sale(sale_id)
            
            return result
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao excluir venda: {str(e)}")
