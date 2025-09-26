"""
Exceções customizadas do domínio.

Aplicando o princípio Single Responsibility Principle (SRP) - 
cada exceção tem uma responsabilidade específica.
"""


class DomainError(Exception):
    """Exceção base para erros de domínio."""
    pass


class ValidationError(DomainError):
    """Exceção para erros de validação de dados."""
    
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(message)


class NotFoundError(DomainError):
    """Exceção para recursos não encontrados."""
    
    def __init__(self, resource: str, identifier: str = None):
        if identifier:
            message = f"{resource} com identificador '{identifier}' não foi encontrado"
        else:
            message = f"{resource} não foi encontrado"
        super().__init__(message)


class BusinessRuleError(DomainError):
    """Exceção para violações de regras de negócio."""
    
    def __init__(self, message: str, rule: str = None):
        self.message = message
        self.rule = rule
        super().__init__(message)


class AuthenticationError(DomainError):
    """Exceção para erros de autenticação."""
    pass


class AuthorizationError(DomainError):
    """Exceção para erros de autorização."""
    pass


class DuplicateError(DomainError):
    """Exceção para recursos duplicados."""
    
    def __init__(self, resource: str, field: str = None, value: str = None):
        if field and value:
            message = f"{resource} com {field} '{value}' já existe"
        else:
            message = f"{resource} já existe"
        super().__init__(message)


class InvalidStateError(DomainError):
    """Exceção para estados inválidos."""
    
    def __init__(self, current_state: str, expected_state: str = None):
        if expected_state:
            message = f"Estado atual '{current_state}' é inválido. Estado esperado: '{expected_state}'"
        else:
            message = f"Estado atual '{current_state}' é inválido"
        super().__init__(message)


class PreconditionError(DomainError):
    """Exceção para precondições não atendidas."""
    
    def __init__(self, message: str, precondition: str = None):
        self.message = message
        self.precondition = precondition
        super().__init__(message)


class ConcurrencyError(DomainError):
    """Exceção para problemas de concorrência."""
    pass


class ExternalServiceError(DomainError):
    """Exceção para erros de serviços externos."""
    
    def __init__(self, service: str, message: str = None):
        self.service = service
        if message:
            full_message = f"Erro no serviço externo '{service}': {message}"
        else:
            full_message = f"Erro no serviço externo '{service}'"
        super().__init__(full_message)


# Exceções específicas para entidades
class EmployeeNotFoundError(NotFoundError):
    """Exceção para funcionário não encontrado."""
    
    def __init__(self, identifier: str = None):
        super().__init__("Funcionário", identifier)


class EmployeeAlreadyExistsError(DuplicateError):
    """Exceção para funcionário já existente."""
    
    def __init__(self, field: str = None, value: str = None):
        super().__init__("Funcionário", field, value)


class MessageNotFoundError(NotFoundError):
    """Exceção para mensagem não encontrada."""
    
    def __init__(self, identifier: str = None):
        super().__init__("Mensagem", identifier)


class SaleNotFoundError(NotFoundError):
    """Exceção para venda não encontrada."""
    
    def __init__(self, identifier: str = None):
        super().__init__("Venda", identifier)


class DatabaseError(DomainError):
    """Exceção para erros de banco de dados."""
    
    def __init__(self, message: str = "Erro de banco de dados"):
        super().__init__(message)
