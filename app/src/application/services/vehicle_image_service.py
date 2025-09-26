"""
Serviço para gerenciamento de imagens de veículos.

Aplicando princípios SOLID:
- SRP: Responsável apenas por operações de imagem
- OCP: Extensível para novos tipos de processamento
- DIP: Depende de abstrações
"""

import os
import uuid
import shutil
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException


class VehicleImageService:
    """Serviço para processamento e armazenamento de imagens de veículos."""
    
    def __init__(self, base_upload_dir: str = "/app/static/uploads"):
        self.base_upload_dir = base_upload_dir
        self.allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.thumbnail_size = (300, 300)
        
        # Garantir que o diretório base de uploads existe
        try:
            os.makedirs(self.base_upload_dir, exist_ok=True)
            # Criar diretórios para diferentes tipos de veículos
            os.makedirs(os.path.join(self.base_upload_dir, "cars"), exist_ok=True)
            os.makedirs(os.path.join(self.base_upload_dir, "motorcycles"), exist_ok=True)
        except Exception as e:
            print(f"[ERROR] Erro ao criar diretório base de uploads: {str(e)}")
    
    async def validate_image_file(self, file: UploadFile) -> None:
        """
        Valida se o arquivo é uma imagem válida.
        
        Args:
            file: Arquivo para validação
            
        Raises:
            HTTPException: Se o arquivo for inválido
        """
        # Validar tipo de arquivo
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="Arquivo deve ser uma imagem"
            )
        
        # Validar extensão
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in self.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Extensão {file_ext} não permitida. Use: {', '.join(self.allowed_extensions)}"
            )
        
        # Validar tamanho
        content = await file.read()
        if len(content) > self.max_file_size:
            raise HTTPException(
                status_code=400,
                detail="Arquivo muito grande. Máximo 10MB"
            )
        
        # Resetar ponteiro do arquivo
        await file.seek(0)
    
    def generate_unique_filename(self, original_filename: str) -> str:
        """
        Gera um nome único para o arquivo.
        
        Args:
            original_filename: Nome original do arquivo
            
        Returns:
            str: Nome único do arquivo
        """
        file_ext = os.path.splitext(original_filename)[1]
        return f"{uuid.uuid4()}{file_ext}"
    
    def create_directories(self, vehicle_id: int, vehicle_type: str = "cars") -> Tuple[str, str]:
        """
        Cria os diretórios necessários para armazenar as imagens.
        
        Args:
            vehicle_id: ID do veículo
            vehicle_type: Tipo do veículo (cars, motorcycles)
            
        Returns:
            Tuple[str, str]: Paths dos diretórios (principal, thumbnails)
        """
        vehicle_dir = os.path.join(self.base_upload_dir, vehicle_type, str(vehicle_id))
        thumbnail_dir = os.path.join(vehicle_dir, "thumbnails")
        
        try:
            os.makedirs(vehicle_dir, exist_ok=True)
            os.makedirs(thumbnail_dir, exist_ok=True)
        except Exception as e:
            print(f"[ERROR] Erro ao criar diretórios: {str(e)}")
            raise
        
        return vehicle_dir, thumbnail_dir
    
    async def save_image_file(self, file: UploadFile, file_path: str) -> None:
        """
        Salva o arquivo de imagem no sistema de arquivos.
        
        Args:
            file: Arquivo para salvar
            file_path: Caminho onde salvar o arquivo
        """
        try:
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
        except Exception as e:
            print(f"[ERROR] Erro ao salvar arquivo: {str(e)}")
            raise
    
    def create_thumbnail(self, source_path: str, thumbnail_path: str) -> bool:
        """
        Cria uma thumbnail da imagem.
        
        Args:
            source_path: Caminho da imagem original
            thumbnail_path: Caminho onde salvar a thumbnail
            
        Returns:
            bool: True se a thumbnail foi criada com sucesso
        """
        try:
            # Por enquanto, apenas copia o arquivo original
            # TODO: Implementar redimensionamento com Pillow
            shutil.copy2(source_path, thumbnail_path)
            return True
        except Exception as e:
            print(f"[ERROR] Erro ao criar thumbnail: {str(e)}")
            return False
    
    async def process_and_save_image(
        self, 
        file: UploadFile, 
        vehicle_id: int,
        vehicle_type: str = "cars"
    ) -> Tuple[str, str, Optional[str]]:
        """
        Processa e salva uma imagem completa com thumbnail.
        
        Args:
            file: Arquivo de imagem
            vehicle_id: ID do veículo
            vehicle_type: Tipo do veículo (cars, motorcycles)
            
        Returns:
            Tuple[str, str, Optional[str]]: (filename, path, thumbnail_path)
        """
        # Validar arquivo
        await self.validate_image_file(file)
        
        # Gerar nome único
        unique_filename = self.generate_unique_filename(file.filename)
        
        # Criar diretórios
        vehicle_dir, thumbnail_dir = self.create_directories(vehicle_id, vehicle_type)
        
        # Paths completos
        file_path = os.path.join(vehicle_dir, unique_filename)
        thumbnail_path = os.path.join(thumbnail_dir, f"thumb_{unique_filename}")
        
        # Salvar arquivo original
        await self.save_image_file(file, file_path)
        
        # Criar thumbnail
        thumbnail_created = self.create_thumbnail(file_path, thumbnail_path)
        
        # Paths relativos para retorno
        relative_path = f"/static/uploads/{vehicle_type}/{vehicle_id}/{unique_filename}"
        relative_thumbnail_path = f"/static/uploads/{vehicle_type}/{vehicle_id}/thumbnails/thumb_{unique_filename}" if thumbnail_created else None
        
        return unique_filename, relative_path, relative_thumbnail_path
    
    def delete_image_files(self, vehicle_id: int, filename: str, vehicle_type: str = "cars") -> None:
        """
        Remove os arquivos de imagem do sistema de arquivos.
        
        Args:
            vehicle_id: ID do veículo
            filename: Nome do arquivo
            vehicle_type: Tipo do veículo (cars, motorcycles)
        """
        try:
            # Remover arquivo principal
            main_path = os.path.join(self.base_upload_dir, vehicle_type, str(vehicle_id), filename)
            if os.path.exists(main_path):
                os.remove(main_path)
            
            # Remover thumbnail
            thumbnail_path = os.path.join(self.base_upload_dir, vehicle_type, str(vehicle_id), "thumbnails", f"thumb_{filename}")
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
                
        except Exception:
            # Log do erro mas não falha a operação
            pass