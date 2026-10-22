"""
应用配置模块
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置类"""
    # 数据库连接URL（MySQL+pymysql驱动），从 .env 读取，不提交真实密码
    DATABASE_URL: str = ""
    # 图片上传目录
    UPLOAD_DIR: str = "uploads"
    # 最大上传文件大小（10MB）
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    # 允许上传的文件扩展名
    ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "gif"}
    # 允许的CORS源（跨域请求来源）
    CORS_ORIGINS: list = ["http://localhost", "http://localhost:8080", "http://localhost:3000"]

    class Config:
        """配置类的配置：从 .env 文件读取环境变量"""
        env_file = ".env"


@lru_cache()
def get_settings():
    """
    获取配置单例（使用LRU缓存，只初始化一次）"""
    return Settings()
