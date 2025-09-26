"""
Router de Autenticação - Driving Adapter

Define rotas FastAPI para operações de autenticação.
Conecta endpoints HTTP aos controllers de autenticação.

Aplicando princípios SOLID:
- SRP: Responsável apenas pelas rotas de autenticação
- OCP: Extensível para novas rotas sem modificar existentes
- DIP: Depende de abstrações (controllers, dependencies)
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from src.domain.entities.user import User
from src.adapters.rest.controllers.auth_controller import AuthController
from src.application.use_cases.logout_use_case import (
    LogoutUseCase,
    LogoutAllTokensUseCase,
    ValidateTokenUseCase,
    CleanupExpiredTokensUseCase
)
from src.application.use_cases.get_current_user_use_case import GetCurrentUserUseCase
from src.application.modules.auth_module import get_auth_module
from src.infrastructure.adapters.driving.auth_dependencies import (
    get_current_user,
    get_current_admin_user,
    extract_token_from_request,
    validate_token
)


def create_auth_router() -> APIRouter:
    """
    Cria e configura o router de autenticação.
    
    Returns:
        APIRouter: Router configurado com todas as rotas de autenticação
    """
    router = APIRouter(prefix="/auth", tags=["Authentication"])
    
    # Obter módulo de autenticação
    auth_module = get_auth_module()
    
    # Criar controller com use cases
    def get_auth_controller() -> AuthController:
        """Factory para criar controller de autenticação."""
        return AuthController(
            logout_use_case=auth_module.get_logout_use_case(),
            logout_all_tokens_use_case=auth_module.get_logout_all_tokens_use_case(),
            validate_token_use_case=auth_module.get_validate_token_use_case(),
            cleanup_expired_tokens_use_case=auth_module.get_cleanup_expired_tokens_use_case(),
            get_current_user_use_case=auth_module.get_current_user_use_case()
        )
    
    @router.post(
        "/logout",
        response_model=Dict[str, Any],
        status_code=status.HTTP_200_OK,
        summary="Logout do usuário",
        description="Invalida o token atual do usuário, realizando logout seguro."
    )
    async def logout_user(
        token: str = Depends(extract_token_from_request),
        current_user: User = Depends(get_current_user),
        controller: AuthController = Depends(get_auth_controller)
    ) -> Dict[str, Any]:
        """
        Realiza logout do usuário atual.
        
        - **token**: Token JWT atual a ser invalidado
        - **current_user**: Usuário autenticado
        
        Returns:
            Confirmação do logout com detalhes
        """
        return await controller.logout(token=token, current_user=current_user)
    
    @router.post(
        "/logout-all",
        response_model=Dict[str, Any],
        status_code=status.HTTP_200_OK,
        summary="Logout de todos os dispositivos",
        description="Invalida todos os tokens do usuário, desconectando de todos os dispositivos."
    )
    async def logout_all_devices(
        current_user: User = Depends(get_current_user),
        controller: AuthController = Depends(get_auth_controller)
    ) -> Dict[str, Any]:
        """
        Realiza logout de todos os dispositivos do usuário.
        
        - **current_user**: Usuário autenticado
        
        Returns:
            Confirmação do logout múltiplo
        """
        return await controller.logout_all_devices(current_user=current_user)
    
    @router.post(
        "/validate",
        response_model=Dict[str, Any],
        status_code=status.HTTP_200_OK,
        summary="Validar token",
        description="Valida se um token JWT ainda está válido e ativo."
    )
    async def validate_user_token(
        token: str = Depends(extract_token_from_request),
        controller: AuthController = Depends(get_auth_controller)
    ) -> Dict[str, Any]:
        """
        Valida um token JWT.
        
        - **token**: Token JWT a ser validado
        
        Returns:
            Informações sobre a validade do token
        """
        return await controller.validate_token(token=token)
    
    @router.get(
        "/me",
        response_model=Dict[str, Any],
        status_code=status.HTTP_200_OK,
        summary="Informações do usuário atual",
        description="Obtém informações detalhadas do usuário autenticado."
    )
    async def get_current_user_info(
        current_user: User = Depends(get_current_user),
        controller: AuthController = Depends(get_auth_controller)
    ) -> Dict[str, Any]:
        """
        Obtém informações do usuário atual.
        
        - **current_user**: Usuário autenticado
        
        Returns:
            Dados completos do usuário autenticado
        """
        return await controller.get_current_user_info(current_user=current_user)
    
    @router.post(
        "/refresh",
        response_model=Dict[str, Any],
        status_code=status.HTTP_200_OK,
        summary="Refresh token",
        description="Atualiza o token de acesso (funcionalidade placeholder)."
    )
    async def refresh_access_token(
        current_user: User = Depends(get_current_user),
        controller: AuthController = Depends(get_auth_controller)
    ) -> Dict[str, Any]:
        """
        Refresh do token de acesso.
        
        - **current_user**: Usuário autenticado
        
        Returns:
            Informações sobre refresh (placeholder)
            
        Note:
            Este endpoint é um placeholder. A implementação completa
            requereria um sistema de refresh tokens separado.
        """
        return await controller.refresh_token(current_user=current_user)
    
    @router.post(
        "/admin/cleanup-tokens",
        response_model=Dict[str, Any],
        status_code=status.HTTP_200_OK,
        summary="Limpeza de tokens expirados (Admin)",
        description="Remove tokens expirados da blacklist. Apenas para administradores."
    )
    async def cleanup_expired_tokens(
        admin_user: User = Depends(get_current_admin_user),
        controller: AuthController = Depends(get_auth_controller)
    ) -> Dict[str, Any]:
        """
        Limpa tokens expirados da blacklist.
        
        - **admin_user**: Usuário administrador autenticado
        
        Returns:
            Estatísticas da limpeza realizada
            
        Requires:
            Privilégios de administrador
        """
        return await controller.cleanup_expired_tokens(admin_user=admin_user)
    
    @router.get(
        "/status",
        response_model=Dict[str, Any],
        status_code=status.HTTP_200_OK,
        summary="Status do sistema de autenticação",
        description="Obtém informações sobre o status do sistema de autenticação."
    )
    async def get_auth_system_status(
        controller: AuthController = Depends(get_auth_controller)
    ) -> Dict[str, Any]:
        """
        Obtém status do sistema de autenticação.
        
        Returns:
            Informações sobre funcionalidades e versão do sistema
        """
        return await controller.get_auth_status()
    
    @router.get(
        "/health",
        response_model=Dict[str, Any],
        status_code=status.HTTP_200_OK,
        summary="Health check do sistema de autenticação",
        description="Verifica a saúde dos componentes de autenticação."
    )
    async def auth_health_check(
        controller: AuthController = Depends(get_auth_controller)
    ) -> Dict[str, Any]:
        """
        Health check do sistema de autenticação.
        
        Returns:
            Status de saúde dos componentes de autenticação
        """
        return await controller.check_health()
    
    return router


# Instância do router para ser usada na aplicação principal
auth_router = create_auth_router()
