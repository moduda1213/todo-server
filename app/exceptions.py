class UserAlreadyExistsError(Exception):
    """사용자가 이미 존재할 때 발생하는 예외"""
    def __init__(self, username : str) :
        self.username = username
        super().__init__(f"Username '{username}' already exists.") # exception

class UserDoesNotExist(Exception):
    """사용자가 존재하지 않을 때 발생하는 예외"""
    pass

class PasswordDoesNotMatch(Exception):
    """패스워드가 일치하지 않을 때 발생하는 예외"""
    pass