import random
from pydantic import BaseModel
from pymonad.tools import curry
from pymonad.either import Either, Left, Right


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


@curry(1)
def get_api_data(request: Request) -> Response | API_ERROR:
    if random.choice([True, False]):
        print(f" Success !! {request} API data successfully retrieved")
        return Response(response="Success")
    else:
        print(" Fail !! API data FAILED")
        return Left(API_ERROR(error_message="API Error"))


@curry(1)
def load_db(response: Response) -> Ack | DB_ERROR:
    if random.choice([True, False]):
        print(f" Success !!  {response} Data loaded to DB")
        return Ack(email="test@gmail.com")
    else:
        print("Fail !! DB Error")
        return Left(DB_ERROR(error_message="DB Error"))


@curry(1)
def notify(ack: Ack) -> bool | NOTIFICATION_ERROR:
    if random.choice([True, False]):
        print(f" Success !! {ack} Email notification sent")
        return True
    else:
        print("Fail !! Email notification sent")
        return Left(NOTIFICATION_ERROR(error_message="Notification error"))


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
    result = (
        Either.insert(req)
        .then(get_api_data)
        .then(load_db)
        .then(notify)
        .either(
            lambda on_failure: print(f"Error: {on_failure}"),
            lambda on_success: on_success,
        )
    )
    print(result)


process_request_fp(Request(req_id="MY_REQUEST"))