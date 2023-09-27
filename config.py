from app.__internal import ConfigBase


class Configuration(ConfigBase):
    # database config
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "root"
    DATABASE: str = "promptsearch-mvp"
    # jwt config
    JWT_SECRET_KEY: str = (
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    JWT_REFRESH_SECRET_KEY: str = (
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )

    OPENAI_API_KEY: str = "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"
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    PINECONE_API_KEY: str = "ac2ac06d-9ba1-438c-812b-a677194f2c4d"
    PINECONE_ENV: str = "gcp-starter"
    
# --- Do not edit anything below this line, or do it, I'm not your mom ----
defaults = Configuration(autoload=False)
cfg = Configuration()