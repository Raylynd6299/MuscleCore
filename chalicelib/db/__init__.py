import os
from entities import  muscle_core_db

# Credentials for connection with supabase
SUPABASE_CONNECTION_STRING = os.getenv(
    "SUPABASE_BD_URL"
)

def init_db():
    # Generate mapping
    muscle_core_db.bind(provider="postgres", dsn=SUPABASE_CONNECTION_STRING)
    muscle_core_db.generate_mapping(create_tables=True, check_tables=False)
