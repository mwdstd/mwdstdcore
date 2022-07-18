
class APIError(BaseException):
    def __init__(self, message = None):
        if(message is None):
            self.message = 'An API error occured'
        else:
            self.message = message


class RequestIsNotJSON(APIError):
    def __init__(self):
        self.message = 'Request body is not in JSON format'


class RequestMalformed(APIError):
    def __init__(self):
        self.message = 'Error parsing request body'


class RequestDataError(APIError):
    def __init__(self):
        self.message = 'Bad request data'
