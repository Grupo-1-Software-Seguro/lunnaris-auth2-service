from mongoengine import Document, StringField, IntField, ListField
from dao.interface import IAuthDAO
from entities.auth_registry import AuthRegistry, Role


class DBAuthRegistry(Document):
    """
    MongoDB ODM Representation of the AuthRegistry
    """
    userId = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    userType = IntField(required=True)
    meta = {'collection': 'user_auth'}

class DBRole(Document):
    userType = IntField(required=True)
    permissions = ListField(StringField())
    meta = {"collection": "user_roles"}


class MongoAuthDAO(IAuthDAO):

    def map_from_db(self, db_auth_registry: DBAuthRegistry) -> AuthRegistry:
        """Maps a database object to business object
        Parameters:
            db_auth_registry: DBAuthRegistry
        Returns:
            AuthRegistry
        """
        return AuthRegistry(
            userId=db_auth_registry.userId,
            email=db_auth_registry.email,
            password=db_auth_registry.password,
            userType=db_auth_registry.userType
        )

    def map_to_db(self, auth_registry: AuthRegistry) -> DBAuthRegistry:
        """Maps a business object to database object
        Parameters:
            auth_registry: AuthRegistry
        Returns:
            DBAuthRegistry
        """
        return DBAuthRegistry(
            userId=auth_registry.userId,
            email=auth_registry.email,
            password=auth_registry.password,
            userType=auth_registry.userType
        )

    def get_by_email(self, email: str) -> AuthRegistry:
        obj: DBAuthRegistry = DBAuthRegistry.objects(email=email).first()
        if obj:
            return self.map_from_db(obj)
        else:
            return None

    def get_by_user_id(self, user_id: str) -> AuthRegistry:
        obj: DBAuthRegistry = DBAuthRegistry.objects(userId=user_id).first()
        if obj:
            return self.map_from_db(obj)
        else:
            return None

    def save(self, auth_registry: AuthRegistry) -> True:
        obj = self.map_to_db(auth_registry)
        obj.save()
        return True

    def update(self, auth_registry: AuthRegistry) -> bool:
        obj: DBAuthRegistry = DBAuthRegistry.objects(userId=auth_registry.userId).first()
        if not obj:
            return False

        count = obj.update(
            email=auth_registry.email,
            password=auth_registry.password,
            userType=auth_registry.userType
            )

        return count > 0
    
    def get_role(self, type: int) -> Role:
        role: DBRole = DBRole.objects(userType=type).first()
        if role:
            return Role(type=role.userType, permissions=role.permissions)
