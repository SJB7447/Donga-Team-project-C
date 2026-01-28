from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

print(f"Connecting to {url}...")

try:
    supabase: Client = create_client(url, key)
    print("Supabase client initialized successfully.")
    # Attempt a basic check - if auth url is properly formed, it's a good sign.
    print(f"Auth URL: {supabase.auth_url}")
except Exception as e:
    print(f"Failed to initialize: {e}")
