from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
import logging

# Infrastructure imports
from src.infrastructure.config.settings import settings
from src.infrastructure.database.connection import create_tables
from src.infrastructure.startup.system_initializer import initialize_system

# Use cases imports
from src.application.use_cases.users import (
    CreateUserUseCase,
    GetUserUseCase,
    AuthenticateUserUseCase,
)

# Adapters imports
from src.adapters.persistence.gateways.user_gateway import UserGateway
from src.adapters.rest.controllers.user_controller import UserController
from src.adapters.rest.presenters.user_presenter import UserPresenter

# Router principal com todos os módulos
from src.adapters.rest.router import clean_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    """
    logger.info("🚀 Iniciando aplicação Car Sales")
    
    # Criar diretórios de upload se não existirem
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Criar diretório de thumbnails
    thumbnail_dir = upload_dir / "thumbnails"
    thumbnail_dir.mkdir(parents=True, exist_ok=True)
    
    # Criar tabelas do banco de dados
    try:
        create_tables()
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {str(e)}")
        raise e
    
    # Inicializar sistema automaticamente (criar usuário admin, etc.)
    try:
        await initialize_system()
    except Exception as e:
        logger.error(f"Erro na inicialização do sistema: {str(e)}")
        logger.warning("Sistema continuará funcionando sem inicialização automática")
    
    yield
    logger.info("🔄 Finalizando aplicação Car Sales")


def create_app() -> FastAPI:
    """
    Factory para criar a aplicação FastAPI.
    
    Aplicando o princípio Dependency Inversion Principle (DIP) - 
    configurando todas as dependências e injeções aqui.
    
    Returns:
        FastAPI: Instância configurada da aplicação
    """
    
    # Criar instância do FastAPI
    app = FastAPI(
        title=settings.app_name,
        description="""
        ## Sistema Completo de Vendas de Veículos
        
        API RESTful para gerenciamento de vendas de carros e motocicletas com Clean Architecture.
        
        ### ✨ Principais Funcionalidades:
        
        * **🔐 Autenticação**: Sistema JWT com controle de acesso por perfis (Administrador/Vendedor)
        * **🚗 Veículos**: CRUD completo para carros e motocicletas
        * **📸 Imagens**: Upload, gerenciamento e organização de imagens dos veículos
        * **👥 Clientes**: Gestão completa de clientes
        * **👨‍💼 Funcionários**: Controle de colaboradores
        * **💰 Vendas**: Registro e acompanhamento de vendas
        * **💬 Mensagens**: Sistema de comunicação e atendimento com autenticação
        * **🔍 Filtros**: Busca avançada com múltiplos critérios
        
        ### 🏗️ Arquitetura:
        
        Esta aplicação segue os princípios de **Clean Architecture** e **SOLID**, proporcionando:
        - **Separação de responsabilidades**
        - **Baixo acoplamento**
        - **Alta coesão**
        - **Facilidade de manutenção**
        - **Testabilidade**
        
        ### 🔑 Autenticação:
        
        1. **Usuário Administrador Automático**: `admin@carsales.com` / `admin123456` (criado automaticamente no startup)
        2. **Login**: Faça login em `/api/auth/login` para obter um token JWT
        3. **Logout**: Use `/api/auth/logout` para invalidar o token atual
        4. **Autorização**: Use o token no header: `Authorization: Bearer <seu-token>`
        5. **Perfis**: **Administrador** (acesso total, sem funcionário) e **Vendedor** (operações de vendas, com funcionário associado)
        
        ### 📖 Como usar:
        1. **Início Rápido**: A aplicação cria automaticamente o usuário administrador na primeira execução
        2. Faça login com as credenciais padrão para obter token de autenticação
        3. ⚠️ **IMPORTANTE**: Altere a senha padrão em produção!
        4. Explore os endpoints abaixo
        5. Use as collections do Postman na pasta `Postman/`
        6. Consulte a documentação completa na pasta `Documentação/`
        
        Use o endpoint `/auth/login` para obter um token JWT e incluí-lo no header das requisições:
        ```
        Authorization: Bearer <seu-token-jwt>
        ```
        """,
        version=settings.app_version,
        lifespan=lifespan
    )
    
    # Configurar arquivos estáticos
    upload_path = Path(settings.upload_dir)
    if upload_path.exists():
        app.mount("/static", StaticFiles(directory=str(upload_path)), name="static")
    
    # Configurar dependências (Injeção de Dependência)
    # Camada de Infraestrutura
    user_gateway = UserGateway()
    
    # Camada de Aplicação (Casos de Uso)
    create_user_use_case = CreateUserUseCase(user_gateway)
    get_user_use_case = GetUserUseCase(user_gateway)
    authenticate_user_use_case = AuthenticateUserUseCase(user_gateway)
    
    # Camada de Adaptadores
    user_presenter = UserPresenter()
    user_controller = UserController(
        create_use_case=create_user_use_case,
        get_use_case=get_user_use_case,
        authenticate_use_case=authenticate_user_use_case,
        user_presenter=user_presenter
    )
    
    # Incluir router principal com todos os módulos Clean Architecture
    app.include_router(clean_router, prefix="/api")
    
    @app.get("/")
    async def root():
        """Endpoint raiz da API"""
        return {
            "message": f"🚗 {settings.app_name} v{settings.app_version}",
            "status": "Running",
            "docs": "/docs",
            "redoc": "/redoc",
            "endpoints": {
                "users": "/users",
                "auth": "/auth", 
                "api_v1": "/api/v1",
                "health": "/health"
            }
        }
    
    @app.get("/health")
    async def health_check():
        """Endpoint para verificação de saúde da aplicação"""
        return {
            "status": "healthy",
            "version": settings.app_version,
            "environment": "development" if settings.debug else "production"
        }
    
    return app


# Criar instância da aplicação
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
