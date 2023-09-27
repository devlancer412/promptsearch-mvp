import pinecone
from config import cfg

# initialize connection to pinecone (get API key at app.pinecone.io)
pinecone.init(
    api_key=cfg.PINECONE_API_KEY,
    environment=cfg.PINECONE_ENV  # find next to API key in console
)

def get_user_index(dimension: int):
  # check if 'openai' index already exists (only create index if not)
  if 'worker-search-mvp' not in pinecone.list_indexes():
      pinecone.create_index('worker-search-mvp', dimension=dimension)
  # connect to index
  index = pinecone.Index('worker-search-mvp')
  return index

def pinecone_user_upsert(id: str, data: dict):
  index = get_user_index(len(data['embedding']))
  index.upsert(vectors=[{ 'id': id, 'values': data['embedding'] }])
  
def remove_user_index(id: int):
  index = get_user_index(0)
  index.delete(ids=[id])
  
def pinecone_user_query(embedding: list, count: int):
  index = get_user_index(len(embedding))
  res = index.query([embedding], top_k=count, include_metadata=True)
  return res['matches']
  