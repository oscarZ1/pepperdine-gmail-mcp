import os.path 
from mcp.server.fastmcp import FastMCP
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CRED_FILE = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

# Initialize the server
mcp = FastMCP("Waves-Context-Server")


def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CRED_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


@mcp.tool()
def fetch_emails(count: int = 5) -> str:
    """Fetches the most recent emails from the inbox."""
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId='me', maxResults=count).execute()
        messages = results.get('messages', [])

        if not messages:
            return "No emails found."

        email_summaries = []
        for msg in messages:
            m = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = m.get('payload', {})
            headers = payload.get('headers', [])
            
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown Sender")
            
            email_summaries.append(f"From: {sender}\nSubject: {subject}\n---")

        return "\n".join(email_summaries)

    except Exception as e:
        return f"An error occurred: {str(e)}"


@mcp.tool()
def get_system_status() -> str:
    """A simple ping tool to verify the MCP server is communicating."""
    return "Waves-Context-Server is online and ready. Go Waves!"


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str: 
    """Get a personalized greeting"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Runs the server using standard input/output (the protocol's default)
    mcp.run()