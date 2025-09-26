"""
Rotas administrativas para gerenciamento de tokens blacklistados.
Implements admin REST endpoints for JWT token blacklisting management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

from src.adapters.rest.dependencies import get_blacklisted_token_controller

blacklisted_token_router = APIRouter()


@blacklisted_token_router.get("/tokens/blacklisted/check/{token_id}")
async def check_token_blacklisted(
    token_id: str,
    controller=Depends(get_blacklisted_token_controller)
):
    """
    Verifica se um token está na blacklist (função administrativa).
    
    Args:
        token_id (str): ID do token para verificar
        controller: Controller de tokens blacklistados
        
    Returns:
        dict: Status do token (blacklistado ou não)
    """
    try:
        is_blacklisted = await controller.is_token_blacklisted(token_id)
        return {
            "token_id": token_id,
            "is_blacklisted": is_blacklisted,
            "checked_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao verificar token"
        )


@blacklisted_token_router.delete("/tokens/blacklisted/cleanup")
async def cleanup_expired_tokens(
    controller=Depends(get_blacklisted_token_controller)
):
    """
    Remove tokens expirados da blacklist (função administrativa).
    
    Args:
        controller: Controller de tokens blacklistados
        
    Returns:
        dict: Resultado da limpeza
    """
    try:
        result = await controller.cleanup_expired_tokens()
        return {
            "message": "Limpeza de tokens expirados realizada",
            "removed_count": result.get("removed_count", 0),
            "cleaned_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao limpar tokens expirados"
        )


@blacklisted_token_router.get("/tokens/blacklisted/stats")
async def get_blacklist_statistics(
    controller=Depends(get_blacklisted_token_controller)
):
    """
    Obtém estatísticas da blacklist de tokens (função administrativa).
    
    Args:
        controller: Controller de tokens blacklistados
        
    Returns:
        dict: Estatísticas da blacklist
    """
    try:
        stats = await controller.get_blacklist_statistics()
        return {
            "total_blacklisted": stats.get("total_count", 0),
            "active_blacklisted": stats.get("active_count", 0),
            "expired_count": stats.get("expired_count", 0),
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor ao obter estatísticas"
        )
