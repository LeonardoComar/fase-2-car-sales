"""
Rotas REST para Users - Adapters Layer

Define os endpoints da API para gerenciamento de usuários e autenticação.
Aplicando padrões REST e Clean Architecture.
"""

from typing import Optional
from uuid import UUID
import logging

from fastapi import APIRouter, Depends, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse

# Configure logging
logger = logging.getLogger(__name__)

from src.application.dtos.user_dto import (
    UserCreateDto, UserUpdateDto, LoginDto
)
from src.adapters.rest.controllers.user_controller import UserController
from src.adapters.rest.dependencies import get_user_controller

# Configuração do bearer token para autenticação
security = HTTPBearer()


# Criar router para usuários
user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={
        404: {"description": "Usuário não encontrado"},
        422: {"description": "Regra de negócio violada"},
        500: {"description": "Erro interno do servidor"}
    }
)

# Router para autenticação
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        401: {"description": "Credenciais inválidas"},
        422: {"description": "Dados inválidos"},
        500: {"description": "Erro interno do servidor"}
    }
)


# === AUTENTICAÇÃO ===

@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Login de usuário",
    description="Autentica um usuário e retorna token de acesso"
)
async def login(
    credentials: LoginDto,
    controller: UserController = Depends(get_user_controller)
) -> JSONResponse:
    """
    Autentica um usuário no sistema.
    
    - **email**: Email do usuário
    - **password**: Senha do usuário
    
    Retorna token JWT para autenticação em requests subsequentes.
    """
    return await controller.authenticate_user(credentials)


@auth_router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout de usuário",
    description="Invalida o token de acesso do usuário"
)
async def logout(
    controller: UserController = Depends(get_user_controller)
) -> JSONResponse:
    """
    Invalida o token do usuário (adiciona à blacklist).
    
    Requer header: Authorization: Bearer {token}
    """
    return await controller.logout_user()


@auth_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Informações do usuário atual",
    description="Obtém informações do usuário autenticado"
)
async def get_current_user_info(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    controller: UserController = Depends(get_user_controller)
) -> JSONResponse:
    """
    Obtém informações do usuário atual baseado no token JWT.
    
    - **Authorization**: Header Bearer token
    
    Retorna dados do usuário autenticado.
    """
    try:
        logger.info("🚀 [AUTH_ENDPOINT] Iniciando endpoint /auth/me")
        logger.info(f"🔑 [AUTH_ENDPOINT] Credentials recebidas: {credentials}")
        logger.info(f"🔐 [AUTH_ENDPOINT] Scheme: {credentials.scheme}")
        logger.info(f"📋 [AUTH_ENDPOINT] Credentials type: {type(credentials.credentials)}")
        
        token = credentials.credentials
        logger.info(f"� [AUTH_ENDPOINT] Token extraído: '{token}'")
        logger.info(f"📐 [AUTH_ENDPOINT] Token length: {len(token) if token else 'None'}")
        logger.info(f"🔍 [AUTH_ENDPOINT] Token preview: {token[:50]}..." if len(token) > 50 else f"Token completo: '{token}'")
        
        result = await controller.get_current_user(token)
        logger.info("✅ [AUTH_ENDPOINT] Endpoint /auth/me concluído com sucesso")
        return result
        
    except Exception as e:
        logger.error(f"💥 [AUTH_ENDPOINT] Erro no endpoint /auth/me: {type(e).__name__}: {str(e)}", exc_info=True)
        raise


# === GERENCIAMENTO DE USUÁRIOS ===

@user_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Criar usuário",
    description="Cria um novo usuário no sistema"
)
async def create_user(
    user_data: UserCreateDto,
    controller: UserController = Depends(get_user_controller)
) -> JSONResponse:
    """
    Cria um novo usuário.
    
    - **email**: Email único do usuário
    - **password**: Senha (será hasheada)
    - **role**: Perfil do usuário (admin, manager, employee)
    - **employee_id**: ID do funcionário associado (opcional)
    """
    return await controller.create_user(user_data)


@user_router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Buscar usuário por ID",
    description="Busca um usuário específico pelo ID"
)
async def get_user_by_id(
    user_id: UUID,
    controller: UserController = Depends(get_user_controller)
) -> JSONResponse:
    """
    Busca um usuário pelo ID.
    
    - **user_id**: ID único do usuário (UUID)
    """
    return await controller.get_user_by_id(user_id)


@user_router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Listar usuários",
    description="Lista usuários com filtros e paginação"
)
async def list_users(
    email: Optional[str] = Query(None, description="Filtrar por email"),
    role: Optional[str] = Query(None, description="Filtrar por perfil"),
    employee_id: Optional[UUID] = Query(None, description="Filtrar por funcionário"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Tamanho da página"),
    controller: UserController = Depends(get_user_controller)
) -> JSONResponse:
    """
    Lista usuários com filtros opcionais e paginação.
    """
    search_data = {
        "email": email,
        "role": role,
        "employee_id": employee_id,
        "page": page,
        "page_size": page_size
    }
    return await controller.search_users(search_data)


@user_router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizar usuário",
    description="Atualiza os dados de um usuário existente"
)
async def update_user(
    user_id: UUID,
    user_data: UserUpdateDto,
    controller: UserController = Depends(get_user_controller)
) -> JSONResponse:
    """Atualiza os dados de um usuário."""
    return await controller.update_user(user_id, user_data)


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar usuário",
    description="Remove um usuário do sistema"
)
async def delete_user(
    user_id: UUID,
    controller: UserController = Depends(get_user_controller)
) -> JSONResponse:
    """Remove um usuário do sistema."""
    return await controller.delete_user(user_id)


@user_router.patch(
    "/{user_id}/change-password",
    status_code=status.HTTP_200_OK,
    summary="Alterar senha",
    description="Altera a senha de um usuário"
)
async def change_password(
    user_id: UUID,
    controller: UserController = Depends(get_user_controller)
) -> JSONResponse:
    """
    Altera a senha de um usuário.
    
    Requer senha atual e nova senha no body.
    """
    return await controller.change_password(user_id)
