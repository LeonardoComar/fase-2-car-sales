"""
ImageManager - Domain Service para gerenciamento de arquivos de imagem

Serviço de domínio responsável por operações relacionadas a arquivos de imagem.
Abstrai operações de sistema de arquivos e processamento de imagens.

Aplicando princípios SOLID:
- SRP: Responsável apenas pelo gerenciamento de arquivos de imagem
- OCP: Extensível para novos tipos de processamento
- LSP: Pode ser substituído por diferentes implementações
- ISP: Interface específica para operações de imagem
- DIP: Define abstrações para implementações de infraestrutura
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
import os


class ImageManager(ABC):
    """
    Interface abstrata para gerenciamento de imagens.
    
    Define contratos para operações com arquivos de imagem,
    permitindo diferentes implementações (local, cloud, etc.).
    """
    
    @abstractmethod
    async def file_exists(self, file_path: str) -> bool:
        """
        Verifica se um arquivo de imagem existe.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            True se o arquivo existe
        """
        pass
    
    @abstractmethod
    async def save_file(self, content: bytes, file_path: str) -> str:
        """
        Salva um arquivo de imagem.
        
        Args:
            content: Conteúdo do arquivo
            file_path: Caminho onde salvar
            
        Returns:
            Caminho final do arquivo salvo
            
        Raises:
            IOError: Se não consegue salvar o arquivo
        """
        pass
    
    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """
        Exclui um arquivo de imagem.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            True se excluído com sucesso
        """
        pass
    
    @abstractmethod
    async def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Obtém informações de um arquivo de imagem.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Dicionário com informações do arquivo
            
        Raises:
            FileNotFoundError: Se o arquivo não existe
        """
        pass
    
    @abstractmethod
    async def generate_thumbnail(
        self, 
        source_path: str, 
        thumbnail_size: Tuple[int, int] = (300, 300)
    ) -> str:
        """
        Gera miniatura de uma imagem.
        
        Args:
            source_path: Caminho da imagem original
            thumbnail_size: Tamanho da miniatura (width, height)
            
        Returns:
            Caminho da miniatura gerada
            
        Raises:
            ProcessingError: Se não consegue gerar a miniatura
        """
        pass
    
    @abstractmethod
    async def validate_image_format(self, file_path: str) -> bool:
        """
        Valida se um arquivo é uma imagem válida.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            True se é uma imagem válida
        """
        pass
    
    @abstractmethod
    async def get_image_dimensions(self, file_path: str) -> Optional[Tuple[int, int]]:
        """
        Obtém dimensões de uma imagem.
        
        Args:
            file_path: Caminho da imagem
            
        Returns:
            Tupla com (width, height) ou None se erro
        """
        pass
    
    @abstractmethod
    async def optimize_image(
        self, 
        source_path: str, 
        quality: int = 85
    ) -> str:
        """
        Otimiza uma imagem para reduzir tamanho.
        
        Args:
            source_path: Caminho da imagem original
            quality: Qualidade da compressão (1-100)
            
        Returns:
            Caminho da imagem otimizada
        """
        pass
    
    @abstractmethod
    async def should_generate_thumbnail(self, file_path: str) -> bool:
        """
        Verifica se deve gerar miniatura para uma imagem.
        
        Args:
            file_path: Caminho da imagem
            
        Returns:
            True se deve gerar miniatura
        """
        pass
    
    @abstractmethod
    async def get_storage_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas de armazenamento.
        
        Returns:
            Dicionário com estatísticas de uso de storage
        """
        pass


class ImageManagerImpl(ImageManager):
    """
    Implementação mock/simples do ImageManager.
    
    Para desenvolvimento e testes, simula operações
    sem processamento real de imagens.
    """
    
    def __init__(self, base_storage_path: str = "/uploads"):
        """
        Inicializa o gerenciador com caminho base.
        
        Args:
            base_storage_path: Caminho base para armazenamento
        """
        self.base_storage_path = base_storage_path
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.thumbnail_size = (300, 300)
    
    async def file_exists(self, file_path: str) -> bool:
        """Verifica se um arquivo existe."""
        # Para implementação mock, simular que alguns arquivos existem
        # Em implementação real, usaria os.path.exists(file_path)
        return True  # Simular que arquivo sempre existe
    
    async def save_file(self, content: bytes, file_path: str) -> str:
        """Salva um arquivo."""
        # Validar tamanho
        if len(content) > self.max_file_size:
            raise ValueError(f"Arquivo muito grande. Máximo: {self.max_file_size} bytes")
        
        # Validar formato pelo caminho
        file_extension = Path(file_path).suffix.lower()
        if file_extension not in self.supported_formats:
            raise ValueError(f"Formato não suportado: {file_extension}")
        
        # Simular salvamento
        # Em implementação real:
        # os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # with open(file_path, 'wb') as f:
        #     f.write(content)
        
        return file_path
    
    async def delete_file(self, file_path: str) -> bool:
        """Exclui um arquivo."""
        # Simular exclusão bem-sucedida
        # Em implementação real: os.remove(file_path)
        return True
    
    async def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Obtém informações do arquivo."""
        # Simular informações do arquivo
        return {
            "size": 1024000,  # 1MB
            "format": Path(file_path).suffix.lower(),
            "width": 1920,
            "height": 1080,
            "created_at": "2024-01-15T10:30:00",
            "modified_at": "2024-01-15T10:30:00"
        }
    
    async def generate_thumbnail(
        self, 
        source_path: str, 
        thumbnail_size: Tuple[int, int] = (300, 300)
    ) -> str:
        """Gera miniatura."""
        if not await self.file_exists(source_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {source_path}")
        
        # Gerar caminho da miniatura
        source_path_obj = Path(source_path)
        thumbnail_dir = source_path_obj.parent / "thumbnails"
        thumbnail_name = f"{source_path_obj.stem}_thumb{source_path_obj.suffix}"
        thumbnail_path = str(thumbnail_dir / thumbnail_name)
        
        # Simular geração da miniatura
        # Em implementação real, usaria Pillow ou similar:
        # from PIL import Image
        # image = Image.open(source_path)
        # image.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        # image.save(thumbnail_path, optimize=True, quality=85)
        
        return thumbnail_path
    
    async def validate_image_format(self, file_path: str) -> bool:
        """Valida formato da imagem."""
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension not in self.supported_formats:
            return False
        
        # Simular validação de conteúdo
        # Em implementação real, abriria o arquivo e verificaria header
        return True
    
    async def get_image_dimensions(self, file_path: str) -> Optional[Tuple[int, int]]:
        """Obtém dimensões da imagem."""
        if not await self.file_exists(file_path):
            return None
        
        if not await self.validate_image_format(file_path):
            return None
        
        # Simular dimensões
        # Em implementação real:
        # from PIL import Image
        # with Image.open(file_path) as img:
        #     return img.size
        
        return (1920, 1080)  # Simular HD
    
    async def optimize_image(
        self, 
        source_path: str, 
        quality: int = 85
    ) -> str:
        """Otimiza imagem."""
        if not await self.file_exists(source_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {source_path}")
        
        if quality < 1 or quality > 100:
            raise ValueError("Qualidade deve estar entre 1 e 100")
        
        # Gerar caminho da imagem otimizada
        source_path_obj = Path(source_path)
        optimized_name = f"{source_path_obj.stem}_optimized{source_path_obj.suffix}"
        optimized_path = str(source_path_obj.parent / optimized_name)
        
        # Simular otimização
        # Em implementação real:
        # from PIL import Image
        # image = Image.open(source_path)
        # image.save(optimized_path, optimize=True, quality=quality)
        
        return optimized_path
    
    async def should_generate_thumbnail(self, file_path: str) -> bool:
        """Verifica se deve gerar miniatura."""
        if not await self.file_exists(file_path):
            return False
        
        if not await self.validate_image_format(file_path):
            return False
        
        # Verificar se já tem miniatura
        thumbnail_path = await self._get_thumbnail_path(file_path)
        if await self.file_exists(thumbnail_path):
            return False
        
        # Verificar tamanho da imagem
        dimensions = await self.get_image_dimensions(file_path)
        if not dimensions:
            return False
        
        width, height = dimensions
        
        # Gerar miniatura se imagem é maior que o thumbnail
        return width > self.thumbnail_size[0] or height > self.thumbnail_size[1]
    
    async def get_storage_statistics(self) -> Dict[str, Any]:
        """Obtém estatísticas de armazenamento."""
        # Simular estatísticas
        return {
            "total_files": 150,
            "total_size_mb": 520.5,
            "average_file_size_mb": 3.47,
            "thumbnails_count": 120,
            "formats_distribution": {
                ".jpg": 80,
                ".png": 45,
                ".webp": 20,
                ".gif": 5
            },
            "storage_efficiency": 85.2,
            "last_cleanup": "2024-01-15T08:00:00"
        }
    
    async def _get_thumbnail_path(self, source_path: str) -> str:
        """Gera caminho da miniatura baseado no arquivo original."""
        source_path_obj = Path(source_path)
        thumbnail_dir = source_path_obj.parent / "thumbnails"
        thumbnail_name = f"{source_path_obj.stem}_thumb{source_path_obj.suffix}"
        return str(thumbnail_dir / thumbnail_name)


# ==============================================
# UTILITÁRIOS E HELPERS
# ==============================================

class ImageValidationHelper:
    """
    Helper para validações relacionadas a imagens.
    
    Centraliza regras de validação que podem ser
    usadas em diferentes partes do sistema.
    """
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MIN_WIDTH = 100
    MIN_HEIGHT = 100
    MAX_WIDTH = 8000
    MAX_HEIGHT = 8000
    
    @classmethod
    def validate_file_extension(cls, filename: str) -> bool:
        """
        Valida extensão do arquivo.
        
        Args:
            filename: Nome do arquivo
            
        Returns:
            True se extensão é válida
        """
        extension = Path(filename).suffix.lower()
        return extension in cls.SUPPORTED_FORMATS
    
    @classmethod
    def validate_file_size(cls, size_bytes: int) -> bool:
        """
        Valida tamanho do arquivo.
        
        Args:
            size_bytes: Tamanho em bytes
            
        Returns:
            True se tamanho é válido
        """
        return 0 < size_bytes <= cls.MAX_FILE_SIZE
    
    @classmethod
    def validate_dimensions(cls, width: int, height: int) -> bool:
        """
        Valida dimensões da imagem.
        
        Args:
            width: Largura em pixels
            height: Altura em pixels
            
        Returns:
            True se dimensões são válidas
        """
        return (
            cls.MIN_WIDTH <= width <= cls.MAX_WIDTH and
            cls.MIN_HEIGHT <= height <= cls.MAX_HEIGHT
        )
    
    @classmethod
    def get_recommended_thumbnail_size(cls, width: int, height: int) -> Tuple[int, int]:
        """
        Calcula tamanho recomendado para miniatura.
        
        Args:
            width: Largura original
            height: Altura original
            
        Returns:
            Tupla com dimensões recomendadas
        """
        max_dimension = 300
        
        if width > height:
            # Landscape
            if width <= max_dimension:
                return (width, height)
            ratio = max_dimension / width
            return (max_dimension, int(height * ratio))
        else:
            # Portrait ou quadrado
            if height <= max_dimension:
                return (width, height)
            ratio = max_dimension / height
            return (int(width * ratio), max_dimension)
    
    @classmethod
    def generate_unique_filename(cls, original_filename: str, prefix: str = "") -> str:
        """
        Gera nome único para arquivo.
        
        Args:
            original_filename: Nome original
            prefix: Prefixo opcional
            
        Returns:
            Nome único gerado
        """
        from datetime import datetime
        import uuid
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        
        file_path = Path(original_filename)
        name_part = file_path.stem
        extension = file_path.suffix
        
        if prefix:
            return f"{prefix}_{timestamp}_{unique_id}_{name_part}{extension}"
        else:
            return f"{timestamp}_{unique_id}_{name_part}{extension}"


class ImagePathHelper:
    """
    Helper para geração de caminhos de imagens.
    
    Centraliza lógica de organização de diretórios
    e nomenclatura de arquivos.
    """
    
    @classmethod
    def generate_vehicle_image_path(
        cls, 
        vehicle_id: str, 
        filename: str, 
        base_path: str = "/uploads"
    ) -> str:
        """
        Gera caminho para imagem de veículo.
        
        Args:
            vehicle_id: ID do veículo
            filename: Nome do arquivo
            base_path: Caminho base
            
        Returns:
            Caminho completo da imagem
        """
        return f"{base_path}/vehicles/{vehicle_id}/{filename}"
    
    @classmethod
    def generate_thumbnail_path(
        cls, 
        original_path: str, 
        base_path: str = "/uploads"
    ) -> str:
        """
        Gera caminho para miniatura.
        
        Args:
            original_path: Caminho da imagem original
            base_path: Caminho base
            
        Returns:
            Caminho da miniatura
        """
        original_file = Path(original_path)
        thumbnail_name = f"{original_file.stem}_thumb{original_file.suffix}"
        
        # Extrair vehicle_id do caminho original
        path_parts = Path(original_path).parts
        if "vehicles" in path_parts:
            vehicle_index = path_parts.index("vehicles")
            if vehicle_index + 1 < len(path_parts):
                vehicle_id = path_parts[vehicle_index + 1]
                return f"{base_path}/thumbnails/{vehicle_id}/{thumbnail_name}"
        
        return f"{base_path}/thumbnails/{thumbnail_name}"
    
    @classmethod
    def organize_by_date(cls, base_path: str) -> str:
        """
        Organiza arquivos por data.
        
        Args:
            base_path: Caminho base
            
        Returns:
            Caminho organizado por data
        """
        from datetime import datetime
        
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        
        return f"{base_path}/{year}/{month}/{day}"
