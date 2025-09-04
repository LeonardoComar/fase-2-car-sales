"""
Entidade VehicleImage - Domain Layer

Representa uma imagem de veículo no sistema de vendas.
Aplicando os princípios da Clean Architecture:
- Independente de frameworks
- Independente de UI
- Independente de banco de dados
- Testável
- Independente de agentes externos

Aplicando princípios SOLID:
- SRP: Responsável apenas pela lógica de negócio de imagens de veículos
- OCP: Aberto para extensão (novos tipos de imagem, validações)
- LSP: Pode ser substituída por implementações específicas
- ISP: Interface coesa sem métodos desnecessários
- DIP: Não depende de implementações concretas
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
import os
import re


@dataclass
class VehicleImage:
    """
    Entidade VehicleImage representando uma imagem de veículo no domínio.
    
    Contém toda a lógica de negócio relacionada ao gerenciamento de imagens
    de veículos, incluindo validações, ordenação e operações de arquivo.
    """
    
    # Constantes de Validação
    MAX_FILENAME_LENGTH = 255
    MAX_PATH_LENGTH = 500
    MAX_POSITION = 99
    MIN_POSITION = 1
    
    # Extensões de arquivo permitidas
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
    
    # Tamanhos máximos (em bytes)
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_THUMBNAIL_SIZE = 2 * 1024 * 1024  # 2MB
    
    # Regex para validação de nome de arquivo
    FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9._-]+$')
    
    # Atributos da entidade
    id: Optional[UUID] = field(default_factory=uuid4)
    vehicle_id: UUID = None
    filename: str = ""
    path: str = ""
    thumbnail_path: Optional[str] = None
    position: int = 1
    is_primary: bool = False
    file_size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    mime_type: Optional[str] = None
    uploaded_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    @classmethod
    def create_vehicle_image(cls, vehicle_id: UUID, filename: str, path: str, 
                           position: int, file_size: Optional[int] = None,
                           width: Optional[int] = None, height: Optional[int] = None,
                           mime_type: Optional[str] = None) -> 'VehicleImage':
        """
        Factory method para criar uma nova imagem de veículo.
        
        Args:
            vehicle_id: ID do veículo
            filename: Nome do arquivo
            path: Caminho do arquivo
            position: Posição da imagem na galeria
            file_size: Tamanho do arquivo em bytes (opcional)
            width: Largura da imagem em pixels (opcional)
            height: Altura da imagem em pixels (opcional)
            mime_type: Tipo MIME do arquivo (opcional)
            
        Returns:
            VehicleImage: Nova instância de imagem
            
        Raises:
            ValueError: Se dados inválidos
        """
        # Criar instância
        image = cls(
            vehicle_id=vehicle_id,
            filename=filename.strip(),
            path=path.strip(),
            position=position,
            file_size=file_size,
            width=width,
            height=height,
            mime_type=mime_type
        )
        
        # Validar dados
        image._validate_creation_data()
        
        return image
    
    def set_as_primary(self) -> None:
        """
        Define esta imagem como principal.
        
        Note: O repositório deve garantir que apenas uma imagem 
        por veículo seja primária.
        """
        self.is_primary = True
        self.updated_at = datetime.utcnow()
    
    def remove_primary_status(self) -> None:
        """Remove o status de imagem principal."""
        self.is_primary = False
        self.updated_at = datetime.utcnow()
    
    def update_position(self, new_position: int) -> None:
        """
        Atualiza a posição da imagem na galeria.
        
        Args:
            new_position: Nova posição (1-99)
            
        Raises:
            ValueError: Se posição inválida
        """
        if not isinstance(new_position, int):
            raise ValueError("Posição deve ser um número inteiro")
        
        if new_position < self.MIN_POSITION or new_position > self.MAX_POSITION:
            raise ValueError(f"Posição deve estar entre {self.MIN_POSITION} e {self.MAX_POSITION}")
        
        self.position = new_position
        self.updated_at = datetime.utcnow()
    
    def set_thumbnail_path(self, thumbnail_path: str) -> None:
        """
        Define o caminho da miniatura.
        
        Args:
            thumbnail_path: Caminho do arquivo de miniatura
            
        Raises:
            ValueError: Se caminho inválido
        """
        thumbnail_path = thumbnail_path.strip()
        
        if not thumbnail_path:
            raise ValueError("Caminho da miniatura não pode estar vazio")
        
        if len(thumbnail_path) > self.MAX_PATH_LENGTH:
            raise ValueError(f"Caminho da miniatura deve ter no máximo {self.MAX_PATH_LENGTH} caracteres")
        
        self.thumbnail_path = thumbnail_path
        self.updated_at = datetime.utcnow()
    
    def update_file_info(self, file_size: Optional[int] = None, 
                        width: Optional[int] = None, 
                        height: Optional[int] = None,
                        mime_type: Optional[str] = None) -> None:
        """
        Atualiza informações técnicas do arquivo.
        
        Args:
            file_size: Tamanho do arquivo em bytes
            width: Largura da imagem em pixels
            height: Altura da imagem em pixels
            mime_type: Tipo MIME do arquivo
        """
        if file_size is not None:
            if file_size < 0:
                raise ValueError("Tamanho do arquivo deve ser positivo")
            if file_size > self.MAX_FILE_SIZE:
                raise ValueError(f"Arquivo muito grande. Máximo permitido: {self.MAX_FILE_SIZE / (1024*1024):.1f}MB")
            self.file_size = file_size
        
        if width is not None:
            if width <= 0:
                raise ValueError("Largura deve ser positiva")
            self.width = width
        
        if height is not None:
            if height <= 0:
                raise ValueError("Altura deve ser positiva")
            self.height = height
        
        if mime_type is not None:
            self.mime_type = mime_type.strip().lower()
        
        self.updated_at = datetime.utcnow()
    
    def get_file_extension(self) -> str:
        """
        Retorna a extensão do arquivo.
        
        Returns:
            str: Extensão do arquivo (com ponto)
        """
        return os.path.splitext(self.filename)[1].lower()
    
    def get_filename_without_extension(self) -> str:
        """
        Retorna o nome do arquivo sem extensão.
        
        Returns:
            str: Nome do arquivo sem extensão
        """
        return os.path.splitext(self.filename)[0]
    
    def is_valid_image_format(self) -> bool:
        """
        Verifica se o formato da imagem é válido.
        
        Returns:
            bool: True se formato válido
        """
        extension = self.get_file_extension()
        return extension in self.ALLOWED_EXTENSIONS
    
    def has_thumbnail(self) -> bool:
        """Verifica se a imagem possui miniatura."""
        return self.thumbnail_path is not None and self.thumbnail_path.strip() != ""
    
    def get_aspect_ratio(self) -> Optional[float]:
        """
        Calcula a proporção da imagem (largura/altura).
        
        Returns:
            Optional[float]: Proporção da imagem ou None se dimensões não disponíveis
        """
        if self.width and self.height and self.height > 0:
            return self.width / self.height
        return None
    
    def is_landscape(self) -> Optional[bool]:
        """
        Verifica se a imagem está em orientação paisagem.
        
        Returns:
            Optional[bool]: True se paisagem, False se retrato, None se dimensões não disponíveis
        """
        if self.width and self.height:
            return self.width > self.height
        return None
    
    def is_portrait(self) -> Optional[bool]:
        """
        Verifica se a imagem está em orientação retrato.
        
        Returns:
            Optional[bool]: True se retrato, False se paisagem, None se dimensões não disponíveis
        """
        landscape = self.is_landscape()
        return not landscape if landscape is not None else None
    
    def is_square(self) -> Optional[bool]:
        """
        Verifica se a imagem é quadrada.
        
        Returns:
            Optional[bool]: True se quadrada, False caso contrário, None se dimensões não disponíveis
        """
        if self.width and self.height:
            return self.width == self.height
        return None
    
    def get_file_size_mb(self) -> Optional[float]:
        """
        Retorna o tamanho do arquivo em megabytes.
        
        Returns:
            Optional[float]: Tamanho em MB ou None se não disponível
        """
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return None
    
    def get_display_name(self) -> str:
        """
        Retorna um nome de exibição amigável.
        
        Returns:
            str: Nome de exibição
        """
        if self.is_primary:
            return f"Imagem Principal - Posição {self.position}"
        else:
            return f"Imagem {self.position}"
    
    def _validate_creation_data(self) -> None:
        """Valida dados obrigatórios para criação."""
        self._validate_vehicle_id()
        self._validate_filename()
        self._validate_path()
        self._validate_position()
    
    def _validate_vehicle_id(self) -> None:
        """Valida o ID do veículo."""
        if not self.vehicle_id:
            raise ValueError("ID do veículo é obrigatório")
    
    def _validate_filename(self) -> None:
        """Valida o nome do arquivo."""
        if not self.filename or not self.filename.strip():
            raise ValueError("Nome do arquivo é obrigatório")
        
        if len(self.filename) > self.MAX_FILENAME_LENGTH:
            raise ValueError(f"Nome do arquivo deve ter no máximo {self.MAX_FILENAME_LENGTH} caracteres")
        
        # Verificar caracteres válidos
        if not self.FILENAME_PATTERN.match(self.filename):
            raise ValueError("Nome do arquivo contém caracteres inválidos. Use apenas letras, números, pontos, hífens e sublinhados")
        
        # Verificar extensão
        extension = self.get_file_extension()
        if not extension:
            raise ValueError("Arquivo deve ter uma extensão")
        
        if extension not in self.ALLOWED_EXTENSIONS:
            allowed = ', '.join(self.ALLOWED_EXTENSIONS)
            raise ValueError(f"Extensão '{extension}' não permitida. Extensões válidas: {allowed}")
    
    def _validate_path(self) -> None:
        """Valida o caminho do arquivo."""
        if not self.path or not self.path.strip():
            raise ValueError("Caminho do arquivo é obrigatório")
        
        if len(self.path) > self.MAX_PATH_LENGTH:
            raise ValueError(f"Caminho do arquivo deve ter no máximo {self.MAX_PATH_LENGTH} caracteres")
    
    def _validate_position(self) -> None:
        """Valida a posição da imagem."""
        if not isinstance(self.position, int):
            raise ValueError("Posição deve ser um número inteiro")
        
        if self.position < self.MIN_POSITION or self.position > self.MAX_POSITION:
            raise ValueError(f"Posição deve estar entre {self.MIN_POSITION} e {self.MAX_POSITION}")
    
    def __post_init__(self):
        """Validações após inicialização."""
        # Garantir que timestamps estejam definidos
        if not self.uploaded_at:
            self.uploaded_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()
        
        # Normalizar caminhos
        if self.path:
            self.path = self.path.replace('\\', '/')
        if self.thumbnail_path:
            self.thumbnail_path = self.thumbnail_path.replace('\\', '/')
    
    def __str__(self) -> str:
        return f"VehicleImage(id={self.id}, vehicle_id={self.vehicle_id}, filename='{self.filename}', position={self.position})"
    
    def __repr__(self) -> str:
        return (f"VehicleImage(id={self.id}, vehicle_id={self.vehicle_id}, "
                f"filename='{self.filename}', position={self.position}, "
                f"is_primary={self.is_primary}, uploaded_at={self.uploaded_at})")
