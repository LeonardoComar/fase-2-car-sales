"""
Interface Message Repository - Domain Layer

Define o contrato para persistência de mensagens.

Aplicando princípios SOLID:
- ISP: Interface específica para operações de mensagem
- DIP: Define abstração que será implementada pela infraestrutura
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from src.domain.entities.message import Message


class MessageRepository(ABC):
    """
    Interface (porta) para o repositório de mensagens.
    Define as operações que devem ser implementadas pela infraestrutura.
    """

    @abstractmethod
    async def create_message(self, message: Message) -> Message:
        """
        Cria uma nova mensagem no repositório.
        
        Args:
            message: Entidade da mensagem
            
        Returns:
            Message: Mensagem criada com ID atribuído
            
        Raises:
            Exception: Em caso de erro na criação
        """
        pass

    @abstractmethod
    async def get_message_by_id(self, message_id: int) -> Optional[Message]:
        """
        Busca uma mensagem por ID.
        
        Args:
            message_id: ID da mensagem
            
        Returns:
            Optional[Message]: Mensagem encontrada ou None
        """
        pass

    @abstractmethod
    async def get_all_messages(
        self,
        limit: int = 100,
        offset: int = 0,
        order_by_value: str = "created_at",
        order_direction: str = "desc",
        status: Optional[str] = None,
        responsible_id: Optional[int] = None,
        vehicle_id: Optional[int] = None
    ) -> List[Message]:
        """
        Busca todas as mensagens com filtros opcionais.
        
        Args:
            limit: Limite de registros por página
            offset: Deslocamento para paginação
            order_by_value: Campo para ordenação
            order_direction: Direção da ordenação (asc/desc)
            status: Filtro por status (opcional)
            responsible_id: Filtro por responsável (opcional)
            vehicle_id: Filtro por veículo (opcional)
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        pass

    @abstractmethod
    async def count_messages(
        self,
        status: Optional[str] = None,
        responsible_id: Optional[int] = None,
        vehicle_id: Optional[int] = None
    ) -> int:
        """
        Conta o número total de mensagens com filtros opcionais.
        
        Args:
            status: Filtro por status (opcional)
            responsible_id: Filtro por responsável (opcional)
            vehicle_id: Filtro por veículo (opcional)
            
        Returns:
            int: Número total de mensagens
        """
        pass

    @abstractmethod
    async def update_message(self, message: Message) -> Message:
        """
        Atualiza uma mensagem existente.
        
        Args:
            message: Entidade da mensagem atualizada
            
        Returns:
            Message: Mensagem atualizada
            
        Raises:
            Exception: Em caso de erro na atualização
        """
        pass

    @abstractmethod
    async def update_message_by_id(self, message_id: int, updates: Dict[str, Any]) -> Message:
        """
        Atualiza campos específicos de uma mensagem por ID.
        
        Args:
            message_id: ID da mensagem
            updates: Dicionário com os campos a serem atualizados
            
        Returns:
            Message: Mensagem atualizada
            
        Raises:
            Exception: Em caso de erro na atualização ou mensagem não encontrada
        """
        pass

    @abstractmethod
    async def delete_message(self, message_id: int) -> bool:
        """
        Remove uma mensagem do repositório.
        
        Args:
            message_id: ID da mensagem
            
        Returns:
            bool: True se a mensagem foi removida, False caso contrário
        """
        pass

    @abstractmethod
    async def start_service(self, message_id: int, responsible_id: int) -> Message:
        """
        Inicia o atendimento de uma mensagem.
        
        Args:
            message_id: ID da mensagem
            responsible_id: ID do funcionário responsável
            
        Returns:
            Message: Mensagem com atendimento iniciado
            
        Raises:
            Exception: Em caso de erro ou mensagem não encontrada
        """
        pass

    @abstractmethod
    async def update_status(self, message_id: int, status: str) -> Message:
        """
        Atualiza o status de uma mensagem.
        
        Args:
            message_id: ID da mensagem
            status: Novo status
            
        Returns:
            Message: Mensagem com status atualizado
            
        Raises:
            Exception: Em caso de erro ou mensagem não encontrada
        """
        pass
