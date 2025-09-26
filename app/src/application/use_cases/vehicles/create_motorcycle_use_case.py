from typing import Optional
import logging
from src.application.dtos.motorcycle_dto import MotorcycleCreateDto, MotorcycleResponseDto
from src.domain.entities.motorcycle import Motorcycle
from src.domain.ports.motorcycle_repository import MotorcycleRepository
from src.domain.exceptions import ValidationError, BusinessRuleError

logger = logging.getLogger(__name__)


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
            logger.info(f"🔍 [CREATE_MOTORCYCLE_USE_CASE] Iniciando criação de motocicleta: {motorcycle_data.model}")
            
            # Para simplificar, vou criar o MotorVehicle e a Motorcycle separadamente
            from decimal import Decimal
            from src.domain.entities.motor_vehicle import MotorVehicle
            
            logger.info("🔍 [CREATE_MOTORCYCLE_USE_CASE] Criando MotorVehicle...")
            # Criar o MotorVehicle diretamente
            motor_vehicle = MotorVehicle.create_motor_vehicle(
                model=motorcycle_data.model,
                year=motorcycle_data.year,
                mileage=motorcycle_data.mileage,
                fuel_type=motorcycle_data.fuel_type,
                color=motorcycle_data.color,
                city=motorcycle_data.city or "",
                price=Decimal(str(motorcycle_data.price)),
                additional_description=motorcycle_data.additional_description
            )
            
            logger.info("🔍 [CREATE_MOTORCYCLE_USE_CASE] Criando Motorcycle...")
            # Criar a Motorcycle
            motorcycle = Motorcycle(
                motor_vehicle=motor_vehicle,
                starter=motorcycle_data.starter,
                fuel_system=motorcycle_data.fuel_system,
                engine_displacement=motorcycle_data.engine_displacement,
                cooling=motorcycle_data.cooling,
                style=motorcycle_data.style,
                engine_type=motorcycle_data.engine_type,
                gears=motorcycle_data.gears,
                front_rear_brake=motorcycle_data.front_rear_brake
            )
            
            logger.info("🔍 [CREATE_MOTORCYCLE_USE_CASE] Validando regras de negócio...")
            # Validações adicionais de negócio
            await self._validate_business_rules(motorcycle)
            
            logger.info("🔍 [CREATE_MOTORCYCLE_USE_CASE] Salvando no repositório...")
            # Salvar no repositório
            saved_motorcycle = await self.motorcycle_repository.save(motorcycle)
            
            logger.info("🔍 [CREATE_MOTORCYCLE_USE_CASE] Convertendo para DTO de resposta...")
            # Converter para DTO de resposta
            response_dto = self._to_response_dto(saved_motorcycle)
            
            logger.info(f"✅ [CREATE_MOTORCYCLE_USE_CASE] Motocicleta criada com sucesso. ID: {saved_motorcycle.id}")
            return response_dto
            
        except ValidationError as e:
            logger.error(f"❌ [CREATE_MOTORCYCLE_USE_CASE] Erro de validação: {str(e)}")
            raise
        except BusinessRuleError as e:
            logger.error(f"❌ [CREATE_MOTORCYCLE_USE_CASE] Erro de regra de negócio: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"❌ [CREATE_MOTORCYCLE_USE_CASE] Erro interno: {str(e)}")
            logger.exception("Stack trace completo do erro:")
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
            model=motorcycle.motor_vehicle.model,
            year_min=int(motorcycle.motor_vehicle.year) if motorcycle.motor_vehicle.year.isdigit() else None,
            year_max=int(motorcycle.motor_vehicle.year) if motorcycle.motor_vehicle.year.isdigit() else None,
            engine_displacement_min=motorcycle.engine_displacement - 50 if motorcycle.engine_displacement else None,
            engine_displacement_max=motorcycle.engine_displacement + 50 if motorcycle.engine_displacement else None,
            limit=1
        )
        
        if similar_motorcycles:
            # Apenas um aviso, não bloqueia a criação
            pass
        
        # Regra: Verificar coerência entre tipo e características
        self._validate_type_consistency(motorcycle)
    
    def _validate_type_consistency(self, motorcycle: Motorcycle) -> None:
        """
        Valida consistência entre tipo e características.
        
        Args:
            motorcycle: Entidade de motocicleta
            
        Raises:
            BusinessRuleError: Se houver inconsistência
        """
        # Validações simplificadas usando os campos que existem na tabela
        if motorcycle.style == "Scooter" and motorcycle.engine_displacement and motorcycle.engine_displacement > 250:
            raise BusinessRuleError(
                "Scooters devem ter cilindrada máxima de 250cc",
                "scooter_max_displacement"
            )
    
    def _to_response_dto(self, motorcycle: Motorcycle) -> MotorcycleResponseDto:
        """
        Converte entidade de domínio para DTO de resposta.
        
        Args:
            motorcycle: Entidade de motocicleta
            
        Returns:
            MotorcycleResponseDto: DTO de resposta
        """
        from datetime import datetime
        
        return MotorcycleResponseDto(
            id=motorcycle.id,
            # Dados do MotorVehicle
            model=motorcycle.motor_vehicle.model,
            year=motorcycle.motor_vehicle.year,
            price=float(motorcycle.motor_vehicle.price),
            mileage=motorcycle.motor_vehicle.mileage,
            fuel_type=motorcycle.motor_vehicle.fuel_type,
            color=motorcycle.motor_vehicle.color,
            city=motorcycle.motor_vehicle.city,
            additional_description=motorcycle.motor_vehicle.additional_description,
            status=motorcycle.motor_vehicle.status,
            # Dados específicos da Motorcycle
            starter=motorcycle.starter,
            fuel_system=motorcycle.fuel_system,
            engine_displacement=motorcycle.engine_displacement,
            cooling=motorcycle.cooling,
            style=motorcycle.style,
            engine_type=motorcycle.engine_type,
            gears=motorcycle.gears,
            front_rear_brake=motorcycle.front_rear_brake,
            # Dados calculados
            display_name=f"{motorcycle.motor_vehicle.model} ({motorcycle.motor_vehicle.year})",
            # Auditoria - usando dados do motor_vehicle para created_at e motorcycle para updated_at
            created_at=motorcycle.motor_vehicle.created_at or datetime.now(),
            updated_at=motorcycle.updated_at or motorcycle.motor_vehicle.updated_at or datetime.now()
        )
