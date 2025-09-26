"""
Módulo para inicialização automática do sistema
"""

from src.domain.entities.user import User
from src.infrastructure.driven.mock_user_repository import MockUserRepository
from src.application.use_cases.users.create_user_use_case import CreateUserUseCase
from src.application.dtos.user_dto import UserCreateDto
from passlib.context import CryptContext
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def create_default_admin_if_not_exists():
    """
    Cria automaticamente um usuário administrador padrão se não existir.
    Esta função é executada no startup da aplicação.
    """
    try:
        # Instanciar repositório
        user_repository = MockUserRepository()
        
        # Verificar se já existe um usuário administrador
        existing_admin = await user_repository.get_user_by_email("admin@carsales.com")
        if existing_admin:
            logger.info("✅ Usuário administrador já existe - sistema pronto para uso")
            logger.info("=" * 60)
            logger.info(f"📧 Email: {existing_admin.email}")
            logger.info(f"👑 Role: {existing_admin.role}")
            logger.info(f"🔗 Employee ID: {existing_admin.employee_id or 'Não associado'}")
            logger.info("=" * 60)
            logger.info("🔐 Use as credenciais: admin@carsales.com / admin123456")
            logger.info("📖 Acesse /docs para ver a documentação interativa da API")
            return
        
        # Criar usuário administrador padrão usando a entidade diretamente
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash("admin123456")
        
        admin_user = User(
            email="admin@carsales.com",
            password=hashed_password,
            role="Administrador",
            employee_id=None,  # Administrador não tem funcionário associado
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Salvar no repositório
        created_admin = await user_repository.save(admin_user)
        
        logger.info("🎉 Usuário administrador criado automaticamente!")
        logger.info("=" * 60)
        logger.info(f"📧 Email: {created_admin.email}")
        logger.info(f"🔑 Senha: admin123456")
        logger.info(f"👑 Role: {created_admin.role}")
        logger.info(f"🔗 Employee ID: {created_admin.employee_id or 'Não associado'}")
        logger.info("=" * 60)
        logger.info("⚠️  ATENÇÃO: Altere a senha padrão 'admin123456' em produção!")
        logger.info("🔐 Faça login em /api/auth/login para obter seu token JWT")
        logger.info("📖 Acesse /docs para ver a documentação interativa da API")
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar usuário administrador: {str(e)}")
        logger.error("⚠️  Sistema iniciará sem usuário administrador adicional")
        logger.info("💡 O sistema já possui usuários padrão no MockUserRepository")


async def initialize_system():
    """
    Inicializa o sistema com dados padrão necessários.
    """
    logger.info("🚀 Iniciando configuração automática do sistema...")
    
    try:
        # Criar usuário administrador (se necessário)
        await create_default_admin_if_not_exists()
        
        logger.info("✅ Configuração automática do sistema concluída!")
        
    except Exception as e:
        logger.error(f"❌ Erro na inicialização automática: {str(e)}")
        logger.error("⚠️  Sistema continuará funcionando com usuários padrão do MockUserRepository")
