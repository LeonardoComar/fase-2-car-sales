"""
Roteador principal da aplicação Clean Architecture.

Aplicando o princípio Single Responsibility Principle (SRP) - 
responsável apenas pelo roteamento de alto nível.
"""

from fastapi import APIRouter

# Routes da estrutura Clean Architecture
from src.adapters.rest.routers.sale_router import sale_router
from src.adapters.rest.routers.employee_router import employee_router
from src.adapters.rest.routers.message_router import message_router
from src.adapters.rest.routers.client_router import client_router
from src.adapters.rest.routers.car_router import car_router
from src.adapters.rest.routers.motorcycle_router import motorcycle_router
from src.adapters.rest.routers.user_router import user_router, auth_router
from src.adapters.rest.routers.blacklisted_token_router import blacklisted_token_router
from src.adapters.rest.routers.vehicle_image_router import vehicle_image_router

# Novo router de autenticação com Clean Architecture completa
# from src.adapters.rest.routers.auth_router import create_auth_router

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
            "vehicle_images": "/api/vehicles/cars/{car_id}/images",
            "admin": "/api/admin"
        },
        "message": "Sistema de vendas de carros - Padrão Postman implementado",
        "postman_compatible": True
    }
