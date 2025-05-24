from fastapi import FastAPI
from recllm_core.db import BasicDatabase
from .dependencies import AuthMiddleware


class RecLLMApp(FastAPI):
  def __init__(self, auth=True, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.db = BasicDatabase()
    if auth:
      self.add_middleware(AuthMiddleware)
  
  def add_routers(self, routers):
    routers = [getattr(routers, attr) for attr in dir(routers) if attr.endswith('router')]
    for router in routers:
      self.include_router(router)