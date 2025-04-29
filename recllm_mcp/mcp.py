from fastmcp import FastMCP



class RecLLMMCP:
  def __init__(self, app):
    self.mcp = FastMCP.from_fastapi(app)
    
  def run(self):
    self.mcp.run(transport='sse')