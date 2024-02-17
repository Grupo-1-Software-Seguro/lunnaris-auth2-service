import src.api.auth_client as api

auth2 = api.Auth2(None)

response = auth2.handle_exception(api.ApiError("Hola"))
print(response)


