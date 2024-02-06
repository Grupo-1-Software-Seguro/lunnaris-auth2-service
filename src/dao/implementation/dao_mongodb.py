from mongoengine import Document, StringField
from dao.interface import IAuthDAO
from entities.auth_registry import AuthRegistry

class DBAuthRegistry(Document):
    userId = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    fullName = StringField(required=True)
    meta = {'collection': 'user_auth'}


class MongoAuthDAO(IAuthDAO):

    def map_from_db(self, db_auth_registry: DBAuthRegistry) -> AuthRegistry:
        return AuthRegistry(
            userId=db_auth_registry.userId,
            email=db_auth_registry.email,
            password=db_auth_registry.password,
            fullName=db_auth_registry.fullName
        )
    
    def map_to_db(self, auth_registry: AuthRegistry) -> DBAuthRegistry:
        return DBAuthRegistry(
            userId=auth_registry.userId,
            email=auth_registry.email,
            password=auth_registry.password,
            fullName=auth_registry.fullName
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
            fullName=auth_registry.fullName)
        
        return count > 0
        