from typing import Optional
from src.application.dtos.motorcycle_dto import MotorcycleUpdateDto, MotorcycleResponseDto
from src.domain.entities.motorcycle import Motorcycle
from src.domain.ports.motorcycle_repository import MotorcycleRepository
from src.domain.exceptions import NotFoundError, ValidationError, BusinessRuleError


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
        existing_motorcycle = await self.motorcycle_repository.find_by_id(motorcycle_id)
        
        if not existing_motorcycle:
            raise NotFoundError("Motocicleta", str(motorcycle_id))
        
        # Validar regras de negócio antes da atualização
        await self._validate_business_rules(existing_motorcycle, update_data)
        
        # Aplicar atualizações
        updated_motorcycle = self._apply_updates(existing_motorcycle, update_data)
        
        # Salvar no repositório
        saved_motorcycle = await self.motorcycle_repository.update(updated_motorcycle)
        
        # Converter para DTO de resposta
        return self._to_response_dto(saved_motorcycle)
    
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
        # Regra: Não permitir alteração de cilindrada se a motocicleta foi vendida
        if (existing_motorcycle.motor_vehicle.status == "Vendido" and 
            update_data.cylinder_capacity is not None and
            update_data.cylinder_capacity != existing_motorcycle.cylinder_capacity):
            raise BusinessRuleError(
                "Não é possível alterar cilindrada de motocicleta vendida",
                "sold_motorcycle_cylinder_change"
            )
        
        # Regra: Não permitir redução de preço muito drástica
        if update_data.price is not None:
            current_price = existing_motorcycle.motor_vehicle.price
            price_reduction_percentage = ((current_price - update_data.price) / current_price) * 100
            
            if price_reduction_percentage > 50:
                raise BusinessRuleError(
                    f"Redução de preço muito drástica ({price_reduction_percentage:.1f}%). "
                    "Máximo permitido: 50%",
                    "excessive_price_reduction"
                )
        
        # Regra: Validar aumento de quilometragem
        if update_data.mileage is not None:
            if update_data.mileage < existing_motorcycle.motor_vehicle.mileage:
                raise BusinessRuleError(
                    "Não é possível reduzir a quilometragem",
                    "mileage_reduction"
                )
        
        # Regra: Verificar mudança de status
        if update_data.status is not None:
            await self._validate_status_change(existing_motorcycle, update_data.status)
    
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
        
        if update_data.brand is not None:
            motor_vehicle_updates['brand'] = update_data.brand
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
            existing_motorcycle.motor_vehicle.update_data(**motor_vehicle_updates)
        
        # Atualizar dados específicos da Motorcycle
        existing_motorcycle.update_motorcycle_data(
            motorcycle_type=update_data.motorcycle_type,
            cylinder_capacity=update_data.cylinder_capacity,
            has_abs=update_data.has_abs,
            has_traction_control=update_data.has_traction_control,
            seat_height=update_data.seat_height,
            dry_weight=update_data.dry_weight,
            fuel_capacity=update_data.fuel_capacity
        )
        
        return existing_motorcycle
    
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
