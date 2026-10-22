"""
CRUD 操作模块（Create, Read, Update, Delete）
功能：
- 封装所有数据库操作
- 提供统一的数据访问接口
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from datetime import datetime
from . import models, schemas
from .models import GradeEnum


def get_regions(db: Session):
    """
    获取所有地区列表
    """
    return db.query(models.Region).all()


def get_categories(db: Session):
    """
    获取所有分类列表
    """
    return db.query(models.Category).all()


def get_film(db: Session, film_id: int):
    """
    根据ID获取单个电影
    """
    return db.query(models.Film).filter(models.Film.id == film_id).first()


def get_films(
    db: Session,
    category: Optional[int] = None,
    region: Optional[int] = None,
    grade: Optional[str] = None,
    sort_by: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    获取电影列表（支持多种筛选和排序方式）
    
    参数：
        category: 分类ID筛选
        region: 地区ID筛选
        grade: 分级筛选
        sort_by: 排序方式（profit票房/score评分/created创建时间）
        skip: 分页偏移量
        limit: 每页最大数量
    """
    query = db.query(models.Film)
    
    # 分类筛选
    if category:
        query = query.filter(models.Film.category == category)
    # 地区筛选
    if region:
        query = query.filter(models.Film.region == region)
    # 分级筛选
    if grade:
        query = query.filter(models.Film.grade == grade)
    # 排序
    if sort_by:
        if sort_by == "profit":
            query = query.order_by(desc(models.Film.profit))  # 按票房降序
        elif sort_by == "score":
            query = query.order_by(desc(models.Film.score))    # 按评分降序
        elif sort_by == "created":
            query = query.order_by(desc(models.Film.created))  # 按创建时间降序
    
    # 分页
    return query.offset(skip).limit(limit).all()


def create_film(db: Session, film: schemas.FilmCreate):
    """
    创建新电影记录
    自动设置创建时间为当前时间
    """
    # 处理分级枚举（兼容字符串和枚举两种输入）
    grade_value = film.grade.value if isinstance(film.grade, GradeEnum) else film.grade
    
    db_film = models.Film(
        title=film.title,
        synopsis=film.synopsis,
        pic=film.pic,
        region=film.region,
        director=film.director,
        release_date=film.release_date,
        times=film.times,
        score=film.score,
        grade=grade_value,
        category=film.category,
        profit=film.profit,
        organization=film.organization,
        created=datetime.now()  # 自动设置创建时间
    )
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film


def update_film(db: Session, film_id: int, film_data: dict):
    """
    更新电影信息（只更新有值的字段）
    
    参数：
        film_id: 电影ID
        film_data: 包含要更新字段的字典
    """
    film = get_film(db, film_id)
    
    if film:
        # 遍历字典，只更新有值的字段
        for key, value in film_data.items():
            if hasattr(film, key) and value is not None:
                setattr(film, key, value)
        db.commit()
        db.refresh(film)
        return film
    
    return None


def delete_film(db: Session, film_id: int):
    """
    删除电影
    返回：True删除成功，False电影不存在
    """
    film = get_film(db, film_id)
    
    if film:
        db.delete(film)
        db.commit()
        return True
    
    return False
