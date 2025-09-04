"""
Implementação Mock do BlacklistedTokenRepository - Infrastructure Layer

Simula operações de persistência para tokens blacklisted em memória.
Útil para testes e desenvolvimento inicial.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela persistência mock de tokens blacklisted
- OCP: Extensível para novas operações sem modificar existentes
- LSP: Pode substituir qualquer implementação do repositório
- ISP: Implementa interface específica do repositório
- DIP: Implementa abstração definida no domínio
"""

from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime, timedelta
import asyncio

from src.domain.entities.blacklisted_token import BlacklistedToken
from src.domain.ports.blacklisted_token_repository import BlacklistedTokenRepository


class MockBlacklistedTokenRepository(BlacklistedTokenRepository):
    """
    Implementação mock do repositório de tokens blacklisted.
    
    Armazena dados em memória com simulação de operações assíncronas.
    Mantém integridade referencial e regras de negócio.
    """
    
    def __init__(self):
        """Inicializa o repositório com dados em memória."""
        self._tokens: Dict[UUID, BlacklistedToken] = {}
        self._jti_index: Dict[str, UUID] = {}
        self._user_index: Dict[UUID, List[UUID]] = {}
        
        # Não populamos dados iniciais para tokens blacklisted
        # pois eles são criados apenas quando necessário
    
    async def save(self, token: BlacklistedToken) -> BlacklistedToken:
        """
        Salva um token blacklisted no repositório.
        
        Args:
            token: Token a ser salvo
            
        Returns:
            BlacklistedToken: Token salvo
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        # Atualizar timestamp se necessário
        if token.id not in self._tokens:
            if not token.blacklisted_at:
                token.blacklisted_at = datetime.utcnow()
        
        # Salvar
        self._tokens[token.id] = token
        
        # Atualizar índices
        self._jti_index[token.jti] = token.id
        
        if token.user_id not in self._user_index:
            self._user_index[token.user_id] = []
        if token.id not in self._user_index[token.user_id]:
            self._user_index[token.user_id].append(token.id)
        
        return token
    
    async def find_by_jti(self, jti: str) -> Optional[BlacklistedToken]:
        """
        Busca um token pelo JTI.
        
        Args:
            jti: JWT ID para buscar
            
        Returns:
            Optional[BlacklistedToken]: Token encontrado ou None
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        token_id = self._jti_index.get(jti)
        if token_id:
            return self._tokens.get(token_id)
        
        return None
    
    async def find_by_id(self, token_id: UUID) -> Optional[BlacklistedToken]:
        """
        Busca um token pelo ID.
        
        Args:
            token_id: ID do token
            
        Returns:
            Optional[BlacklistedToken]: Token encontrado ou None
        """
        await asyncio.sleep(0.01)  # Simular latência
        return self._tokens.get(token_id)
    
    async def find_by_user_id(self, user_id: UUID) -> List[BlacklistedToken]:
        """
        Busca todos os tokens blacklisted de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            List[BlacklistedToken]: Lista de tokens do usuário
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        token_ids = self._user_index.get(user_id, [])
        tokens = []
        
        for token_id in token_ids:
            token = self._tokens.get(token_id)
            if token:
                tokens.append(token)
        
        return tokens
    
    async def is_token_blacklisted(self, jti: str) -> bool:
        """
        Verifica se um token está na blacklist.
        
        Args:
            jti: JWT ID para verificar
            
        Returns:
            bool: True se estiver blacklisted
        """
        await asyncio.sleep(0.01)  # Simular latência
        return jti in self._jti_index
    
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
        await asyncio.sleep(0.01)  # Simular latência
        
        # Verificar se já existe
        if token.jti in self._jti_index:
            raise Exception(f"Token com JTI '{token.jti}' já está na blacklist")
        
        return await self.save(token)
    
    async def remove_from_blacklist(self, jti: str) -> bool:
        """
        Remove um token da blacklist.
        
        Args:
            jti: JWT ID do token a remover
            
        Returns:
            bool: True se removido com sucesso
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        token_id = self._jti_index.get(jti)
        if not token_id:
            return False
        
        token = self._tokens.get(token_id)
        if not token:
            return False
        
        # Remover dos índices
        if jti in self._jti_index:
            del self._jti_index[jti]
        
        if token.user_id in self._user_index:
            if token_id in self._user_index[token.user_id]:
                self._user_index[token.user_id].remove(token_id)
                
                # Se lista ficou vazia, remover o usuário do índice
                if not self._user_index[token.user_id]:
                    del self._user_index[token.user_id]
        
        # Remover token
        del self._tokens[token_id]
        
        return True
    
    async def find_expired_tokens(self) -> List[BlacklistedToken]:
        """
        Busca todos os tokens expirados.
        
        Returns:
            List[BlacklistedToken]: Lista de tokens expirados
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        now = datetime.utcnow()
        expired_tokens = []
        
        for token in self._tokens.values():
            if token.expires_at < now:
                expired_tokens.append(token)
        
        return expired_tokens
    
    async def cleanup_expired_tokens(self) -> int:
        """
        Remove tokens expirados da blacklist.
        
        Returns:
            int: Número de tokens removidos
        """
        await asyncio.sleep(0.02)  # Simular operação mais complexa
        
        expired_tokens = await self.find_expired_tokens()
        removed_count = 0
        
        for token in expired_tokens:
            success = await self.remove_from_blacklist(token.jti)
            if success:
                removed_count += 1
        
        return removed_count
    
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
        await asyncio.sleep(0.01)  # Simular latência
        
        tokens_in_range = []
        
        for token in self._tokens.values():
            if start_date <= token.blacklisted_at <= end_date:
                tokens_in_range.append(token)
        
        return tokens_in_range
    
    async def count_all(self) -> int:
        """
        Conta total de tokens blacklisted.
        
        Returns:
            int: Número total de tokens
        """
        await asyncio.sleep(0.01)  # Simular latência
        return len(self._tokens)
    
    async def count_by_user(self, user_id: UUID) -> int:
        """
        Conta tokens blacklisted de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            int: Número de tokens do usuário
        """
        await asyncio.sleep(0.01)  # Simular latência
        return len(self._user_index.get(user_id, []))
    
    async def count_expired(self) -> int:
        """
        Conta tokens expirados.
        
        Returns:
            int: Número de tokens expirados
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        now = datetime.utcnow()
        expired_count = 0
        
        for token in self._tokens.values():
            if token.expires_at < now:
                expired_count += 1
        
        return expired_count
    
    async def find_recent_tokens(self, hours: int = 24) -> List[BlacklistedToken]:
        """
        Busca tokens blacklisted recentemente.
        
        Args:
            hours: Janela de tempo em horas
            
        Returns:
            List[BlacklistedToken]: Tokens recentes
        """
        await asyncio.sleep(0.01)  # Simular latência
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        recent_tokens = []
        
        for token in self._tokens.values():
            if token.blacklisted_at >= cutoff_time:
                recent_tokens.append(token)
        
        return recent_tokens
    
    async def bulk_add_to_blacklist(self, tokens: List[BlacklistedToken]) -> List[BlacklistedToken]:
        """
        Adiciona múltiplos tokens à blacklist.
        
        Args:
            tokens: Lista de tokens a adicionar
            
        Returns:
            List[BlacklistedToken]: Tokens adicionados
        """
        await asyncio.sleep(0.02)  # Simular operação em lote
        
        added_tokens = []
        
        for token in tokens:
            try:
                added_token = await self.add_to_blacklist(token)
                added_tokens.append(added_token)
            except Exception:
                # Ignorar tokens que já estão na blacklist
                pass
        
        return added_tokens
    
    async def delete_all_by_user(self, user_id: UUID) -> int:
        """
        Remove todos os tokens de um usuário da blacklist.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            int: Número de tokens removidos
        """
        await asyncio.sleep(0.02)  # Simular operação complexa
        
        user_tokens = await self.find_by_user_id(user_id)
        removed_count = 0
        
        for token in user_tokens:
            success = await self.remove_from_blacklist(token.jti)
            if success:
                removed_count += 1
        
        return removed_count
    
    async def exists(self, token_id: UUID) -> bool:
        """
        Verifica se um token existe.
        
        Args:
            token_id: ID do token
            
        Returns:
            bool: True se existe
        """
        await asyncio.sleep(0.01)  # Simular latência
        return token_id in self._tokens
    
    async def get_statistics(self) -> dict:
        """
        Obtém estatísticas da blacklist.
        
        Returns:
            dict: Estatísticas da blacklist
        """
        await asyncio.sleep(0.05)  # Simular query complexa
        
        total_tokens = await self.count_all()
        expired_tokens = await self.count_expired()
        active_tokens = total_tokens - expired_tokens
        
        # Contar por usuário
        users_with_tokens = len(self._user_index)
        
        # Contar tokens recentes (últimas 24h)
        recent_tokens = await self.find_recent_tokens(24)
        recent_count = len(recent_tokens)
        
        # Calcular distribuição por tempo
        now = datetime.utcnow()
        distribution = {
            "last_hour": 0,
            "last_24_hours": 0,
            "last_week": 0,
            "older": 0
        }
        
        for token in self._tokens.values():
            age = now - token.blacklisted_at
            
            if age.total_seconds() <= 3600:  # 1 hora
                distribution["last_hour"] += 1
            elif age.total_seconds() <= 86400:  # 24 horas
                distribution["last_24_hours"] += 1
            elif age.days <= 7:  # 1 semana
                distribution["last_week"] += 1
            else:
                distribution["older"] += 1
        
        return {
            "total_blacklisted_tokens": total_tokens,
            "active_blacklisted_tokens": active_tokens,
            "expired_blacklisted_tokens": expired_tokens,
            "users_with_blacklisted_tokens": users_with_tokens,
            "recent_blacklisted_tokens_24h": recent_count,
            "tokens_by_time_period": distribution,
            "cleanup_recommended": expired_tokens > 0
        }
