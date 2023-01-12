import dataclasses

from users.models import CustomUser


@dataclasses.dataclass
class UserCreator:
    validated_data: dict

    def execute(self):
        username = self.validated_data["username"]
        password = self.validated_data["password"]
        group = self.validated_data["group"]
        email = self.validated_data["email"]
        user = CustomUser(username=username, email=email, group=group)
        user.set_password(password)
        user.save()
        return user
