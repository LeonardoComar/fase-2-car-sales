"""
Use Case para Exclusão de Cliente - Application Layer

Responsável por excluir clientes aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela exclusão de clientes
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para exclusão
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from src.domain.ports.client_repository import ClientRepository


class DeleteClientUseCase:
    """
    Use Case para exclusão de clientes.
    
    Coordena a validação e exclusão de clientes do sistema.
    """
    
    def __init__(self, client_repository: ClientRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            client_repository: Repositório de clientes
        """
        self._client_repository = client_repository
    
    async def execute(self, client_id: int) -> bool:
        """
        Executa a exclusão de um cliente.
        
        Args:
            client_id: ID do cliente a ser excluído
            
        Returns:
            bool: True se excluído com sucesso, False se não encontrado
            
        Raises:
            ValueError: Se ID inválido for fornecido
            Exception: Se houver erro na exclusão
        """
        try:
            if client_id <= 0:
                raise ValueError("ID do cliente deve ser maior que zero")
            
            # Verificar se cliente existe
            existing_client = await self._client_repository.find_by_id(client_id)
            if not existing_client:
                return False
            
            # Excluir cliente
            return await self._client_repository.delete(client_id)
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erro ao excluir cliente: {str(e)}")
