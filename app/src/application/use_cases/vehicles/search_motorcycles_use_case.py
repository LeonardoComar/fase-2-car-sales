import math
import logging
from typing import List
from src.application.dtos.motorcycle_dto import MotorcycleSearchDto, MotorcycleListResponseDto, MotorcycleResponseDto
from src.domain.entities.motorcycle import Motorcycle
from src.domain.ports.motorcycle_repository import MotorcycleRepository

# Setup logging
logger = logging.getLogger(__name__)


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
        try:
            logger.info(f"🔍 [SEARCH_MOTORCYCLES_USE_CASE] Iniciando busca de motocicletas")
            logger.info(f"🔍 [SEARCH_MOTORCYCLES_USE_CASE] Critérios: {search_criteria}")
            
            # Validar parâmetros de busca
            logger.info("🔍 [SEARCH_MOTORCYCLES_USE_CASE] Validando parâmetros...")
            if search_criteria.skip < 0:
                raise ValueError("Parâmetro 'skip' deve ser maior ou igual a zero")
            
            if search_criteria.limit <= 0 or search_criteria.limit > 1000:
                raise ValueError("Parâmetro 'limit' deve estar entre 1 e 1000")
            
            # Buscar motocicletas no repositório
            logger.info("🔍 [SEARCH_MOTORCYCLES_USE_CASE] Chamando repositório find_by_criteria...")
            motorcycles = await self.motorcycle_repository.find_by_criteria(
                model=search_criteria.model,
                price_min=search_criteria.price_min,
                price_max=search_criteria.price_max,
                fuel_type=search_criteria.fuel_type,
                style=search_criteria.style,  # Usando style diretamente
                engine_displacement_min=search_criteria.engine_displacement_min,
                engine_displacement_max=search_criteria.engine_displacement_max,
                status=search_criteria.status,
                available_only=search_criteria.available_only,
                order_by_price=search_criteria.order_by_price,
                skip=search_criteria.skip,
                limit=search_criteria.limit
            )
            logger.info(f"🔍 [SEARCH_MOTORCYCLES_USE_CASE] Repositório retornou {len(motorcycles) if motorcycles else 0} motocicletas")
            
            # Converter para DTOs de resposta
            logger.info("🔍 [SEARCH_MOTORCYCLES_USE_CASE] Convertendo para DTOs...")
            motorcycle_dtos = [self._to_response_dto(motorcycle) for motorcycle in motorcycles]
            logger.info(f"🔍 [SEARCH_MOTORCYCLES_USE_CASE] {len(motorcycle_dtos)} DTOs criados")
            
            # Para simplificar, retornamos o número de motocicletas encontradas como total
            # Em uma implementação real, você faria uma consulta separada para contar o total
            total = len(motorcycle_dtos)
            
            result = MotorcycleListResponseDto(
                motorcycles=motorcycle_dtos,
                total=total,
                skip=search_criteria.skip,
                limit=search_criteria.limit
            )
            logger.info(f"🔍 [SEARCH_MOTORCYCLES_USE_CASE] Resultado final criado com sucesso")
            return result
            
        except Exception as e:
            logger.error(f"❌ [SEARCH_MOTORCYCLES_USE_CASE] Erro na busca: {str(e)}", exc_info=True)
            raise e
    
    def _to_response_dto(self, motorcycle: Motorcycle) -> MotorcycleResponseDto:
        """
        Converte entidade de domínio para DTO de resposta.
        
        Args:
            motorcycle: Entidade de motocicleta
            
        Returns:
            MotorcycleResponseDto: DTO de resposta
        """
        from datetime import datetime
        
        # Tratar valores None de forma segura
        motor_vehicle = motorcycle.motor_vehicle
        
        return MotorcycleResponseDto(
            id=motorcycle.id or 0,
            # Dados do MotorVehicle
            model=motor_vehicle.model or "",
            year=motor_vehicle.year or "",
            price=float(motor_vehicle.price) if motor_vehicle.price else 0.0,
            mileage=motor_vehicle.mileage or 0,
            fuel_type=motor_vehicle.fuel_type or "",
            color=motor_vehicle.color or "",
            city=motor_vehicle.city,
            additional_description=motor_vehicle.additional_description,
            status=motor_vehicle.status or "Ativo",
            # Dados específicos da Motorcycle (usando campos reais do banco)
            starter=motorcycle.starter,
            fuel_system=motorcycle.fuel_system,
            engine_displacement=motorcycle.engine_displacement,
            cooling=motorcycle.cooling,
            style=motorcycle.style,
            engine_type=motorcycle.engine_type,
            gears=motorcycle.gears,
            front_rear_brake=motorcycle.front_rear_brake,
            # Dados calculados
            display_name=f"{motor_vehicle.model or 'Desconhecido'} ({motor_vehicle.year or 'N/A'})",
            # Auditoria - convertendo para string se necessário
            created_at=motorcycle.created_at or motor_vehicle.created_at or datetime.now(),
            updated_at=motorcycle.updated_at or motor_vehicle.updated_at or datetime.now()
        )
