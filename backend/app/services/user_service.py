from datetime import datetime
from typing import Optional
from app.core.databricks import execute_query, execute_update
from app.core.security import get_password_hash, verify_password
from app.models.user import UserSignup, UserProfile

class UserService:
    @staticmethod
    def get_user_by_username(username: str) -> Optional[dict]:
        query = "SELECT * FROM default.users WHERE username = :username"
        results = execute_query(query, {"username": username})
        return results[0] if results else None
    
    @staticmethod
    def create_user(user: UserSignup) -> UserProfile:
        # Check if user exists
        if UserService.get_user_by_username(user.username):
            raise ValueError("Username already exists")
        
        # Hash password
        hashed_password = get_password_hash(user.password)
        
        # Insert user
        query = """
        INSERT INTO default.users 
        (username, password_hash, name, age, investment_style, 
         investment_goal, budget, experience, created_at, updated_at)
        VALUES (:username, :password_hash, :name, :age, :investment_style,
                :investment_goal, :budget, :experience, :created_at, :updated_at)
        """
        
        now = datetime.now().isoformat()
        params = {
            "username": user.username,
            "password_hash": hashed_password,
            "name": user.name,
            "age": user.age,
            "investment_style": user.investment_style,
            "investment_goal": user.investment_goal,
            "budget": user.budget,
            "experience": user.experience,
            "created_at": now,
            "updated_at": now
        }
        
        execute_update(query, params)
        
        return UserProfile(
            username=user.username,
            name=user.name,
            age=user.age,
            investment_style=user.investment_style,
            investment_goal=user.investment_goal,
            budget=user.budget,
            experience=user.experience,
            created_at=now
        )
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[dict]:
        user = UserService.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user['password_hash']):
            return None
        return user
    
    @staticmethod
    def update_user(username: str, update_data) -> UserProfile:
        query = """
        UPDATE default.users
        SET name = :name,
            age = :age,
            investment_style = :investment_style,
            investment_goal = :investment_goal,
            budget = :budget,
            experience = :experience,
            updated_at = :updated_at
        WHERE username = :username
        """
        
        params = {
            "username": username,
            "name": update_data.name,
            "age": update_data.age,
            "investment_style": update_data.investment_style,
            "investment_goal": update_data.investment_goal,
            "budget": update_data.budget,
            "experience": update_data.experience,
            "updated_at": datetime.now().isoformat()
        }
        
        execute_update(query, params)
        
        # Return updated profile
        return UserProfile(
            username=username,
            name=update_data.name,
            age=update_data.age,
            investment_style=update_data.investment_style,
            investment_goal=update_data.investment_goal,
            budget=update_data.budget,
            experience=update_data.experience
        )

user_service = UserService()
