"""
Interface do repositório de mensagens - Domain Layer

Define o contrato para persistência de mensagens seguindo o princípio
Dependency Inversion Principle (DIP) da arquitetura limpa.

A interface pertence ao domínio e as implementações concretas
ficam na camada de infraestrutura.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import date, datetime

from src.domain.entities.message import Message


class MessageRepository(ABC):
    """
    Interface abstrata para repositório de mensagens.
    
    Define todas as operações de persistência necessárias
    para o domínio de mensagens, incluindo CRUD, buscas
    específicas e operações de relatórios.
    
    Aplicando o princípio Interface Segregation Principle (ISP) -
    interface coesa com métodos relacionados apenas a mensagens.
    """
    
    @abstractmethod
    async def save(self, message: Message) -> Message:
        """
        Salva uma mensagem (create ou update).
        
        Args:
            message: Mensagem a ser salva
            
        Returns:
            Message: Mensagem salva com dados atualizados
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, message_id: UUID) -> Optional[Message]:
        """
        Busca uma mensagem pelo ID.
        
        Args:
            message_id: ID da mensagem
            
        Returns:
            Optional[Message]: A mensagem encontrada ou None
        """
        pass
    
    @abstractmethod
    async def find_by_criteria(self, **kwargs) -> List[Message]:
        """
        Busca mensagens por múltiplos critérios.
        
        Args:
            **kwargs: Critérios de busca (status, responsible_id, vehicle_id, etc.)
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str, **kwargs) -> List[Message]:
        """
        Busca mensagens por email.
        
        Args:
            email: Email do interessado
            **kwargs: Parâmetros adicionais (limit, skip, order_by)
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        pass
    
    @abstractmethod
    async def find_by_responsible(self, responsible_id: UUID, **kwargs) -> List[Message]:
        """
        Busca mensagens por responsável.
        
        Args:
            responsible_id: ID do funcionário responsável
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        pass
    
    @abstractmethod
    async def find_by_vehicle(self, vehicle_id: UUID, **kwargs) -> List[Message]:
        """
        Busca mensagens por veículo.
        
        Args:
            vehicle_id: ID do veículo
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        pass
    
    @abstractmethod
    async def find_by_status(self, status: str, **kwargs) -> List[Message]:
        """
        Busca mensagens por status.
        
        Args:
            status: Status das mensagens
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        pass
    
    @abstractmethod
    async def find_by_date_range(self, start_date: date, end_date: date, **kwargs) -> List[Message]:
        """
        Busca mensagens por período.
        
        Args:
            start_date: Data inicial
            end_date: Data final
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens encontradas
        """
        pass
    
    @abstractmethod
    async def find_pending_messages(self, **kwargs) -> List[Message]:
        """
        Busca mensagens pendentes.
        
        Args:
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens pendentes
        """
        pass
    
    @abstractmethod
    async def find_unassigned_messages(self, **kwargs) -> List[Message]:
        """
        Busca mensagens sem responsável atribuído.
        
        Args:
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens sem responsável
        """
        pass
    
    @abstractmethod
    async def find_overdue_messages(self, hours_threshold: int = 24, **kwargs) -> List[Message]:
        """
        Busca mensagens em atraso (pendentes há muito tempo).
        
        Args:
            hours_threshold: Número de horas para considerar em atraso
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Message]: Lista de mensagens em atraso
        """
        pass
    
    @abstractmethod
    async def delete(self, message_id: UUID) -> None:
        """
        Remove uma mensagem.
        
        Args:
            message_id: ID da mensagem a ser removida
        """
        pass
    
    @abstractmethod
    async def exists_by_id(self, message_id: UUID) -> bool:
        """
        Verifica se existe mensagem com o ID.
        
        Args:
            message_id: ID a ser verificado
            
        Returns:
            bool: True se existir mensagem com o ID
        """
        pass
    
    @abstractmethod
    async def count_by_status(self, status: str) -> int:
        """
        Conta mensagens por status.
        
        Args:
            status: Status das mensagens
            
        Returns:
            int: Número de mensagens com o status
        """
        pass
    
    @abstractmethod
    async def count_by_responsible(self, responsible_id: UUID) -> int:
        """
        Conta mensagens por responsável.
        
        Args:
            responsible_id: ID do funcionário responsável
            
        Returns:
            int: Número de mensagens do responsável
        """
        pass
    
    @abstractmethod
    async def count_by_vehicle(self, vehicle_id: UUID) -> int:
        """
        Conta mensagens por veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            int: Número de mensagens do veículo
        """
        pass
    
    @abstractmethod
    async def count_pending_messages(self) -> int:
        """
        Conta mensagens pendentes.
        
        Returns:
            int: Número de mensagens pendentes
        """
        pass
    
    @abstractmethod
    async def count_unassigned_messages(self) -> int:
        """
        Conta mensagens sem responsável.
        
        Returns:
            int: Número de mensagens sem responsável
        """
        pass
    
    @abstractmethod
    async def get_response_time_statistics(self, start_date: Optional[date] = None, 
                                          end_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Calcula estatísticas de tempo de resposta.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            dict: Estatísticas de tempo de resposta
        """
        pass
    
    @abstractmethod
    async def get_messages_statistics(self, start_date: Optional[date] = None, 
                                     end_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Busca estatísticas gerais de mensagens.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            
        Returns:
            dict: Estatísticas das mensagens
        """
        pass
    
    @abstractmethod
    async def get_top_performers(self, start_date: Optional[date] = None, 
                                end_date: Optional[date] = None, 
                                limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca funcionários com melhor performance no atendimento.
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            limit: Número máximo de resultados
            
        Returns:
            List[Dict]: Lista de funcionários com estatísticas
        """
        pass
    
    @abstractmethod
    async def get_vehicles_with_most_interest(self, start_date: Optional[date] = None, 
                                            end_date: Optional[date] = None, 
                                            limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca veículos com mais interesse (mais mensagens).
        
        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            limit: Número máximo de resultados
            
        Returns:
            List[Dict]: Lista de veículos com estatísticas
        """
        pass
