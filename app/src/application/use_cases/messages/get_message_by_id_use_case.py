"""
Use Case para Buscar Mensagem por ID - Application Layer

Responsável por buscar mensagens por ID aplicando regras de negócio.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela busca de mensagens por ID
- OCP: Extensível para novas validações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para busca
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from src.domain.entities.message import Message
from src.domain.ports.message_repository import MessageRepository
from src.application.dtos.message_dto import MessageResponse


class GetMessageByIdUseCase:
    """
    Use Case para busca de mensagens por ID.
    
    Coordena a busca e conversão de dados para resposta.
    """
    
    def __init__(self, message_repository: MessageRepository):
        """
        Inicializa o use case com as dependências necessárias.
        
        Args:
            message_repository: Repositório de mensagens
        """
        self._message_repository = message_repository
    
    async def execute(self, message_id: int) -> Optional[MessageResponse]:
        """
        Executa a busca de uma mensagem por ID.
        
        Args:
            message_id: ID da mensagem a ser buscada
            
        Returns:
            Optional[MessageResponse]: Dados da mensagem encontrada ou None
            
        Raises:
            ValueError: Se ID inválido for fornecido
            Exception: Se houver erro na busca
        """
        # Validação do ID
        if message_id <= 0:
            raise ValueError("ID da mensagem deve ser um número positivo")
        
        # Buscar no repositório
        message = await self._message_repository.get_message_by_id(message_id)
        
        if not message:
            return None
        
        # Converter para DTO de resposta
        return MessageResponse(
            id=message.id,
            name=message.name,
            email=message.email,
            phone=message.phone,
            message=message.message,
            vehicle_id=message.vehicle_id,
            responsible_id=message.responsible_id,
            status=message.status,
            service_start_time=message.service_start_time,
            created_at=message.created_at,
            updated_at=message.updated_at
        )
