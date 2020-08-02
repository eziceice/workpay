class AssemblyPaymentError(Exception):
    SYSTEM_ERROR = 'Internal Server Error, Please Contact the System Admin'
    CONNECTION_ERROR = 'Failed to Connect to the Payment System'

    def __init__(self, message, http_status: int, content=None):
        super().__init__(message)
        self.http_status = http_status
        self.content = content


class AssemblyPaymentAuthError(AssemblyPaymentError):
    def __init__(self, message, http_status: int, content):
        super().__init__(message, http_status, content)


class ResourceNotFoundError(Exception):
    def __init__(self, message, http_status: int):
        super().__init__(message)
        self.http_status = http_status
