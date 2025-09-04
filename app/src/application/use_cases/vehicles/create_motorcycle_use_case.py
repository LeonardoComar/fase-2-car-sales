from typing import Optional
from src.application.dtos.motorcycle_dto import MotorcycleCreateDto, MotorcycleResponseDto
from src.domain.entities.motorcycle import Motorcycle
from src.domain.ports.motorcycle_repository import MotorcycleRepository
from src.domain.exceptions import ValidationError, BusinessRuleError


class CreateMotorcycleUseCase:
    """
    Use case para criação de motocicletas.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela criação de motocicletas.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração MotorcycleRepository, não da implementação.
    """
    
    def __init__(self, motorcycle_repository: MotorcycleRepository):
        self.motorcycle_repository = motorcycle_repository
    
    async def execute(self, motorcycle_data: MotorcycleCreateDto) -> MotorcycleResponseDto:
        """
        Executa a criação de uma nova motocicleta.
        
        Args:
            motorcycle_data: Dados da motocicleta a ser criada
            
        Returns:
            MotorcycleResponseDto: Dados da motocicleta criada
            
        Raises:
            ValidationError: Se os dados não forem válidos
            BusinessRuleError: Se as regras de negócio não forem atendidas
        """
        try:
            # Criar a entidade de domínio
            motorcycle = Motorcycle.create_complete_motorcycle(
                # Dados do MotorVehicle
                brand=motorcycle_data.brand,
                model=motorcycle_data.model,
                year=motorcycle_data.year,
                price=motorcycle_data.price,
                mileage=motorcycle_data.mileage,
                fuel_type=motorcycle_data.fuel_type,
                engine_power=motorcycle_data.engine_power,
                color=motorcycle_data.color,
                description=motorcycle_data.description,
                # Dados específicos da Motorcycle
                motorcycle_type=motorcycle_data.motorcycle_type,
                cylinder_capacity=motorcycle_data.cylinder_capacity,
                has_abs=motorcycle_data.has_abs,
                has_traction_control=motorcycle_data.has_traction_control,
                seat_height=motorcycle_data.seat_height,
                dry_weight=motorcycle_data.dry_weight,
                fuel_capacity=motorcycle_data.fuel_capacity
            )
            
            # Validações adicionais de negócio
            await self._validate_business_rules(motorcycle)
            
            # Salvar no repositório
            saved_motorcycle = await self.motorcycle_repository.save(motorcycle)
            
            # Converter para DTO de resposta
            return self._to_response_dto(saved_motorcycle)
            
        except ValidationError:
            raise
        except BusinessRuleError:
            raise
        except Exception as e:
            raise ValidationError(f"Erro interno durante criação da motocicleta: {str(e)}")
    
    async def _validate_business_rules(self, motorcycle: Motorcycle) -> None:
        """
        Valida regras de negócio específicas para criação.
        
        Args:
            motorcycle: Entidade de motocicleta a ser validada
            
        Raises:
            BusinessRuleError: Se alguma regra de negócio for violada
        """
        # Regra: Verificar se já existe uma motocicleta muito similar
        similar_motorcycles = await self.motorcycle_repository.find_by_criteria(
            brand=motorcycle.motor_vehicle.brand,
            model=motorcycle.motor_vehicle.model,
            year=motorcycle.motor_vehicle.year,
            cylinder_capacity_min=motorcycle.cylinder_capacity - 50,
            cylinder_capacity_max=motorcycle.cylinder_capacity + 50,
            limit=1
        )
        
        if similar_motorcycles:
            # Apenas um aviso, não bloqueia a criação
            pass
        
        # Regra: Motocicletas novas (0 km) devem ter preço mínimo baseado na cilindrada
        if motorcycle.motor_vehicle.mileage == 0:
            min_price = self._calculate_min_price_for_new_motorcycle(motorcycle.cylinder_capacity)
            if motorcycle.motor_vehicle.price < min_price:
                raise BusinessRuleError(
                    f"Preço muito baixo para motocicleta nova de {motorcycle.cylinder_capacity}cc. "
                    f"Preço mínimo sugerido: R$ {min_price:,.2f}",
                    "new_motorcycle_min_price"
                )
        
        # Regra: Verificar coerência entre tipo e características
        self._validate_type_consistency(motorcycle)
    
    def _calculate_min_price_for_new_motorcycle(self, cylinder_capacity: int) -> float:
        """
        Calcula preço mínimo baseado na cilindrada.
        
        Args:
            cylinder_capacity: Cilindrada da motocicleta
            
        Returns:
            float: Preço mínimo sugerido
        """
        if cylinder_capacity <= 150:
            return 8000.0
        elif cylinder_capacity <= 250:
            return 15000.0
        elif cylinder_capacity <= 600:
            return 25000.0
        elif cylinder_capacity <= 1000:
            return 40000.0
        else:
            return 60000.0
    
    def _validate_type_consistency(self, motorcycle: Motorcycle) -> None:
        """
        Valida consistência entre tipo e características.
        
        Args:
            motorcycle: Entidade de motocicleta
            
        Raises:
            BusinessRuleError: Se houver inconsistência
        """
        # Scooters devem ter baixa cilindrada
        if motorcycle.motorcycle_type == "Scooter" and motorcycle.cylinder_capacity > 250:
            raise BusinessRuleError(
                "Scooters devem ter cilindrada máxima de 250cc",
                "scooter_max_cylinder_capacity"
            )
        
        # Motocicletas Sport de alta cilindrada devem ter sistemas de segurança
        if (motorcycle.motorcycle_type == "Sport" and 
            motorcycle.cylinder_capacity > 600 and 
            not motorcycle.has_abs):
            # Apenas um aviso para motocicletas sport
            pass
    
    def _to_response_dto(self, motorcycle: Motorcycle) -> MotorcycleResponseDto:
        """
        Converte entidade de domínio para DTO de resposta.
        
        Args:
            motorcycle: Entidade de motocicleta
            
        Returns:
            MotorcycleResponseDto: DTO de resposta
        """
        return MotorcycleResponseDto(
            id=motorcycle.id,
            # Dados do MotorVehicle
            brand=motorcycle.motor_vehicle.brand,
            model=motorcycle.motor_vehicle.model,
            year=motorcycle.motor_vehicle.year,
            price=motorcycle.motor_vehicle.price,
            mileage=motorcycle.motor_vehicle.mileage,
            fuel_type=motorcycle.motor_vehicle.fuel_type,
            engine_power=motorcycle.motor_vehicle.engine_power,
            color=motorcycle.motor_vehicle.color,
            status=motorcycle.motor_vehicle.status,
            description=motorcycle.motor_vehicle.description,
            # Dados específicos da Motorcycle
            motorcycle_type=motorcycle.motorcycle_type,
            cylinder_capacity=motorcycle.cylinder_capacity,
            has_abs=motorcycle.has_abs,
            has_traction_control=motorcycle.has_traction_control,
            seat_height=motorcycle.seat_height,
            dry_weight=motorcycle.dry_weight,
            fuel_capacity=motorcycle.fuel_capacity,
            # Dados calculados
            is_high_performance=motorcycle.is_high_performance(),
            power_to_weight_ratio=motorcycle.get_power_to_weight_ratio(),
            display_name=motorcycle.get_display_name(),
            # Auditoria
            created_at=motorcycle.created_at,
            updated_at=motorcycle.updated_at
        )
