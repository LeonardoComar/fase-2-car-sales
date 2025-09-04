"""
Entidade BlacklistedToken - Domain Layer

Representa um token JWT invalidado (logout) no domínio.
Responsável pelas regras de negócio relacionadas a tokens blacklisted.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela representação de tokens invalidados
- OCP: Extensível para novas funcionalidades sem modificar existentes
- ISP: Interface limpa e específica
"""

from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


class BlacklistedToken:
    """
    Entidade de domínio para tokens JWT invalidados.
    
    Representa tokens que foram explicitamente invalidados
    através de logout ou por questões de segurança.
    """
    
    def __init__(
        self,
        jti: str,
        token: str,
        user_id: UUID,
        expires_at: datetime,
        token_id: Optional[UUID] = None,
        blacklisted_at: Optional[datetime] = None
    ):
        """
        Inicializa um token blacklisted.
        
        Args:
            jti: JWT ID único do token
            token: Token JWT completo
            user_id: ID do usuário que possui o token
            expires_at: Data de expiração natural do token
            token_id: ID único do registro (opcional)
            blacklisted_at: Data de blacklist (opcional, usa agora se não fornecido)
        """
        self.id = token_id or uuid4()
        self.jti = jti
        self.token = token
        self.user_id = user_id
        self.expires_at = expires_at
        self.blacklisted_at = blacklisted_at or datetime.utcnow()
        
        self._validate_token_data()
    
    def _validate_token_data(self) -> None:
        """Valida os dados do token blacklisted."""
        if not self.jti or not self.jti.strip():
            raise ValueError("JTI não pode ser vazio")
        
        if not self.token or not self.token.strip():
            raise ValueError("Token não pode ser vazio")
        
        if not self.user_id:
            raise ValueError("User ID é obrigatório")
        
        if not self.expires_at:
            raise ValueError("Data de expiração é obrigatória")
        
        if self.blacklisted_at > self.expires_at:
            raise ValueError("Data de blacklist não pode ser posterior à expiração")
    
    @classmethod
    def create_blacklisted_token(
        cls,
        jti: str,
        token: str,
        user_id: UUID,
        expires_at: datetime
    ) -> "BlacklistedToken":
        """
        Factory method para criar um token blacklisted.
        
        Args:
            jti: JWT ID único
            token: Token JWT completo
            user_id: ID do usuário
            expires_at: Data de expiração do token
            
        Returns:
            BlacklistedToken: Nova instância
            
        Raises:
            ValueError: Se dados inválidos
        """
        return cls(
            jti=jti,
            token=token,
            user_id=user_id,
            expires_at=expires_at
        )
    
    def is_expired(self) -> bool:
        """
        Verifica se o token já expirou naturalmente.
        
        Returns:
            bool: True se expirado
        """
        return datetime.utcnow() > self.expires_at
    
    def is_recently_blacklisted(self, minutes: int = 5) -> bool:
        """
        Verifica se o token foi blacklisted recentemente.
        
        Args:
            minutes: Janela de tempo em minutos
            
        Returns:
            bool: True se blacklisted nos últimos X minutos
        """
        from datetime import timedelta
        threshold = datetime.utcnow() - timedelta(minutes=minutes)
        return self.blacklisted_at > threshold
    
    def get_remaining_time(self) -> int:
        """
        Calcula o tempo restante até expiração natural.
        
        Returns:
            int: Segundos restantes (0 se já expirado)
        """
        if self.is_expired():
            return 0
        
        remaining = self.expires_at - datetime.utcnow()
        return max(0, int(remaining.total_seconds()))
    
    def should_be_cleaned(self) -> bool:
        """
        Verifica se o token pode ser removido da blacklist.
        
        Tokens expirados podem ser removidos da blacklist para economizar espaço.
        
        Returns:
            bool: True se pode ser removido
        """
        return self.is_expired()
    
    def get_summary(self) -> dict:
        """
        Retorna resumo do token blacklisted.
        
        Returns:
            dict: Informações resumidas
        """
        return {
            "id": str(self.id),
            "jti": self.jti,
            "user_id": str(self.user_id),
            "blacklisted_at": self.blacklisted_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "is_expired": self.is_expired(),
            "remaining_time_seconds": self.get_remaining_time(),
            "can_be_cleaned": self.should_be_cleaned()
        }
    
    def __str__(self) -> str:
        """Representação string do token blacklisted."""
        return f"BlacklistedToken(jti={self.jti}, user_id={self.user_id})"
    
    def __repr__(self) -> str:
        """Representação detalhada do token blacklisted."""
        return (
            f"BlacklistedToken("
            f"id={self.id}, "
            f"jti={self.jti}, "
            f"user_id={self.user_id}, "
            f"blacklisted_at={self.blacklisted_at}, "
            f"expires_at={self.expires_at})"
        )
    
    def __eq__(self, other) -> bool:
        """Igualdade baseada no JTI."""
        if not isinstance(other, BlacklistedToken):
            return False
        return self.jti == other.jti
    
    def __hash__(self) -> int:
        """Hash baseado no JTI."""
        return hash(self.jti)
