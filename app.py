from chalice.app import Chalice, Response
from chalicelib.muscle_core_handler import muscle_core_handler
from chalicelib.db import init_db 

app = Chalice(app_name='MuscleCore')
app.debug = True
app.api.cors = True

init_db()

#  MIDDLEWARES


@app.middleware("http")
def require_authorization_header_middleware(event, get_response):
    # Middleware to require the Authorization header
    unauthorized_paths = ["/sign-up", "/healthcheck"]
    url_path = event.context["resourcePath"]
    print("URL PATH: ", url_path)

    if event.method == "OPTIONS":
        return get_response(event)
    
    if url_path in unauthorized_paths:
        return get_response(event)

    token = event.headers.get("Authorization")

    # Token validations
    if not token:
        msg = {"error": "Bearer token has not been provided."}

        return Response(
            body=msg, status_code=401, headers={"Content-Type": "application/json"}
        )
    
    parts_token = token.split(" ")

    if len(parts_token) != 2 or parts_token[0] != "Bearer":
        msg = {"error": "Bearer token has not correct format."}

        return Response(
            body=msg, status_code=400, headers={"Content-Type": "application/json"}
        )
    
    jwt_token = parts_token[1]

    if not jwt_token:
        msg = {"error": "Bearer token has not been provided."}
        return Response(
            body=msg, status_code=401, headers={"Content-Type": "application/json"}
        )

    # Decode token
    try:
        token_decoded = muscle_core_handler.api.authentication.decode_authentication_jwt(jwt_token)
    except Exception:
        msg = {"error": "Token is invalid or expired."}
        return Response(
            body=msg, status_code=401, headers={"Content-Type": "application/json"}
        )
    
    # Inject request.user
    event.user_id = token_decoded["user_id"]

    # Inject request.jwt
    event.jwt_token = jwt_token

    # Inject request.decoded_token
    event.decoded_token = token_decoded

    return get_response(event)

@app.route('/sign-up', methods=['POST'])
def index():
    request = app.current_request

    try :
        response = muscle_core_handler.api.authentication.user_handler(request)
        return response
    except Exception as e:
        return Response(
            body={"error": f"Error while creating user. Exception: {e}"},
            status_code=400,
            headers={"Content-Type": "application/json"},
        )
