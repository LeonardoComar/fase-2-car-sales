"""
Configuração e inicialização do módulo VehicleImage

Configura injeção de dependência e registra componentes
do módulo VehicleImage seguindo Clean Architecture.

Aplicando princípios SOLID:
- SRP: Responsável apenas pela configuração do módulo VehicleImage
- OCP: Extensível para novas implementações sem modificar existentes
- LSP: Permite substituição de implementações
- ISP: Interfaces específicas para cada responsabilidade
- DIP: Configuração baseada em abstrações
"""

from typing import Dict, Any
from fastapi import APIRouter

# Domain
from ...domain.services.image_manager import ImageManager, ImageManagerImpl
from ...domain.ports.vehicle_image_repository import VehicleImageRepository

# Application
from ...application.services.vehicle_image_service import (
    CreateVehicleImageUseCase,
    CreateVehicleImageUseCaseImpl,
    UpdateVehicleImageUseCase,
    UpdateVehicleImageUseCaseImpl,
    DeleteVehicleImageUseCase,
    DeleteVehicleImageUseCaseImpl,
    GetVehicleImageUseCase,
    GetVehicleImageUseCaseImpl,
    SearchVehicleImagesUseCase,
    SearchVehicleImagesUseCaseImpl,
    GetVehicleGalleryUseCase,
    GetVehicleGalleryUseCaseImpl,
    ReorderVehicleImagesUseCase,
    ReorderVehicleImagesUseCaseImpl,
    SetPrimaryImageUseCase,
    SetPrimaryImageUseCaseImpl,
    GenerateThumbnailUseCase,
    GenerateThumbnailUseCaseImpl,
    GetImageStatisticsUseCase,
    GetImageStatisticsUseCaseImpl
)

# Infrastructure
from ...infrastructure.driven.vehicle_image_repository_mock import VehicleImageRepositoryMock
from ...infrastructure.adapters.vehicle_image_controller import create_vehicle_image_router


class VehicleImageModuleConfig:
    """
    Configuração do módulo VehicleImage.
    
    Centraliza a configuração de todas as dependências
    e componentes do módulo VehicleImage.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Inicializa a configuração do módulo.
        
        Args:
            config: Configurações específicas do módulo
        """
        self.config = config or {}
        self._repository: VehicleImageRepository = None
        self._image_manager: ImageManager = None
        self._use_cases: Dict[str, Any] = {}
        self._router: APIRouter = None
    
    def get_repository(self) -> VehicleImageRepository:
        """
        Obtém instância do repositório de imagens.
        
        Returns:
            Implementação do repositório
        """
        if self._repository is None:
            # Por enquanto usando implementação mock
            # Em produção, seria injetado via configuração
            repository_type = self.config.get('repository_type', 'mock')
            
            if repository_type == 'mock':
                self._repository = VehicleImageRepositoryMock()
            else:
                # Outras implementações (SQL, NoSQL, etc.)
                raise NotImplementedError(f"Repository type '{repository_type}' not implemented")
        
        return self._repository
    
    def get_image_manager(self) -> ImageManager:
        """
        Obtém instância do gerenciador de imagens.
        
        Returns:
            Implementação do gerenciador de imagens
        """
        if self._image_manager is None:
            # Por enquanto usando implementação mock
            # Em produção, seria injetado via configuração
            manager_type = self.config.get('image_manager_type', 'mock')
            storage_path = self.config.get('storage_path', '/uploads')
            
            if manager_type == 'mock':
                self._image_manager = ImageManagerImpl(storage_path)
            else:
                # Outras implementações (S3, Azure, etc.)
                raise NotImplementedError(f"Image manager type '{manager_type}' not implemented")
        
        return self._image_manager
    
    def get_create_use_case(self) -> CreateVehicleImageUseCase:
        """Obtém use case de criação de imagem."""
        if 'create' not in self._use_cases:
            self._use_cases['create'] = CreateVehicleImageUseCaseImpl(
                repository=self.get_repository(),
                image_manager=self.get_image_manager()
            )
        return self._use_cases['create']
    
    def get_update_use_case(self) -> UpdateVehicleImageUseCase:
        """Obtém use case de atualização de imagem."""
        if 'update' not in self._use_cases:
            self._use_cases['update'] = UpdateVehicleImageUseCaseImpl(
                repository=self.get_repository(),
                image_manager=self.get_image_manager()
            )
        return self._use_cases['update']
    
    def get_delete_use_case(self) -> DeleteVehicleImageUseCase:
        """Obtém use case de exclusão de imagem."""
        if 'delete' not in self._use_cases:
            self._use_cases['delete'] = DeleteVehicleImageUseCaseImpl(
                repository=self.get_repository(),
                image_manager=self.get_image_manager()
            )
        return self._use_cases['delete']
    
    def get_get_use_case(self) -> GetVehicleImageUseCase:
        """Obtém use case de obtenção de imagem."""
        if 'get' not in self._use_cases:
            self._use_cases['get'] = GetVehicleImageUseCaseImpl(
                repository=self.get_repository()
            )
        return self._use_cases['get']
    
    def get_search_use_case(self) -> SearchVehicleImagesUseCase:
        """Obtém use case de busca de imagens."""
        if 'search' not in self._use_cases:
            self._use_cases['search'] = SearchVehicleImagesUseCaseImpl(
                repository=self.get_repository()
            )
        return self._use_cases['search']
    
    def get_gallery_use_case(self) -> GetVehicleGalleryUseCase:
        """Obtém use case de galeria de veículo."""
        if 'gallery' not in self._use_cases:
            self._use_cases['gallery'] = GetVehicleGalleryUseCaseImpl(
                repository=self.get_repository()
            )
        return self._use_cases['gallery']
    
    def get_reorder_use_case(self) -> ReorderVehicleImagesUseCase:
        """Obtém use case de reordenação de imagens."""
        if 'reorder' not in self._use_cases:
            self._use_cases['reorder'] = ReorderVehicleImagesUseCaseImpl(
                repository=self.get_repository()
            )
        return self._use_cases['reorder']
    
    def get_set_primary_use_case(self) -> SetPrimaryImageUseCase:
        """Obtém use case de definição de imagem principal."""
        if 'set_primary' not in self._use_cases:
            self._use_cases['set_primary'] = SetPrimaryImageUseCaseImpl(
                repository=self.get_repository()
            )
        return self._use_cases['set_primary']
    
    def get_generate_thumbnail_use_case(self) -> GenerateThumbnailUseCase:
        """Obtém use case de geração de miniatura."""
        if 'generate_thumbnail' not in self._use_cases:
            self._use_cases['generate_thumbnail'] = GenerateThumbnailUseCaseImpl(
                repository=self.get_repository(),
                image_manager=self.get_image_manager()
            )
        return self._use_cases['generate_thumbnail']
    
    def get_statistics_use_case(self) -> GetImageStatisticsUseCase:
        """Obtém use case de estatísticas."""
        if 'statistics' not in self._use_cases:
            self._use_cases['statistics'] = GetImageStatisticsUseCaseImpl(
                repository=self.get_repository()
            )
        return self._use_cases['statistics']
    
    def get_router(self) -> APIRouter:
        """
        Obtém router configurado com todos os endpoints.
        
        Returns:
            Router do FastAPI configurado
        """
        if self._router is None:
            self._router = create_vehicle_image_router(
                create_use_case=self.get_create_use_case(),
                update_use_case=self.get_update_use_case(),
                delete_use_case=self.get_delete_use_case(),
                get_use_case=self.get_get_use_case(),
                search_use_case=self.get_search_use_case(),
                gallery_use_case=self.get_gallery_use_case(),
                reorder_use_case=self.get_reorder_use_case(),
                set_primary_use_case=self.get_set_primary_use_case(),
                generate_thumbnail_use_case=self.get_generate_thumbnail_use_case(),
                statistics_use_case=self.get_statistics_use_case()
            )
        
        return self._router
    
    def configure_settings(self, settings: Dict[str, Any]) -> None:
        """
        Configura settings específicos do módulo.
        
        Args:
            settings: Configurações a aplicar
        """
        self.config.update(settings)
        
        # Limpar cache de instâncias para recriar com novas configurações
        self._repository = None
        self._image_manager = None
        self._use_cases.clear()
        self._router = None
    
    def health_check(self) -> Dict[str, Any]:
        """
        Verifica saúde do módulo.
        
        Returns:
            Status de saúde dos componentes
        """
        health_status = {
            "module": "vehicle_image",
            "status": "healthy",
            "components": {}
        }
        
        try:
            # Verificar repositório
            repository = self.get_repository()
            health_status["components"]["repository"] = {
                "type": type(repository).__name__,
                "status": "healthy"
            }
        except Exception as e:
            health_status["components"]["repository"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "unhealthy"
        
        try:
            # Verificar image manager
            image_manager = self.get_image_manager()
            health_status["components"]["image_manager"] = {
                "type": type(image_manager).__name__,
                "status": "healthy"
            }
        except Exception as e:
            health_status["components"]["image_manager"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "unhealthy"
        
        try:
            # Verificar use cases
            use_cases_count = len([
                self.get_create_use_case(),
                self.get_update_use_case(),
                self.get_delete_use_case(),
                self.get_get_use_case(),
                self.get_search_use_case(),
                self.get_gallery_use_case(),
                self.get_reorder_use_case(),
                self.get_set_primary_use_case(),
                self.get_generate_thumbnail_use_case(),
                self.get_statistics_use_case()
            ])
            
            health_status["components"]["use_cases"] = {
                "count": use_cases_count,
                "status": "healthy"
            }
        except Exception as e:
            health_status["components"]["use_cases"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["status"] = "unhealthy"
        
        return health_status


# ==============================================
# FACTORY FUNCTIONS
# ==============================================

def create_vehicle_image_module(config: Dict[str, Any] = None) -> VehicleImageModuleConfig:
    """
    Factory para criar módulo VehicleImage configurado.
    
    Args:
        config: Configurações do módulo
        
    Returns:
        Módulo VehicleImage configurado
    """
    return VehicleImageModuleConfig(config)


def create_development_module() -> VehicleImageModuleConfig:
    """
    Factory para módulo de desenvolvimento.
    
    Returns:
        Módulo configurado para desenvolvimento
    """
    config = {
        'repository_type': 'mock',
        'image_manager_type': 'mock',
        'storage_path': '/tmp/uploads',
        'enable_thumbnails': True,
        'max_file_size': 10 * 1024 * 1024,  # 10MB
        'allowed_formats': ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    }
    
    return VehicleImageModuleConfig(config)


def create_production_module(
    repository_type: str = 'sql',
    storage_path: str = '/var/uploads'
) -> VehicleImageModuleConfig:
    """
    Factory para módulo de produção.
    
    Args:
        repository_type: Tipo do repositório (sql, nosql, etc.)
        storage_path: Caminho de armazenamento
        
    Returns:
        Módulo configurado para produção
    """
    config = {
        'repository_type': repository_type,
        'image_manager_type': 'production',
        'storage_path': storage_path,
        'enable_thumbnails': True,
        'thumbnail_quality': 85,
        'max_file_size': 10 * 1024 * 1024,  # 10MB
        'allowed_formats': ['.jpg', '.jpeg', '.png', '.webp'],
        'auto_optimize': True,
        'compression_quality': 90
    }
    
    return VehicleImageModuleConfig(config)


# ==============================================
# INTEGRATION HELPERS
# ==============================================

def register_vehicle_image_routes(app, module_config: VehicleImageModuleConfig) -> None:
    """
    Registra rotas do módulo VehicleImage na aplicação FastAPI.
    
    Args:
        app: Instância do FastAPI
        module_config: Configuração do módulo
    """
    router = module_config.get_router()
    app.include_router(router)


async def initialize_vehicle_image_module(module_config: VehicleImageModuleConfig) -> None:
    """
    Inicializa módulo VehicleImage com dados e configurações necessárias.
    
    Args:
        module_config: Configuração do módulo
    """
    # Verificar saúde do módulo
    health = module_config.health_check()
    
    if health["status"] != "healthy":
        raise RuntimeError(f"Vehicle Image module is not healthy: {health}")
    
    # Executar inicializações necessárias
    repository = module_config.get_repository()
    image_manager = module_config.get_image_manager()
    
    # Verificar e criar diretórios necessários
    storage_path = module_config.config.get('storage_path', '/uploads')
    
    # Em implementação real, criaria diretórios:
    # import os
    # os.makedirs(f"{storage_path}/vehicles", exist_ok=True)
    # os.makedirs(f"{storage_path}/thumbnails", exist_ok=True)
    
    print(f"Vehicle Image module initialized successfully")
    print(f"Storage path: {storage_path}")
    print(f"Repository: {type(repository).__name__}")
    print(f"Image Manager: {type(image_manager).__name__}")


def get_module_info() -> Dict[str, Any]:
    """
    Obtém informações sobre o módulo VehicleImage.
    
    Returns:
        Informações do módulo
    """
    return {
        "name": "VehicleImage",
        "version": "1.0.0",
        "description": "Módulo para gerenciamento de imagens de veículos",
        "features": [
            "Upload de imagens",
            "Galeria de veículos",
            "Geração de miniaturas",
            "Reordenação de imagens",
            "Imagem principal",
            "Estatísticas de uso",
            "Otimização de imagens",
            "Validação de formatos"
        ],
        "endpoints": [
            "POST /vehicle-images/upload/{vehicle_id}",
            "POST /vehicle-images/",
            "PUT /vehicle-images/{image_id}",
            "DELETE /vehicle-images/{image_id}",
            "GET /vehicle-images/{image_id}",
            "POST /vehicle-images/search",
            "GET /vehicle-images/vehicle/{vehicle_id}/gallery",
            "PUT /vehicle-images/vehicle/{vehicle_id}/reorder",
            "PATCH /vehicle-images/{image_id}/set-primary",
            "PATCH /vehicle-images/{image_id}/generate-thumbnail",
            "GET /vehicle-images/statistics"
        ],
        "supported_formats": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
        "max_file_size": "10MB",
        "architecture": "Clean Architecture"
    }
