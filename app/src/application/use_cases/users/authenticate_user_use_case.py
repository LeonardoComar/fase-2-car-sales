from typing import Optional
from datetime import datetime, timedelta
import jwt
import uuid
from src.domain.entities.user import User
from src.domain.ports.user_repository import UserRepository
from src.application.dtos.user_dto import LoginDto, TokenDto
from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)


class AuthenticateUserUseCase:
    """
    Caso de uso para autenticação de usuário.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela autenticação e geração de tokens.
    """
    
    # Configurações JWT - em produção devem vir de variáveis de ambiente
    SECRET_KEY = "your-secret-key-here-change-in-production"  # Mudar em produção
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def execute(self, login: LoginDto) -> Optional[TokenDto]:
        """
        Executa o caso de uso de autenticação.
        
        Args:
            login: DTO com credenciais de login
            
        Returns:
            Optional[TokenDto]: Token de acesso ou None se autenticação falhar
            
        Raises:
            Exception: Para erros internos
        """
        try:
            # Autenticar usuário
            user = await self._authenticate_user(login)
            if not user:
                return None
            
            # Gerar token
            access_token, jti, expires_at = self._create_access_token(
                data={
                    "sub": user.id,
                    "email": user.email,
                    "role": user.role
                }
            )
            
            expires_in = int((expires_at - datetime.utcnow()).total_seconds())
            
            return TokenDto(
                access_token=access_token,
                token_type="bearer",
                expires_in=expires_in
            )
            
        except Exception as e:
            logger.error(f"Erro na autenticação: {str(e)}")
            raise Exception(f"Erro interno do servidor: {str(e)}")
    
    async def _authenticate_user(self, login: LoginDto) -> Optional[User]:
        """
        Autentica um usuário.
        
        Args:
            login: Credenciais de login
            
        Returns:
            Optional[User]: Usuário autenticado ou None
        """
        try:
            user = await self._user_repository.get_user_by_email(login.email)
            if not user or not self._verify_password(login.password, user.password):
                return None
            return user
            
        except Exception as e:
            logger.error(f"Erro na autenticação: {str(e)}")
            return None
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se a senha está correta.
        
        Args:
            plain_password: Senha em texto plano
            hashed_password: Hash da senha armazenada
            
        Returns:
            bool: True se a senha estiver correta
        """
        return self._pwd_context.verify(plain_password, hashed_password)
    
    def _create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> tuple[str, str, datetime]:
        """
        Cria um token JWT de acesso com JTI.
        
        Args:
            data: Dados a serem incluídos no token
            expires_delta: Tempo de expiração customizado
            
        Returns:
            tuple: (token, jti, expires_at)
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # Gerar JTI único
        jti = str(uuid.uuid4())
        
        to_encode.update({
            "exp": expire,
            "jti": jti  # JWT ID para identificar tokens únicos
        })
        
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt, jti, expire
