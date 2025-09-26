from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal
from .motor_vehicle import MotorVehicle


@dataclass
class Car:
    """
    Entidade Car do domínio - representa um carro no sistema.
    
    Esta entidade contém apenas a lógica de negócio específica para carros.
    Aplicando o princípio Single Responsibility Principle (SRP) do SOLID.
    
    Compõe um MotorVehicle para reutilizar funcionalidades comuns.
    """
    
    # Tipos de carroceria válidos
    VALID_BODYWORK_TYPES = [
        "Sedan", "Hatchback", "SUV", "Coupe", "Conversivel", 
        "Station Wagon", "Pickup", "Van", "Minivan"
    ]
    
    # Tipos de transmissão válidos
    VALID_TRANSMISSION_TYPES = [
        "Manual", "Automatica", "Automatizada", "CVT"
    ]

    id: Optional[int] = None
    motor_vehicle: Optional[MotorVehicle] = None
    bodywork: str = ""
    transmission: str = ""
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validações após a inicialização"""
        if self.bodywork and not self.is_valid_bodywork(self.bodywork):
            raise ValueError(f"Tipo de carroceria inválido. Deve ser um de: {', '.join(self.VALID_BODYWORK_TYPES)}")
        
        if self.transmission and not self.is_valid_transmission(self.transmission):
            raise ValueError(f"Tipo de transmissão inválido. Deve ser um de: {', '.join(self.VALID_TRANSMISSION_TYPES)}")

    @classmethod
    def create_car(cls, motor_vehicle: MotorVehicle, bodywork: str, transmission: str) -> 'Car':
        """
        Método de classe para criar um carro.
        
        Args:
            motor_vehicle: Instância do veículo motor base
            bodywork: Tipo de carroceria
            transmission: Tipo de transmissão
            
        Returns:
            Car: Nova instância de carro
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        if not cls.is_valid_bodywork(bodywork):
            raise ValueError(f"Tipo de carroceria inválido. Deve ser um de: {', '.join(cls.VALID_BODYWORK_TYPES)}")
        
        if not cls.is_valid_transmission(transmission):
            raise ValueError(f"Tipo de transmissão inválido. Deve ser um de: {', '.join(cls.VALID_TRANSMISSION_TYPES)}")
        
        return cls(
            motor_vehicle=motor_vehicle,
            bodywork=bodywork,
            transmission=transmission,
            updated_at=datetime.now()
        )

    @classmethod
    def create_complete_car(
        cls,
        model: str, 
        year: str, 
        mileage: int, 
        fuel_type: str,
        color: str, 
        city: str, 
        price: Decimal, 
        bodywork: str,
        transmission: str,
        additional_description: Optional[str] = None
    ) -> 'Car':
        """
        Método de classe para criar um carro completo (com MotorVehicle).
        
        Args:
            model: Modelo do veículo
            year: Ano do veículo
            mileage: Quilometragem
            fuel_type: Tipo de combustível
            color: Cor do veículo
            city: Cidade onde está o veículo
            price: Preço do veículo
            bodywork: Tipo de carroceria
            transmission: Tipo de transmissão
            additional_description: Descrição adicional (opcional)
            
        Returns:
            Car: Nova instância de carro completo
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        # Criar o veículo motor base
        motor_vehicle = MotorVehicle.create_motor_vehicle(
            model=model,
            year=year,
            mileage=mileage,
            fuel_type=fuel_type,
            color=color,
            city=city,
            price=price,
            additional_description=additional_description
        )
        
        # Criar o carro
        return cls.create_car(motor_vehicle, bodywork, transmission)

    @classmethod
    def is_valid_bodywork(cls, bodywork: str) -> bool:
        """
        Verifica se o tipo de carroceria é válido.
        
        Args:
            bodywork: Tipo de carroceria a ser validado
            
        Returns:
            bool: True se for válido
        """
        return bodywork in cls.VALID_BODYWORK_TYPES

    @classmethod
    def is_valid_transmission(cls, transmission: str) -> bool:
        """
        Verifica se o tipo de transmissão é válido.
        
        Args:
            transmission: Tipo de transmissão a ser validado
            
        Returns:
            bool: True se for válido
        """
        return transmission in cls.VALID_TRANSMISSION_TYPES

    def update_bodywork(self, new_bodywork: str) -> None:
        """
        Atualiza o tipo de carroceria.
        
        Args:
            new_bodywork: Novo tipo de carroceria
            
        Raises:
            ValueError: Se o tipo de carroceria for inválido
        """
        if not self.is_valid_bodywork(new_bodywork):
            raise ValueError(f"Tipo de carroceria inválido. Deve ser um de: {', '.join(self.VALID_BODYWORK_TYPES)}")
        
        self.bodywork = new_bodywork
        self.updated_at = datetime.now()

    def update_transmission(self, new_transmission: str) -> None:
        """
        Atualiza o tipo de transmissão.
        
        Args:
            new_transmission: Novo tipo de transmissão
            
        Raises:
            ValueError: Se o tipo de transmissão for inválido
        """
        if not self.is_valid_transmission(new_transmission):
            raise ValueError(f"Tipo de transmissão inválido. Deve ser um de: {', '.join(self.VALID_TRANSMISSION_TYPES)}")
        
        self.transmission = new_transmission
        self.updated_at = datetime.now()

    def is_automatic(self) -> bool:
        """
        Verifica se o carro possui transmissão automática.
        
        Returns:
            bool: True se for automático
        """
        return self.transmission in ["Automatica", "Automatizada", "CVT"]

    def is_luxury_category(self) -> bool:
        """
        Verifica se o carro está na categoria de luxo baseado na carroceria.
        
        Returns:
            bool: True se for categoria de luxo
        """
        luxury_types = ["Coupe", "Conversivel"]
        return self.bodywork in luxury_types

    def is_family_car(self) -> bool:
        """
        Verifica se o carro é adequado para famílias.
        
        Returns:
            bool: True se for adequado para famílias
        """
        family_types = ["SUV", "Station Wagon", "Van", "Minivan"]
        return self.bodywork in family_types

    def is_compact(self) -> bool:
        """
        Verifica se o carro é compacto.
        
        Returns:
            bool: True se for compacto
        """
        compact_types = ["Hatchback"]
        return self.bodywork in compact_types

    def get_motor_vehicle_info(self) -> Optional[MotorVehicle]:
        """
        Retorna as informações do veículo motor.
        
        Returns:
            Optional[MotorVehicle]: Informações do veículo motor
        """
        return self.motor_vehicle

    def get_full_description(self) -> str:
        """
        Retorna uma descrição completa do carro.
        
        Returns:
            str: Descrição completa
        """
        if not self.motor_vehicle:
            return f"{self.bodywork} {self.transmission}"
        
        return f"{self.motor_vehicle.model} {self.motor_vehicle.year} - {self.bodywork} {self.transmission}"

    def get_price(self) -> Optional[Decimal]:
        """
        Retorna o preço do carro.
        
        Returns:
            Optional[Decimal]: Preço do carro
        """
        return self.motor_vehicle.price if self.motor_vehicle else None

    def is_available_for_sale(self) -> bool:
        """
        Verifica se o carro está disponível para venda.
        
        Returns:
            bool: True se estiver disponível
        """
        return self.motor_vehicle.is_available_for_sale() if self.motor_vehicle else False

    def mark_as_sold(self) -> None:
        """
        Marca o carro como vendido.
        """
        if self.motor_vehicle:
            self.motor_vehicle.mark_as_sold()
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        model_info = f"model='{self.motor_vehicle.model}'" if self.motor_vehicle else "model=None"
        return f"<Car(id={self.id}, {model_info}, bodywork='{self.bodywork}', transmission='{self.transmission}')>"
