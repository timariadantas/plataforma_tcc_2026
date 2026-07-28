class ChangePasswordRequestDto:
    def __init__(self, new_password):
        
        self.new_password = new_password
        
    @staticmethod
    def from_dict(data):
        return ChangePasswordRequestDto(
            new_password=data.get("new_password")
        ) 