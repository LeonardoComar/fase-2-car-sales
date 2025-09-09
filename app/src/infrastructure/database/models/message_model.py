from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from src.infrastructure.database.connection import Base


class MessageModel(Base):
    """
    Modelo SQLAlchemy para Message.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela persistência dos dados de mensagem.
    """
    
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Relacionamentos
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=True, index=True)  # Pode ser atribuído depois
    
    # Dados da mensagem
    subject = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(50), nullable=False, index=True)  # "Duvida", "Interesse", "Reclamacao", etc.
    priority = Column(String(20), nullable=False, default="Media", index=True)  # "Baixa", "Media", "Alta"
    
    # Status
    status = Column(String(20), nullable=False, default="Pendente", index=True)  # "Pendente", "Em_andamento", "Respondida", "Fechada"
    is_read = Column(Boolean, nullable=False, default=False, index=True)
    
    # Dados de contato
    client_name = Column(String(100), nullable=False)
    client_email = Column(String(100), nullable=False, index=True)
    client_phone = Column(String(20))
    
    # Resposta
    response = Column(Text)
    response_date = Column(DateTime)
    
    # Auditoria
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<MessageModel(id={self.id}, subject='{self.subject}', status='{self.status}')>"
    
    def to_dict(self):
        """Converte o modelo para dicionário."""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "employee_id": self.employee_id,
            "subject": self.subject,
            "content": self.content,
            "message_type": self.message_type,
            "priority": self.priority,
            "status": self.status,
            "is_read": self.is_read,
            "client_name": self.client_name,
            "client_email": self.client_email,
            "client_phone": self.client_phone,
            "response": self.response,
            "response_date": self.response_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
