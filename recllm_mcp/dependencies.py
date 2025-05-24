from fastapi import status, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from uuid import UUID



def get_db(request: Request):
	try:
		yield request.app.db
	finally:
		pass  # Connection handling is managed by BasicDatabase class


def get_user(api_key, db):
  existing_tables = db.pull_existing_tables(['user'])
  UserTable = existing_tables['user']
  with db.Session() as session:
    user = session.query(UserTable).filter(UserTable.api_key==api_key).first()
  return user


class AuthMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next):
    request.state.db = next(get_db(request))
    # Get API Key
    api_key = request.headers.get('authorization')
    # Authorization: Bearer 
    if api_key:
      api_key = api_key.replace('Bearer ', '')
    # RecLLM-API-Key
    if not api_key:
      api_key = request.headers.get('RecLLM-API-Key')
    if not api_key:
      return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={'detail': 'API key is missing'}
      )
    # Validate if api_key is a valid UUID
    try:
      UUID(api_key)
    except ValueError:
      return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={'detail': 'Invalid API key format - must be a valid API Key'}
      )
    # Get user
    user = get_user(api_key, request.state.db)
    if not user:
      return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={'detail': 'Invalid API key'}
      )
    request.state.user = user
    response = await call_next(request)
    return response 