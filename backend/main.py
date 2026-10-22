"""
宝莱坞影视系统 - FastAPI 主应用
"""

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
from app import config, database, models, schemas, crud

# ================= 应用初始化 =================

# 获取配置
settings = config.get_settings()

# 创建 FastAPI 应用
app = FastAPI(title="宝莱坞影视系统API")

# 配置 CORS 中间件（允许跨域请求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录（如果不存在）
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
# 挂载静态文件服务（用于访问上传的图片）
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


def get_db():
    """
    数据库会话依赖注入函数
    每个请求都会获得一个独立的数据库会话，用完自动关闭
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= API 路由定义 =================

@app.get("/api/regions", response_model=list[schemas.Region])
def get_regions(db: Session = Depends(get_db)):
    """
    获取所有地区列表
    """
    return crud.get_regions(db)


@app.get("/api/categories", response_model=list[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    """
    获取所有分类列表
    """
    return crud.get_categories(db)


@app.get("/api/films", response_model=list[schemas.FilmDetail])
def get_films(
    category: Optional[int] = None,
    region: Optional[int] = None,
    grade: Optional[str] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取电影列表（支持筛选和排序）
    
    查询参数：
        category: 按分类ID筛选
        region: 按地区ID筛选
        grade: 按分级筛选
        sort_by: 排序方式（profit/score/created）
    """
    films = crud.get_films(db, category=category, region=region, grade=grade, sort_by=sort_by)
    
    # 补充地区名和分类名，用于前端展示
    result = []
    for film in films:
        film_dict = schemas.Film.model_validate(film).model_dump()
        film_dict["region_name"] = film.region_rel.name if film.region_rel else None
        film_dict["category_name"] = film.category_rel.name if film.category_rel else None
        result.append(schemas.FilmDetail(**film_dict))
    
    return result


@app.get("/api/films/{film_id}", response_model=schemas.FilmDetail)
def get_film(film_id: int, db: Session = Depends(get_db)):
    """
    获取单个电影详情
    
    路径参数：
        film_id: 电影ID
    """
    film = crud.get_film(db, film_id=film_id)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # 补充地区名和分类名
    film_dict = schemas.Film.model_validate(film).model_dump()
    film_dict["region_name"] = film.region_rel.name if film.region_rel else None
    film_dict["category_name"] = film.category_rel.name if film.category_rel else None
    
    return schemas.FilmDetail(**film_dict)


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    上传图片文件
    
    功能：
        - 检查文件是否存在
        - 验证文件扩展名
        - 生成唯一文件名（UUID）
        - 保存到上传目录
    返回：
        文件名
    """
    # 检查文件是否提供
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # 获取并验证文件扩展名
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # 生成唯一文件名（UUID + 原扩展名）
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return {"filename": unique_filename}


@app.post("/api/films", response_model=schemas.Film)
def create_film(film: schemas.FilmCreate, db: Session = Depends(get_db)):
    """
    添加新电影
    注意：图片需要先通过 /api/upload 接口上传
    """
    return crud.create_film(db=db, film=film)


@app.put("/api/films/{film_id}", response_model=schemas.Film)
def update_film(film_id: int, film: schemas.FilmUpdate, db: Session = Depends(get_db)):
    """
    更新电影信息
    
    路径参数：
        film_id: 电影ID
    请求体：
        要更新的字段（只更新提供的字段）
    """
    existing_film = crud.get_film(db, film_id=film_id)
    if not existing_film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # exclude_unset=True：只更新用户提供的字段，保留未提供的字段原值
    updated_film = crud.update_film(db, film_id, film.model_dump(exclude_unset=True))
    if not updated_film:
        raise HTTPException(status_code=500, detail="Update failed")
    
    return updated_film


@app.delete("/api/films/{film_id}")
def delete_film(film_id: int, db: Session = Depends(get_db)):
    """
    删除电影（同时删除关联的图片文件）
    
    路径参数：
        film_id: 电影ID
    """
    film = crud.get_film(db, film_id=film_id)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    
    # 删除关联的图片文件（如果存在）
    if film.pic:
        pic_path = os.path.join(settings.UPLOAD_DIR, film.pic)
        if os.path.exists(pic_path):
            os.remove(pic_path)
    
    # 删除数据库记录
    success = crud.delete_film(db=db, film_id=film_id)
    if not success:
        raise HTTPException(status_code=500, detail="Delete failed")
    
    return {"message": "Film deleted successfully"}


# ================= 开发环境启动 =================

if __name__ == "__main__":
    """
    开发环境直接运行
    生产环境使用 uvicorn 命令或 systemd 服务启动
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
