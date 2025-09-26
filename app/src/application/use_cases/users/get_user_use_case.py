from typing import Optional
from src.domain.repositories.user_repository import UserRepository
from src.application.dtos.user_dto import UserResponseDto
import logging

logger = logging.getLogger(__name__)


class GetUserUseCase:
    """
    Caso de uso para buscar usuário por ID.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela busca de usuários por ID.
    """
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, user_id: int) -> Optional[UserResponseDto]:
        """
        Executa o caso de uso de busca de usuário por ID.
        
        Args:
            user_id: ID do usuário a ser buscado
            
        Returns:
            Optional[UserResponseDto]: Dados do usuário encontrado ou None
            
        Raises:
            ValueError: Se user_id for inválido
            Exception: Para outros erros
        """
        try:
            if user_id <= 0:
                raise ValueError("ID do usuário deve ser um número positivo")
            
            user = await self._user_repository.get_user_by_id(user_id)
            
            if not user:
                return None
            
            return UserResponseDto(
                id=user.id,
                email=user.email,
                role=user.role,
                employee_id=user.employee_id,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            
        except ValueError as e:
            logger.error(f"Erro de validação ao buscar usuário: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao buscar usuário: {str(e)}")
            raise Exception(f"Erro interno do servidor: {str(e)}")
