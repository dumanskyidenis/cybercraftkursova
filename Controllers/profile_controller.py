from typing import List
from Domain.ViewModels.pc_viewmodels import (
    UserProfileViewModel, 
    ProfileUpdateRequestViewModel, 
    PasswordChangeRequestViewModel, 
    ComponentShortViewModel,
    SaveBuildRequestViewModel # <--- Додали сюди
)
from BusinessLogic.profile_service import ProfileService

class ProfileController:
    # === DEPENDENCY INJECTION ===
    def __init__(self, profile_service: ProfileService):
        self._profile_service = profile_service

    def get_my_profile(self, user_id: int) -> UserProfileViewModel:
        """Отримати всю інформацію про свій профіль"""
        return self._profile_service.get_my_profile(user_id)

    def update_profile(self, user_id: int, request: ProfileUpdateRequestViewModel) -> UserProfileViewModel:
        """Змінити ім'я користувача або контактний email"""
        return self._profile_service.update_profile(user_id, request)

    def change_password(self, user_id: int, request: PasswordChangeRequestViewModel) -> bool:
        """Безпечна зміна пароля"""
        return self._profile_service.change_password(user_id, request)

    def save_build_to_favorites(self, user_id: int, request: SaveBuildRequestViewModel) -> bool:
        """Зберегти конфігурацію ПК в 'Улюблене' з усіма комплектуючими та периферією"""
        return self._profile_service.save_build_to_favorites(user_id, request)

    def get_my_saved_builds(self, user_id: int) -> List[ComponentShortViewModel]:
        """Вивести список усіх збережених збірок"""
        return self._profile_service.get_my_saved_builds(user_id)
    
    def rename_saved_build(self, user_id: int, build_id: int, new_name: str) -> bool:
        return self._profile_service.rename_saved_build(user_id, build_id, new_name)