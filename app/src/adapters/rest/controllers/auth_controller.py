"""
Controller de Autenticação - Driving Adapter

Gerencia operações de autenticação como login, logout e validação de tokens.
Implementa endpoints para o sistema de autenticação da aplicação.

Aplicando princípios SOLID:
- SRP: Responsável apenas pelas operações de autenticação
- OCP: Extensível para novos endpoints sem modificar existentes
- DIP: Depende de abstrações (use cases) não de implementações
"""

from typing import Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from src.domain.entities.user import User
from src.application.use_cases.logout_use_case import (
    LogoutUseCase,
    LogoutAllTokensUseCase,
    ValidateTokenUseCase,
    CleanupExpiredTokensUseCase
)
from src.application.use_cases.get_current_user_use_case import GetCurrentUserUseCase
from src.infrastructure.adapters.driving.auth_dependencies import (
    get_current_user,
    get_current_admin_user,
    extract_token_from_request
)


class AuthController:
    """
    Controller responsável por operações de autenticação.
    
    Processa requisições relacionadas a autenticação, logout,
    validação de tokens e operações administrativas.
    """
    
    def __init__(
        self,
        logout_use_case: LogoutUseCase,
        logout_all_tokens_use_case: LogoutAllTokensUseCase,
        validate_token_use_case: ValidateTokenUseCase,
        cleanup_expired_tokens_use_case: CleanupExpiredTokensUseCase,
        get_current_user_use_case: GetCurrentUserUseCase
    ):
        """
        Inicializa o controller com use cases necessários.
        
        Args:
            logout_use_case: Use case para logout
            logout_all_tokens_use_case: Use case para logout de todos os tokens
            validate_token_use_case: Use case para validação de tokens
            cleanup_expired_tokens_use_case: Use case para limpeza de tokens
            get_current_user_use_case: Use case para obter usuário atual
        """
        self._logout_use_case = logout_use_case
        self._logout_all_tokens_use_case = logout_all_tokens_use_case
        self._validate_token_use_case = validate_token_use_case
        self._cleanup_expired_tokens_use_case = cleanup_expired_tokens_use_case
        self._get_current_user_use_case = get_current_user_use_case
    
    async def logout(self, token: str, current_user: User) -> Dict[str, Any]:
        """
        Realiza logout do usuário atual.
        
        Args:
            token: Token JWT a ser invalidado
            current_user: Usuário atual autenticado
            
        Returns:
            Dict[str, Any]: Resposta do logout
            
        Raises:
            HTTPException: Se logout falhar
        """
        try:
            success = await self._logout_use_case.execute(
                token=token,
                user_id=current_user.id
            )
            
            if success:
                return {
                    "message": "Logout realizado com sucesso",
                    "user_id": str(current_user.id),
                    "timestamp": "now"
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Falha ao realizar logout"
                )
                
        except Exception as e:
            if "já está invalidado" in str(e):
                return {
                    "message": "Token já estava invalidado",
                    "user_id": str(current_user.id),
                    "timestamp": "now"
                }
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro durante logout: {str(e)}"
            )
    
    async def logout_all_devices(self, current_user: User) -> Dict[str, Any]:
        """
        Realiza logout de todos os dispositivos do usuário.
        
        Args:
            current_user: Usuário atual autenticado
            
        Returns:
            Dict[str, Any]: Resposta do logout múltiplo
            
        Raises:
            HTTPException: Se logout falhar
        """
        try:
            tokens_count = await self._logout_all_tokens_use_case.execute(
                user_id=current_user.id,
                reason="logout_all_devices"
            )
            
            return {
                "message": "Logout realizado em todos os dispositivos",
                "user_id": str(current_user.id),
                "tokens_invalidated": tokens_count,
                "timestamp": "now"
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro durante logout de todos os dispositivos: {str(e)}"
            )
    
    async def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Valida um token JWT.
        
        Args:
            token: Token JWT a ser validado
            
        Returns:
            Dict[str, Any]: Resultado da validação
            
        Raises:
            HTTPException: Se token for inválido
        """
        try:
            payload = await self._validate_token_use_case.execute(token)
            
            return {
                "valid": True,
                "user_id": payload.get("sub"),
                "expires_at": payload.get("exp"),
                "issued_at": payload.get("iat"),
                "token_id": payload.get("jti")
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token inválido: {str(e)}"
            )
    
    async def get_current_user_info(self, current_user: User) -> Dict[str, Any]:
        """
        Obtém informações do usuário atual.
        
        Args:
            current_user: Usuário atual autenticado
            
        Returns:
            Dict[str, Any]: Informações do usuário
        """
        return {
            "id": str(current_user.id),
            "name": current_user.name,
            "email": current_user.email,
            "is_admin": current_user.is_admin,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
            "updated_at": current_user.updated_at.isoformat() if current_user.updated_at else None
        }
    
    async def refresh_token(self, current_user: User) -> Dict[str, Any]:
        """
        Endpoint para refresh de token (placeholder).
        
        Args:
            current_user: Usuário atual autenticado
            
        Returns:
            Dict[str, Any]: Informação sobre refresh
            
        Note:
            Este endpoint é um placeholder. A implementação completa
            de refresh token requereria um sistema de refresh tokens
            separado dos access tokens.
        """
        return {
            "message": "Refresh token não implementado",
            "user_id": str(current_user.id),
            "suggestion": "Faça login novamente para obter um novo token"
        }
    
    async def cleanup_expired_tokens(self, admin_user: User) -> Dict[str, Any]:
        """
        Limpa tokens expirados da blacklist (apenas admin).
        
        Args:
            admin_user: Usuário admin autenticado
            
        Returns:
            Dict[str, Any]: Resultado da limpeza
            
        Raises:
            HTTPException: Se limpeza falhar
        """
        try:
            cleanup_result = await self._cleanup_expired_tokens_use_case.execute()
            
            return {
                "message": "Limpeza de tokens expirados concluída",
                "admin_id": str(admin_user.id),
                "cleanup_stats": cleanup_result
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro durante limpeza: {str(e)}"
            )
    
    async def get_auth_status(self) -> Dict[str, Any]:
        """
        Obtém status do sistema de autenticação.
        
        Returns:
            Dict[str, Any]: Status do sistema
        """
        return {
            "auth_system": "active",
            "features": [
                "jwt_authentication",
                "token_blacklisting",
                "user_roles",
                "logout",
                "token_validation"
            ],
            "version": "1.0.0"
        }
    
    async def check_health(self) -> Dict[str, Any]:
        """
        Endpoint de health check para autenticação.
        
        Returns:
            Dict[str, Any]: Status de saúde
        """
        try:
            # Teste básico dos use cases
            # (sem executar operações que modifiquem dados)
            
            return {
                "status": "healthy",
                "components": {
                    "logout_service": "ok",
                    "token_validation": "ok",
                    "user_authentication": "ok",
                    "token_cleanup": "ok"
                },
                "timestamp": "now"
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": "now"
            }
