# fase-2-car-sales

## Como executar

```bash
# Subir a aplicação
docker compose up -d

# Parar a aplicação
docker compose down

# Remover volume do banco (resetar dados)
docker volume rm fase-2-car-sales_db_carsales_data

# Rebuild forçado (se houver problemas)
docker compose up -d --build
```

## Endpoints

- **API**: http://localhost:8180
- **Health Check**: http://localhost:8180/api/health_check
- **Banco MySQL**: localhost:3306 (carsales/Mudar123!)

