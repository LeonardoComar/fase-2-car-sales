from typing import Optional
from src.domain.entities.car import Car
from src.domain.entities.motor_vehicle import MotorVehicle
from src.domain.ports.car_repository import CarRepository
from src.application.dtos.car_dto import CarUpdateDto, CarResponseDto, MotorVehicleResponseDto
import logging

logger = logging.getLogger(__name__)


class UpdateCarUseCase:
    """
    Caso de uso para atualização de carro.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela atualização de carros.
    """
    
    def __init__(self, car_repository: CarRepository):
        self._car_repository = car_repository
    
    async def execute(self, car_id: int, car_update: CarUpdateDto) -> Optional[CarResponseDto]:
        """
        Executa o caso de uso de atualização de carro.
        
        Args:
            car_id: ID do carro a ser atualizado
            car_update: DTO com dados para atualização
            
        Returns:
            Optional[CarResponseDto]: Dados do carro atualizado ou None se não encontrado
            
        Raises:
            ValueError: Se dados inválidos
            Exception: Para outros erros
        """
        try:
            if car_id <= 0:
                raise ValueError("ID do carro deve ser um número positivo")
            
            # Buscar o carro existente
            existing_car = await self._car_repository.find_by_id(car_id)
            if not existing_car:
                return None
            
            # Validar dados específicos do carro se fornecidos
            if car_update.bodywork is not None and not Car.is_valid_bodywork(car_update.bodywork):
                raise ValueError(f"Tipo de carroceria inválido. Deve ser um de: {', '.join(Car.VALID_BODYWORK_TYPES)}")
            
            if car_update.transmission is not None and not Car.is_valid_transmission(car_update.transmission):
                raise ValueError(f"Tipo de transmissão inválido. Deve ser um de: {', '.join(Car.VALID_TRANSMISSION_TYPES)}")
            
            # Validar dados do veículo motor se fornecidos
            if car_update.fuel_type is not None and not MotorVehicle.is_valid_fuel_type(car_update.fuel_type):
                raise ValueError(f"Tipo de combustível inválido. Deve ser um de: {', '.join(MotorVehicle.VALID_FUEL_TYPES)}")
            
            # Atualizar o carro com os novos dados
            updated_car = self._apply_updates(existing_car, car_update)
            
            # Persistir as alterações
            result_car = await self._car_repository.update(updated_car)
            
            if not result_car:
                return None
            
            return self._car_to_response_dto(result_car)
            
        except ValueError as e:
            logger.error(f"Erro de validação ao atualizar carro: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Erro ao atualizar carro: {str(e)}")
            raise Exception(f"Erro interno do servidor: {str(e)}")
    
    def _apply_updates(self, existing_car: Car, car_update: CarUpdateDto) -> Car:
        """
        Aplica as atualizações ao carro existente.
        
        Args:
            existing_car: Carro existente
            car_update: Dados de atualização
            
        Returns:
            Car: Carro com dados atualizados
        """
        # Atualizar dados específicos do carro
        if car_update.bodywork is not None:
            existing_car.update_bodywork(car_update.bodywork)
        
        if car_update.transmission is not None:
            existing_car.update_transmission(car_update.transmission)
        
        # Atualizar dados do veículo motor se existir
        if existing_car.motor_vehicle:
            if car_update.model is not None:
                existing_car.motor_vehicle.model = car_update.model
                existing_car.motor_vehicle.updated_at = existing_car.updated_at
            
            if car_update.year is not None:
                existing_car.motor_vehicle.year = car_update.year
                existing_car.motor_vehicle.updated_at = existing_car.updated_at
            
            if car_update.mileage is not None:
                existing_car.motor_vehicle.update_mileage(car_update.mileage)
            
            if car_update.fuel_type is not None:
                existing_car.motor_vehicle.fuel_type = car_update.fuel_type
                existing_car.motor_vehicle.updated_at = existing_car.updated_at
            
            if car_update.color is not None:
                existing_car.motor_vehicle.color = car_update.color
                existing_car.motor_vehicle.updated_at = existing_car.updated_at
            
            if car_update.city is not None:
                existing_car.motor_vehicle.city = car_update.city
                existing_car.motor_vehicle.updated_at = existing_car.updated_at
            
            if car_update.price is not None:
                existing_car.motor_vehicle.update_price(car_update.price)
            
            if car_update.additional_description is not None:
                existing_car.motor_vehicle.additional_description = car_update.additional_description
                existing_car.motor_vehicle.updated_at = existing_car.updated_at
        
        return existing_car
    
    def _car_to_response_dto(self, car: Car) -> CarResponseDto:
        """
        Converte entidade Car para DTO de resposta.
        
        Args:
            car: Entidade Car
            
        Returns:
            CarResponseDto: DTO de resposta
        """
        motor_vehicle_dto = None
        if car.motor_vehicle:
            motor_vehicle_dto = MotorVehicleResponseDto(
                id=car.motor_vehicle.id,
                model=car.motor_vehicle.model,
                year=car.motor_vehicle.year,
                mileage=car.motor_vehicle.mileage,
                fuel_type=car.motor_vehicle.fuel_type,
                color=car.motor_vehicle.color,
                city=car.motor_vehicle.city,
                price=car.motor_vehicle.price,
                additional_description=car.motor_vehicle.additional_description,
                status=car.motor_vehicle.status,
                created_at=car.motor_vehicle.created_at,
                updated_at=car.motor_vehicle.updated_at
            )
        
        return CarResponseDto(
            id=car.id,
            motor_vehicle=motor_vehicle_dto,
            bodywork=car.bodywork,
            transmission=car.transmission,
            updated_at=car.updated_at
        )
