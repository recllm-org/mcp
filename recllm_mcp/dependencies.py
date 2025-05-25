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

def get_api_key(request: Request):
  # Authorization: Bearer 
  api_key = request.headers.get('authorization')
  if api_key:
    api_key = api_key.replace('Bearer ', '')
  # RecLLM-API-Key
  if not api_key:
    api_key = request.headers.get('RecLLM-API-Key')
  return api_key

def validate_api_key(api_key):
  try:
    UUID(api_key)
  except ValueError:
    return False
  return True


class AuthMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next):
    api_key = get_api_key(request)
    if not api_key:
      return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={'detail': 'API key is missing'}
      )
    # Validate if api_key is a valid UUID
    if not validate_api_key(api_key):
      return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={'detail': 'Invalid API key format - must be a valid API Key'}
      )
    # Get user
    user = get_user(api_key, request.app.db)
    if not user:
      return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={'detail': 'Invalid API key'}
      )
    request.state.user = user
    response = await call_next(request)
    return response 