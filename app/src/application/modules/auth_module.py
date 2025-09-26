"""
Módulo de Configuração de Autenticação - Application Layer

Configura injeção de dependências para o módulo de autenticação.
Centralizava configuração de use cases e repositórios relacionados à autenticação.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela configuração do módulo de autenticação
- OCP: Extensível para novos casos de uso sem modificar existentes
- DIP: Configura dependências usando abstrações
"""

import os
from typing import Protocol

from src.domain.ports.user_repository import UserRepository
from src.domain.ports.blacklisted_token_repository import BlacklistedTokenRepository
from src.infrastructure.driven.mock_user_repository import MockUserRepository
from src.infrastructure.driven.mock_blacklisted_token_repository import MockBlacklistedTokenRepository
from src.application.use_cases.get_current_user_use_case import (
    GetCurrentUserUseCase,
    GetCurrentAdminUserUseCase,
    ValidateTokenPermissionsUseCase,
    ExtractTokenPayloadUseCase
)
from src.application.use_cases.logout_use_case import (
    LogoutUseCase,
    LogoutAllTokensUseCase,
    ValidateTokenUseCase,
    CleanupExpiredTokensUseCase
)


class AuthConfig(Protocol):
    """Protocol para configuração de autenticação."""
    
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class DefaultAuthConfig:
    """Configuração padrão de autenticação."""
    
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


class AuthModule:
    """
    Módulo de configuração de autenticação.
    
    Centraliza a criação e configuração de todos os use cases
    relacionados à autenticação e autorização.
    """
    
    def __init__(
        self,
        user_repository: UserRepository = None,
        blacklisted_token_repository: BlacklistedTokenRepository = None,
        config: AuthConfig = None
    ):
        """
        Inicializa o módulo de autenticação.
        
        Args:
            user_repository: Repositório de usuários (usa mock se não fornecido)
            blacklisted_token_repository: Repositório de tokens blacklisted (usa mock se não fornecido)
            config: Configuração de autenticação (usa padrão se não fornecida)
        """
        # Configuração
        self._config = config or DefaultAuthConfig()
        
        # Repositórios (usa implementações mock por padrão)
        self._user_repository = user_repository or MockUserRepository()
        self._blacklisted_token_repository = blacklisted_token_repository or MockBlacklistedTokenRepository()
        
        # Use cases de usuário atual
        self._get_current_user_use_case = None
        self._get_current_admin_user_use_case = None
        self._validate_token_permissions_use_case = None
        self._extract_token_payload_use_case = None
        
        # Use cases de logout
        self._logout_use_case = None
        self._logout_all_tokens_use_case = None
        self._validate_token_use_case = None
        self._cleanup_expired_tokens_use_case = None
    
    @property
    def config(self) -> AuthConfig:
        """Obtém configuração de autenticação."""
        return self._config
    
    @property
    def user_repository(self) -> UserRepository:
        """Obtém repositório de usuários."""
        return self._user_repository
    
    @property
    def blacklisted_token_repository(self) -> BlacklistedTokenRepository:
        """Obtém repositório de tokens blacklisted."""
        return self._blacklisted_token_repository
    
    def get_current_user_use_case(self) -> GetCurrentUserUseCase:
        """
        Obtém use case para buscar usuário atual.
        
        Returns:
            GetCurrentUserUseCase: Use case configurado
        """
        if self._get_current_user_use_case is None:
            self._get_current_user_use_case = GetCurrentUserUseCase(
                user_repository=self._user_repository,
                blacklisted_token_repository=self._blacklisted_token_repository,
                secret_key=self._config.secret_key
            )
        
        return self._get_current_user_use_case
    
    def get_current_admin_user_use_case(self) -> GetCurrentAdminUserUseCase:
        """
        Obtém use case para buscar usuário admin atual.
        
        Returns:
            GetCurrentAdminUserUseCase: Use case configurado
        """
        if self._get_current_admin_user_use_case is None:
            self._get_current_admin_user_use_case = GetCurrentAdminUserUseCase(
                user_repository=self._user_repository,
                blacklisted_token_repository=self._blacklisted_token_repository,
                secret_key=self._config.secret_key
            )
        
        return self._get_current_admin_user_use_case
    
    def get_validate_token_permissions_use_case(self) -> ValidateTokenPermissionsUseCase:
        """
        Obtém use case para validar permissões de token.
        
        Returns:
            ValidateTokenPermissionsUseCase: Use case configurado
        """
        if self._validate_token_permissions_use_case is None:
            self._validate_token_permissions_use_case = ValidateTokenPermissionsUseCase(
                user_repository=self._user_repository,
                blacklisted_token_repository=self._blacklisted_token_repository,
                secret_key=self._config.secret_key
            )
        
        return self._validate_token_permissions_use_case
    
    def get_extract_token_payload_use_case(self) -> ExtractTokenPayloadUseCase:
        """
        Obtém use case para extrair payload de token.
        
        Returns:
            ExtractTokenPayloadUseCase: Use case configurado
        """
        if self._extract_token_payload_use_case is None:
            self._extract_token_payload_use_case = ExtractTokenPayloadUseCase(
                blacklisted_token_repository=self._blacklisted_token_repository,
                secret_key=self._config.secret_key
            )
        
        return self._extract_token_payload_use_case
    
    def get_logout_use_case(self) -> LogoutUseCase:
        """
        Obtém use case para logout.
        
        Returns:
            LogoutUseCase: Use case configurado
        """
        if self._logout_use_case is None:
            self._logout_use_case = LogoutUseCase(
                blacklisted_token_repository=self._blacklisted_token_repository,
                secret_key=self._config.secret_key
            )
        
        return self._logout_use_case
    
    def get_logout_all_tokens_use_case(self) -> LogoutAllTokensUseCase:
        """
        Obtém use case para logout de todos os tokens.
        
        Returns:
            LogoutAllTokensUseCase: Use case configurado
        """
        if self._logout_all_tokens_use_case is None:
            self._logout_all_tokens_use_case = LogoutAllTokensUseCase(
                blacklisted_token_repository=self._blacklisted_token_repository
            )
        
        return self._logout_all_tokens_use_case
    
    def get_validate_token_use_case(self) -> ValidateTokenUseCase:
        """
        Obtém use case para validar token.
        
        Returns:
            ValidateTokenUseCase: Use case configurado
        """
        if self._validate_token_use_case is None:
            self._validate_token_use_case = ValidateTokenUseCase(
                blacklisted_token_repository=self._blacklisted_token_repository,
                secret_key=self._config.secret_key
            )
        
        return self._validate_token_use_case
    
    def get_cleanup_expired_tokens_use_case(self) -> CleanupExpiredTokensUseCase:
        """
        Obtém use case para limpeza de tokens expirados.
        
        Returns:
            CleanupExpiredTokensUseCase: Use case configurado
        """
        if self._cleanup_expired_tokens_use_case is None:
            self._cleanup_expired_tokens_use_case = CleanupExpiredTokensUseCase(
                blacklisted_token_repository=self._blacklisted_token_repository
            )
        
        return self._cleanup_expired_tokens_use_case


# Instância global do módulo de autenticação (singleton)
_auth_module = None


def get_auth_module() -> AuthModule:
    """
    Obtém instância singleton do módulo de autenticação.
    
    Returns:
        AuthModule: Módulo de autenticação configurado
    """
    global _auth_module
    if _auth_module is None:
        _auth_module = AuthModule()
    
    return _auth_module


def configure_auth_module(
    user_repository: UserRepository = None,
    blacklisted_token_repository: BlacklistedTokenRepository = None,
    config: AuthConfig = None
) -> AuthModule:
    """
    Configura o módulo de autenticação com dependências customizadas.
    
    Args:
        user_repository: Repositório de usuários customizado
        blacklisted_token_repository: Repositório de tokens blacklisted customizado
        config: Configuração customizada
        
    Returns:
        AuthModule: Módulo de autenticação configurado
    """
    global _auth_module
    _auth_module = AuthModule(
        user_repository=user_repository,
        blacklisted_token_repository=blacklisted_token_repository,
        config=config
    )
    
    return _auth_module


def reset_auth_module():
    """
    Reseta o módulo de autenticação.
    
    Útil para testes ou quando precisar reconfigurar completamente.
    """
    global _auth_module
    _auth_module = None


class AuthServiceProvider:
    """
    Provedor de serviços de autenticação.
    
    Facilita a obtenção de use cases configurados de forma consistente.
    """
    
    def __init__(self, auth_module: AuthModule = None):
        """
        Inicializa o provedor com módulo de autenticação.
        
        Args:
            auth_module: Módulo de autenticação (usa singleton se não fornecido)
        """
        self._auth_module = auth_module or get_auth_module()
    
    def get_current_user_service(self) -> GetCurrentUserUseCase:
        """Obtém serviço de usuário atual."""
        return self._auth_module.get_current_user_use_case()
    
    def get_admin_user_service(self) -> GetCurrentAdminUserUseCase:
        """Obtém serviço de usuário admin."""
        return self._auth_module.get_current_admin_user_use_case()
    
    def get_logout_service(self) -> LogoutUseCase:
        """Obtém serviço de logout."""
        return self._auth_module.get_logout_use_case()
    
    def get_token_validation_service(self) -> ValidateTokenUseCase:
        """Obtém serviço de validação de token."""
        return self._auth_module.get_validate_token_use_case()
    
    def get_cleanup_service(self) -> CleanupExpiredTokensUseCase:
        """Obtém serviço de limpeza."""
        return self._auth_module.get_cleanup_expired_tokens_use_case()
