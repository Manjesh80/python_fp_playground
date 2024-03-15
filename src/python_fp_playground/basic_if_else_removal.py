import random
from pydantic import BaseModel


class APP_ERROR(BaseModel):
    error_message: str


class DB_ERROR(APP_ERROR):
    pass


class API_ERROR(APP_ERROR):
    pass


class NOTIFICATION_ERROR(APP_ERROR):
    pass


class Request(BaseModel):
    req_id: str


class Response(BaseModel):
    response: str


class Ack(BaseModel):
    email: str


def get_api_data(request: Request) -> Response | API_ERROR:
    if random.choice([True, False]):
        print(" Success !! API data successfully retrieved")
        return Response(response="Success")
    else:
        print(" Fail !! API data FAILED")
        return API_ERROR(error_message="API Error")


def load_db(response: Response) -> Ack | DB_ERROR:
    if random.choice([True, False]):
        print(" Success !!  Data loaded to DB")
        return Ack(email="test@gmail.com")
    else:
        print("Fail !! DB Error")
        return DB_ERROR(error_message="DB Error")


def notify(ack: Ack) -> bool | NOTIFICATION_ERROR:
    if random.choice([True, False]):
        print(" Success !! Email notification sent")
        return True
    else:
        print("Fail !! Email notification sent")
        return NOTIFICATION_ERROR(error_message="Notification error")


def process_request_non_fp(req: Request) -> bool:
    resp = get_api_data(request=req)
    if type(resp) is Response:
        api_res = load_db(response=resp)
        if type(api_res) is Ack:
            ack_resp = notify(api_res)
            if type(ack_resp) is bool:
                return ack_resp
            else:
                return False
        else:
            return False
    else:
        return False


def process_request_fp(req: Request) -> bool:
    # (get_api_data)(load_db)(notify)(req).else(lambda x -> API_ERROR : print(Error))
    # How to implement this in functional way
    pass


process_request_non_fp(Request(req_id="MY_REQUEST"))
