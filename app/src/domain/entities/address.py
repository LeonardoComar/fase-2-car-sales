"""
Address Entity - Domain Layer

Entidade para gerenciamento de endereços seguindo Clean Architecture
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from src.domain.exceptions import ValidationError


@dataclass
class Address:
    """
    Entidade de domínio para endereços.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela lógica de negócio de endereços.
    """
    
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "Brasil"
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validações após inicialização"""
        self.validate()
    
    def validate(self) -> None:
        """
        Valida os dados do endereço.
        
        Raises:
            ValidationError: Se dados inválidos
        """
        if not self.street or len(self.street.strip()) < 5:
            raise ValidationError("Rua deve ter pelo menos 5 caracteres")
        
        if not self.city or len(self.city.strip()) < 2:
            raise ValidationError("Cidade deve ter pelo menos 2 caracteres")
        
        if not self.state or len(self.state.strip()) < 2:
            raise ValidationError("Estado deve ter pelo menos 2 caracteres")
        
        if not self.zip_code or len(self.zip_code.replace("-", "").strip()) != 8:
            raise ValidationError("CEP deve ter 8 dígitos")
        
        if not self.country or len(self.country.strip()) < 2:
            raise ValidationError("País deve ter pelo menos 2 caracteres")
    
    def get_full_address(self) -> str:
        """
        Retorna endereço completo formatado.
        
        Returns:
            str: Endereço completo
        """
        return f"{self.street}, {self.city} - {self.state}, {self.zip_code}, {self.country}"
    
    def format_zip_code(self) -> str:
        """
        Formata CEP com hífen.
        
        Returns:
            str: CEP formatado (12345-678)
        """
        clean_zip = self.zip_code.replace("-", "")
        if len(clean_zip) == 8:
            return f"{clean_zip[:5]}-{clean_zip[5:]}"
        return self.zip_code
    
    def is_same_city(self, other_address: 'Address') -> bool:
        """
        Verifica se é da mesma cidade.
        
        Args:
            other_address: Outro endereço para comparar
            
        Returns:
            bool: True se mesma cidade e estado
        """
        return (
            self.city.lower() == other_address.city.lower() and
            self.state.lower() == other_address.state.lower()
        )
