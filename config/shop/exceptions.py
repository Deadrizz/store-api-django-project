from rest_framework.exceptions import APIException
class KeyedAPIException(APIException):
    status_code = 400
    default_detail = "Bad request."
    default_code = "error"
    def __init__(self,detail=None,key=None,status_code=None,**extras):
        if status_code is not None:
            self.status_code = status_code
        self.key = key or 'detail'
        self.extras = extras
        super().__init__(detail or self.default_detail)
    def get_full_details(self):
        data = {'detail':str(self.detail),'key':self.key}
        if self.extras:
            data.update(self.extras)
        return data

class NotFoundKeyed(KeyedAPIException):
    status_code=404
    default_detail='Object not found'
    def __init__(self,detail=None,key='object'):
        super().__init__(detail or self.default_detail,key=key,status_code=404)

class StockError(KeyedAPIException):
    def __init__(self,available,detail='Not enough in stock.'):
        super().__init__(detail=detail,key='quantity',available=available)
