from typing import Optional
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.application.dtos.user_dto import UserCreateDto, UserResponseDto
from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    """
    Caso de uso para criação de usuário.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela criação de usuários.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende de abstrações (UserRepository) e não de implementações concretas.
    """
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def execute(self, user_create: UserCreateDto) -> UserResponseDto:
        """
        Executa o caso de uso de criação de usuário.
        
        Args:
            user_create: DTO com dados para criação do usuário
            
        Returns:
            UserResponseDto: Dados do usuário criado
            
        Raises:
            ValueError: Se email já estiver em uso ou dados inválidos
            Exception: Para outros erros
        """
        try:
            # Verificar se email já existe
            existing_user = await self._user_repository.get_user_by_email(user_create.email)
            if existing_user:
                raise ValueError("Email já está em uso")
            
            # Validar role
            if not User.is_valid_role(user_create.role):
                raise ValueError(f"Role inválida. Deve ser uma de: {', '.join(User.VALID_ROLES)}")
            
            # Criar usuário com senha hasheada
            hashed_password = self._hash_password(user_create.password)
            
            user = User.create_user(
                email=user_create.email,
                password_hash=hashed_password,
                role=user_create.role,
                employee_id=user_create.employee_id
            )
            
            created_user = await self._user_repository.create_user(user)
            
            return UserResponseDto(
                id=created_user.id,
                email=created_user.email,
                role=created_user.role,
                employee_id=created_user.employee_id,
                created_at=created_user.created_at,
                updated_at=created_user.updated_at
            )
            
        except ValueError as e:
            logger.error(f"Erro de validação ao criar usuário: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {str(e)}")
            raise Exception(f"Erro interno do servidor: {str(e)}")
    
    def _hash_password(self, password: str) -> str:
        """
        Gera hash da senha.
        
        Args:
            password: Senha em texto plano
            
        Returns:
            str: Hash da senha
        """
        return self._pwd_context.hash(password)
