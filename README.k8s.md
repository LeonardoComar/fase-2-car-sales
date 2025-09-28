# Kubernetes - Car Sales API

Este diretório contém os manifests Kubernetes para deploy da aplicação Car Sales API com banco de dados MySQL no namespace `car-sales`.

## 🏗️ Estrutura de Arquivos Kubernetes

```
k8s/
├── namespace.yaml                      # Namespace car-sales
├── mysql-secret.yaml                   # Credenciais MySQL (Secret)
├── mysql-configmap-pvc-deployment.yaml # MySQL (ConfigMap + PVC + Deployment + Service)
├── app-deployment-service.yaml         # Aplicação (ConfigMap + Deployment + Service)
├── static-pvc.yaml                     # PVC para uploads de imagens
├── storageclass.yaml                   # StorageClass para minikube
├── kustomization.yaml                  # Orquestração de todos os recursos
└── README.k8s.md                       # Este arquivo
```

## 📦 Recursos Implementados

### ✅ Recursos Obrigatórios
- **Deployment**: 2 deployments (aplicação + MySQL)
- **ConfigMap**: 3 ConfigMaps (app config + MySQL config + migrações SQL)
- **Secrets**: 1 Secret (credenciais do banco de dados)
- **Services**: 2 Services (app NodePort + MySQL ClusterIP)

### 🎯 Recursos Adicionais
- **Namespace**: Isolamento de recursos no namespace `car-sales`
- **PersistentVolumes**: PVCs para dados MySQL e uploads de imagens
- **StorageClass**: Configuração de storage para minikube
- **Kustomization**: Gerenciamento centralizado dos recursos

## 🐳 Imagem Docker

- **Imagem pública**: `leocomar/carsales:latest`
- **Repositório**: Docker Hub público
- **CI/CD**: O workflow GitHub Actions (`.github/workflows/ci-cd.yaml`) faz build e push automaticamente para essa imagem

## 🚀 Como Executar no Kubernetes local (Minikube)

### Passo-a-Passo

1. **Iniciar o minikube**:
```powershell
minikube start
```

2. **Build da imagem local**:
```powershell
# Na raiz do repositório
docker build -t leocomar/carsales:latest .
```

3. **Carregar imagem no minikube**:
```powershell
minikube image load leocomar/carsales:latest
```

4. **Aplicar todos os manifests**:
```powershell
kubectl apply -k k8s/
```

5. **Verificar se os pods estão rodando**:
```powershell
kubectl get pods -n car-sales -w
```

6. **Verificar logs da aplicação**:
```powershell
kubectl -n car-sales logs deployment/carsales --tail=10
```

7. **Obter URL da aplicação**:
```powershell
minikube service carsales -n car-sales
```

### 🌐 Acessando a Aplicação

O comando `minikube service` abrirá automaticamente a aplicação no browser e mostrará a URL para usar no Postman:

```
|-----------|----------|-------------|---------------------------|
| NAMESPACE |   NAME   | TARGET PORT |            URL            |
|-----------|----------|-------------|---------------------------|
| car-sales | carsales |        8080 | http://127.0.0.1:xxxxx   |
|-----------|----------|-------------|---------------------------|
```

Use a URL mostrada (ex: `http://127.0.0.1:60979`) nas suas collections do Postman.

## 🔍 Comandos Úteis para Debug

```powershell
# Ver status de todos os recursos
kubectl get all -n car-sales

# Ver PVCs
kubectl get pvc -n car-sales

# Ver logs da aplicação
kubectl -n car-sales logs deployment/carsales -f

# Ver logs do MySQL
kubectl -n car-sales logs deployment/mysql -f
```

## 🔒 Observações de Segurança

- O arquivo `mysql-secret.yaml` contém valores de exemplo em base64
- Para produção, use um gerenciador de secrets (Vault, AWS Secrets Manager)
- As credenciais padrão são apenas para desenvolvimento local

## 📋 Estrutura de Serviços

| Serviço | Tipo | Porta | Descrição |
|---------|------|-------|-----------|
| `carsales` | NodePort | 8080:30180 | API FastAPI da aplicação |
| `mysql` | ClusterIP | 3306 | Banco de dados MySQL |

## 🗄️ Volumes Persistentes

| PVC | Tamanho | Descrição |
|-----|---------|-----------|
| `mysql-pvc` | 5Gi | Dados do banco MySQL |
| `static-pvc` | 2Gi | Uploads de imagens da aplicação |