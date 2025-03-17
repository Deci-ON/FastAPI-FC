from fastapi import APIRouter
import json
from core.database import engines
router = APIRouter()

@router.get("/admin/db-pool-status")
async def get_db_pool_status():
    """Retorna estatísticas sobre os pools de conexão."""
    pool_stats = {}
   
    for name, engine in engines.items():
        pool = engine.pool
        pool_stats[name] = {
            "size": pool.size(),
            "checkedin": pool.checkedin(),
            "checkedout": pool.checkedout(),
            "overflow": pool.overflow(),
            # Note: checkedout_connections() is not available in async pools
            # You can use the other metrics to understand pool usage
        }
   
    return pool_stats