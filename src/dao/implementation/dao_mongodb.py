from mongoengine import Document, StringField
from dao.interface import IAuthDAO
from entities.auth_registry import AuthRegistry

class DBAuthRegistry(Document):
    userId = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    meta = {'collection': 'user_auth'}


class MongoAuthDAO(IAuthDAO):
    
    def get_by_email(self, email: str) -> AuthRegistry:
        obj: DBAuthRegistry = DBAuthRegistry.objects(email=email).first()
        if obj:
            return AuthRegistry(
                userId=obj.userId, 
                email=obj.email,
                password=obj.password)
        else:
            return None

    def get_by_user_id(self, user_id: str) -> AuthRegistry:
        obj: DBAuthRegistry = DBAuthRegistry.objects(userId=user_id).first()
        if obj:
            return AuthRegistry(
                userId=obj.userId, 
                email=obj.email,
                password=obj.password)
        else:
            return None
    
    def save(self, auth_registry: AuthRegistry) -> True:
        obj = DBAuthRegistry(
            userId=auth_registry.userId,
            password=auth_registry.password,
            email=auth_registry.email
        )
        obj.save()
        return True
    
    def update(self, auth_registry: AuthRegistry) -> bool:
        obj: DBAuthRegistry = DBAuthRegistry.objects(userId=auth_registry.userId).first()
        if not obj:
            return False

        count = obj.update(email=auth_registry.email, password=auth_registry.password)
        return count > 0
        