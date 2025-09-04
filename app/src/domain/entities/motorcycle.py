from typing import Optional
from datetime import datetime
from dataclasses import dataclass

from src.domain.entities.motor_vehicle import MotorVehicle
from src.domain.exceptions import ValidationError, BusinessRuleError


@dataclass
class Motorcycle:
    """
    Entidade de domínio para Motorcycle.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela lógica de negócio de motocicletas.
    
    Aplicando o princípio Open/Closed Principle (OCP) - 
    aberta para extensão, fechada para modificação.
    
    Compõe MotorVehicle ao invés de herdar, aplicando composição sobre herança.
    """
    
    motor_vehicle: MotorVehicle
    motorcycle_type: str  # "Street", "Sport", "Cruiser", "Adventure", "Touring", "Scooter", "Custom"
    cylinder_capacity: int  # em cc
    has_abs: bool = False
    has_traction_control: bool = False
    seat_height: Optional[int] = None  # em cm
    dry_weight: Optional[int] = None  # em kg
    fuel_capacity: Optional[float] = None  # em litros
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Tipos válidos de motocicleta
    VALID_MOTORCYCLE_TYPES = [
        "Street", "Sport", "Cruiser", "Adventure", 
        "Touring", "Scooter", "Custom", "Trail"
    ]
    
    @classmethod
    def create_complete_motorcycle(
        cls,
        # Dados do MotorVehicle
        brand: str,
        model: str,
        year: int,
        price: float,
        mileage: int,
        fuel_type: str,
        engine_power: str,
        color: str,
        # Dados específicos da Motorcycle
        motorcycle_type: str,
        cylinder_capacity: int,
        description: Optional[str] = None,
        has_abs: bool = False,
        has_traction_control: bool = False,
        seat_height: Optional[int] = None,
        dry_weight: Optional[int] = None,
        fuel_capacity: Optional[float] = None
    ) -> "Motorcycle":
        """
        Método factory para criar uma motocicleta completa.
        
        Args:
            Todos os parâmetros necessários para criar motocicleta e motor vehicle
            
        Returns:
            Motorcycle: Nova instância de motocicleta
            
        Raises:
            ValidationError: Se os dados não forem válidos
            BusinessRuleError: Se as regras de negócio não forem atendidas
        """
        # Criar o motor vehicle
        motor_vehicle = MotorVehicle.create_motor_vehicle(
            brand=brand,
            model=model,
            year=year,
            price=price,
            mileage=mileage,
            fuel_type=fuel_type,
            engine_power=engine_power,
            color=color,
            description=description
        )
        
        # Criar a motocicleta
        motorcycle = cls(
            motor_vehicle=motor_vehicle,
            motorcycle_type=motorcycle_type,
            cylinder_capacity=cylinder_capacity,
            has_abs=has_abs,
            has_traction_control=has_traction_control,
            seat_height=seat_height,
            dry_weight=dry_weight,
            fuel_capacity=fuel_capacity
        )
        
        # Validar dados específicos da motocicleta
        motorcycle._validate_motorcycle_data()
        motorcycle._apply_business_rules()
        
        return motorcycle
    
    def update_motorcycle_data(
        self,
        motorcycle_type: Optional[str] = None,
        cylinder_capacity: Optional[int] = None,
        has_abs: Optional[bool] = None,
        has_traction_control: Optional[bool] = None,
        seat_height: Optional[int] = None,
        dry_weight: Optional[int] = None,
        fuel_capacity: Optional[float] = None
    ) -> None:
        """
        Atualiza dados específicos da motocicleta.
        
        Args:
            Campos opcionais para atualização
            
        Raises:
            ValidationError: Se os dados não forem válidos
            BusinessRuleError: Se as regras de negócio não forem atendidas
        """
        if motorcycle_type is not None:
            self.motorcycle_type = motorcycle_type
        
        if cylinder_capacity is not None:
            self.cylinder_capacity = cylinder_capacity
        
        if has_abs is not None:
            self.has_abs = has_abs
        
        if has_traction_control is not None:
            self.has_traction_control = has_traction_control
        
        if seat_height is not None:
            self.seat_height = seat_height
        
        if dry_weight is not None:
            self.dry_weight = dry_weight
        
        if fuel_capacity is not None:
            self.fuel_capacity = fuel_capacity
        
        # Revalidar após atualização
        self._validate_motorcycle_data()
        self._apply_business_rules()
        self.updated_at = datetime.now()
    
    def _validate_motorcycle_data(self) -> None:
        """
        Valida os dados específicos da motocicleta.
        
        Raises:
            ValidationError: Se algum dado for inválido
        """
        # Validar tipo de motocicleta
        if not self.motorcycle_type or self.motorcycle_type not in self.VALID_MOTORCYCLE_TYPES:
            raise ValidationError(
                f"Tipo de motocicleta deve ser um dos seguintes: {', '.join(self.VALID_MOTORCYCLE_TYPES)}",
                "motorcycle_type"
            )
        
        # Validar cilindrada
        if not isinstance(self.cylinder_capacity, int) or self.cylinder_capacity <= 0:
            raise ValidationError("Cilindrada deve ser um número inteiro positivo", "cylinder_capacity")
        
        if self.cylinder_capacity < 50 or self.cylinder_capacity > 2500:
            raise ValidationError("Cilindrada deve estar entre 50cc e 2500cc", "cylinder_capacity")
        
        # Validar altura do assento (se fornecida)
        if self.seat_height is not None:
            if not isinstance(self.seat_height, int) or self.seat_height <= 0:
                raise ValidationError("Altura do assento deve ser um número inteiro positivo", "seat_height")
            
            if self.seat_height < 60 or self.seat_height > 120:
                raise ValidationError("Altura do assento deve estar entre 60cm e 120cm", "seat_height")
        
        # Validar peso seco (se fornecido)
        if self.dry_weight is not None:
            if not isinstance(self.dry_weight, int) or self.dry_weight <= 0:
                raise ValidationError("Peso seco deve ser um número inteiro positivo", "dry_weight")
            
            if self.dry_weight < 50 or self.dry_weight > 500:
                raise ValidationError("Peso seco deve estar entre 50kg e 500kg", "dry_weight")
        
        # Validar capacidade do tanque (se fornecida)
        if self.fuel_capacity is not None:
            if not isinstance(self.fuel_capacity, (int, float)) or self.fuel_capacity <= 0:
                raise ValidationError("Capacidade do tanque deve ser um número positivo", "fuel_capacity")
            
            if self.fuel_capacity < 1 or self.fuel_capacity > 50:
                raise ValidationError("Capacidade do tanque deve estar entre 1L e 50L", "fuel_capacity")
    
    def _apply_business_rules(self) -> None:
        """
        Aplica regras de negócio específicas de motocicletas.
        
        Raises:
            BusinessRuleError: Se alguma regra de negócio for violada
        """
        # Regra: Motocicletas sport normalmente têm ABS
        if self.motorcycle_type == "Sport" and self.cylinder_capacity > 600 and not self.has_abs:
            # Apenas um aviso, não um erro bloqueante
            pass
        
        # Regra: Scooters normalmente têm baixa cilindrada
        if self.motorcycle_type == "Scooter" and self.cylinder_capacity > 250:
            raise BusinessRuleError(
                "Scooters normalmente têm cilindrada até 250cc",
                "scooter_cylinder_capacity"
            )
        
        # Regra: Motocicletas de alta cilindrada devem ter controle de tração
        if self.cylinder_capacity > 1000 and not self.has_traction_control:
            # Apenas um aviso para motocicletas potentes
            pass
        
        # Regra: Verificar combustível adequado para o tipo
        if self.motorcycle_type == "Sport" and self.motor_vehicle.fuel_type not in ["Gasolina", "Etanol"]:
            raise BusinessRuleError(
                "Motocicletas sport normalmente usam gasolina ou etanol",
                "sport_fuel_type"
            )
    
    def can_be_sold(self) -> bool:
        """
        Verifica se a motocicleta pode ser vendida.
        
        Returns:
            bool: True se pode ser vendida
        """
        return self.motor_vehicle.status == "Ativo"
    
    def is_high_performance(self) -> bool:
        """
        Verifica se é uma motocicleta de alta performance.
        
        Returns:
            bool: True se for de alta performance
        """
        return (
            self.motorcycle_type in ["Sport", "Adventure"] and
            self.cylinder_capacity > 600 and
            self.has_abs and
            self.has_traction_control
        )
    
    def get_power_to_weight_ratio(self) -> Optional[float]:
        """
        Calcula a relação potência/peso se os dados estiverem disponíveis.
        
        Returns:
            Optional[float]: Relação potência/peso ou None
        """
        if not self.dry_weight or not self.motor_vehicle.engine_power:
            return None
        
        try:
            # Extrair número da potência (assumindo formato como "150 cv")
            power_str = self.motor_vehicle.engine_power.lower().replace("cv", "").replace("hp", "").strip()
            power = float(power_str)
            return round(power / self.dry_weight, 2)
        except (ValueError, ZeroDivisionError):
            return None
    
    def get_display_name(self) -> str:
        """
        Retorna nome de exibição da motocicleta.
        
        Returns:
            str: Nome formatado para exibição
        """
        return f"{self.motor_vehicle.brand} {self.motor_vehicle.model} {self.motor_vehicle.year} - {self.cylinder_capacity}cc"
    
    def __str__(self) -> str:
        return self.get_display_name()
