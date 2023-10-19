import os

class Config:
    """Base configuration class. Uses class-based configuration to set default values for all environments."""
    
    # What prefix should we look for in the environment to override these defaults
    ENV_VAR_PREFIX = "GPU_ALLOCATOR_"

    # Set the database type. Currently only sqlite is accepted.
    DATABASE_TYPE = 'sqlite'

    # SQLite Configuration options
    SQLITE_DB_LOCATION = '/db/gpu_allocation.sqlite'

    # Set to a value greater than 1 to enable GPU Oversubscripiton.
    # Do not set this to less than 1.
    OVERSUBSCRIPTION_LIMIT = 1

    @classmethod
    def get_env_var(cls, key):
        env_var_name = f'{cls.ENV_VAR_PREFIX}{key}'
        return os.environ.get(env_var_name)
    
    @classmethod
    def get_config_value(cls, key, default_value):
        return cls.get_env_var(key) or default_value

config_by_name = dict(
    default=Config
)