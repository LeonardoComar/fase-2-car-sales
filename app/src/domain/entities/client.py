from typing import Optional
from datetime import datetime, date
from dataclasses import dataclass
import re

from src.domain.exceptions import ValidationError, BusinessRuleError


@dataclass
class Client:
    """
    Entidade de domínio para Client.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela lógica de negócio de clientes.
    
    Aplicando o princípio Open/Closed Principle (OCP) - 
    aberta para extensão, fechada para modificação.
    """
    
    name: str
    email: str
    phone: str
    cpf: str
    birth_date: date
    address: str
    city: str
    state: str
    zip_code: str
    status: str = "Ativo"  # "Ativo", "Inativo", "Bloqueado"
    notes: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Status válidos para cliente
    VALID_STATUSES = ["Ativo", "Inativo", "Bloqueado"]
    
    # Estados válidos do Brasil
    VALID_STATES = [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]
    
    @classmethod
    def create_client(
        cls,
        name: str,
        email: str,
        phone: str,
        cpf: str,
        birth_date: date,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        notes: Optional[str] = None
    ) -> "Client":
        """
        Método factory para criar um cliente.
        
        Args:
            name: Nome completo do cliente
            email: Email do cliente
            phone: Telefone do cliente
            cpf: CPF do cliente
            birth_date: Data de nascimento
            address: Endereço completo
            city: Cidade
            state: Estado (sigla)
            zip_code: CEP
            notes: Observações opcionais
            
        Returns:
            Client: Nova instância de cliente
            
        Raises:
            ValidationError: Se os dados não forem válidos
            BusinessRuleError: Se as regras de negócio não forem atendidas
        """
        # Criar o cliente
        client = cls(
            name=name,
            email=email,
            phone=phone,
            cpf=cpf,
            birth_date=birth_date,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            notes=notes,
            status="Ativo"
        )
        
        # Validar dados
        client._validate_client_data()
        client._apply_business_rules()
        
        return client
    
    def update_client_data(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        zip_code: Optional[str] = None,
        status: Optional[str] = None,
        notes: Optional[str] = None
    ) -> None:
        """
        Atualiza dados do cliente.
        
        Args:
            Campos opcionais para atualização
            
        Raises:
            ValidationError: Se os dados não forem válidos
            BusinessRuleError: Se as regras de negócio não forem atendidas
        """
        if name is not None:
            self.name = name
        
        if email is not None:
            self.email = email
        
        if phone is not None:
            self.phone = phone
        
        if address is not None:
            self.address = address
        
        if city is not None:
            self.city = city
        
        if state is not None:
            self.state = state
        
        if zip_code is not None:
            self.zip_code = zip_code
        
        if status is not None:
            self.status = status
        
        if notes is not None:
            self.notes = notes
        
        # Revalidar após atualização
        self._validate_client_data()
        self._apply_business_rules()
        self.updated_at = datetime.now()
    
    def _validate_client_data(self) -> None:
        """
        Valida os dados do cliente.
        
        Raises:
            ValidationError: Se algum dado for inválido
        """
        # Validar nome
        if not self.name or len(self.name.strip()) < 2:
            raise ValidationError("Nome deve ter pelo menos 2 caracteres", "name")
        
        if len(self.name) > 100:
            raise ValidationError("Nome deve ter no máximo 100 caracteres", "name")
        
        # Validar email
        if not self.email:
            raise ValidationError("Email é obrigatório", "email")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValidationError("Email deve ter formato válido", "email")
        
        # Validar telefone
        if not self.phone:
            raise ValidationError("Telefone é obrigatório", "phone")
        
        # Remover caracteres não numéricos para validação
        phone_digits = re.sub(r'[^\d]', '', self.phone)
        if len(phone_digits) < 10 or len(phone_digits) > 11:
            raise ValidationError("Telefone deve ter 10 ou 11 dígitos", "phone")
        
        # Validar CPF
        if not self.cpf:
            raise ValidationError("CPF é obrigatório", "cpf")
        
        if not self._validate_cpf(self.cpf):
            raise ValidationError("CPF deve ter formato válido", "cpf")
        
        # Validar data de nascimento
        if not self.birth_date:
            raise ValidationError("Data de nascimento é obrigatória", "birth_date")
        
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        
        if age < 18:
            raise ValidationError("Cliente deve ser maior de idade", "birth_date")
        
        if age > 120:
            raise ValidationError("Data de nascimento inválida", "birth_date")
        
        # Validar endereço
        if not self.address or len(self.address.strip()) < 5:
            raise ValidationError("Endereço deve ter pelo menos 5 caracteres", "address")
        
        # Validar cidade
        if not self.city or len(self.city.strip()) < 2:
            raise ValidationError("Cidade deve ter pelo menos 2 caracteres", "city")
        
        # Validar estado
        if not self.state or self.state.upper() not in self.VALID_STATES:
            raise ValidationError(f"Estado deve ser uma sigla válida: {', '.join(self.VALID_STATES)}", "state")
        
        # Padronizar estado para maiúsculo
        self.state = self.state.upper()
        
        # Validar CEP
        if not self.zip_code:
            raise ValidationError("CEP é obrigatório", "zip_code")
        
        zip_digits = re.sub(r'[^\d]', '', self.zip_code)
        if len(zip_digits) != 8:
            raise ValidationError("CEP deve ter 8 dígitos", "zip_code")
        
        # Validar status
        if self.status not in self.VALID_STATUSES:
            raise ValidationError(f"Status deve ser um dos seguintes: {', '.join(self.VALID_STATUSES)}", "status")
        
        # Validar observações (se fornecidas)
        if self.notes and len(self.notes) > 1000:
            raise ValidationError("Observações devem ter no máximo 1000 caracteres", "notes")
    
    def _validate_cpf(self, cpf: str) -> bool:
        """
        Valida CPF usando algoritmo oficial.
        
        Args:
            cpf: CPF a ser validado
            
        Returns:
            bool: True se CPF válido
        """
        # Remove caracteres não numéricos
        cpf = re.sub(r'[^\d]', '', cpf)
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Validação do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        primeiro_digito = 11 - (soma % 11)
        if primeiro_digito >= 10:
            primeiro_digito = 0
        
        if int(cpf[9]) != primeiro_digito:
            return False
        
        # Validação do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        segundo_digito = 11 - (soma % 11)
        if segundo_digito >= 10:
            segundo_digito = 0
        
        return int(cpf[10]) == segundo_digito
    
    def _apply_business_rules(self) -> None:
        """
        Aplica regras de negócio específicas de clientes.
        
        Raises:
            BusinessRuleError: Se alguma regra de negócio for violada
        """
        # Regra: Verificar se é cliente VIP baseado na idade
        age = self.get_age()
        if age >= 65:
            # Cliente idoso - pode ter condições especiais
            pass
        
        # Regra: Validar formato do nome (deve ter pelo menos nome e sobrenome)
        name_parts = self.name.strip().split()
        if len(name_parts) < 2:
            raise BusinessRuleError(
                "Nome deve conter pelo menos nome e sobrenome",
                "incomplete_name"
            )
    
    def get_age(self) -> int:
        """
        Calcula a idade do cliente.
        
        Returns:
            int: Idade em anos
        """
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    def get_formatted_cpf(self) -> str:
        """
        Retorna CPF formatado.
        
        Returns:
            str: CPF no formato XXX.XXX.XXX-XX
        """
        cpf_digits = re.sub(r'[^\d]', '', self.cpf)
        return f"{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}"
    
    def get_formatted_phone(self) -> str:
        """
        Retorna telefone formatado.
        
        Returns:
            str: Telefone formatado
        """
        phone_digits = re.sub(r'[^\d]', '', self.phone)
        if len(phone_digits) == 11:
            return f"({phone_digits[:2]}) {phone_digits[2:7]}-{phone_digits[7:]}"
        else:
            return f"({phone_digits[:2]}) {phone_digits[2:6]}-{phone_digits[6:]}"
    
    def get_formatted_zip_code(self) -> str:
        """
        Retorna CEP formatado.
        
        Returns:
            str: CEP no formato XXXXX-XXX
        """
        zip_digits = re.sub(r'[^\d]', '', self.zip_code)
        return f"{zip_digits[:5]}-{zip_digits[5:]}"
    
    def is_active(self) -> bool:
        """
        Verifica se o cliente está ativo.
        
        Returns:
            bool: True se ativo
        """
        return self.status == "Ativo"
    
    def is_vip(self) -> bool:
        """
        Verifica se é cliente VIP (65+ anos).
        
        Returns:
            bool: True se VIP
        """
        return self.get_age() >= 65
    
    def can_make_purchase(self) -> bool:
        """
        Verifica se o cliente pode fazer compras.
        
        Returns:
            bool: True se pode fazer compras
        """
        return self.status in ["Ativo"]
    
    def get_full_address(self) -> str:
        """
        Retorna endereço completo formatado.
        
        Returns:
            str: Endereço completo
        """
        return f"{self.address}, {self.city} - {self.state}, {self.get_formatted_zip_code()}"
    
    def get_display_name(self) -> str:
        """
        Retorna nome de exibição do cliente.
        
        Returns:
            str: Nome formatado para exibição
        """
        return self.name.title()
    
    def __str__(self) -> str:
        return f"{self.get_display_name()} ({self.get_formatted_cpf()})"
