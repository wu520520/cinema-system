"""
数据模型定义模块
功能：
- 定义数据库表对应的ORM模型
- 定义枚举类型
- 配置表之间的关系
使用 SQLAlchemy 2.0 新语法
"""

from enum import Enum
from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class GradeEnum(str, Enum):
    """
    电影分级枚举（美国电影协会MPAA分级）
    - G：大众级，适合所有人
    - PG：建议家长指导
    - PG-13：13岁以下需家长指导
    - R：17岁以下需成人陪同
    - NC-17：17岁以下禁止
    - NR：未分级
    """
    G = "G"
    PG = "PG"
    PG_13 = "PG-13"
    R = "R"
    NC_17 = "NC-17"
    NR = "NR"


class Region(Base):
    """
    地区表模型（movie_region）
    关系：一个地区对应多部电影
    """
    __tablename__ = "movie_region"

    # 地区ID（主键，自增）
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # 地区名称（唯一）
    name: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    # 关系：该地区的所有电影（反向关系）
    films = relationship("Film", back_populates="region_rel")


class Category(Base):
    """
    分类表模型（movie_category）
    关系：一个分类对应多部电影
    """
    __tablename__ = "movie_category"

    # 分类ID（主键，自增）
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # 分类名称（唯一）
    name: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    films = relationship("Film", back_populates="category_rel")


class Film(Base):
    """
    影片表模型（movie_film）
    关系：
      - 多对一：多个电影属于一个地区
      - 多对一：多个电影属于一个分类
    """
    __tablename__ = "movie_film"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    synopsis: Mapped[Optional[str]] = mapped_column(String(1024))
    pic: Mapped[Optional[str]] = mapped_column(String(80))
    # 地区（外键，关联movie_region.id）
    region: Mapped[Optional[int]] = mapped_column(ForeignKey("movie_region.id"))
    director: Mapped[Optional[str]] = mapped_column(String(30))
    release_date: Mapped[Optional[date]] = mapped_column()
    times: Mapped[int] = mapped_column(nullable=False)
    score: Mapped[Optional[float]] = mapped_column(Float)
    grade: Mapped[str] = mapped_column(String(5), nullable=False)
    # 所属分类ID（外键，关联movie_category.id，必填）
    category: Mapped[int] = mapped_column(ForeignKey("movie_category.id"), nullable=False)
    profit: Mapped[Optional[int]] = mapped_column()
    organization: Mapped[Optional[str]] = mapped_column(String(128))
    created: Mapped[Optional[datetime]] = mapped_column()
    region_rel = relationship("Region", back_populates="films")
    category_rel = relationship("Category", back_populates="films")
