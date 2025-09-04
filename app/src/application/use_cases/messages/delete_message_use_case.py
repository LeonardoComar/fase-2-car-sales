"""
Caso de uso para deletar mensagem - Application Layer

Implementa a lógica de aplicação para remover uma mensagem.
Aplicando Clean Architecture e princípios SOLID.
"""

from uuid import UUID

from src.domain.ports.message_repository import MessageRepository


class DeleteMessageUseCase:
    """
    Caso de uso para deletar mensagem.
    
    Aplicando princípios SOLID:
    - SRP: Responsável apenas pela remoção de mensagens
    - OCP: Extensível para novas validações
    - LSP: Pode ser substituído por outras implementações
    - ISP: Interface coesa
    - DIP: Depende de abstrações (MessageRepository)
    """
    
    def __init__(self, message_repository: MessageRepository):
        """
        Inicializa o caso de uso.
        
        Args:
            message_repository: Repositório de mensagens
        """
        self._message_repository = message_repository
    
    async def execute(self, message_id: UUID) -> bool:
        """
        Executa a remoção de uma mensagem.
        
        Args:
            message_id: ID da mensagem a ser removida
            
        Returns:
            bool: True se mensagem foi removida, False se não encontrada
            
        Raises:
            Exception: Se erro na persistência
        """
        # Verificar se mensagem existe
        exists = await self._message_repository.exists_by_id(message_id)
        
        if not exists:
            return False
        
        # Remover mensagem
        await self._message_repository.delete(message_id)
        
        return True
