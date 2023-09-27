import json

from src.models import User

from src.utils.openai import get_embeds
from src.utils.pinecone import pinecone_user_upsert, pinecone_user_query, remove_user_index

def upset_user(user: User):
  # get embedding verctor
  embedding = get_embeds(json.dumps({
    "name": user.name,
    "email": user.email,
    "skills": user.skills
  }))

  pinecone_user_upsert(f"worker_{user.id}", {
    "embedding": embedding
  })

def query_user(query: str, count: int):
  embedding = get_embeds(query)
  matches = pinecone_user_query(embedding, count)
  return matches

def remove_user(id: int):
  remove_user_index(f"worker_{id}")