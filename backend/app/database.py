"""
数据库连接模块
功能：
- 创建数据库引擎
- 配置会话工厂
- 提供依赖注入函数
- 定义ORM基类
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

# 获取配置实例
settings = get_settings()

# 创建数据库引擎
# pool_pre_ping：连接前自动ping检查连接是否有效
# pool_recycle：连接最大存活时间（秒），避免超时断开
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)

# 创建会话工厂（用于生成数据库会话对象）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类：所有ORM模型都继承自此基类
Base = declarative_base()


def get_db():
    """
    数据库会话依赖注入函数（FastAPI的Depends用）
    用法：db: Session = Depends(get_db)
    自动处理会话的打开和关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
