from dishka import Provider, Scope, provide

from .memory.repositories import UserRepoMemory


class AppProvider(Provider):
    user_repo = provide(UserRepoMemory, scope=Scope.APP)
