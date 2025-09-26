from typing import List, Optional
from src.domain.entities.vehicle_image import VehicleImage
from src.domain.ports.repositories.vehicle_image_repository import VehicleImageRepository
from src.domain.exceptions import NotFoundError, ValidationError, BusinessRuleError


class CreateVehicleImageUseCase:
    """Use case para criar uma nova imagem de veículo."""
    
    def __init__(self, repository: VehicleImageRepository):
        self.repository = repository
    
    def execute(self, vehicle_image: VehicleImage) -> VehicleImage:
        """
        Executa a criação de uma nova imagem de veículo.
        
        Args:
            vehicle_image: A imagem a ser criada
            
        Returns:
            VehicleImage: A imagem criada
            
        Raises:
            ValidationError: Se os dados são inválidos
            BusinessRuleError: Se violou regras de negócio
        """
        # Validar se o veículo não excedeu o limite de imagens
        current_count = self.repository.count_by_vehicle_id(vehicle_image.vehicle_id)
        if current_count >= VehicleImage.MAX_IMAGES_PER_VEHICLE:
            raise BusinessRuleError(
                f"Veículo já possui o máximo de {VehicleImage.MAX_IMAGES_PER_VEHICLE} imagens"
            )
        
        # Se não foi especificada uma posição, usar a próxima disponível
        if vehicle_image.position is None:
            vehicle_image.position = self.repository.get_next_position(vehicle_image.vehicle_id)
        
        # Se é para ser a imagem principal, remover primary de outras imagens
        if vehicle_image.is_primary:
            current_primary = self.repository.get_primary_by_vehicle_id(vehicle_image.vehicle_id)
            if current_primary:
                current_primary.remove_primary()
                self.repository.update(current_primary)
        
        # Se é a primeira imagem do veículo, automaticamente torná-la principal
        if current_count == 0:
            vehicle_image.set_as_primary()
        
        return self.repository.create(vehicle_image)


class GetVehicleImageUseCase:
    """Use case para buscar uma imagem específica."""
    
    def __init__(self, repository: VehicleImageRepository):
        self.repository = repository
    
    def execute(self, vehicle_image_id: int) -> VehicleImage:
        """
        Executa a busca de uma imagem por ID.
        
        Args:
            vehicle_image_id: ID da imagem
            
        Returns:
            VehicleImage: A imagem encontrada
            
        Raises:
            NotFoundError: Se a imagem não existe
        """
        vehicle_image = self.repository.get_by_id(vehicle_image_id)
        if not vehicle_image:
            raise NotFoundError(f"Imagem com ID {vehicle_image_id} não encontrada")
        
        return vehicle_image


class GetVehicleImagesUseCase:
    """Use case para buscar todas as imagens de um veículo."""
    
    def __init__(self, repository: VehicleImageRepository):
        self.repository = repository
    
    def execute(self, vehicle_id: int) -> List[VehicleImage]:
        """
        Executa a busca de todas as imagens de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            List[VehicleImage]: Lista de imagens do veículo
        """
        return self.repository.get_by_vehicle_id(vehicle_id)


class GetPrimaryVehicleImageUseCase:
    """Use case para buscar a imagem principal de um veículo."""
    
    def __init__(self, repository: VehicleImageRepository):
        self.repository = repository
    
    def execute(self, vehicle_id: int) -> Optional[VehicleImage]:
        """
        Executa a busca da imagem principal de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Optional[VehicleImage]: A imagem principal ou None
        """
        return self.repository.get_primary_by_vehicle_id(vehicle_id)


class UpdateVehicleImageUseCase:
    """Use case para atualizar uma imagem de veículo."""
    
    def __init__(self, repository: VehicleImageRepository):
        self.repository = repository
    
    def execute(self, vehicle_image_id: int, **updates) -> VehicleImage:
        """
        Executa a atualização de uma imagem.
        
        Args:
            vehicle_image_id: ID da imagem
            **updates: Campos a serem atualizados
            
        Returns:
            VehicleImage: A imagem atualizada
            
        Raises:
            NotFoundError: Se a imagem não existe
            BusinessRuleError: Se violou regras de negócio
        """
        vehicle_image = self.repository.get_by_id(vehicle_image_id)
        if not vehicle_image:
            raise NotFoundError(f"Imagem com ID {vehicle_image_id} não encontrada")
        
        # Se está definindo como principal, remover primary de outras imagens
        if updates.get('is_primary') is True and not vehicle_image.is_primary:
            current_primary = self.repository.get_primary_by_vehicle_id(vehicle_image.vehicle_id)
            if current_primary and current_primary.id != vehicle_image_id:
                current_primary.remove_primary()
                self.repository.update(current_primary)
        
        # Aplicar atualizações
        for field, value in updates.items():
            if hasattr(vehicle_image, field):
                if field == 'position' and value is not None:
                    vehicle_image.update_position(value)
                elif field == 'is_primary':
                    if value:
                        vehicle_image.set_as_primary()
                    else:
                        vehicle_image.remove_primary()
                else:
                    setattr(vehicle_image, field, value)
        
        return self.repository.update(vehicle_image)


class DeleteVehicleImageUseCase:
    """Use case para deletar uma imagem de veículo."""
    
    def __init__(self, repository: VehicleImageRepository):
        self.repository = repository
    
    def execute(self, vehicle_image_id: int) -> bool:
        """
        Executa a remoção de uma imagem.
        
        Args:
            vehicle_image_id: ID da imagem
            
        Returns:
            bool: True se removida com sucesso
            
        Raises:
            NotFoundError: Se a imagem não existe
            BusinessRuleError: Se violou regras de negócio
        """
        vehicle_image = self.repository.get_by_id(vehicle_image_id)
        if not vehicle_image:
            raise NotFoundError(f"Imagem com ID {vehicle_image_id} não encontrada")
        
        # Verificar se não é a única imagem do veículo
        current_count = self.repository.count_by_vehicle_id(vehicle_image.vehicle_id)
        if current_count <= VehicleImage.MIN_IMAGES_PER_VEHICLE:
            raise BusinessRuleError(
                f"Não é possível remover a imagem. Veículo deve ter pelo menos {VehicleImage.MIN_IMAGES_PER_VEHICLE} imagem"
            )
        
        # Se era a imagem principal, definir outra como principal
        was_primary = vehicle_image.is_primary
        deleted_position = vehicle_image.position
        
        success = self.repository.delete(vehicle_image_id)
        
        if success:
            # Remover arquivos físicos
            try:
                from src.application.services.vehicle_image_service import VehicleImageService
                image_service = VehicleImageService()
                image_service.delete_image_files(vehicle_image.vehicle_id, vehicle_image.filename)
            except Exception:
                # Se falhar ao remover arquivos, continuar (dados no banco já foram removidos)
                pass
            
            # Reorganizar posições das imagens restantes
            self.repository.update_positions_after_delete(vehicle_image.vehicle_id, deleted_position)
            
            # Se era principal, definir a primeira imagem como nova principal
            if was_primary:
                remaining_images = self.repository.get_by_vehicle_id(vehicle_image.vehicle_id)
                if remaining_images:
                    # Ordenar por posição e pegar a primeira
                    remaining_images.sort(key=lambda x: x.position)
                    new_primary = remaining_images[0]
                    new_primary.set_as_primary()
                    self.repository.update(new_primary)
        
        return success


class SetPrimaryVehicleImageUseCase:
    """Use case para definir uma imagem como principal."""
    
    def __init__(self, repository: VehicleImageRepository):
        self.repository = repository
    
    def execute(self, vehicle_image_id: int) -> VehicleImage:
        """
        Executa a definição de uma imagem como principal.
        
        Args:
            vehicle_image_id: ID da imagem
            
        Returns:
            VehicleImage: A imagem definida como principal
            
        Raises:
            NotFoundError: Se a imagem não existe
        """
        vehicle_image = self.repository.get_by_id(vehicle_image_id)
        if not vehicle_image:
            raise NotFoundError(f"Imagem com ID {vehicle_image_id} não encontrada")
        
        # Remover primary de outras imagens do mesmo veículo
        current_primary = self.repository.get_primary_by_vehicle_id(vehicle_image.vehicle_id)
        if current_primary and current_primary.id != vehicle_image_id:
            current_primary.remove_primary()
            self.repository.update(current_primary)
        
        # Definir como principal
        vehicle_image.set_as_primary()
        return self.repository.update(vehicle_image)
