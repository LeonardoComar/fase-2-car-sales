from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class VehicleImage:
    """
    Entidade VehicleImage do domínio - representa uma imagem de veículo no sistema.
    
    Esta entidade contém apenas a lógica de negócio específica para imagens de veículos.
    Aplicando o princípio Single Responsibility Principle (SRP) do SOLID.
    """
    
    # Extensões de arquivo válidas
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    
    # Configurações de limites
    MAX_IMAGES_PER_VEHICLE = 10
    MIN_IMAGES_PER_VEHICLE = 1
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    THUMBNAIL_SIZE = (300, 300)
    
    id: Optional[int] = None
    vehicle_id: int = None
    filename: str = None
    path: str = None
    thumbnail_path: Optional[str] = None
    position: int = None
    is_primary: bool = False
    uploaded_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validações automáticas após inicialização."""
        if self.uploaded_at is None:
            self.uploaded_at = datetime.utcnow()
        
        self._validate_position()
        self._validate_filename()
    
    def _validate_position(self):
        """Valida se a posição está dentro do range permitido."""
        if self.position is not None:
            if not (1 <= self.position <= self.MAX_IMAGES_PER_VEHICLE):
                raise ValueError(f"Posição deve estar entre 1 e {self.MAX_IMAGES_PER_VEHICLE}")
    
    def _validate_filename(self):
        """Valida se o arquivo tem extensão permitida."""
        if self.filename:
            from pathlib import Path
            file_ext = Path(self.filename).suffix.lower()
            if file_ext not in self.ALLOWED_EXTENSIONS:
                raise ValueError(f"Extensão {file_ext} não permitida. Use: {', '.join(self.ALLOWED_EXTENSIONS)}")
    
    def set_as_primary(self):
        """Define esta imagem como principal."""
        self.is_primary = True
    
    def remove_primary(self):
        """Remove o status de imagem principal."""
        self.is_primary = False
    
    def update_position(self, new_position: int):
        """Atualiza a posição da imagem."""
        if not (1 <= new_position <= self.MAX_IMAGES_PER_VEHICLE):
            raise ValueError(f"Posição deve estar entre 1 e {self.MAX_IMAGES_PER_VEHICLE}")
        self.position = new_position
    
    def get_file_extension(self) -> str:
        """Retorna a extensão do arquivo."""
        if not self.filename:
            return ""
        from pathlib import Path
        return Path(self.filename).suffix.lower()
    
    def is_valid_extension(self) -> bool:
        """Verifica se a extensão do arquivo é válida."""
        return self.get_file_extension() in self.ALLOWED_EXTENSIONS
    
    def to_dict(self) -> dict:
        """Converte a entidade para dicionário."""
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "filename": self.filename,
            "path": self.path,
            "thumbnail_path": self.thumbnail_path,
            "position": self.position,
            "is_primary": self.is_primary,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'VehicleImage':
        """Cria uma instância a partir de um dicionário."""
        uploaded_at = None
        if data.get("uploaded_at"):
            if isinstance(data["uploaded_at"], str):
                uploaded_at = datetime.fromisoformat(data["uploaded_at"].replace('Z', '+00:00'))
            else:
                uploaded_at = data["uploaded_at"]
        
        return cls(
            id=data.get("id"),
            vehicle_id=data.get("vehicle_id"),
            filename=data.get("filename"),
            path=data.get("path"),
            thumbnail_path=data.get("thumbnail_path"),
            position=data.get("position"),
            is_primary=data.get("is_primary", False),
            uploaded_at=uploaded_at
        )
    
    def __str__(self) -> str:
        return f"VehicleImage(id={self.id}, vehicle_id={self.vehicle_id}, filename={self.filename}, position={self.position})"
    
    def __repr__(self) -> str:
        return self.__str__()
