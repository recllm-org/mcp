from .app import RecLLMApp
from fastmcp import FastMCP



class RecLLMMCP:
  def __init__(self):
    self.app = RecLLMApp()
    self.mcp = FastMCP.from_fastapi(self.app)
    
  def run(self):
    self.mcp.run(transport='sse')