from fastapi import Request



def get_db(request: Request):
	try:
		yield request.app.db
	finally:
		pass  # Connection handling is managed by BasicDatabase class