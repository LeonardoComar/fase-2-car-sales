"""
Testes para o caso de uso CreateUserUseCase.

Demonstra como testar casos de uso seguindo Clean Architecture.
"""

import pytest
from unittest.mock import AsyncMock
from src.application.use_cases.users import CreateUserUseCase
from src.application.dtos.user_dto import UserCreateDto, UserResponseDto
from src.domain.entities.user import User


class TestCreateUserUseCase:
    """
    Testes para o caso de uso de criação de usuário.
    
    Estes testes focam na lógica de aplicação, usando mocks
    para isolar as dependências.
    """
    
    @pytest.fixture
    def create_user_use_case(self, mock_user_repository):
        """
        Fixture que cria uma instância do caso de uso com mock repository.
        """
        return CreateUserUseCase(mock_user_repository)
    
    @pytest.mark.asyncio
    async def test_create_user_with_valid_data(self, create_user_use_case, mock_user_repository):
        """
        Testa criação de usuário com dados válidos.
        """
        # Arrange
        user_create_dto = UserCreateDto(
            email="test@example.com",
            password="password123",
            role="Vendedor",
            employee_id=None
        )
        
        expected_user = User.create_user(
            email="test@example.com",
            password_hash="hashed_password",
            role="Vendedor",
            employee_id=None
        )
        expected_user.id = 1
        
        mock_user_repository.get_user_by_email.return_value = None
        mock_user_repository.create_user.return_value = expected_user
        
        # Act
        result = await create_user_use_case.execute(user_create_dto)
        
        # Assert
        assert isinstance(result, UserResponseDto)
        assert result.email == "test@example.com"
        assert result.role == "Vendedor"
        assert result.id == 1
        
        # Verificar que o repositório foi chamado corretamente
        mock_user_repository.get_user_by_email.assert_called_once_with("test@example.com")
        mock_user_repository.create_user.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_user_with_existing_email_raises_error(self, create_user_use_case, mock_user_repository):
        """
        Testa que criar usuário com email existente levanta erro.
        """
        # Arrange
        user_create_dto = UserCreateDto(
            email="existing@example.com",
            password="password123",
            role="Vendedor",
            employee_id=None
        )
        
        existing_user = User.create_user(
            email="existing@example.com",
            password_hash="old_hash",
            role="Administrador"
        )
        
        mock_user_repository.get_user_by_email.return_value = existing_user
        
        # Act & Assert
        with pytest.raises(ValueError, match="Email já está em uso"):
            await create_user_use_case.execute(user_create_dto)
        
        # Verificar que create_user não foi chamado
        mock_user_repository.create_user.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_create_user_with_invalid_role_raises_error(self, create_user_use_case, mock_user_repository):
        """
        Testa que criar usuário com role inválida levanta erro.
        """
        # Arrange
        user_create_dto = UserCreateDto(
            email="test@example.com",
            password="password123",
            role="RoleInvalida",  # Role inválida
            employee_id=None
        )
        
        mock_user_repository.get_user_by_email.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="Role inválida"):
            await create_user_use_case.execute(user_create_dto)
        
        # Verificar que create_user não foi chamado
        mock_user_repository.create_user.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_create_user_repository_error_propagates(self, create_user_use_case, mock_user_repository):
        """
        Testa que erros do repositório são propagados corretamente.
        """
        # Arrange
        user_create_dto = UserCreateDto(
            email="test@example.com",
            password="password123",
            role="Vendedor",
            employee_id=None
        )
        
        mock_user_repository.get_user_by_email.return_value = None
        mock_user_repository.create_user.side_effect = Exception("Database error")
        
        # Act & Assert
        with pytest.raises(Exception, match="Erro interno do servidor"):
            await create_user_use_case.execute(user_create_dto)
    
    @pytest.mark.asyncio
    async def test_create_user_hashes_password(self, create_user_use_case, mock_user_repository):
        """
        Testa que a senha é hasheada corretamente.
        """
        # Arrange
        user_create_dto = UserCreateDto(
            email="test@example.com",
            password="plain_password",
            role="Vendedor",
            employee_id=None
        )
        
        mock_user_repository.get_user_by_email.return_value = None
        
        # Mock do usuário criado
        created_user = User.create_user(
            email="test@example.com",
            password_hash="hashed_password",
            role="Vendedor"
        )
        created_user.id = 1
        mock_user_repository.create_user.return_value = created_user
        
        # Act
        result = await create_user_use_case.execute(user_create_dto)
        
        # Assert
        # Verificar que create_user foi chamado com User
        call_args = mock_user_repository.create_user.call_args[0][0]
        assert isinstance(call_args, User)
        assert call_args.email == "test@example.com"
        assert call_args.role == "Vendedor"
        # A senha deve ter sido hasheada (não deve ser "plain_password")
        assert call_args.password != "plain_password"
        assert len(call_args.password) > 10  # Hash deve ser mais longo


@pytest.mark.unit
class TestCreateUserUseCaseValidations:
    """
    Testes específicos para validações do caso de uso.
    """
    
    @pytest.fixture
    def create_user_use_case(self, mock_user_repository):
        """
        Fixture que cria uma instância do caso de uso.
        """
        return CreateUserUseCase(mock_user_repository)
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("role", ["Vendedor", "Administrador"])
    async def test_create_user_with_valid_roles(self, create_user_use_case, mock_user_repository, role):
        """
        Testa criação de usuário com todas as roles válidas.
        """
        # Arrange
        user_create_dto = UserCreateDto(
            email="test@example.com",
            password="password123",
            role=role,
            employee_id=None
        )
        
        created_user = User.create_user("test@example.com", "hash", role)
        created_user.id = 1
        
        mock_user_repository.get_user_by_email.return_value = None
        mock_user_repository.create_user.return_value = created_user
        
        # Act
        result = await create_user_use_case.execute(user_create_dto)
        
        # Assert
        assert result.role == role
    
    @pytest.mark.asyncio
    async def test_create_user_with_employee_id(self, create_user_use_case, mock_user_repository):
        """
        Testa criação de usuário com employee_id.
        """
        # Arrange
        user_create_dto = UserCreateDto(
            email="employee@example.com",
            password="password123",
            role="Vendedor",
            employee_id=123
        )
        
        created_user = User.create_user("employee@example.com", "hash", "Vendedor", 123)
        created_user.id = 1
        
        mock_user_repository.get_user_by_email.return_value = None
        mock_user_repository.create_user.return_value = created_user
        
        # Act
        result = await create_user_use_case.execute(user_create_dto)
        
        # Assert
        assert result.employee_id == 123
