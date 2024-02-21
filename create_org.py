from supabase import create_client, Client
import os
import uuid

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def initialize_supabase(url, key):
    supabase: Client = create_client(url, key)
    return supabase

def generate_random_hex_id():
    # Generate a random UUID
    random_uuid = uuid.uuid4()
    # Convert the UUID to a hexadecimal string
    hex_id = random_uuid.hex
    return hex_id

def create_org(name, stream_id):
    # Try to fetch the org based on the given name
    response = supabase.table('orgs').select("name", "org_id").eq("stream_id", stream_id).execute()
    orgs = response.data

    # Check if the org exists
    if orgs and len(orgs) > 0:
        # Org exists, return the existing org_id
        print(f"This org already exists: {orgs[0]['org_id']}")
        return orgs[0]['org_id']
    else:
        # Org does not exist, create a new one
        try:
            hex_id = generate_random_hex_id()
            print(hex_id)
            # Insert new org
            supabase.table("orgs").insert({
                "name": name,
                "org_id": hex_id,
                "stream_id": stream_id
                # Additional fields can be added here
            }).execute()
            print("Org created successfully.")
            return hex_id
        except Exception as e:
            print(f"There was an error creating the org: {e}")
            return False
