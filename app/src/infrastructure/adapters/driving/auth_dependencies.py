"""
Dependências de Autenticação - Infrastructure Layer

Fornece dependências FastAPI para autenticação e autorização.
Implementa decoradores e funções para validação de tokens JWT.

Aplicando princípios SOLID:
- SRP: Responsável apenas pelas dependências de autenticação
- OCP: Extensível para novos tipos de autenticação
- DIP: Depende de abstrações (use cases) não de implementações
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

from src.domain.entities.user import User
from src.application.use_cases.get_current_user_use_case import (
    GetCurrentUserUseCase,
    GetCurrentAdminUserUseCase,
    ValidateTokenPermissionsUseCase
)
from src.application.use_cases.logout_use_case import ValidateTokenUseCase
from src.infrastructure.driven.mock_user_repository import MockUserRepository
from src.infrastructure.driven.mock_blacklisted_token_repository import MockBlacklistedTokenRepository


# Configuração do esquema de autenticação
security = HTTPBearer()

# Chave secreta para JWT (em produção, deve vir de variável de ambiente)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

# Instâncias dos repositórios (singleton pattern para mock)
_user_repository = None
_blacklisted_token_repository = None


def get_user_repository() -> MockUserRepository:
    """
    Fornece instância singleton do repositório de usuários.
    
    Returns:
        MockUserRepository: Repositório de usuários
    """
    global _user_repository
    if _user_repository is None:
        _user_repository = MockUserRepository()
    return _user_repository


def get_blacklisted_token_repository() -> MockBlacklistedTokenRepository:
    """
    Fornece instância singleton do repositório de tokens blacklisted.
    
    Returns:
        MockBlacklistedTokenRepository: Repositório de tokens blacklisted
    """
    global _blacklisted_token_repository
    if _blacklisted_token_repository is None:
        _blacklisted_token_repository = MockBlacklistedTokenRepository()
    return _blacklisted_token_repository


def get_current_user_use_case(
    user_repository: MockUserRepository = Depends(get_user_repository),
    blacklisted_token_repository: MockBlacklistedTokenRepository = Depends(get_blacklisted_token_repository)
) -> GetCurrentUserUseCase:
    """
    Fornece use case para obter usuário atual.
    
    Args:
        user_repository: Repositório de usuários
        blacklisted_token_repository: Repositório de tokens blacklisted
        
    Returns:
        GetCurrentUserUseCase: Use case configurado
    """
    return GetCurrentUserUseCase(
        user_repository=user_repository,
        blacklisted_token_repository=blacklisted_token_repository,
        secret_key=SECRET_KEY
    )


def get_current_admin_user_use_case(
    user_repository: MockUserRepository = Depends(get_user_repository),
    blacklisted_token_repository: MockBlacklistedTokenRepository = Depends(get_blacklisted_token_repository)
) -> GetCurrentAdminUserUseCase:
    """
    Fornece use case para obter usuário admin atual.
    
    Args:
        user_repository: Repositório de usuários
        blacklisted_token_repository: Repositório de tokens blacklisted
        
    Returns:
        GetCurrentAdminUserUseCase: Use case configurado
    """
    return GetCurrentAdminUserUseCase(
        user_repository=user_repository,
        blacklisted_token_repository=blacklisted_token_repository,
        secret_key=SECRET_KEY
    )


def get_validate_token_use_case(
    blacklisted_token_repository: MockBlacklistedTokenRepository = Depends(get_blacklisted_token_repository)
) -> ValidateTokenUseCase:
    """
    Fornece use case para validar tokens.
    
    Args:
        blacklisted_token_repository: Repositório de tokens blacklisted
        
    Returns:
        ValidateTokenUseCase: Use case configurado
    """
    return ValidateTokenUseCase(
        blacklisted_token_repository=blacklisted_token_repository,
        secret_key=SECRET_KEY
    )


def get_validate_permissions_use_case(
    user_repository: MockUserRepository = Depends(get_user_repository),
    blacklisted_token_repository: MockBlacklistedTokenRepository = Depends(get_blacklisted_token_repository)
) -> ValidateTokenPermissionsUseCase:
    """
    Fornece use case para validar permissões.
    
    Args:
        user_repository: Repositório de usuários
        blacklisted_token_repository: Repositório de tokens blacklisted
        
    Returns:
        ValidateTokenPermissionsUseCase: Use case configurado
    """
    return ValidateTokenPermissionsUseCase(
        user_repository=user_repository,
        blacklisted_token_repository=blacklisted_token_repository,
        secret_key=SECRET_KEY
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    get_user_use_case: GetCurrentUserUseCase = Depends(get_current_user_use_case)
) -> User:
    """
    Dependência FastAPI para obter usuário atual autenticado.
    
    Args:
        credentials: Credenciais HTTP Bearer
        get_user_use_case: Use case para obter usuário atual
        
    Returns:
        User: Usuário autenticado
        
    Raises:
        HTTPException: Se autenticação falhar
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acesso requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user = await get_user_use_case.execute(credentials.credentials)
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    get_admin_use_case: GetCurrentAdminUserUseCase = Depends(get_current_admin_user_use_case)
) -> User:
    """
    Dependência FastAPI para obter usuário admin atual.
    
    Args:
        credentials: Credenciais HTTP Bearer
        get_admin_use_case: Use case para obter usuário admin
        
    Returns:
        User: Usuário admin autenticado
        
    Raises:
        HTTPException: Se autenticação/autorização falhar
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acesso requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        admin_user = await get_admin_use_case.execute(credentials.credentials)
        return admin_user
        
    except Exception as e:
        if "privilégios administrativos" in str(e):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )


async def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    validate_use_case: ValidateTokenUseCase = Depends(get_validate_token_use_case)
) -> dict:
    """
    Dependência FastAPI para validar token sem buscar usuário.
    
    Args:
        credentials: Credenciais HTTP Bearer
        validate_use_case: Use case para validar token
        
    Returns:
        dict: Payload do token validado
        
    Raises:
        HTTPException: Se token for inválido
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acesso requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = await validate_use_case.execute(credentials.credentials)
        return payload
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    get_user_use_case: GetCurrentUserUseCase = Depends(get_current_user_use_case)
) -> Optional[User]:
    """
    Dependência FastAPI para obter usuário atual opcional.
    
    Retorna None se não houver token ou se token for inválido,
    em vez de levantar exceção.
    
    Args:
        credentials: Credenciais HTTP Bearer (opcional)
        get_user_use_case: Use case para obter usuário atual
        
    Returns:
        Optional[User]: Usuário autenticado ou None
    """
    if not credentials:
        return None
    
    try:
        user = await get_user_use_case.execute(credentials.credentials)
        return user
        
    except Exception:
        return None


def require_permissions(admin_required: bool = False, active_required: bool = True):
    """
    Factory para criar dependências que requerem permissões específicas.
    
    Args:
        admin_required: Se requer privilégios admin
        active_required: Se requer usuário ativo
        
    Returns:
        Função de dependência configurada
    """
    async def permission_dependency(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        validate_permissions_use_case: ValidateTokenPermissionsUseCase = Depends(get_validate_permissions_use_case)
    ) -> User:
        """
        Dependência que valida permissões específicas.
        
        Args:
            credentials: Credenciais HTTP Bearer
            validate_permissions_use_case: Use case para validar permissões
            
        Returns:
            User: Usuário com permissões validadas
            
        Raises:
            HTTPException: Se não tiver permissões necessárias
        """
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de acesso requerido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        try:
            user, _ = await validate_permissions_use_case.execute(
                token=credentials.credentials,
                required_admin=admin_required,
                required_active=active_required
            )
            return user
            
        except Exception as e:
            if "privilégios administrativos" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=str(e)
                )
            elif "inativo" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=str(e)
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=str(e),
                    headers={"WWW-Authenticate": "Bearer"},
                )
    
    return permission_dependency


# Dependências pré-configuradas para uso comum
require_admin = require_permissions(admin_required=True, active_required=True)
require_active_user = require_permissions(admin_required=False, active_required=True)


async def extract_token_from_request(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Extrai o token das credenciais HTTP.
    
    Args:
        credentials: Credenciais HTTP Bearer
        
    Returns:
        str: Token JWT
        
    Raises:
        HTTPException: Se token não estiver presente
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acesso requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials
