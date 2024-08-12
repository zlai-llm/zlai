from pydantic import BaseModel


__all__ = [
    "CacheConfig",
    "cache_config",
]


class CacheConfig(BaseModel):
    """"""
    max_size: float = 2
    ttl: float = 20 * 60


cache_config = CacheConfig()
