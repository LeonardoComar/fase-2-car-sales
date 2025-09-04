"""
Use Case para obter usuário atual - Application Layer

Responsável por extrair e validar informações do usuário
a partir do token JWT fornecido nas requisições.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela extração/validação de usuário atual
- OCP: Extensível para novas validações sem modificar o core
- DIP: Depende de abstrações (repositórios) não de implementações
"""

from typing import Optional
from uuid import UUID
import jwt

from src.domain.entities.user import User
from src.domain.ports.user_repository import UserRepository
from src.domain.ports.blacklisted_token_repository import BlacklistedTokenRepository


class GetCurrentUserUseCase:
    """
    Use Case para obter informações do usuário atual.
    
    Extrai informações do token JWT e valida se o usuário
    ainda existe e tem permissões adequadas.
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        blacklisted_token_repository: BlacklistedTokenRepository,
        secret_key: str
    ):
        """
        Inicializa o use case com dependências.
        
        Args:
            user_repository: Repositório de usuários
            blacklisted_token_repository: Repositório de tokens blacklisted
            secret_key: Chave secreta para decodificar JWT
        """
        self._user_repository = user_repository
        self._blacklisted_token_repository = blacklisted_token_repository
        self._secret_key = secret_key
    
    async def execute(self, token: str) -> User:
        """
        Obtém o usuário atual a partir do token.
        
        Args:
            token: Token JWT do usuário
            
        Returns:
            User: Dados do usuário atual
            
        Raises:
            Exception: Se token for inválido, usuário não existir, etc.
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
            
            # Extrair ID do usuário
            user_id_str = payload.get("sub")
            if not user_id_str:
                raise Exception("Token não contém ID do usuário")
            
            try:
                user_id = UUID(user_id_str)
            except ValueError:
                raise Exception("ID do usuário inválido no token")
            
            # Buscar usuário no repositório
            user = await self._user_repository.find_by_id(user_id)
            if not user:
                raise Exception("Usuário não encontrado")
            
            # Verificar se usuário está ativo
            if not user.is_active:
                raise Exception("Usuário inativo")
            
            return user
            
        except jwt.ExpiredSignatureError:
            raise Exception("Token expirado")
            
        except jwt.InvalidTokenError:
            raise Exception("Token inválido")
            
        except Exception as e:
            if "Token" in str(e) or "Usuário" in str(e):
                raise e
            raise Exception(f"Erro ao obter usuário atual: {str(e)}")


class GetCurrentAdminUserUseCase:
    """
    Use Case para obter usuário admin atual.
    
    Similar ao GetCurrentUserUseCase, mas valida se o usuário
    tem privilégios administrativos.
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        blacklisted_token_repository: BlacklistedTokenRepository,
        secret_key: str
    ):
        """
        Inicializa o use case com dependências.
        
        Args:
            user_repository: Repositório de usuários
            blacklisted_token_repository: Repositório de tokens blacklisted
            secret_key: Chave secreta para decodificar JWT
        """
        self._user_repository = user_repository
        self._blacklisted_token_repository = blacklisted_token_repository
        self._secret_key = secret_key
    
    async def execute(self, token: str) -> User:
        """
        Obtém o usuário admin atual a partir do token.
        
        Args:
            token: Token JWT do usuário
            
        Returns:
            User: Dados do usuário admin atual
            
        Raises:
            Exception: Se token for inválido, usuário não for admin, etc.
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
            
            # Extrair ID do usuário
            user_id_str = payload.get("sub")
            if not user_id_str:
                raise Exception("Token não contém ID do usuário")
            
            try:
                user_id = UUID(user_id_str)
            except ValueError:
                raise Exception("ID do usuário inválido no token")
            
            # Buscar usuário no repositório
            user = await self._user_repository.find_by_id(user_id)
            if not user:
                raise Exception("Usuário não encontrado")
            
            # Verificar se usuário está ativo
            if not user.is_active:
                raise Exception("Usuário inativo")
            
            # Verificar se usuário é admin
            if not user.is_admin:
                raise Exception("Usuário não tem privilégios administrativos")
            
            return user
            
        except jwt.ExpiredSignatureError:
            raise Exception("Token expirado")
            
        except jwt.InvalidTokenError:
            raise Exception("Token inválido")
            
        except Exception as e:
            if "Token" in str(e) or "Usuário" in str(e):
                raise e
            raise Exception(f"Erro ao obter usuário admin atual: {str(e)}")


class ExtractTokenPayloadUseCase:
    """
    Use Case para extrair payload de um token sem validar usuário.
    
    Útil para casos onde precisamos apenas das informações do token
    sem fazer validações completas de usuário.
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
    
    async def execute(self, token: str, verify_blacklist: bool = True) -> dict:
        """
        Extrai payload do token.
        
        Args:
            token: Token JWT
            verify_blacklist: Se deve verificar blacklist
            
        Returns:
            dict: Payload do token
            
        Raises:
            Exception: Se token for inválido ou blacklisted
        """
        try:
            # Decodificar token
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=["HS256"]
            )
            
            # Verificar blacklist se solicitado
            if verify_blacklist:
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
            if "Token" in str(e):
                raise e
            raise Exception(f"Erro ao extrair payload do token: {str(e)}")


class ValidateTokenPermissionsUseCase:
    """
    Use Case para validar permissões específicas de um token.
    
    Verifica se o usuário do token tem permissões específicas
    para executar determinadas operações.
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        blacklisted_token_repository: BlacklistedTokenRepository,
        secret_key: str
    ):
        """
        Inicializa o use case com dependências.
        
        Args:
            user_repository: Repositório de usuários
            blacklisted_token_repository: Repositório de tokens blacklisted
            secret_key: Chave secreta para decodificar JWT
        """
        self._user_repository = user_repository
        self._blacklisted_token_repository = blacklisted_token_repository
        self._secret_key = secret_key
    
    async def execute(
        self,
        token: str,
        required_admin: bool = False,
        required_active: bool = True
    ) -> tuple[User, dict]:
        """
        Valida permissões do token.
        
        Args:
            token: Token JWT
            required_admin: Se requer privilégios admin
            required_active: Se requer usuário ativo
            
        Returns:
            tuple[User, dict]: Usuário e payload do token
            
        Raises:
            Exception: Se token for inválido ou não tiver permissões
        """
        try:
            # Decodificar token
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=["HS256"]
            )
            
            # Verificar blacklist
            jti = payload.get("jti")
            if jti:
                is_blacklisted = await self._blacklisted_token_repository.is_token_blacklisted(jti)
                if is_blacklisted:
                    raise Exception("Token foi invalidado")
            
            # Extrair e validar user ID
            user_id_str = payload.get("sub")
            if not user_id_str:
                raise Exception("Token não contém ID do usuário")
            
            try:
                user_id = UUID(user_id_str)
            except ValueError:
                raise Exception("ID do usuário inválido no token")
            
            # Buscar usuário
            user = await self._user_repository.find_by_id(user_id)
            if not user:
                raise Exception("Usuário não encontrado")
            
            # Validar requisitos
            if required_active and not user.is_active:
                raise Exception("Usuário inativo")
            
            if required_admin and not user.is_admin:
                raise Exception("Usuário não tem privilégios administrativos")
            
            return user, payload
            
        except jwt.ExpiredSignatureError:
            raise Exception("Token expirado")
            
        except jwt.InvalidTokenError:
            raise Exception("Token inválido")
            
        except Exception as e:
            if "Token" in str(e) or "Usuário" in str(e):
                raise e
            raise Exception(f"Erro na validação de permissões: {str(e)}")
