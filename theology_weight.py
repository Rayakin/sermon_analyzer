from cosine import cosine_similarity
import json

transcripts_file = "transcripts_master.json"
theology_topics_file = "theology_topics.json"


with open(transcripts_file, 'r') as file:
    transcripts = json.load(file)

with open(theology_topics_file, 'r') as file:
    theology_topics = json.load(file)

def compare_sermons_to_topics(transcripts, theology_topics, output_filename):
    sermon_topic = []
    for sermon in transcripts:
        s_id = sermon['id']
        s_embedding = sermon['embedding']
        for topic in theology_topics:
            t_id = topic['id']
            t_embedding = topic['embedding']
            similarity = cosine_similarity(s_embedding, t_embedding)
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


comparisons = compare_sermons_to_topics(transcripts, theology_topics, "sermon_to_topic_comparison.json")
pivoted_data = pivot_topics(comparisons)
print(pivoted_data)