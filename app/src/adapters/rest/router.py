"""
Roteador principal da aplicação Clean Architecture.

Aplicando o princípio Single Responsibility Principle (SRP) - 
responsável apenas pelo roteamento de alto nível.
"""

from fastapi import APIRouter

# Routes da estrutura Clean Architecture
from src.adapters.rest.sale_routes import sale_router
from src.adapters.rest.employee_routes import employee_router
from src.adapters.rest.message_routes import message_router
from src.adapters.rest.client_routes import client_router
from src.adapters.rest.car_routes import car_router
from src.adapters.rest.motorcycle_routes import motorcycle_router
from src.adapters.rest.user_routes import user_router, auth_router
from src.adapters.rest.blacklisted_token_routes import blacklisted_token_router
from src.adapters.rest.vehicle_image_routes import vehicle_image_router

# Novo router de autenticação com Clean Architecture completa
# from src.adapters.rest.routers.auth_router import auth_router as clean_auth_router

# Criar roteador principal para a nova estrutura
clean_router = APIRouter()

# Incluir todas as rotas
clean_router.include_router(sale_router, prefix="/sales", tags=["Vendas"])
clean_router.include_router(employee_router, prefix="/employees", tags=["Funcionários"]) 
clean_router.include_router(message_router, prefix="/messages", tags=["Mensagens"])
clean_router.include_router(client_router, prefix="/clients", tags=["Clientes"])
clean_router.include_router(car_router, prefix="/cars", tags=["Carros"])
clean_router.include_router(motorcycle_router, prefix="/motorcycles", tags=["Motocicletas"])
clean_router.include_router(user_router, prefix="", tags=["Usuários"])
clean_router.include_router(auth_router, prefix="", tags=["Autenticação"])
clean_router.include_router(blacklisted_token_router, prefix="/admin", tags=["Administração de Tokens"])
clean_router.include_router(vehicle_image_router, prefix="/vehicles", tags=["Imagens de Veículos"])

# Rota de Health Check para a nova estrutura
@clean_router.get("/health_check")
async def health_check():
    """Endpoint de verificação de saúde da aplicação."""
    return {
        "status": "healthy",
        "architecture": "Clean Architecture",
        "version": "1.0.0",
        "endpoints": {
            "sales": "/api/sales",
            "employees": "/api/employees", 
            "messages": "/api/messages",
            "clients": "/api/clients",
            "cars": "/api/cars",
            "motorcycles": "/api/motorcycles",
            "auth": "/api/auth",
            "users": "/api/users",
            "vehicle_images": "/api/vehicles/{type}/{id}/images",
            "admin": "/api/admin"
        },
        "message": "Sistema de vendas de carros - Padrão Postman implementado",
        "postman_compatible": True
    }
