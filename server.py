from mcp.server.fastmcp import FastMCP

# Initialize the server
mcp = FastMCP("Waves-Context-Server")

@mcp.tool()
def get_system_status() -> str:
    """A simple ping tool to verify the MCP server is communicating."""
    return "Waves-Context-Server is online and ready. Go Waves!"

# Placeholder for your future Gmail tool
@mcp.tool()
def placeholder_fetch_emails(count: int = 5) -> str:
    """Fetches the most recent emails from the inbox."""
    return f"This will eventually return your {count} most recent emails."

if __name__ == "__main__":
    # Runs the server using standard input/output (the protocol's default)
    mcp.run()