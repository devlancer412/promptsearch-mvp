import json

from src.models import User

from src.utils.openai import get_embeds
from src.utils.pinecone import pinecone_user_upset, pinecone_user_query

def upset_user(user: User):
  # get embedding verctor
  embedding = get_embeds(json.dumps({
    "name": user.name,
    "email": user.email,
    "skills": user.skills
  }))

  pinecone_user_upset(user.id, {
    "name": user.name,
    "email": user.email,
    "skills": user.skills,
    "embedding": embedding
  })

def query_user(query: str, count: int):
  embedding = get_embeds(query)
  matches = pinecone_user_query(embedding, count)
  return matches