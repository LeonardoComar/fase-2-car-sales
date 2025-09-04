from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class MotorVehicle:
    """
    Entidade base MotorVehicle do domínio - representa um veículo motorizado no sistema.
    
    Esta entidade contém a lógica de negócio comum a todos os veículos motorizados.
    Aplicando o princípio Single Responsibility Principle (SRP) do SOLID.
    """
    
    # Status possíveis para veículos
    STATUS_ATIVO = "Ativo"
    STATUS_INATIVO = "Inativo" 
    STATUS_VENDIDO = "Vendido"
    STATUS_RESERVADO = "Reservado"
    STATUS_MANUTENCAO = "Em Manutenção"
    
    VALID_STATUSES = [STATUS_ATIVO, STATUS_INATIVO, STATUS_VENDIDO, STATUS_RESERVADO, STATUS_MANUTENCAO]
    
    # Tipos de combustível válidos
    VALID_FUEL_TYPES = [
        "Gasolina", "Etanol", "Flex", "Diesel", "GNV", "Elétrico", "Híbrido"
    ]

    id: Optional[int] = None
    model: str = ""
    year: str = ""
    mileage: int = 0
    fuel_type: str = ""
    color: str = ""
    city: str = ""
    additional_description: Optional[str] = None
    price: Decimal = Decimal('0.00')
    status: str = STATUS_ATIVO
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validações após a inicialização"""
        if self.price and self.price <= 0:
            raise ValueError("Preço deve ser maior que zero")
        
        if self.mileage and self.mileage < 0:
            raise ValueError("Quilometragem não pode ser negativa")
        
        if self.status and not self.is_valid_status(self.status):
            raise ValueError(f"Status inválido. Deve ser um de: {', '.join(self.VALID_STATUSES)}")
        
        if self.fuel_type and not self.is_valid_fuel_type(self.fuel_type):
            raise ValueError(f"Tipo de combustível inválido. Deve ser um de: {', '.join(self.VALID_FUEL_TYPES)}")

    @classmethod
    def create_motor_vehicle(
        cls, 
        model: str, 
        year: str, 
        mileage: int, 
        fuel_type: str,
        color: str, 
        city: str, 
        price: Decimal, 
        additional_description: Optional[str] = None,
        status: str = None
    ) -> 'MotorVehicle':
        """
        Método de classe para criar um veículo motorizado.
        
        Args:
            model: Modelo do veículo
            year: Ano do veículo
            mileage: Quilometragem
            fuel_type: Tipo de combustível
            color: Cor do veículo
            city: Cidade onde está o veículo
            price: Preço do veículo
            additional_description: Descrição adicional (opcional)
            status: Status do veículo (opcional, padrão é ATIVO)
            
        Returns:
            MotorVehicle: Nova instância de veículo motorizado
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        if status is None:
            status = cls.STATUS_ATIVO
            
        if price <= 0:
            raise ValueError("Preço deve ser maior que zero")
        
        if mileage < 0:
            raise ValueError("Quilometragem não pode ser negativa")
        
        if not cls.is_valid_status(status):
            raise ValueError(f"Status inválido. Deve ser um de: {', '.join(cls.VALID_STATUSES)}")
        
        if not cls.is_valid_fuel_type(fuel_type):
            raise ValueError(f"Tipo de combustível inválido. Deve ser um de: {', '.join(cls.VALID_FUEL_TYPES)}")
        
        return cls(
            model=model,
            year=year,
            mileage=mileage,
            fuel_type=fuel_type,
            color=color,
            city=city,
            price=price,
            additional_description=additional_description,
            status=status,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    @classmethod
    def is_valid_status(cls, status: str) -> bool:
        """
        Verifica se o status é válido.
        
        Args:
            status: Status a ser validado
            
        Returns:
            bool: True se o status for válido
        """
        return status in cls.VALID_STATUSES

    @classmethod
    def is_valid_fuel_type(cls, fuel_type: str) -> bool:
        """
        Verifica se o tipo de combustível é válido.
        
        Args:
            fuel_type: Tipo de combustível a ser validado
            
        Returns:
            bool: True se o tipo for válido
        """
        return fuel_type in cls.VALID_FUEL_TYPES

    def is_active(self) -> bool:
        """
        Verifica se o veículo está ativo.
        
        Returns:
            bool: True se estiver ativo
        """
        return self.status == self.STATUS_ATIVO

    def is_sold(self) -> bool:
        """
        Verifica se o veículo foi vendido.
        
        Returns:
            bool: True se foi vendido
        """
        return self.status == self.STATUS_VENDIDO

    def is_available_for_sale(self) -> bool:
        """
        Verifica se o veículo está disponível para venda.
        
        Returns:
            bool: True se estiver disponível
        """
        return self.status in [self.STATUS_ATIVO]

    def mark_as_sold(self) -> None:
        """
        Marca o veículo como vendido.
        """
        self.status = self.STATUS_VENDIDO
        self.updated_at = datetime.now()

    def mark_as_reserved(self) -> None:
        """
        Marca o veículo como reservado.
        """
        self.status = self.STATUS_RESERVADO
        self.updated_at = datetime.now()

    def mark_as_active(self) -> None:
        """
        Marca o veículo como ativo.
        """
        self.status = self.STATUS_ATIVO
        self.updated_at = datetime.now()

    def update_price(self, new_price: Decimal) -> None:
        """
        Atualiza o preço do veículo.
        
        Args:
            new_price: Novo preço do veículo
            
        Raises:
            ValueError: Se o preço for inválido
        """
        if new_price <= 0:
            raise ValueError("Preço deve ser maior que zero")
        
        self.price = new_price
        self.updated_at = datetime.now()

    def update_mileage(self, new_mileage: int) -> None:
        """
        Atualiza a quilometragem do veículo.
        
        Args:
            new_mileage: Nova quilometragem
            
        Raises:
            ValueError: Se a quilometragem for inválida
        """
        if new_mileage < 0:
            raise ValueError("Quilometragem não pode ser negativa")
        
        if new_mileage < self.mileage:
            raise ValueError("Nova quilometragem não pode ser menor que a atual")
        
        self.mileage = new_mileage
        self.updated_at = datetime.now()

    def is_eco_friendly(self) -> bool:
        """
        Verifica se o veículo é ecológico.
        
        Returns:
            bool: True se for ecológico
        """
        eco_fuels = ["Elétrico", "Híbrido", "Etanol"]
        return self.fuel_type in eco_fuels

    def get_age_in_years(self) -> int:
        """
        Calcula a idade do veículo em anos.
        
        Returns:
            int: Idade em anos
        """
        try:
            vehicle_year = int(self.year)
            current_year = datetime.now().year
            return max(0, current_year - vehicle_year)
        except ValueError:
            return 0

    def __repr__(self) -> str:
        return f"<MotorVehicle(id={self.id}, model='{self.model}', year='{self.year}', status='{self.status}')>"
