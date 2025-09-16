"""
Entidade Message - Domain Layer

Entidade que representa uma mensagem no domínio da aplicação.

Aplicando princípios SOLID:
- SRP: Responsável apenas por representar e validar dados de mensagens
- OCP: Extensível para novas funcionalidades sem modificar código existente
- LSP: Pode ser substituída por especializações
- ISP: Interface específica e coesa
- DIP: Não depende de detalhes de implementação
"""

from typing import Optional
from datetime import datetime


class Message:
    """
    Entidade Message que representa uma mensagem no domínio da aplicação.
    """
    
    # Status possíveis para mensagens
    STATUS_PENDENTE = "Pendente"
    STATUS_CONTATO_INICIADO = "Contato iniciado"
    STATUS_FINALIZADO = "Finalizado"
    STATUS_CANCELADO = "Cancelado"
    
    VALID_STATUSES = [STATUS_PENDENTE, STATUS_CONTATO_INICIADO, STATUS_FINALIZADO, STATUS_CANCELADO]

    def __init__(
        self,
        name: str,
        email: str,
        message: str,
        phone: Optional[str] = None,
        vehicle_id: Optional[int] = None,
        responsible_id: Optional[int] = None,
        status: str = STATUS_PENDENTE,
        service_start_time: Optional[datetime] = None,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Inicializa uma nova mensagem.
        
        Args:
            name: Nome do remetente
            email: Email do remetente
            message: Conteúdo da mensagem
            phone: Telefone do remetente (opcional)
            vehicle_id: ID do veículo relacionado (opcional)
            responsible_id: ID do funcionário responsável (opcional)
            status: Status da mensagem
            service_start_time: Data/hora de início do atendimento (opcional)
            id: ID da mensagem (opcional, para entidades já persistidas)
            created_at: Data de criação (opcional)
            updated_at: Data de atualização (opcional)
        """
        # Validações de negócio
        if not name or len(name.strip()) == 0:
            raise ValueError("Nome é obrigatório")
        
        if not email or len(email.strip()) == 0:
            raise ValueError("Email é obrigatório")
        
        if not message or len(message.strip()) == 0:
            raise ValueError("Mensagem é obrigatória")
        
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status deve ser um dos valores: {', '.join(self.VALID_STATUSES)}")
        
        # Validação de email básica
        if "@" not in email:
            raise ValueError("Email deve ter um formato válido")
        
        # Atribuições
        self._id = id
        self._name = name.strip()
        self._email = email.strip().lower()
        self._phone = phone.strip() if phone else None
        self._message = message.strip()
        self._vehicle_id = vehicle_id
        self._responsible_id = responsible_id
        self._status = status
        self._service_start_time = service_start_time
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or datetime.utcnow()
    
    # Properties (getters)
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def phone(self) -> Optional[str]:
        return self._phone
    
    @property
    def message(self) -> str:
        return self._message
    
    @property
    def vehicle_id(self) -> Optional[int]:
        return self._vehicle_id
    
    @property
    def responsible_id(self) -> Optional[int]:
        return self._responsible_id
    
    @property
    def status(self) -> str:
        return self._status
    
    @property
    def service_start_time(self) -> Optional[datetime]:
        return self._service_start_time
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    # Métodos de negócio
    def start_service(self, responsible_id: int) -> None:
        """
        Inicia o atendimento da mensagem.
        
        Args:
            responsible_id: ID do funcionário responsável pelo atendimento
        """
        if self._responsible_id is not None:
            raise ValueError("Mensagem já possui responsável atribuído")
        
        if self._status != self.STATUS_PENDENTE:
            raise ValueError(f"Só é possível iniciar atendimento de mensagens com status '{self.STATUS_PENDENTE}'")
        
        self._responsible_id = responsible_id
        self._service_start_time = datetime.utcnow()
        self._status = self.STATUS_CONTATO_INICIADO
        self._updated_at = datetime.utcnow()
    
    def update_status(self, new_status: str) -> None:
        """
        Atualiza o status da mensagem.
        
        Args:
            new_status: Novo status da mensagem
        """
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Status deve ser um dos valores: {', '.join(self.VALID_STATUSES)}")
        
        self._status = new_status
        self._updated_at = datetime.utcnow()
    
    def finish_service(self) -> None:
        """
        Finaliza o atendimento da mensagem.
        """
        if self._responsible_id is None:
            raise ValueError("Não é possível finalizar uma mensagem sem responsável atribuído")
        
        if self._status in [self.STATUS_FINALIZADO, self.STATUS_CANCELADO]:
            raise ValueError(f"Mensagem já está finalizada ou cancelada")
        
        self._status = self.STATUS_FINALIZADO
        self._updated_at = datetime.utcnow()
    
    def cancel_service(self) -> None:
        """
        Cancela o atendimento da mensagem.
        """
        if self._status == self.STATUS_CANCELADO:
            raise ValueError("Mensagem já está cancelada")
        
        self._status = self.STATUS_CANCELADO
        self._updated_at = datetime.utcnow()
    
    def __eq__(self, other) -> bool:
        """Verifica igualdade entre duas mensagens."""
        if not isinstance(other, Message):
            return False
        return self._id is not None and self._id == other._id
    
    def __hash__(self) -> int:
        """Hash baseado no ID da mensagem."""
        return hash(self._id) if self._id else hash((self._email, self._created_at))
    
    def __str__(self) -> str:
        """Representação string da mensagem."""
        return f"Message(id={self._id}, name='{self._name}', status='{self._status}')"
    
    def __repr__(self) -> str:
        """Representação detalhada da mensagem."""
        return (f"Message(id={self._id}, name='{self._name}', email='{self._email}', "
                f"status='{self._status}', vehicle_id={self._vehicle_id}, "
                f"responsible_id={self._responsible_id})")
