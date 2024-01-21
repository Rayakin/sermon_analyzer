import numpy as np
import json

topics_file = 'theology_topics.json'

with open(topics_file, 'r') as file:
    topics = json.load(file)

def cosine_similarity(embedding1, embedding2):
    # Convert lists to numpy arrays
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)

    # Normalize the embeddings to unit vectors
    embedding1_normalized = embedding1 / np.linalg.norm(embedding1)
    embedding2_normalized = embedding2 / np.linalg.norm(embedding2)
 
    # Compute the cosine similarity
    similarity = np.dot(embedding1_normalized, embedding2_normalized)
 
    return similarity

def euclidean_distance(embedding1, embedding2):
    # Convert lists to numpy arrays
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)

    # Calculate the Euclidean distance
    distance = np.sqrt(np.sum((embedding1 - embedding2) ** 2))
    return distance

# Dictionary to hold similarity scores
similarity_scores = {}
euclidean_distances = {}

# Compare each object with every other object
for i in range(len(topics)):
    for j in range(i + 1, len(topics)):
        obj1 = topics[i]
        obj2 = topics[j]

        # Calculate cosine similarity
        similarity = cosine_similarity(obj1['embedding'], obj2['embedding'])
        distance = euclidean_distance(obj1['embedding'], obj2['embedding'])

        # Save the similarity score
        pair_key = f"{obj1['id']} - {obj2['id']}"
        similarity_scores[pair_key] = similarity
        euclidean_distances[pair_key] = distance

# Output the results
for pair, score in similarity_scores.items():
    print(f"Similarity between {pair}: {score}")

for pair, score in euclidean_distances.items():
    print(f"Distance between {pair}: {score}")
