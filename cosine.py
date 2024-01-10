import numpy as np

def cosine_similarity(embedding1, embedding2):
    # Normalize the embeddings to unit vectors
    embedding1_normalized = embedding1 / np.linalg.norm(embedding1)
    embedding2_normalized = embedding2 / np.linalg.norm(embedding2)
    
    # Compute the cosine similarity
    similarity = np.dot(embedding1_normalized, embedding2_normalized)
    
    return similarity