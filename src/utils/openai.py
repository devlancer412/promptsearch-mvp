import openai
from config import cfg

openai.api_key = cfg.OPENAI_API_KEY
openai.Engine.list()  # check we have authenticated

def get_embeds(params: str):
  res = openai.Embedding.create(
    input=params, engine=cfg.EMBEDDING_MODEL
  )
  embeds = res['data'][0]['embedding']

  return embeds