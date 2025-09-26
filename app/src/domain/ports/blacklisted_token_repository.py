"""
Interface BlacklistedTokenRepository - Domain Layer

Define o contrato para persistência de tokens blacklisted.
Parte do domínio, implementada na camada de infraestrutura.

Aplicando princípios SOLID:
- SRP: Responsável apenas por definir operações de persistência de tokens
- OCP: Extensível sem modificar o contrato
- LSP: Qualquer implementação deve respeitar o contrato
- ISP: Interface específica para tokens blacklisted
- DIP: Dependência de abstração, não de implementação
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from src.domain.entities.blacklisted_token import BlacklistedToken


class BlacklistedTokenRepository(ABC):
    """
    Interface do repositório para tokens blacklisted.
    
    Define todas as operações necessárias para gerenciar
    tokens JWT invalidados no sistema.
    """
    
    @abstractmethod
    async def save(self, token: BlacklistedToken) -> BlacklistedToken:
        """
        Salva um token blacklisted.
        
        Args:
            token: Token a ser salvo
            
        Returns:
            BlacklistedToken: Token salvo
            
        Raises:
            Exception: Se houver erro na persistência
        """
        pass
    
    @abstractmethod
    async def find_by_jti(self, jti: str) -> Optional[BlacklistedToken]:
        """
        Busca um token pelo JTI.
        
        Args:
            jti: JWT ID para buscar
            
        Returns:
            Optional[BlacklistedToken]: Token encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, token_id: UUID) -> Optional[BlacklistedToken]:
        """
        Busca um token pelo ID.
        
        Args:
            token_id: ID do token
            
        Returns:
            Optional[BlacklistedToken]: Token encontrado ou None
        """
        pass
    
    @abstractmethod
    async def find_by_user_id(self, user_id: UUID) -> List[BlacklistedToken]:
        """
        Busca todos os tokens blacklisted de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            List[BlacklistedToken]: Lista de tokens do usuário
        """
        pass
    
    @abstractmethod
    async def is_token_blacklisted(self, jti: str) -> bool:
        """
        Verifica se um token está na blacklist.
        
        Args:
            jti: JWT ID para verificar
            
        Returns:
            bool: True se estiver blacklisted
        """
        pass
    
    @abstractmethod
    async def add_to_blacklist(self, token: BlacklistedToken) -> BlacklistedToken:
        """
        Adiciona um token à blacklist.
        
        Args:
            token: Token a ser adicionado
            
        Returns:
            BlacklistedToken: Token adicionado
            
        Raises:
            Exception: Se token já estiver na blacklist
        """
        pass
    
    @abstractmethod
    async def remove_from_blacklist(self, jti: str) -> bool:
        """
        Remove um token da blacklist.
        
        Args:
            jti: JWT ID do token a remover
            
        Returns:
            bool: True se removido com sucesso
        """
        pass
    
    @abstractmethod
    async def find_expired_tokens(self) -> List[BlacklistedToken]:
        """
        Busca todos os tokens expirados.
        
        Returns:
            List[BlacklistedToken]: Lista de tokens expirados
        """
        pass
    
    @abstractmethod
    async def cleanup_expired_tokens(self) -> int:
        """
        Remove tokens expirados da blacklist.
        
        Returns:
            int: Número de tokens removidos
        """
        pass
    
    @abstractmethod
    async def find_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[BlacklistedToken]:
        """
        Busca tokens blacklisted em um período.
        
        Args:
            start_date: Data inicial
            end_date: Data final
            
        Returns:
            List[BlacklistedToken]: Tokens no período
        """
        pass
    
    @abstractmethod
    async def count_all(self) -> int:
        """
        Conta total de tokens blacklisted.
        
        Returns:
            int: Número total de tokens
        """
        pass
    
    @abstractmethod
    async def count_by_user(self, user_id: UUID) -> int:
        """
        Conta tokens blacklisted de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            int: Número de tokens do usuário
        """
        pass
    
    @abstractmethod
    async def count_expired(self) -> int:
        """
        Conta tokens expirados.
        
        Returns:
            int: Número de tokens expirados
        """
        pass
    
    @abstractmethod
    async def find_recent_tokens(self, hours: int = 24) -> List[BlacklistedToken]:
        """
        Busca tokens blacklisted recentemente.
        
        Args:
            hours: Janela de tempo em horas
            
        Returns:
            List[BlacklistedToken]: Tokens recentes
        """
        pass
    
    @abstractmethod
    async def bulk_add_to_blacklist(self, tokens: List[BlacklistedToken]) -> List[BlacklistedToken]:
        """
        Adiciona múltiplos tokens à blacklist.
        
        Args:
            tokens: Lista de tokens a adicionar
            
        Returns:
            List[BlacklistedToken]: Tokens adicionados
        """
        pass
    
    @abstractmethod
    async def delete_all_by_user(self, user_id: UUID) -> int:
        """
        Remove todos os tokens de um usuário da blacklist.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            int: Número de tokens removidos
        """
        pass
    
    @abstractmethod
    async def exists(self, token_id: UUID) -> bool:
        """
        Verifica se um token existe.
        
        Args:
            token_id: ID do token
            
        Returns:
            bool: True se existe
        """
        pass
    
    @abstractmethod
    async def get_statistics(self) -> dict:
        """
        Obtém estatísticas da blacklist.
        
        Returns:
            dict: Estatísticas da blacklist
        """
        pass
