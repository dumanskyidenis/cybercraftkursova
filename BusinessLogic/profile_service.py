from typing import List
from Domain.ViewModels.pc_viewmodels import (
    UserProfileViewModel, 
    ProfileUpdateRequestViewModel, 
    PasswordChangeRequestViewModel, 
    ComponentShortViewModel,
    SaveBuildRequestViewModel
)
from Domain.Models.saved_build import SavedBuild
from Repositories.user_repository import UserRepository
from Repositories.saved_build_repository import SavedBuildRepository

# ДОДАНО: Імпорти для правильної роботи з хешами паролів
from werkzeug.security import generate_password_hash, check_password_hash

class ProfileService:
    def __init__(self, user_repository: UserRepository, build_repository: SavedBuildRepository):
        self.user_repo = user_repository
        self.build_repo = build_repository

    def get_my_profile(self, user_id: int) -> UserProfileViewModel:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return UserProfileViewModel(id=0, username="Не знайдено", email="", saved_builds_count=0)
            
        return UserProfileViewModel(
            id=user.id,
            username=user.username,
            email=user.email,
            saved_builds_count=len(user.saved_builds)
        )

    def update_profile(self, user_id: int, request: ProfileUpdateRequestViewModel) -> UserProfileViewModel:
        user = self.user_repo.get_by_id(user_id)
        if user:
            if request.username:
                user.username = request.username
            if request.email:
                user.email = request.email
            self.user_repo.update()
        return self.get_my_profile(user_id)

    def change_password(self, user_id: int, request: PasswordChangeRequestViewModel) -> bool:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False

        # ВИПРАВЛЕНО: Тепер ми правильно порівнюємо хеш із введеним паролем
        if check_password_hash(user.password_hash, request.old_password):
            # Новий пароль також хешуємо перед збереженням
            user.password_hash = generate_password_hash(request.new_password)
            self.user_repo.update()
            return True
        return False

    def save_build_to_favorites(self, user_id: int, request: SaveBuildRequestViewModel) -> bool:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False

        new_build = SavedBuild(
            user_id=user.id, 
            build_name=request.build_name,
            cpu_id=request.cpu_id, gpu_id=request.gpu_id,
            motherboard_id=request.motherboard_id, ram_id=request.ram_id,
            storage_id=request.storage_id, psu_id=request.psu_id,
            cooler_id=request.cooler_id, case_id=request.case_id,
            mouse_id=request.mouse_id, keyboard_id=request.keyboard_id,
            headset_id=request.headset_id
        )
        self.build_repo.add(new_build)
        return True

    # НОВА ФУНКЦІЯ: Перейменування збірки
    def rename_saved_build(self, user_id: int, build_id: int, new_name: str) -> bool:
        builds = self.build_repo.get_by_user_id(user_id)
        for b in builds:
            if b.id == build_id:
                b.build_name = new_name
                self.user_repo.update()
                return True
        return False

    # ВИПРАВЛЕНО: Повертаємо всі ID деталей, щоб фронтенд міг їх гарно відобразити
    def get_my_saved_builds(self, user_id: int) -> List[dict]:
        builds = self.build_repo.get_by_user_id(user_id)
        if not builds: return []

        result = []
        for b in builds:
            result.append({
                "id": b.id, "name": b.build_name,
                "cpu_id": b.cpu_id, "gpu_id": b.gpu_id, "motherboard_id": b.motherboard_id,
                "ram_id": b.ram_id, "storage_id": b.storage_id, "psu_id": b.psu_id,
                "cooler_id": b.cooler_id, "case_id": b.case_id,
                # ДОДАЛИ ПЕРИФЕРІЮ:
                "mouse_id": b.mouse_id, "keyboard_id": b.keyboard_id, "headset_id": b.headset_id
            })
        return result