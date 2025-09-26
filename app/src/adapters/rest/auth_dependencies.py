"""
Dependências de Autenticação para Routers - Adapters Layer

Fornece dependências específicas para autenticação em routers REST.
Reutiliza as dependências robustas da infrastructure layer.
"""

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from src.domain.entities.user import User
from src.infrastructure.adapters.driving.auth_dependencies import (
    get_current_user as get_current_user_infrastructure
)

# Reutilizar a dependência da infrastructure layer diretamente
get_current_user = get_current_user_infrastructure


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency para verificar se o usuário atual é administrador.
    """
    if current_user.role != 'Administrador':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin role required."
        )
    return current_user


async def get_current_vendedor_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency para verificar se o usuário atual é vendedor.
    """
    if current_user.role != 'Vendedor':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Vendedor role required."
        )
    return current_user


async def get_current_admin_or_vendedor_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency para verificar se o usuário atual é administrador ou vendedor.
    """
    if current_user.role not in ['Administrador', 'Vendedor']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin or Vendedor role required."
        )
    return current_user


# Configuração do bearer token para funções opcionais
security = HTTPBearer()

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """
    Dependency para obter o usuário atual (opcional).
    Retorna None se não autenticado.
    """
    if not credentials:
        return None
    
    try:
        from src.infrastructure.adapters.driving.auth_dependencies import get_current_user_use_case
        
        get_user_use_case = get_current_user_use_case()
        user = await get_user_use_case.execute(credentials.credentials)
        return user
    except Exception:
        return None