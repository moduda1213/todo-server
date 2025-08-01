"""사용자가 이미 존재할 때 발생하는 예외"""
class UserAlreadyExistsError(Exception):
    def __init__(self, username : str) :
        self.username = username
        super().__init__(f"Username '{username}' already exists.") # exception

"""사용자가 존재하지 않을 때 발생하는 예외"""
class UserDoesNotExist(Exception):
    def __init__(self, username : str) :
        super().__init__("Your email or password does not match.")

"""패스워드가 일치하지 않을 때 발생하는 예외"""
class PasswordDoesNotMatch(Exception):
    def __init__(self, username : str) :
        super().__init__("Your email or password does not match.")
