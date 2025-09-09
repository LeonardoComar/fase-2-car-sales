from src.application.dtos.user_dto import UserResponseDto, TokenDto
from src.domain.entities.user import User
from typing import Optional


class UserPresenter:
    """
    Presenter para formatação de dados de usuário.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela apresentação dos dados de usuário.
    
    Aplicando o princípio Open/Closed Principle (OCP) - 
    aberto para extensão, fechado para modificação.
    """
    
    @staticmethod
    def present_user(user: User) -> dict:
        """
        Apresenta os dados de um objeto User como dict.
        
        Args:
            user: Entidade User do domínio
            
        Returns:
            dict: Dados do usuário formatados para API
        """
        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "employee_id": user.employee_id,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
    
    @staticmethod
    def present(user_response: UserResponseDto) -> UserResponseDto:
        """
        Apresenta os dados do usuário.
        
        Args:
            user_response: DTO com dados do usuário
            
        Returns:
            UserResponseDto: DTO formatado para apresentação
        """
        # Por enquanto apenas retorna o DTO, mas pode ser extendido
        # para formatação específica, ocultação de campos sensíveis, etc.
        return user_response
    
    @staticmethod
    def present_list(user_responses: list[UserResponseDto]) -> list[UserResponseDto]:
        """
        Apresenta uma lista de usuários.
        
        Args:
            user_responses: Lista de DTOs com dados dos usuários
            
        Returns:
            list[UserResponseDto]: Lista de DTOs formatados para apresentação
        """
        return [UserPresenter.present(user) for user in user_responses]
    
    @staticmethod
    def present_authentication(token_data: Optional[TokenDto]) -> Optional[dict]:
        """
        Apresenta os dados de autenticação.
        
        Args:
            token_data: DTO com dados do token
            
        Returns:
            Optional[dict]: Dados formatados para apresentação ou None se autenticação falhou
        """
        if token_data is None:
            return None
            
        return {
            "access_token": token_data.access_token,
            "token_type": token_data.token_type,
            "expires_in": token_data.expires_in
        }
