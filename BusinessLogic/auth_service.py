from Domain.Models.user import User
from Domain.ViewModels.pc_viewmodels import UserAuthRequestViewModel, UserProfileViewModel
from werkzeug.security import generate_password_hash, check_password_hash
# 1. Імпортуємо наш новий репозиторій
from Repositories.user_repository import UserRepository 

class AuthService:
    # 2. Dependency Injection: передаємо репозиторій всередину сервісу
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    def register(self, request: UserAuthRequestViewModel) -> UserProfileViewModel:
        # 3. Використовуємо репозиторій замість User.query
        existing_user = self.user_repo.get_by_email(request.email)
        if existing_user:
            raise ValueError("Користувач з таким email вже існує!")

        generated_username = request.email.split('@')[0]
        hashed_password = generate_password_hash(request.password_hash)

        new_user = User(
            username=generated_username,
            email=request.email,
            password_hash=hashed_password
        )
        
        # 4. Репозиторій сам робить db.session.add() та db.session.commit()
        self.user_repo.add(new_user)

        return UserProfileViewModel(
            id=new_user.id, 
            username=new_user.username, 
            email=new_user.email, 
            saved_builds_count=0
        )

    def login(self, request: UserAuthRequestViewModel) -> str:
        # Шукаємо користувача через репозиторій
        user = self.user_repo.get_by_email(request.email)
        
        if user and check_password_hash(user.password_hash, request.password_hash):
            return f"jwt_mock_token_header.payload_user_id_{user.id}.signature_secret"
            
        return ""

    def logout(self, token: str) -> bool:
        if token:
            return True
        return False