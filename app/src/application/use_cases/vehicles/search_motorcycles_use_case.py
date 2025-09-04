import math
from typing import List
from src.application.dtos.motorcycle_dto import MotorcycleSearchDto, MotorcycleListResponseDto, MotorcycleResponseDto
from src.domain.entities.motorcycle import Motorcycle
from src.domain.ports.motorcycle_repository import MotorcycleRepository


class SearchMotorcyclesUseCase:
    """
    Use case para buscar motocicletas com filtros.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela busca de motocicletas com filtros.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração MotorcycleRepository, não da implementação.
    """
    
    def __init__(self, motorcycle_repository: MotorcycleRepository):
        self.motorcycle_repository = motorcycle_repository
    
    async def execute(self, search_criteria: MotorcycleSearchDto) -> MotorcycleListResponseDto:
        """
        Executa a busca de motocicletas com filtros.
        
        Args:
            search_criteria: Critérios de busca
            
        Returns:
            MotorcycleListResponseDto: Lista de motocicletas encontradas
        """
        # Calcular skip para paginação
        skip = (search_criteria.page - 1) * search_criteria.size
        
        # Buscar motocicletas no repositório
        motorcycles = await self.motorcycle_repository.find_by_criteria(
            brand=search_criteria.brand,
            model=search_criteria.model,
            year_min=search_criteria.year_min,
            year_max=search_criteria.year_max,
            price_min=search_criteria.price_min,
            price_max=search_criteria.price_max,
            mileage_max=search_criteria.mileage_max,
            fuel_type=search_criteria.fuel_type,
            motorcycle_type=search_criteria.motorcycle_type,
            cylinder_capacity_min=search_criteria.cylinder_capacity_min,
            cylinder_capacity_max=search_criteria.cylinder_capacity_max,
            has_abs=search_criteria.has_abs,
            has_traction_control=search_criteria.has_traction_control,
            status=search_criteria.status,
            available_only=search_criteria.available_only,
            skip=skip,
            limit=search_criteria.size
        )
        
        # Contar total de registros para paginação
        total = await self.motorcycle_repository.count_by_criteria(
            brand=search_criteria.brand,
            model=search_criteria.model,
            year_min=search_criteria.year_min,
            year_max=search_criteria.year_max,
            price_min=search_criteria.price_min,
            price_max=search_criteria.price_max,
            mileage_max=search_criteria.mileage_max,
            fuel_type=search_criteria.fuel_type,
            motorcycle_type=search_criteria.motorcycle_type,
            cylinder_capacity_min=search_criteria.cylinder_capacity_min,
            cylinder_capacity_max=search_criteria.cylinder_capacity_max,
            has_abs=search_criteria.has_abs,
            has_traction_control=search_criteria.has_traction_control,
            status=search_criteria.status,
            available_only=search_criteria.available_only
        )
        
        # Calcular total de páginas
        total_pages = math.ceil(total / search_criteria.size) if total > 0 else 0
        
        # Converter para DTOs de resposta
        motorcycle_dtos = [self._to_response_dto(motorcycle) for motorcycle in motorcycles]
        
        return MotorcycleListResponseDto(
            motorcycles=motorcycle_dtos,
            total=total,
            page=search_criteria.page,
            size=search_criteria.size,
            total_pages=total_pages
        )
    
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
