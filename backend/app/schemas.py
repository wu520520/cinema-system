"""
Pydantic 数据验证模型
功能：
- 定义API请求和响应的数据结构
- 自动验证数据格式
- 支持ORM对象转JSON
"""

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from .models import GradeEnum


# ================= 地区相关模型 =================

class RegionBase(BaseModel):
    """地区基础模型（公共字段）"""
    name: str


class RegionCreate(RegionBase):
    """创建地区时使用的模型"""
    pass


class Region(RegionBase):
    """返回地区信息时使用的模型"""
    id: int

    class Config:
        from_attributes = True  # 支持从ORM对象转换


# ================= 分类相关模型 =================

class CategoryBase(BaseModel):
    """分类基础模型（公共字段）"""
    name: str


class CategoryCreate(CategoryBase):
    """创建分类时使用的模型"""
    pass


class Category(CategoryBase):
    """返回分类信息时使用的模型"""
    id: int

    class Config:
        from_attributes = True


# ================= 电影相关模型 =================

class FilmBase(BaseModel):
    """电影基础模型（公共字段）"""
    title: str                      # 电影标题
    synopsis: Optional[str] = None  # 剧情简介
    region: Optional[int] = None    # 地区ID
    director: Optional[str] = None  # 导演
    release_date: Optional[date] = None  # 上映日期
    times: int                      # 时长（秒）
    score: Optional[float] = None   # IMDb评分
    grade: GradeEnum                # 电影分级
    category: int                   # 分类ID
    profit: Optional[int] = None    # 票房（万元）
    organization: Optional[str] = None  # 制作/发行机构


class FilmCreate(FilmBase):
    """创建电影时使用的模型"""
    pic: Optional[str] = None       # 封面图片文件名


class FilmUpdate(FilmBase):
    """更新电影时使用的模型"""
    pic: Optional[str] = None       # 封面图片文件名


class Film(FilmBase):
    """返回电影信息时使用的模型"""
    id: int                         # 电影ID
    pic: Optional[str] = None       # 封面图片文件名
    created: Optional[datetime]     # 创建时间

    class Config:
        from_attributes = True


class FilmDetail(Film):
    """返回电影详情时使用的模型（包含地区名和分类名）"""
    region_name: Optional[str] = None      # 地区名称
    category_name: Optional[str] = None    # 分类名称
