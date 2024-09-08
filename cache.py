import redis
from config import settings
import asyncio

# class Cache:
#     def __init__(self):
#         self.redis_host = settings.REDIS_HOST
#         self.redis_port = settings.REDIS_PORT
#         self.cache_timeout = settings.REDIS_CACHE_TIMEOUT
#         self.redis = redis.from_url(f"redis://{self.redis_host}:{self.redis_port}")
    
#     @staticmethod
#     async def cache_product(self, product):
#         """Cache product price if not already cached or update it if changed."""
#         cached_price = await asyncio.to_thread(self.redis.get, product.product_title)
#         if cached_price and float(cached_price) == product.product_price:
#             return True
#         await asyncio.to_thread(self.redis.set, product.product_title, product.product_price, ex=self.cache_timeout)
#         return False




class Cache:
    redis = redis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")

    @staticmethod
    async def cache_product(product):
        """Cache product price if not already cached or update it if changed."""
        cached_price = await asyncio.to_thread(Cache.redis.get, product.product_title)
        if cached_price and float(cached_price) == product.product_price:
            return True
        await asyncio.to_thread(Cache.redis.set, product.product_title, product.product_price, ex=settings.REDIS_CACHE_TIMEOUT)
        return False