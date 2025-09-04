from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserCreateDto(BaseModel):
    """
    DTO para criação de usuário.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela transferência de dados de criação.
    """
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=6, description="Senha do usuário (mínimo 6 caracteres)")
    role: str = Field(..., description="Perfil do usuário")
    employee_id: Optional[int] = Field(None, description="ID do funcionário associado (opcional)")


class UserUpdateDto(BaseModel):
    """
    DTO para atualização de usuário.
    
    Aplicando o princípio Open/Closed Principle (OCP) - 
    aberto para extensão, fechado para modificação.
    """
    email: Optional[EmailStr] = Field(None, description="Email do usuário")
    password: Optional[str] = Field(None, min_length=6, description="Senha do usuário (mínimo 6 caracteres)")
    role: Optional[str] = Field(None, description="Perfil do usuário")
    employee_id: Optional[int] = Field(None, description="ID do funcionário associado")


class UserResponseDto(BaseModel):
    """
    DTO para resposta de usuário.
    
    Responsável apenas pela apresentação dos dados do usuário.
    """
    id: int = Field(..., description="ID do usuário")
    email: str = Field(..., description="Email do usuário")
    role: str = Field(..., description="Perfil do usuário")
    employee_id: Optional[int] = Field(None, description="ID do funcionário associado (opcional)")
    created_at: Optional[datetime] = Field(None, description="Data de criação")
    updated_at: Optional[datetime] = Field(None, description="Data de última atualização")

    class Config:
        from_attributes = True


class LoginDto(BaseModel):
    """DTO para login"""
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., description="Senha do usuário")


class TokenDto(BaseModel):
    """DTO para resposta de token"""
    access_token: str = Field(..., description="Token de acesso JWT")
    token_type: str = Field(default="bearer", description="Tipo do token")
    expires_in: int = Field(..., description="Tempo de expiração em segundos")


class TokenDataDto(BaseModel):
    """DTO para dados do token"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
