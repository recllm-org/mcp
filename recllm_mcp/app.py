from fastapi import FastAPI
from .db import BasicDatabase



class RecLLMApp(FastAPI):
  def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.db = BasicDatabase()
	
	def add_routers(self, routers):
		routers = [getattr(routers, attr) for attr in dir(routers) if attr.endswith('router')]
		for router in routers:
			self.include_router(router)