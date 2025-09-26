"""
Use Case para Criação de Mensagem - Application Layer

Responsável por coordenar a criação de mensagens aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela criação de mensagens
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para criação
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from src.domain.entities.message import Message
from src.domain.ports.message_repository import MessageRepository
from src.application.dtos.message_dto import CreateMessageRequest, MessageCreatedResponse


class CreateMessageUseCase:
    """
    Use Case para criação de mensagens.
    
    Coordena a validação de dados, aplicação de regras de negócio
    e persistência de mensagens no sistema.
    """
    
    def __init__(self, message_repository: MessageRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            message_repository: Repositório de mensagens
        """
        self._message_repository = message_repository
    
    async def execute(self, message_data: CreateMessageRequest) -> MessageCreatedResponse:
        """
        Executa a criação de uma mensagem.
        
        Args:
            message_data: Dados para criação da mensagem
            
        Returns:
            MessageCreatedResponse: Dados da mensagem criada
            
        Raises:
            ValueError: Se dados inválidos forem fornecidos
            Exception: Se houver erro na criação
        """
        # Validação adicional se necessário
        if message_data.phone and len(message_data.phone.strip()) == 0:
            message_data.phone = None
        
        # Criar entidade de domínio
        message = Message(
            name=message_data.name,
            email=message_data.email,
            phone=message_data.phone,
            message=message_data.message,
            vehicle_id=message_data.vehicle_id,
            status=Message.STATUS_PENDENTE
        )
        
        # Persistir no repositório
        created_message = await self._message_repository.create_message(message)
        
        # Retornar resposta
        return MessageCreatedResponse(
            id=created_message.id,
            name=created_message.name,
            email=created_message.email,
            status=created_message.status,
            message=created_message.message,
            created_at=created_message.created_at
        )
