from cosine import cosine_similarity
import os
import json
import numpy as np
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def initialize_supabase(url, key):
    supabase: Client = create_client(url, key)
    return supabase

theology_topics_file = "theology_topics.json"

with open(theology_topics_file, 'r') as file:
    theology_topics = json.load(file)

orgId = '8dfac8d9bc29521e1e87a6c121d7a5c2'

response = supabase.table('sermons').select("id", "embedding").eq("orgId", orgId).eq("has_been_embedded", True).execute()
sermon1 = supabase.table('sermons').select("id", "embedding", "title").eq("id", 1000632196794).execute()
sermon2 = supabase.table('sermons').select("id", "embedding", "title").eq("id", 1000628202546).execute()

sermon_data = sermon1.data
sermon_data2 = sermon2.data

transcripts = response.data

def normalize_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
        return v
    return v / norm

embedding1 = json.loads(transcripts[0]['embedding'])
embedding2 = json.loads(transcripts[1]['embedding'])
embedding3 = json.loads(transcripts[2]['embedding'])
sermon1 = json.loads(sermon1.data[0]['embedding'])
sermon2 = json.loads(sermon2.data[0]['embedding'])
embedding1_normalized = normalize_vector(np.array(embedding1))
embedding2_normalized = normalize_vector(np.array(embedding2))
embedding3_normalized = normalize_vector(np.array(embedding3))
sermon1_normalized = normalize_vector(np.array(sermon1))
sermon2_normalized = normalize_vector(np.array(sermon2))
similarity = cosine_similarity(sermon1_normalized, sermon2_normalized)
print(similarity)

def compare_sermons_to_topics(transcripts, theology_topics, output_filename):
    sermon_topic = []
    for sermon in transcripts:
        # print(sermon['id'])
        s_id = sermon['id']
        s_embedding = json.loads(sermon['embedding'])
        s_embedding_normalized = normalize_vector(np.array(s_embedding))
        for topic in theology_topics:
            t_id = topic['id']
            t_embedding = topic['embedding']
            t_embedding_normalized = normalize_vector(np.array(t_embedding))
            similarity = cosine_similarity(s_embedding_normalized, t_embedding_normalized)
            print(similarity)
            sermon_topic.append({ "s_id": s_id, "t_id": t_id, "similarity": similarity})
    with open(output_filename, 'w') as file:
        json.dump(sermon_topic, file, indent=4)
    return sermon_topic


# Iterate over each item and sum the similarities
def pivot_topics(comparisons):
    sum_similarities = {}
    for topic in comparisons:
        t_id = topic["t_id"]
        similarity = topic["similarity"]
        
        if t_id in sum_similarities:
            sum_similarities[t_id] += similarity
        else:
            sum_similarities[t_id] = similarity
    return sum_similarities


comparisons = compare_sermons_to_topics(sermon_data2, theology_topics, "sermon2.json")
pivoted_data = pivot_topics(comparisons)
print(pivoted_data)