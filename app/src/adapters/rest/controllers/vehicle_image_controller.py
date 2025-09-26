"""
Controller para VehicleImages - Adapter Layer

Responsável por coordenar as requisições HTTP relacionadas a imagens de veículos.

Aplicando princípios SOLID:
- SRP: Responsável apenas por coordenar operações de imagens de veículos
- OCP: Extensível para novas operações sem modificar código existente
- LSP: Pode ser substituído por outras implementações
- ISP: Interface específica para operações de imagens de veículos
- DIP: Depende de abstrações (use cases) não de implementações
"""

from typing import List, Optional
from fastapi import HTTPException
from src.application.use_cases.vehicles.vehicle_image_use_cases import (
    CreateVehicleImageUseCase,
    GetVehicleImageUseCase,
    GetVehicleImagesUseCase,
    GetPrimaryVehicleImageUseCase,
    UpdateVehicleImageUseCase,
    DeleteVehicleImageUseCase,
    SetPrimaryVehicleImageUseCase
)
from src.application.dtos.vehicle_image_dto import (
    VehicleImageCreateDTO,
    VehicleImageUpdateDTO,
    VehicleImageResponseDTO,
    VehicleImageListResponseDTO,
    VehicleImageUploadResponseDTO
)
from src.adapters.rest.presenters.vehicle_image_presenter import VehicleImagePresenter
from src.domain.entities.vehicle_image import VehicleImage
from src.domain.exceptions import NotFoundError, ValidationError, BusinessRuleError


class VehicleImageController:
    """
    Controller para gerenciamento de imagens de veículos.
    
    Coordena as operações CRUD relacionadas a imagens de veículos,
    delegando a lógica de negócio para os use cases apropriados.
    """
    
    def __init__(
        self,
        create_vehicle_image_use_case: CreateVehicleImageUseCase,
        get_vehicle_image_use_case: GetVehicleImageUseCase,
        get_vehicle_images_use_case: GetVehicleImagesUseCase,
        get_primary_vehicle_image_use_case: GetPrimaryVehicleImageUseCase,
        update_vehicle_image_use_case: UpdateVehicleImageUseCase,
        delete_vehicle_image_use_case: DeleteVehicleImageUseCase,
        set_primary_vehicle_image_use_case: SetPrimaryVehicleImageUseCase,
        presenter: VehicleImagePresenter
    ):
        """
        Inicializa o controller com os use cases necessários.
        
        Args:
            create_vehicle_image_use_case: Use case para criação de imagens
            get_vehicle_image_use_case: Use case para busca por ID
            get_vehicle_images_use_case: Use case para listagem de imagens
            get_primary_vehicle_image_use_case: Use case para busca da imagem principal
            update_vehicle_image_use_case: Use case para atualização de imagens
            delete_vehicle_image_use_case: Use case para exclusão de imagens
            set_primary_vehicle_image_use_case: Use case para definir imagem principal
        """
        self._create_vehicle_image_use_case = create_vehicle_image_use_case
        self._get_vehicle_image_use_case = get_vehicle_image_use_case
        self._get_vehicle_images_use_case = get_vehicle_images_use_case
        self._get_primary_vehicle_image_use_case = get_primary_vehicle_image_use_case
        self._update_vehicle_image_use_case = update_vehicle_image_use_case
        self._delete_vehicle_image_use_case = delete_vehicle_image_use_case
        self._set_primary_vehicle_image_use_case = set_primary_vehicle_image_use_case
        self._presenter = presenter
    
    async def create_vehicle_image(self, image_data: VehicleImageCreateDTO) -> VehicleImageUploadResponseDTO:
        """
        Cria uma nova imagem de veículo.
        
        Args:
            image_data: Dados da imagem a ser criada
            
        Returns:
            VehicleImageUploadResponseDTO: Dados da imagem criada
            
        Raises:
            HTTPException: Em caso de erro na criação
        """
        try:
            # Validar se os dados básicos são válidos
            if not image_data.filename or not image_data.path:
                raise HTTPException(
                    status_code=400, 
                    detail="Filename e path são obrigatórios"
                )
            
            # Converter DTO para entidade
            vehicle_image = VehicleImage(
                vehicle_id=image_data.vehicle_id,
                filename=image_data.filename,
                path=image_data.path,
                thumbnail_path=image_data.thumbnail_path,
                position=image_data.position,
                is_primary=image_data.is_primary
            )
            
            created_image = self._create_vehicle_image_use_case.execute(vehicle_image)
            
            # Converter entidade para DTO de resposta com URLs completas
            image_response = self._presenter.to_response_dto(created_image)
            
            return VehicleImageUploadResponseDTO(
                success=True,
                image=image_response,
                message="Imagem criada com sucesso"
            )
            
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        except BusinessRuleError as e:
            raise HTTPException(status_code=422, detail=str(e))
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    async def get_vehicle_image_by_id(self, image_id: int) -> VehicleImageResponseDTO:
        """
        Busca uma imagem por ID.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            VehicleImageResponseDTO: Dados da imagem encontrada
            
        Raises:
            HTTPException: Se imagem não for encontrada ou houver erro
        """
        try:
            vehicle_image = self._get_vehicle_image_use_case.execute(image_id)
            
            return VehicleImageResponseDTO(
                id=vehicle_image.id,
                vehicle_id=vehicle_image.vehicle_id,
                filename=vehicle_image.filename,
                path=vehicle_image.path,
                thumbnail_path=vehicle_image.thumbnail_path,
                position=vehicle_image.position,
                is_primary=vehicle_image.is_primary,
                uploaded_at=vehicle_image.uploaded_at
            )
            
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    async def get_vehicle_images(self, vehicle_id: int) -> VehicleImageListResponseDTO:
        """
        Lista todas as imagens de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            VehicleImageListResponseDTO: Lista de imagens do veículo
            
        Raises:
            HTTPException: Em caso de erro na listagem
        """
        try:
            vehicle_images = self._get_vehicle_images_use_case.execute(vehicle_id)
            primary_image = self._get_primary_vehicle_image_use_case.execute(vehicle_id)
            
            # Converter entidades para DTOs
            images_response = [
                VehicleImageResponseDTO(
                    id=image.id,
                    vehicle_id=image.vehicle_id,
                    filename=image.filename,
                    path=image.path,
                    thumbnail_path=image.thumbnail_path,
                    position=image.position,
                    is_primary=image.is_primary,
                    uploaded_at=image.uploaded_at
                )
                for image in vehicle_images
            ]
            
            primary_response = None
            if primary_image:
                primary_response = VehicleImageResponseDTO(
                    id=primary_image.id,
                    vehicle_id=primary_image.vehicle_id,
                    filename=primary_image.filename,
                    path=primary_image.path,
                    thumbnail_path=primary_image.thumbnail_path,
                    position=primary_image.position,
                    is_primary=primary_image.is_primary,
                    uploaded_at=primary_image.uploaded_at
                )
            
            return VehicleImageListResponseDTO(
                vehicle_id=vehicle_id,
                images=images_response,
                total_images=len(images_response),
                primary_image=primary_response
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    async def get_primary_vehicle_image(self, vehicle_id: int) -> Optional[VehicleImageResponseDTO]:
        """
        Busca a imagem principal de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            
        Returns:
            Optional[VehicleImageResponseDTO]: Imagem principal ou None
            
        Raises:
            HTTPException: Em caso de erro na busca
        """
        try:
            primary_image = self._get_primary_vehicle_image_use_case.execute(vehicle_id)
            
            if not primary_image:
                return None
            
            return VehicleImageResponseDTO(
                id=primary_image.id,
                vehicle_id=primary_image.vehicle_id,
                filename=primary_image.filename,
                path=primary_image.path,
                thumbnail_path=primary_image.thumbnail_path,
                position=primary_image.position,
                is_primary=primary_image.is_primary,
                uploaded_at=primary_image.uploaded_at
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    async def update_vehicle_image(self, image_id: int, update_data: VehicleImageUpdateDTO) -> VehicleImageResponseDTO:
        """
        Atualiza uma imagem de veículo.
        
        Args:
            image_id: ID da imagem
            update_data: Dados para atualização
            
        Returns:
            VehicleImageResponseDTO: Dados da imagem atualizada
            
        Raises:
            HTTPException: Se imagem não for encontrada ou houver erro
        """
        try:
            # Converter apenas campos não nulos para dicionário
            updates = {}
            if update_data.position is not None:
                updates['position'] = update_data.position
            if update_data.is_primary is not None:
                updates['is_primary'] = update_data.is_primary
            
            updated_image = self._update_vehicle_image_use_case.execute(image_id, **updates)
            
            return VehicleImageResponseDTO(
                id=updated_image.id,
                vehicle_id=updated_image.vehicle_id,
                filename=updated_image.filename,
                path=updated_image.path,
                thumbnail_path=updated_image.thumbnail_path,
                position=updated_image.position,
                is_primary=updated_image.is_primary,
                uploaded_at=updated_image.uploaded_at
            )
            
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        
        except BusinessRuleError as e:
            raise HTTPException(status_code=422, detail=str(e))
        
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    async def delete_vehicle_image(self, image_id: int) -> dict:
        """
        Remove uma imagem de veículo.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            dict: Confirmação da remoção
            
        Raises:
            HTTPException: Se imagem não for encontrada ou houver erro
        """
        try:
            success = self._delete_vehicle_image_use_case.execute(image_id)
            
            if not success:
                raise HTTPException(status_code=404, detail=f"Imagem com ID {image_id} não encontrada")
            
            return {"message": "Imagem removida com sucesso"}
            
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        
        except BusinessRuleError as e:
            raise HTTPException(status_code=422, detail=str(e))
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
    
    async def set_primary_image(self, image_id: int) -> VehicleImageResponseDTO:
        """
        Define uma imagem como principal.
        
        Args:
            image_id: ID da imagem
            
        Returns:
            VehicleImageResponseDTO: Dados da imagem definida como principal
            
        Raises:
            HTTPException: Se imagem não for encontrada ou houver erro
        """
        try:
            updated_image = self._set_primary_vehicle_image_use_case.execute(image_id)
            
            return VehicleImageResponseDTO(
                id=updated_image.id,
                vehicle_id=updated_image.vehicle_id,
                filename=updated_image.filename,
                path=updated_image.path,
                thumbnail_path=updated_image.thumbnail_path,
                position=updated_image.position,
                is_primary=updated_image.is_primary,
                uploaded_at=updated_image.uploaded_at
            )
            
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
