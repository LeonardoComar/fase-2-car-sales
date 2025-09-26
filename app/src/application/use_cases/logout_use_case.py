"""
Use Case para Logout de Usuário - Application Layer

Responsável por invalidar tokens JWT quando um usuário faz logout.
Adiciona o token à blacklist para evitar reutilização.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela operação de logout
- OCP: Extensível para novas validações sem modificar o core
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from uuid import UUID
from datetime import datetime, timedelta
import jwt

from src.domain.entities.blacklisted_token import BlacklistedToken
from src.domain.ports.blacklisted_token_repository import BlacklistedTokenRepository


class LogoutUseCase:
    """
    Use Case para processar logout de usuário.
    
    Invalida o token JWT atual adicionando-o à blacklist.
    Garante que o token não possa ser reutilizado após logout.
    """
    
    def __init__(
        self,
        blacklisted_token_repository: BlacklistedTokenRepository,
        secret_key: str
    ):
        """
        Inicializa o use case com dependências.
        
        Args:
            blacklisted_token_repository: Repositório de tokens blacklisted
            secret_key: Chave secreta para decodificar JWT
        """
        self._blacklisted_token_repository = blacklisted_token_repository
        self._secret_key = secret_key
    
    async def execute(self, token: str, user_id: Optional[UUID] = None) -> bool:
        """
        Executa o logout invalidando o token.
        
        Args:
            token: Token JWT a ser invalidado
            user_id: ID do usuário (opcional, será extraído do token se não fornecido)
            
        Returns:
            bool: True se logout foi realizado com sucesso
            
        Raises:
            Exception: Se token for inválido ou já estiver na blacklist
        """
        try:
            # Decodificar o token para extrair informações
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=["HS256"],
                options={"verify_exp": False}  # Não verificar expiração aqui
            )
            
            # Extrair informações do payload
            jti = payload.get("jti")
            if not jti:
                raise Exception("Token não contém JTI (JWT ID)")
            
            # Usar user_id do parâmetro ou extrair do token
            token_user_id = user_id or UUID(payload.get("sub"))
            if not token_user_id:
                raise Exception("Não foi possível determinar o usuário do token")
            
            # Verificar se token já está na blacklist
            existing_token = await self._blacklisted_token_repository.find_by_jti(jti)
            if existing_token:
                raise Exception("Token já está invalidado")
            
            # Calcular expiração do token
            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                expires_at = datetime.fromtimestamp(exp_timestamp)
            else:
                # Se não tiver exp, usar expiração padrão (24 horas)
                expires_at = datetime.utcnow() + timedelta(hours=24)
            
            # Criar token blacklisted
            blacklisted_token = BlacklistedToken.create(
                jti=jti,
                user_id=token_user_id,
                expires_at=expires_at,
                reason="user_logout"
            )
            
            # Adicionar à blacklist
            await self._blacklisted_token_repository.add_to_blacklist(blacklisted_token)
            
            return True
            
        except jwt.ExpiredSignatureError:
            # Token já expirado, mas ainda pode ser útil adicioná-lo à blacklist
            # para evitar tentativas de uso
            raise Exception("Token expirado")
            
        except jwt.InvalidTokenError:
            raise Exception("Token inválido")
            
        except Exception as e:
            raise Exception(f"Erro durante logout: {str(e)}")


class LogoutAllTokensUseCase:
    """
    Use Case para invalidar todos os tokens de um usuário.
    
    Útil para logout forçado ou quando usuário quer desconectar
    de todos os dispositivos.
    """
    
    def __init__(
        self,
        blacklisted_token_repository: BlacklistedTokenRepository
    ):
        """
        Inicializa o use case com dependências.
        
        Args:
            blacklisted_token_repository: Repositório de tokens blacklisted
        """
        self._blacklisted_token_repository = blacklisted_token_repository
    
    async def execute(self, user_id: UUID, reason: str = "logout_all_devices") -> int:
        """
        Executa logout de todos os dispositivos do usuário.
        
        Args:
            user_id: ID do usuário
            reason: Motivo da invalidação
            
        Returns:
            int: Número de tokens adicionados à blacklist
            
        Note:
            Este método não pode invalidar tokens que ainda não foram
            blacklisted, apenas marca para invalidação futura.
            Para invalidação completa, seria necessário acesso ao
            repositório de tokens ativos.
        """
        try:
            # Por enquanto, esta implementação é limitada
            # pois não temos acesso a todos os tokens ativos do usuário
            # Apenas podemos contar tokens já blacklisted
            
            existing_tokens_count = await self._blacklisted_token_repository.count_by_user(user_id)
            
            # Em uma implementação completa, aqui buscaríamos todos
            # os tokens ativos do usuário em um repositório de sessões
            # e os adicionaríamos à blacklist
            
            return existing_tokens_count
            
        except Exception as e:
            raise Exception(f"Erro durante logout de todos os dispositivos: {str(e)}")


class ValidateTokenUseCase:
    """
    Use Case para validar se um token está válido e não blacklisted.
    
    Verifica se o token não está na blacklist antes de permitir acesso.
    """
    
    def __init__(
        self,
        blacklisted_token_repository: BlacklistedTokenRepository,
        secret_key: str
    ):
        """
        Inicializa o use case com dependências.
        
        Args:
            blacklisted_token_repository: Repositório de tokens blacklisted
            secret_key: Chave secreta para decodificar JWT
        """
        self._blacklisted_token_repository = blacklisted_token_repository
        self._secret_key = secret_key
    
    async def execute(self, token: str) -> dict:
        """
        Valida um token JWT.
        
        Args:
            token: Token JWT a ser validado
            
        Returns:
            dict: Payload do token se válido
            
        Raises:
            Exception: Se token for inválido, expirado ou blacklisted
        """
        try:
            # Decodificar e validar token
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=["HS256"]
            )
            
            # Verificar se token está na blacklist
            jti = payload.get("jti")
            if jti:
                is_blacklisted = await self._blacklisted_token_repository.is_token_blacklisted(jti)
                if is_blacklisted:
                    raise Exception("Token foi invalidado")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise Exception("Token expirado")
            
        except jwt.InvalidTokenError:
            raise Exception("Token inválido")
            
        except Exception as e:
            raise Exception(f"Erro na validação do token: {str(e)}")


class CleanupExpiredTokensUseCase:
    """
    Use Case para limpeza de tokens expirados da blacklist.
    
    Remove tokens que já expiraram naturalmente para
    manter a blacklist limpa e performática.
    """
    
    def __init__(
        self,
        blacklisted_token_repository: BlacklistedTokenRepository
    ):
        """
        Inicializa o use case com dependências.
        
        Args:
            blacklisted_token_repository: Repositório de tokens blacklisted
        """
        self._blacklisted_token_repository = blacklisted_token_repository
    
    async def execute(self) -> dict:
        """
        Executa limpeza de tokens expirados.
        
        Returns:
            dict: Estatísticas da limpeza
        """
        try:
            # Contar tokens antes da limpeza
            total_before = await self._blacklisted_token_repository.count_all()
            expired_before = await self._blacklisted_token_repository.count_expired()
            
            # Executar limpeza
            removed_count = await self._blacklisted_token_repository.cleanup_expired_tokens()
            
            # Contar tokens após limpeza
            total_after = await self._blacklisted_token_repository.count_all()
            
            return {
                "tokens_before_cleanup": total_before,
                "expired_tokens_found": expired_before,
                "tokens_removed": removed_count,
                "tokens_after_cleanup": total_after,
                "cleanup_successful": removed_count == expired_before
            }
            
        except Exception as e:
            raise Exception(f"Erro durante limpeza de tokens: {str(e)}")
