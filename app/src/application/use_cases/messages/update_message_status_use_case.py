"""
Use Case para Atualizar Status de Mensagem - Application Layer

Responsável por atualizar o status de mensagens aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela atualização de status de mensagens
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para atualização de status
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from src.domain.entities.message import Message
from src.domain.ports.message_repository import MessageRepository
from src.application.dtos.message_dto import UpdateMessageStatusRequest, MessageResponse


class UpdateMessageStatusUseCase:
    """
    Use Case para atualização de status de mensagens.
    
    Coordena a validação e execução da atualização de status.
    """
    
    def __init__(self, message_repository: MessageRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            message_repository: Repositório de mensagens
        """
        self._message_repository = message_repository
    
    async def execute(self, message_id: int, status_data: UpdateMessageStatusRequest) -> MessageResponse:
        """
        Executa a atualização de status de uma mensagem.
        
        Args:
            message_id: ID da mensagem
            status_data: Dados do novo status
            
        Returns:
            MessageResponse: Dados da mensagem com status atualizado
            
        Raises:
            ValueError: Se dados inválidos forem fornecidos
            Exception: Se houver erro na atualização
        """
        # Validações
        if message_id <= 0:
            raise ValueError("ID da mensagem deve ser um número positivo")
        
        # Buscar mensagem
        message = await self._message_repository.get_message_by_id(message_id)
        
        if not message:
            raise ValueError(f"Mensagem com ID {message_id} não encontrada")
        
        # Atualizar status usando o método do repositório
        updated_message = await self._message_repository.update_status(
            message_id, 
            status_data.status.value
        )
        
        # Retornar resposta
        return MessageResponse(
            id=updated_message.id,
            name=updated_message.name,
            email=updated_message.email,
            phone=updated_message.phone,
            message=updated_message.message,
            vehicle_id=updated_message.vehicle_id,
            responsible_id=updated_message.responsible_id,
            status=updated_message.status,
            service_start_time=updated_message.service_start_time,
            created_at=updated_message.created_at,
            updated_at=updated_message.updated_at
        )
