from Domain.ViewModels.pc_viewmodels import UserAuthRequestViewModel, UserProfileViewModel
from BusinessLogic.auth_service import AuthService

class AuthController:
    # === DEPENDENCY INJECTION ===
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service

    def register(self, request: UserAuthRequestViewModel) -> UserProfileViewModel:
        """Реєстрація нового користувача з перевіркою унікальності email"""
        return self._auth_service.register(request)

    def login(self, request: UserAuthRequestViewModel) -> str:
        """Авторизація користувача (перевірка пароля та видача токена доступу)"""
        return self._auth_service.login(request)

    def logout(self, token: str) -> bool:
        """Вихід з акаунта (анулювання токена безпеки)"""
        return self._auth_service.logout(token)