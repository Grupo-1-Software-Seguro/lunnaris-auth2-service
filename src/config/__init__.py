from lunnaris_pyinject import Dependency
import services
import dao


class Configuration:
    mail = Dependency(services.QueuedMailService, is_singleton=True)
    token = Dependency(services.TokenGenerator, is_singleton=True)
    dao = Dependency(dao.MongoAuthDAO, is_singleton=True)
    service = Dependency(services.AuthService, dao=dao, token_generator=token, mail=mail, is_singleton=True)
