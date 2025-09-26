from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal

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
    # Campos que realmente existem na tabela motorcycles
    starter: Optional[str] = None
    fuel_system: Optional[str] = None
    engine_displacement: Optional[int] = None  # Cilindrada em cc
    cooling: Optional[str] = None
    style: Optional[str] = None  # Tipo/estilo da motocicleta
    engine_type: Optional[str] = None
    gears: Optional[int] = None
    front_rear_brake: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Tipos válidos de estilo (baseado no campo 'style' da tabela)
    VALID_STYLES = [
        "Street", "Sport", "Cruiser", "Adventure", 
        "Touring", "Scooter", "Custom", "Trail", "Naked"
    ]
    
    @classmethod
    def create_complete_motorcycle(
        cls,
        # Dados do MotorVehicle
        model: str,
        year: str,
        price: float,
        mileage: int,
        fuel_type: str,
        color: str,
        city: Optional[str] = None,
        additional_description: Optional[str] = None,
        status: Optional[str] = None,
        # Dados específicos da Motorcycle
        starter: Optional[str] = None,
        fuel_system: Optional[str] = None,
        engine_displacement: Optional[int] = None,
        cooling: Optional[str] = None,
        style: Optional[str] = None,
        engine_type: Optional[str] = None,
        gears: Optional[int] = None,
        front_rear_brake: Optional[str] = None
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
            model=model,
            year=year,
            mileage=mileage,
            fuel_type=fuel_type,
            color=color,
            city=city or "",
            price=Decimal(str(price)),
            additional_description=additional_description,
            status=status
        )
        
        # Criar a motocicleta
        motorcycle = cls(
            motor_vehicle=motor_vehicle,
            starter=starter,
            fuel_system=fuel_system,
            engine_displacement=engine_displacement,
            cooling=cooling,
            style=style,
            engine_type=engine_type,
            gears=gears,
            front_rear_brake=front_rear_brake
        )
        
        # Validar dados específicos da motocicleta
        motorcycle._validate_motorcycle_data()
        motorcycle._apply_business_rules()
        
        return motorcycle
    
    def update_motorcycle_data(
        self,
        style: Optional[str] = None,
        starter: Optional[str] = None,
        fuel_system: Optional[str] = None,
        engine_displacement: Optional[int] = None,
        cooling: Optional[str] = None,
        engine_type: Optional[str] = None,
        gears: Optional[int] = None,
        front_rear_brake: Optional[str] = None
    ) -> None:
        """
        Atualiza dados específicos da motocicleta.
        
        Args:
            Campos opcionais para atualização
            
        Raises:
            ValidationError: Se os dados não forem válidos
            BusinessRuleError: Se as regras de negócio não forem atendidas
        """
        if style is not None:
            self.style = style
        
        if starter is not None:
            self.starter = starter
        
        if fuel_system is not None:
            self.fuel_system = fuel_system
        
        if engine_displacement is not None:
            self.engine_displacement = engine_displacement
        
        if cooling is not None:
            self.cooling = cooling
        
        if engine_type is not None:
            self.engine_type = engine_type
        
        if gears is not None:
            self.gears = gears
        
        if front_rear_brake is not None:
            self.front_rear_brake = front_rear_brake
        
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
        # Validar estilo da motocicleta
        if not self.style or self.style not in self.VALID_STYLES:
            raise ValidationError(
                f"Estilo de motocicleta deve ser um dos seguintes: {', '.join(self.VALID_STYLES)}",
                "style"
            )
        
        # Validar cilindrada (se fornecida)
        if self.engine_displacement is not None:
            if not isinstance(self.engine_displacement, int) or self.engine_displacement <= 0:
                raise ValidationError("Cilindrada deve ser um número inteiro positivo", "engine_displacement")
            
            if self.engine_displacement < 50 or self.engine_displacement > 2500:
                raise ValidationError("Cilindrada deve estar entre 50cc e 2500cc", "engine_displacement")
        
        # Validar número de marchas (se fornecido)
        if self.gears is not None:
            if not isinstance(self.gears, int) or self.gears <= 0:
                raise ValidationError("Número de marchas deve ser um número inteiro positivo", "gears")
            
            if self.gears < 1 or self.gears > 7:
                raise ValidationError("Número de marchas deve estar entre 1 e 7", "gears")
    
    def _apply_business_rules(self) -> None:
        """
        Aplica regras de negócio específicas de motocicletas.
        
        Raises:
            BusinessRuleError: Se alguma regra de negócio for violada
        """
        # Regra: Verificar combustível adequado para o tipo
        if self.style == "Sport" and self.motor_vehicle.fuel_type not in ["Gasolina", "Etanol"]:
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
            self.style in ["Sport", "Adventure"] and
            self.engine_displacement and self.engine_displacement > 600
        )
    
    def get_display_name(self) -> str:
        """
        Retorna nome de exibição da motocicleta.
        
        Returns:
            str: Nome formatado para exibição
        """
        displacement_info = f" - {self.engine_displacement}cc" if self.engine_displacement else ""
        return f"{self.motor_vehicle.model} {self.motor_vehicle.year}{displacement_info}"
    
    def __str__(self) -> str:
        return self.get_display_name()
