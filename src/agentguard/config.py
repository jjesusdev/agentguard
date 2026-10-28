from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict

class Settings(BaseSettings):
    journal_dir: str = Field(default="/var/lib/agentguard/sessions")
    log_level: str = Field(default="INFO")
    rules_dir: str = Field(default="/etc/agentguard/rules")
    sandbox_user: str = Field(default="agentguard")

    model_config = ConfigDict(env_prefix="AGENTGUARD_", env_file=".env")

settings = Settings()
