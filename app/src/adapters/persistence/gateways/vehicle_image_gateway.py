"""
Gateway para VehicleImages - Infrastructure Layer

Implementação do repositório de imagens de veículos usando SQLAlchemy.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc, asc
from src.domain.entities.vehicle_image import VehicleImage
from src.domain.ports.repositories.vehicle_image_repository import VehicleImageRepository
from src.infrastructure.database.models.vehicle_image_model import VehicleImageModel
import logging

logger = logging.getLogger(__name__)


class VehicleImageGateway(VehicleImageRepository):
    """Gateway para operações de imagens de veículos."""
    
    def __init__(self, session: Session):
        """
        Inicializa o gateway com uma sessão do banco de dados.
        
        Args:
            session: Sessão do SQLAlchemy
        """
        self._session = session
    
    def create(self, vehicle_image: VehicleImage) -> VehicleImage:
        """Cria uma nova imagem de veículo."""
        try:
            vehicle_image_model = VehicleImageModel(
                vehicle_id=vehicle_image.vehicle_id,
                filename=vehicle_image.filename,
                path=vehicle_image.path,
                thumbnail_path=vehicle_image.thumbnail_path,
                position=vehicle_image.position,
                is_primary=vehicle_image.is_primary,
                uploaded_at=vehicle_image.uploaded_at
            )
            
            self._session.add(vehicle_image_model)
            self._session.commit()  # Commit para persistir no banco
            self._session.refresh(vehicle_image_model)  # Refresh para obter dados atualizados
            
            # Converter de volta para entidade de domínio
            return self._model_to_entity(vehicle_image_model)
            
        except Exception as e:
            logger.error(f"Erro ao criar imagem de veículo: {str(e)}")
            self._session.rollback()
            raise
    
    def get_by_id(self, vehicle_image_id: int) -> Optional[VehicleImage]:
        """Busca uma imagem de veículo por ID."""
        try:
            vehicle_image_model = self._session.query(VehicleImageModel).filter(
                VehicleImageModel.id == vehicle_image_id
            ).first()
            
            if not vehicle_image_model:
                return None
            
            return self._model_to_entity(vehicle_image_model)
            
        except Exception as e:
            logger.error(f"Erro ao buscar imagem por ID {vehicle_image_id}: {str(e)}")
            raise
    
    def get_by_vehicle_id(self, vehicle_id: int) -> List[VehicleImage]:
        """Busca todas as imagens de um veículo específico."""
        try:
            vehicle_image_models = self._session.query(VehicleImageModel).filter(
                VehicleImageModel.vehicle_id == vehicle_id
            ).order_by(asc(VehicleImageModel.position)).all()
            
            # Converter para entidades de domínio
            return [self._model_to_entity(model) for model in vehicle_image_models]
            
        except Exception as e:
            logger.error(f"Erro ao buscar imagens do veículo {vehicle_id}: {str(e)}")
            raise
    
    def get_primary_by_vehicle_id(self, vehicle_id: int) -> Optional[VehicleImage]:
        """Busca a imagem principal de um veículo específico."""
        try:
            vehicle_image_model = self._session.query(VehicleImageModel).filter(
                and_(
                    VehicleImageModel.vehicle_id == vehicle_id,
                    VehicleImageModel.is_primary == True
                )
            ).first()
            
            if not vehicle_image_model:
                return None
            
            return self._model_to_entity(vehicle_image_model)
            
        except Exception as e:
            logger.error(f"Erro ao buscar imagem principal do veículo {vehicle_id}: {str(e)}")
            raise
    
    def update(self, vehicle_image: VehicleImage) -> VehicleImage:
        """Atualiza uma imagem de veículo existente."""
        try:
            vehicle_image_model = self._session.query(VehicleImageModel).filter(
                VehicleImageModel.id == vehicle_image.id
            ).first()
            
            if not vehicle_image_model:
                raise ValueError(f"Imagem com ID {vehicle_image.id} não encontrada")
            
            # Atualizar campos
            vehicle_image_model.vehicle_id = vehicle_image.vehicle_id
            vehicle_image_model.filename = vehicle_image.filename
            vehicle_image_model.path = vehicle_image.path
            vehicle_image_model.thumbnail_path = vehicle_image.thumbnail_path
            vehicle_image_model.position = vehicle_image.position
            vehicle_image_model.is_primary = vehicle_image.is_primary
            vehicle_image_model.uploaded_at = vehicle_image.uploaded_at
            
            self._session.commit()
            self._session.refresh(vehicle_image_model)
            
            return self._model_to_entity(vehicle_image_model)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar imagem {vehicle_image.id}: {str(e)}")
            self._session.rollback()
            raise
    
    def delete(self, vehicle_image_id: int) -> bool:
        """Remove uma imagem de veículo."""
        try:
            vehicle_image_model = self._session.query(VehicleImageModel).filter(
                VehicleImageModel.id == vehicle_image_id
            ).first()
            
            if not vehicle_image_model:
                return False
            
            self._session.delete(vehicle_image_model)
            self._session.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao deletar imagem {vehicle_image_id}: {str(e)}")
            self._session.rollback()
            raise
    
    def exists(self, vehicle_image_id: int) -> bool:
        """Verifica se uma imagem existe."""
        try:
            count = self._session.query(VehicleImageModel).filter(
                VehicleImageModel.id == vehicle_image_id
            ).count()
            
            return count > 0
            
        except Exception as e:
            logger.error(f"Erro ao verificar existência da imagem {vehicle_image_id}: {str(e)}")
            raise
    
    def count_by_vehicle_id(self, vehicle_id: int) -> int:
        """Conta quantas imagens um veículo possui."""
        try:
            count = self._session.query(VehicleImageModel).filter(
                VehicleImageModel.vehicle_id == vehicle_id
            ).count()
            
            return count
            
        except Exception as e:
            logger.error(f"Erro ao contar imagens do veículo {vehicle_id}: {str(e)}")
            raise
    
    def get_next_position(self, vehicle_id: int) -> int:
        """Retorna a próxima posição disponível para uma nova imagem."""
        try:
            max_position = self._session.query(func.max(VehicleImageModel.position)).filter(
                VehicleImageModel.vehicle_id == vehicle_id
            ).scalar()
            
            return (max_position or 0) + 1
            
        except Exception as e:
            logger.error(f"Erro ao obter próxima posição para o veículo {vehicle_id}: {str(e)}")
            raise
    
    def update_positions_after_delete(self, vehicle_id: int, deleted_position: int) -> None:
        """Reorganiza as posições das imagens após uma exclusão."""
        try:
            # Buscar todas as imagens com posição maior que a deletada
            vehicle_images = self._session.query(VehicleImageModel).filter(
                and_(
                    VehicleImageModel.vehicle_id == vehicle_id,
                    VehicleImageModel.position > deleted_position
                )
            ).all()
            
            # Decrementar a posição de cada uma
            for image in vehicle_images:
                image.position -= 1
            
            self._session.commit()
            
        except Exception as e:
            logger.error(f"Erro ao reorganizar posições após deletar posição {deleted_position} do veículo {vehicle_id}: {str(e)}")
            self._session.rollback()
            raise
    
    def _model_to_entity(self, vehicle_image_model: VehicleImageModel) -> VehicleImage:
        """Converte um modelo SQLAlchemy para entidade de domínio."""
        return VehicleImage(
            id=vehicle_image_model.id,
            vehicle_id=vehicle_image_model.vehicle_id,
            filename=vehicle_image_model.filename,
            path=vehicle_image_model.path,
            thumbnail_path=vehicle_image_model.thumbnail_path,
            position=vehicle_image_model.position,
            is_primary=vehicle_image_model.is_primary,
            uploaded_at=vehicle_image_model.uploaded_at
        )
