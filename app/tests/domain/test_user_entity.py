"""
Testes para a entidade User do domínio.

Demonstra como testar entidades de domínio seguindo Clean Architecture.
"""

import pytest
from datetime import datetime
from src.domain.entities.user import User


class TestUserEntity:
    """
    Testes para a entidade User.
    
    Estes testes focam apenas na lógica de negócio da entidade,
    sem dependências externas (banco de dados, frameworks, etc.).
    """
    
    def test_create_user_with_valid_data(self):
        """
        Testa a criação de usuário com dados válidos.
        """
        # Arrange
        email = "test@example.com"
        password_hash = "hashed_password"
        role = "Vendedor"
        employee_id = 123
        
        # Act
        user = User.create_user(email, password_hash, role, employee_id)
        
        # Assert
        assert user.email == email
        assert user.password == password_hash
        assert user.role == role
        assert user.employee_id == employee_id
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
    
    def test_create_user_with_invalid_role_raises_error(self):
        """
        Testa que criar usuário com role inválida levanta erro.
        """
        # Arrange
        email = "test@example.com"
        password_hash = "hashed_password"
        invalid_role = "RoleInvalida"
        
        # Act & Assert
        with pytest.raises(ValueError, match="Role inválida"):
            User.create_user(email, password_hash, invalid_role)
    
    def test_is_valid_role_with_valid_roles(self):
        """
        Testa validação de roles válidas.
        """
        # Act & Assert
        assert User.is_valid_role("Vendedor") is True
        assert User.is_valid_role("Administrador") is True
        assert User.is_valid_role("RoleInvalida") is False
    
    def test_is_admin_returns_true_for_admin_user(self):
        """
        Testa que is_admin retorna True para usuário administrador.
        """
        # Arrange
        user = User.create_user("admin@example.com", "hash", "Administrador")
        
        # Act & Assert
        assert user.is_admin() is True
        assert user.is_vendedor() is False
    
    def test_is_vendedor_returns_true_for_vendedor_user(self):
        """
        Testa que is_vendedor retorna True para usuário vendedor.
        """
        # Arrange
        user = User.create_user("vendedor@example.com", "hash", "Vendedor")
        
        # Act & Assert
        assert user.is_vendedor() is True
        assert user.is_admin() is False
    
    def test_can_access_admin_features_for_admin_user(self):
        """
        Testa que administrador pode acessar funcionalidades administrativas.
        """
        # Arrange
        admin_user = User.create_user("admin@example.com", "hash", "Administrador")
        vendedor_user = User.create_user("vendedor@example.com", "hash", "Vendedor")
        
        # Act & Assert
        assert admin_user.can_access_admin_features() is True
        assert vendedor_user.can_access_admin_features() is False
    
    def test_update_role_with_valid_role(self):
        """
        Testa atualização de role com role válida.
        """
        # Arrange
        user = User.create_user("user@example.com", "hash", "Vendedor")
        original_updated_at = user.updated_at
        
        # Act
        user.update_role("Administrador")
        
        # Assert
        assert user.role == "Administrador"
        assert user.updated_at > original_updated_at
    
    def test_update_role_with_invalid_role_raises_error(self):
        """
        Testa que atualizar role com role inválida levanta erro.
        """
        # Arrange
        user = User.create_user("user@example.com", "hash", "Vendedor")
        
        # Act & Assert
        with pytest.raises(ValueError, match="Role inválida"):
            user.update_role("RoleInvalida")
    
    def test_user_repr(self):
        """
        Testa a representação string do usuário.
        """
        # Arrange
        user = User.create_user("test@example.com", "hash", "Vendedor")
        user.id = 1
        
        # Act
        repr_str = repr(user)
        
        # Assert
        assert "User(id=1" in repr_str
        assert "email='test@example.com'" in repr_str
        assert "role='Vendedor'" in repr_str
    
    def test_user_post_init_validation(self):
        """
        Testa validação no __post_init__.
        """
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Role inválida"):
            User(
                email="test@example.com",
                password="hash",
                role="RoleInvalida"
            )


@pytest.mark.unit
class TestUserEntityValidations:
    """
    Testes específicos para validações da entidade User.
    """
    
    @pytest.mark.parametrize("role", ["Vendedor", "Administrador"])
    def test_valid_roles(self, role):
        """
        Testa que todas as roles válidas são aceitas.
        """
        user = User.create_user("test@example.com", "hash", role)
        assert user.role == role
    
    @pytest.mark.parametrize("invalid_role", ["Admin", "Seller", "Manager", ""])
    def test_invalid_roles(self, invalid_role):
        """
        Testa que roles inválidas são rejeitadas.
        """
        with pytest.raises(ValueError):
            User.create_user("test@example.com", "hash", invalid_role)
    
    def test_user_creation_sets_timestamps(self):
        """
        Testa que criação de usuário define timestamps corretamente.
        """
        # Arrange
        before_creation = datetime.now()
        
        # Act
        user = User.create_user("test@example.com", "hash", "Vendedor")
        
        # Assert
        after_creation = datetime.now()
        assert before_creation <= user.created_at <= after_creation
        assert before_creation <= user.updated_at <= after_creation
