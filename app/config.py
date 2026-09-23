from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    embedding_api_key: str = ""
    embedding_base_url: str = ""
    embedding_model: str = ""

    llm_api_key: str = ""
    llm_base_url: str = ""
    llm_model: str = ""

    chunk_size: int = 400
    chunk_overlap: int = 80
    top_k: int = 4
    chroma_dir: str = "./data/chroma"


settings = Settings()