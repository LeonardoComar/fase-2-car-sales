"""
Entidade Message - Domain Layer

Representa uma mensagem de contato/interesse em um veículo no sistema de vendas.
Aplicando os princípios da Clean Architecture:
- Independente de frameworks
- Independente de UI
- Independente de banco de dados
- Testável
- Independente de agentes externos

Aplicando princípios SOLID:
- SRP: Responsável apenas pela lógica de negócio de mensagens
- OCP: Aberto para extensão (novos status, validações)
- LSP: Pode ser substituída por implementações específicas
- ISP: Interface coesa sem métodos desnecessários
- DIP: Não depende de implementações concretas
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
import re


@dataclass
class Message:
    """
    Entidade Message representando uma mensagem de contato no domínio.
    
    Contém toda a lógica de negócio relacionada a mensagens de interesse
    em veículos, incluindo validações e regras de status.
    """
    
    # Constantes de Status
    STATUS_PENDENTE = "Pendente"
    STATUS_CONTATO_INICIADO = "Contato iniciado"
    STATUS_FINALIZADO = "Finalizado"
    STATUS_CANCELADO = "Cancelado"
    
    VALID_STATUSES = [
        STATUS_PENDENTE,
        STATUS_CONTATO_INICIADO,
        STATUS_FINALIZADO,
        STATUS_CANCELADO
    ]
    
    # Constantes de Validação
    MAX_NAME_LENGTH = 100
    MAX_EMAIL_LENGTH = 100
    MAX_PHONE_LENGTH = 50
    MAX_MESSAGE_LENGTH = 5000
    
    # Regex para validação de email
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    # Regex para validação de telefone brasileiro
    PHONE_PATTERN = re.compile(r'^\(\d{2}\)\s\d{4,5}-\d{4}$|^\d{10,11}$')
    
    # Atributos da entidade
    id: Optional[UUID] = field(default_factory=uuid4)
    responsible_id: Optional[UUID] = None
    vehicle_id: Optional[UUID] = None
    name: str = ""
    email: str = ""
    phone: Optional[str] = None
    message: str = ""
    status: str = field(default=STATUS_PENDENTE)
    service_start_time: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    @classmethod
    def create_message(cls, name: str, email: str, message: str, 
                      vehicle_id: Optional[UUID] = None, 
                      phone: Optional[str] = None) -> 'Message':
        """
        Factory method para criar uma nova mensagem.
        
        Args:
            name: Nome do interessado
            email: Email do interessado
            message: Mensagem/interesse
            vehicle_id: ID do veículo de interesse (opcional)
            phone: Telefone do interessado (opcional)
            
        Returns:
            Message: Nova instância de mensagem
            
        Raises:
            ValueError: Se dados inválidos
        """
        # Criar instância
        new_message = cls(
            name=name.strip(),
            email=email.strip().lower(),
            message=message.strip(),
            vehicle_id=vehicle_id,
            phone=phone.strip() if phone else None
        )
        
        # Validar dados
        new_message._validate_creation_data()
        
        return new_message
    
    def assign_responsible(self, responsible_id: UUID) -> None:
        """
        Atribui um responsável para a mensagem.
        
        Args:
            responsible_id: ID do funcionário responsável
            
        Raises:
            ValueError: Se mensagem já finalizada ou cancelada
        """
        if self.status in [self.STATUS_FINALIZADO, self.STATUS_CANCELADO]:
            raise ValueError(f"Não é possível atribuir responsável para mensagem com status '{self.status}'")
        
        self.responsible_id = responsible_id
        self.updated_at = datetime.utcnow()
    
    def start_service(self, responsible_id: UUID) -> None:
        """
        Inicia o atendimento da mensagem.
        
        Args:
            responsible_id: ID do funcionário responsável
            
        Raises:
            ValueError: Se mensagem não pode ser iniciada
        """
        if self.status != self.STATUS_PENDENTE:
            raise ValueError(f"Mensagem deve estar '{self.STATUS_PENDENTE}' para iniciar atendimento")
        
        self.responsible_id = responsible_id
        self.status = self.STATUS_CONTATO_INICIADO
        self.service_start_time = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def finish_service(self) -> None:
        """
        Finaliza o atendimento da mensagem.
        
        Raises:
            ValueError: Se mensagem não pode ser finalizada
        """
        if self.status not in [self.STATUS_PENDENTE, self.STATUS_CONTATO_INICIADO]:
            raise ValueError(f"Mensagem deve estar em atendimento para ser finalizada")
        
        if self.status == self.STATUS_PENDENTE:
            # Se ainda estava pendente, marcar horário de início
            self.service_start_time = datetime.utcnow()
        
        self.status = self.STATUS_FINALIZADO
        self.updated_at = datetime.utcnow()
    
    def cancel_message(self, reason: Optional[str] = None) -> None:
        """
        Cancela a mensagem.
        
        Args:
            reason: Motivo do cancelamento (opcional)
            
        Raises:
            ValueError: Se mensagem já finalizada
        """
        if self.status == self.STATUS_FINALIZADO:
            raise ValueError("Não é possível cancelar mensagem já finalizada")
        
        self.status = self.STATUS_CANCELADO
        self.updated_at = datetime.utcnow()
        
        # Adicionar motivo ao final da mensagem se fornecido
        if reason:
            self.message += f"\n\n[CANCELAMENTO: {reason}]"
    
    def update_contact_info(self, name: Optional[str] = None, 
                           email: Optional[str] = None, 
                           phone: Optional[str] = None) -> None:
        """
        Atualiza informações de contato.
        
        Args:
            name: Novo nome (opcional)
            email: Novo email (opcional)
            phone: Novo telefone (opcional)
            
        Raises:
            ValueError: Se dados inválidos ou mensagem finalizada
        """
        if self.status in [self.STATUS_FINALIZADO, self.STATUS_CANCELADO]:
            raise ValueError(f"Não é possível atualizar mensagem com status '{self.status}'")
        
        # Atualizar campos fornecidos
        if name is not None:
            self.name = name.strip()
            self._validate_name()
        
        if email is not None:
            self.email = email.strip().lower()
            self._validate_email()
        
        if phone is not None:
            self.phone = phone.strip() if phone else None
            if self.phone:
                self._validate_phone()
        
        self.updated_at = datetime.utcnow()
    
    def update_message_content(self, new_message: str) -> None:
        """
        Atualiza o conteúdo da mensagem.
        
        Args:
            new_message: Novo conteúdo da mensagem
            
        Raises:
            ValueError: Se mensagem finalizada ou conteúdo inválido
        """
        if self.status in [self.STATUS_FINALIZADO, self.STATUS_CANCELADO]:
            raise ValueError(f"Não é possível atualizar mensagem com status '{self.status}'")
        
        self.message = new_message.strip()
        self._validate_message_content()
        self.updated_at = datetime.utcnow()
    
    def is_pending(self) -> bool:
        """Verifica se a mensagem está pendente."""
        return self.status == self.STATUS_PENDENTE
    
    def is_in_service(self) -> bool:
        """Verifica se a mensagem está em atendimento."""
        return self.status == self.STATUS_CONTATO_INICIADO
    
    def is_finished(self) -> bool:
        """Verifica se a mensagem foi finalizada."""
        return self.status == self.STATUS_FINALIZADO
    
    def is_cancelled(self) -> bool:
        """Verifica se a mensagem foi cancelada."""
        return self.status == self.STATUS_CANCELADO
    
    def is_active(self) -> bool:
        """Verifica se a mensagem está ativa (não cancelada)."""
        return self.status != self.STATUS_CANCELADO
    
    def has_responsible(self) -> bool:
        """Verifica se a mensagem tem responsável atribuído."""
        return self.responsible_id is not None
    
    def has_vehicle(self) -> bool:
        """Verifica se a mensagem está relacionada a um veículo."""
        return self.vehicle_id is not None
    
    def get_service_duration_minutes(self) -> Optional[int]:
        """
        Calcula duração do atendimento em minutos.
        
        Returns:
            int: Duração em minutos ou None se não iniciado
        """
        if not self.service_start_time:
            return None
        
        end_time = datetime.utcnow()
        if self.is_finished():
            end_time = self.updated_at
        
        duration = end_time - self.service_start_time
        return int(duration.total_seconds() / 60)
    
    def _validate_creation_data(self) -> None:
        """Valida dados obrigatórios para criação."""
        self._validate_name()
        self._validate_email()
        self._validate_message_content()
        
        if self.phone:
            self._validate_phone()
    
    def _validate_name(self) -> None:
        """Valida o nome."""
        if not self.name or not self.name.strip():
            raise ValueError("Nome é obrigatório")
        
        if len(self.name) > self.MAX_NAME_LENGTH:
            raise ValueError(f"Nome deve ter no máximo {self.MAX_NAME_LENGTH} caracteres")
        
        # Verificar se contém apenas letras, espaços e acentos
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', self.name):
            raise ValueError("Nome deve conter apenas letras e espaços")
    
    def _validate_email(self) -> None:
        """Valida o email."""
        if not self.email or not self.email.strip():
            raise ValueError("Email é obrigatório")
        
        if len(self.email) > self.MAX_EMAIL_LENGTH:
            raise ValueError(f"Email deve ter no máximo {self.MAX_EMAIL_LENGTH} caracteres")
        
        if not self.EMAIL_PATTERN.match(self.email):
            raise ValueError("Formato de email inválido")
    
    def _validate_phone(self) -> None:
        """Valida o telefone."""
        if self.phone and len(self.phone) > self.MAX_PHONE_LENGTH:
            raise ValueError(f"Telefone deve ter no máximo {self.MAX_PHONE_LENGTH} caracteres")
        
        if self.phone and not self.PHONE_PATTERN.match(self.phone):
            raise ValueError("Formato de telefone inválido. Use (11) 99999-9999 ou 11999999999")
    
    def _validate_message_content(self) -> None:
        """Valida o conteúdo da mensagem."""
        if not self.message or not self.message.strip():
            raise ValueError("Mensagem é obrigatória")
        
        if len(self.message) > self.MAX_MESSAGE_LENGTH:
            raise ValueError(f"Mensagem deve ter no máximo {self.MAX_MESSAGE_LENGTH} caracteres")
    
    def _validate_status(self) -> None:
        """Valida o status."""
        if self.status not in self.VALID_STATUSES:
            raise ValueError(f"Status deve ser um de: {', '.join(self.VALID_STATUSES)}")
    
    def __post_init__(self):
        """Validações após inicialização."""
        if self.status not in self.VALID_STATUSES:
            self.status = self.STATUS_PENDENTE
        
        # Garantir que timestamps estejam definidos
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()
    
    def __str__(self) -> str:
        return f"Message(id={self.id}, name='{self.name}', status='{self.status}')"
    
    def __repr__(self) -> str:
        return (f"Message(id={self.id}, name='{self.name}', email='{self.email}', "
                f"status='{self.status}', created_at={self.created_at})")
