"""
Controller para gerenciamento de usuários - Adapters Layer

Aplicando Clean Architecture e SOLID Principles
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from src.application.dtos.user_dto import (
    UserCreateDto,
    UserUpdateDto,
    LoginDto
)
from src.application.use_cases.users import (
    CreateUserUseCase,
    GetUserUseCase,
    AuthenticateUserUseCase,
)
from src.adapters.rest.presenters.user_presenter import UserPresenter
from src.domain.exceptions import ValidationError, NotFoundError, BusinessRuleError


class UserController:
    """
    Controller para gerenciamento de usuários - Adapters Layer
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas por coordenar operações HTTP de usuários.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende de abstrações (use cases) e não de implementações.
    """
    
    def __init__(
        self,
        create_use_case: CreateUserUseCase,
        get_use_case: GetUserUseCase,
        authenticate_use_case: AuthenticateUserUseCase,
        user_presenter: UserPresenter
    ):
        self._create_use_case = create_use_case
        self._get_use_case = get_use_case
        self._authenticate_use_case = authenticate_use_case
        self._presenter = user_presenter

    async def create_user(self, user_data: UserCreateDto) -> JSONResponse:
        """
        Cria um novo usuário.
        
        Args:
            user_data: Dados para criação do usuário
            
        Returns:
            JSONResponse com dados do usuário criado
            
        Raises:
            HTTPException: Em caso de erro de validação ou regra de negócio
        """
        try:
            user = await self._create_use_case.execute(user_data)
            response_data = self._presenter.present_user(user)
            
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": "Usuário criado com sucesso",
                    "data": response_data
                }
            )
            
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
        except BusinessRuleError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def get_user_by_id(self, user_id: UUID) -> JSONResponse:
        """
        Busca um usuário pelo ID.
        
        Args:
            user_id: ID do usuário a ser buscado
            
        Returns:
            JSONResponse com dados do usuário
            
        Raises:
            HTTPException: Em caso de usuário não encontrado
        """
        try:
            user = await self._get_use_case.execute(user_id)
            response_data = self._presenter.present_user(user)
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Usuário encontrado com sucesso",
                    "data": response_data
                }
            )
            
        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def authenticate_user(self, credentials: LoginDto) -> JSONResponse:
        """
        Autentica um usuário.
        
        Args:
            credentials: Credenciais de login
            
        Returns:
            JSONResponse com token de autenticação
            
        Raises:
            HTTPException: Em caso de credenciais inválidas
        """
        try:
            auth_result = await self._authenticate_use_case.execute(credentials)
            
            if auth_result is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciais inválidas"
                )
            
            response_data = self._presenter.present_authentication(auth_result)
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Autenticação realizada com sucesso",
                    "data": response_data
                }
            )
            
        except HTTPException:
            raise
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )

    async def logout_user(self) -> JSONResponse:
        """
        Realiza logout do usuário (invalidando token).
        
        Returns:
            JSONResponse confirmando logout
        """
        try:
            # TODO: Implementar invalidação de token (blacklist)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Logout realizado com sucesso"
                }
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def search_users(self, search_dto: dict) -> JSONResponse:
        """
        Busca usuários com filtros.
        
        Args:
            search_dto: Filtros de busca
            
        Returns:
            JSONResponse com lista de usuários
        """
        try:
            # TODO: Implementar SearchUsersUseCase
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Busca de usuários não implementada",
                    "data": []
                }
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def update_user(self, user_id: UUID, user_data: UserUpdateDto) -> JSONResponse:
        """
        Atualiza um usuário existente.
        
        Args:
            user_id: ID do usuário a ser atualizado
            user_data: Dados para atualização
            
        Returns:
            JSONResponse com dados do usuário atualizado
        """
        try:
            # TODO: Implementar UpdateUserUseCase
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Atualização de usuário não implementada"
                }
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def delete_user(self, user_id: UUID) -> JSONResponse:
        """
        Remove um usuário do sistema.
        
        Args:
            user_id: ID do usuário a ser removido
            
        Returns:
            JSONResponse confirmando remoção
        """
        try:
            # TODO: Implementar DeleteUserUseCase
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Exclusão de usuário não implementada"
                }
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )

    async def change_password(self, user_id: UUID) -> JSONResponse:
        """
        Altera a senha de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            JSONResponse confirmando alteração de senha
        """
        try:
            # TODO: Implementar ChangePasswordUseCase
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Alteração de senha não implementada"
                }
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )
