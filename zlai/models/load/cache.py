from pydantic import BaseModel


__all__ = [
    "CacheConfig",
    "cache_config",
]


class CacheConfig(BaseModel):
    """"""
    maxsize: float = 8
    # ttl: float = 20 * 60


cache_config = CacheConfig()
