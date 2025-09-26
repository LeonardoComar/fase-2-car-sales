"""
Use Case para Iniciar Atendimento de Mensagem - Application Layer

Responsável por iniciar o atendimento de mensagens aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pelo início de atendimento de mensagens
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para início de atendimento
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from src.domain.entities.message import Message
from src.domain.ports.message_repository import MessageRepository
from src.application.dtos.message_dto import StartServiceRequest, MessageResponse


class StartServiceUseCase:
    """
    Use Case para início de atendimento de mensagens.
    
    Coordena a validação e execução do início de atendimento.
    """
    
    def __init__(self, message_repository: MessageRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            message_repository: Repositório de mensagens
        """
        self._message_repository = message_repository
    
    async def execute(self, message_id: int, service_data: StartServiceRequest) -> MessageResponse:
        """
        Executa o início de atendimento de uma mensagem.
        
        Args:
            message_id: ID da mensagem
            service_data: Dados do início de atendimento
            
        Returns:
            MessageResponse: Dados da mensagem com atendimento iniciado
            
        Raises:
            ValueError: Se dados inválidos forem fornecidos
            Exception: Se houver erro no início do atendimento
        """
        # Validações
        if message_id <= 0:
            raise ValueError("ID da mensagem deve ser um número positivo")
        
        if service_data.responsible_id <= 0:
            raise ValueError("ID do responsável deve ser um número positivo")
        
        # Buscar mensagem
        message = await self._message_repository.get_message_by_id(message_id)
        
        if not message:
            raise ValueError(f"Mensagem com ID {message_id} não encontrada")
        
        # Validar se pode iniciar atendimento
        if message.responsible_id is not None:
            raise ValueError("Mensagem já possui responsável atribuído")
        
        if message.status != Message.STATUS_PENDENTE:
            raise ValueError(f"Só é possível iniciar atendimento de mensagens com status '{Message.STATUS_PENDENTE}'")
        
        # Iniciar atendimento usando o método do repositório
        updated_message = await self._message_repository.start_service(
            message_id, 
            service_data.responsible_id
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
