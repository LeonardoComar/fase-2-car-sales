from typing import Optional
import logging
from src.application.dtos.motorcycle_dto import MotorcycleUpdateDto, MotorcycleResponseDto
from src.domain.entities.motorcycle import Motorcycle
from src.domain.ports.motorcycle_repository import MotorcycleRepository
from src.domain.exceptions import NotFoundError, ValidationError, BusinessRuleError

# Setup logging
logger = logging.getLogger(__name__)


class UpdateMotorcycleUseCase:
    """
    Use case para atualização de motocicletas.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela atualização de motocicletas.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    depende da abstração MotorcycleRepository, não da implementação.
    """
    
    def __init__(self, motorcycle_repository: MotorcycleRepository):
        self.motorcycle_repository = motorcycle_repository
    
    async def execute(
        self, 
        motorcycle_id: int, 
        update_data: MotorcycleUpdateDto
    ) -> MotorcycleResponseDto:
        """
        Executa a atualização de uma motocicleta.
        
        Args:
            motorcycle_id: ID da motocicleta a ser atualizada
            update_data: Dados para atualização
            
        Returns:
            MotorcycleResponseDto: Dados da motocicleta atualizada
            
        Raises:
            NotFoundError: Se a motocicleta não for encontrada
            ValidationError: Se os dados não forem válidos
            BusinessRuleError: Se as regras de negócio não forem atendidas
        """
        # Buscar a motocicleta existente
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Buscando motocicleta ID: {motorcycle_id}")
        existing_motorcycle = await self.motorcycle_repository.find_by_id(motorcycle_id)
        
        if not existing_motorcycle:
            logger.error(f"❌ [UPDATE_MOTORCYCLE_USE_CASE] Motocicleta não encontrada: {motorcycle_id}")
            raise NotFoundError("Motocicleta", str(motorcycle_id))
        
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Motocicleta encontrada. Preço atual: {existing_motorcycle.motor_vehicle.price}")
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Quilometragem atual: {existing_motorcycle.motor_vehicle.mileage}")
        
        # Validar regras de negócio antes da atualização
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Validando regras de negócio...")
        await self._validate_business_rules(existing_motorcycle, update_data)
        
        # Aplicar atualizações
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Aplicando atualizações...")
        updated_motorcycle = self._apply_updates(existing_motorcycle, update_data)
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Atualizações aplicadas com sucesso")
        
        # Salvar no repositório
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Salvando no repositório...")
        saved_motorcycle = await self.motorcycle_repository.update(updated_motorcycle)
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Motocicleta salva com sucesso")
        
        # Converter para DTO de resposta
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Convertendo para DTO de resposta...")
        result = self._to_response_dto(saved_motorcycle)
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] DTO de resposta criado com sucesso")
        
        return result
    
    async def _validate_business_rules(
        self, 
        existing_motorcycle: Motorcycle, 
        update_data: MotorcycleUpdateDto
    ) -> None:
        """
        Valida regras de negócio para atualização.
        
        Args:
            existing_motorcycle: Motocicleta existente
            update_data: Dados de atualização
            
        Raises:
            BusinessRuleError: Se alguma regra de negócio for violada
        """
        # Regra: Não permitir redução de preço muito drástica
        if update_data.price is not None:
            logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Validando preço. Atual: {existing_motorcycle.motor_vehicle.price}, Novo: {update_data.price}")
            current_price = existing_motorcycle.motor_vehicle.price
            
            # Verificar se há mudança de preço
            if current_price != update_data.price:
                price_reduction_percentage = ((current_price - update_data.price) / current_price) * 100
                logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Redução de preço: {price_reduction_percentage:.1f}%")
                
                if price_reduction_percentage > 50:
                    raise BusinessRuleError(
                        f"Redução de preço muito drástica ({price_reduction_percentage:.1f}%). "
                        "Máximo permitido: 50%",
                        "excessive_price_reduction"
                    )
            else:
                logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Preço mantido igual - sem mudanças")
        
        # Regra: Validar aumento de quilometragem
        if update_data.mileage is not None:
            logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Validando quilometragem. Atual: {existing_motorcycle.motor_vehicle.mileage}, Nova: {update_data.mileage}")
            if update_data.mileage < existing_motorcycle.motor_vehicle.mileage:
                raise BusinessRuleError(
                    "Não é possível reduzir a quilometragem",
                    "mileage_reduction"
                )
        
        # Regra: Verificar mudança de status
        if update_data.status is not None:
            logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Validando status. Atual: {existing_motorcycle.motor_vehicle.status}, Novo: {update_data.status}")
            await self._validate_status_change(existing_motorcycle, update_data.status)
        
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Todas as regras de negócio validadas com sucesso")
    
    async def _validate_status_change(
        self, 
        existing_motorcycle: Motorcycle, 
        new_status: str
    ) -> None:
        """
        Valida mudança de status.
        
        Args:
            existing_motorcycle: Motocicleta existente
            new_status: Novo status
            
        Raises:
            BusinessRuleError: Se a mudança de status não for válida
        """
        current_status = existing_motorcycle.motor_vehicle.status
        
        # Regra: Motocicleta vendida não pode voltar para outros status
        if current_status == "Vendido" and new_status != "Vendido":
            raise BusinessRuleError(
                "Motocicleta vendida não pode ter seu status alterado",
                "sold_motorcycle_status_change"
            )
        
        # Regra: Validar transições válidas
        valid_transitions = {
            "Ativo": ["Inativo", "Vendido", "Reservado", "Em Manutenção"],
            "Inativo": ["Ativo", "Em Manutenção"],
            "Reservado": ["Ativo", "Vendido", "Em Manutenção"],
            "Em Manutenção": ["Ativo", "Inativo"],
            "Vendido": []  # Vendido não pode ser alterado
        }
        
        if new_status not in valid_transitions.get(current_status, []):
            raise BusinessRuleError(
                f"Transição de status inválida: {current_status} -> {new_status}",
                "invalid_status_transition"
            )
    
    def _apply_updates(
        self, 
        existing_motorcycle: Motorcycle, 
        update_data: MotorcycleUpdateDto
    ) -> Motorcycle:
        """
        Aplica as atualizações à entidade existente.
        
        Args:
            existing_motorcycle: Motocicleta existente
            update_data: Dados de atualização
            
        Returns:
            Motorcycle: Motocicleta atualizada
        """
        # Atualizar dados do MotorVehicle
        motor_vehicle_updates = {}
        
        if update_data.model is not None:
            motor_vehicle_updates['model'] = update_data.model
        if update_data.year is not None:
            motor_vehicle_updates['year'] = update_data.year
        if update_data.price is not None:
            motor_vehicle_updates['price'] = update_data.price
        if update_data.mileage is not None:
            motor_vehicle_updates['mileage'] = update_data.mileage
        if update_data.fuel_type is not None:
            motor_vehicle_updates['fuel_type'] = update_data.fuel_type
        if update_data.engine_power is not None:
            motor_vehicle_updates['engine_power'] = update_data.engine_power
        if update_data.color is not None:
            motor_vehicle_updates['color'] = update_data.color
        if update_data.status is not None:
            motor_vehicle_updates['status'] = update_data.status
        if update_data.description is not None:
            motor_vehicle_updates['description'] = update_data.description
        
        # Aplicar atualizações ao MotorVehicle
        if motor_vehicle_updates:
            logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Aplicando atualizações ao MotorVehicle: {motor_vehicle_updates}")
            
            # Atualizar campos diretamente
            for field, value in motor_vehicle_updates.items():
                if hasattr(existing_motorcycle.motor_vehicle, field):
                    setattr(existing_motorcycle.motor_vehicle, field, value)
                    logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Campo {field} atualizado para: {value}")
                    
            logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] MotorVehicle atualizado com sucesso")
        
        # Atualizar dados específicos da Motorcycle
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Aplicando atualizações específicas da Motorcycle...")
        existing_motorcycle.update_motorcycle_data(
            style=update_data.style,
            starter=update_data.starter,
            fuel_system=update_data.fuel_system,
            engine_displacement=update_data.engine_displacement,
            cooling=update_data.cooling,
            engine_type=update_data.engine_type,
            gears=update_data.gears,
            front_rear_brake=update_data.front_rear_brake
        )
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Motorcycle atualizada com sucesso")
        
        return existing_motorcycle
    
    def _to_response_dto(self, motorcycle: Motorcycle) -> MotorcycleResponseDto:
        """
        Converte entidade de domínio para DTO de resposta.
        
        Args:
            motorcycle: Entidade de motocicleta
            
        Returns:
            MotorcycleResponseDto: DTO de resposta
        """
        logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Criando DTO de resposta para motocicleta ID: {motorcycle.id}")
        
        try:
            # Testar acesso aos campos básicos
            logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Acessando dados básicos...")
            id_val = motorcycle.id
            model_val = motorcycle.motor_vehicle.model
            year_val = motorcycle.motor_vehicle.year
            logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Dados básicos OK - ID: {id_val}, Model: {model_val}, Year: {year_val}")
            
            # Testar campos específicos da motorcycle
            logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Acessando dados específicos...")
            style_val = motorcycle.style
            starter_val = motorcycle.starter
            logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Dados específicos OK - Style: {style_val}, Starter: {starter_val}")
            
            # Testar métodos calculados
            logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Acessando métodos calculados...")
            display_name_val = motorcycle.get_display_name()
            logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Display name OK: {display_name_val}")
            
            # Criar o DTO
            logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] Criando DTO...")
            result = MotorcycleResponseDto(
                id=motorcycle.id,
                # Dados do MotorVehicle
                model=motorcycle.motor_vehicle.model,
                year=motorcycle.motor_vehicle.year,
                price=motorcycle.motor_vehicle.price,
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
                display_name=motorcycle.get_display_name(),
                # Auditoria
                created_at=motorcycle.created_at,
                updated_at=motorcycle.updated_at
            )
            logger.info(f"🔍 [UPDATE_MOTORCYCLE_USE_CASE] DTO criado com sucesso")
            return result
            
        except Exception as e:
            logger.error(f"❌ [UPDATE_MOTORCYCLE_USE_CASE] Erro ao criar DTO: {str(e)}", exc_info=True)
            raise e
