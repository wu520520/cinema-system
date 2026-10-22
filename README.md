# 宝莱坞影视系统

## 项目简介

一个基于 **Python + FastAPI + MySQL + Vue 3** 的电影管理系统，实现了完整的电影库管理功能，包括电影的添加、编辑、删除、查看、筛选和排序等操作。

### 功能特性

- ✅ **电影管理**：添加、编辑、删除电影信息
- ✅ **图片上传**：支持电影封面图片上传
- ✅ **智能筛选**：按类型、地区、分级联合筛选
- ✅ **多种排序**：按票房、IMDb评分、上映时间排序
- ✅ **详情展示**：完整展示电影信息，时长自动转换为时分秒格式
- ✅ **分级系统**：使用 G/PG/PG-13/R/NC-17/NR 六级电影分级

---

## 目录结构

```
cinema system/
├── backend/                 # 后端项目
│   ├── app/                 # 应用模块
│   │   ├── __init__.py
│   │   ├── config.py        # 数据库配置
│   │   ├── database.py      # SQLAlchemy 连接
│   │   ├── models.py        # 数据模型（ORM）
│   │   ├── schemas.py       # Pydantic 验证模型
│   │   └── crud.py          # CRUD 操作封装
│   ├── database/
│   │   ├── init.sql         # 数据库初始化脚本
│   │   └── test_data.sql    # 测试数据脚本
│   ├── uploads/             # 上传文件存储目录
│   ├── main.py              # FastAPI 主入口
│   ├── add_test_data.py     # 测试数据添加脚本
│   └── requirements.txt     # Python 依赖列表
└── frontend/                # 前端项目
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── api/             # API 接口封装
    │   │   └── index.js
    │   ├── utils/           # 工具函数
    │   │   └── index.js
    │   ├── views/           # 页面组件
    │   │   ├── FilmList.vue     # 电影列表页
    │   │   ├── FilmDetail.vue   # 电影详情页
    │   │   ├── AddFilm.vue      # 添加电影页
    │   │   └── EditFilm.vue     # 编辑电影页
    │   ├── router/          # 路由配置
    │   │   └── index.js
    │   ├── App.vue
    │   └── main.js
    ├── package.json
    └── vue.config.js        # Vue 配置（含代理）
```

---

## 一、环境要求

| 组件 | 版本要求 |
|------|----------|
| Python | 3.8+ |
| Node.js | 16+ |
| MySQL | 5.7+ |

---

## 二、数据库初始化

### 2.1 创建数据库和表

首先确保 MySQL 服务已启动，然后执行初始化脚本：

```bash
# 登录 MySQL
mysql -u root -p

# 执行初始化脚本（在 MySQL 客户端中）
source /path/to/backend/database/init.sql;
```

或使用命令行：

```bash
mysql -u root -p < backend/database/init.sql
```

### 2.2 数据库配置

修改 `backend/app/config.py` 或后端根目录下的 `.env` 中的数据库连接信息：

```python
# 默认配置（推荐使用 .env 方式，不提交真实密码）
DATABASE_URL = "mysql+pymysql://root:你的密码@localhost:3306/cinema_system"
```

### 2.3 初始数据

数据库初始化后，已自动包含：

**地区表（movie_region）**：
- 内地、港台、欧美、亚洲、其它

**分类表（movie_category）**：
- 动作、喜剧、爱情、动画、剧情、惊悚、犯罪、科幻、战争、纪录、电视剧、其他

---

## 三、Windows 本地测试指南

### 3.1 启动后端服务

```powershell
# 进入后端目录
cd "g:\人工智能\P2\cinema system\backend"

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 启动服务
python main.py
```

后端服务运行在：http://localhost:8000

### 3.2 添加测试数据

```powershell
# 在已激活的虚拟环境中运行
python add_test_data.py
```

### 3.3 启动前端服务

打开新的 PowerShell 窗口：

```powershell
# 进入前端目录
cd "g:\人工智能\P2\cinema system\frontend"

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run serve
```

前端服务运行在：http://localhost:8080

### 3.4 访问应用

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端页面 | http://localhost:8080 | 主应用入口 |
| 后端 API | http://localhost:8000/api/films | 电影数据接口 |
| API 文档 | http://localhost:8000/docs | Swagger 文档 |

---

## 四、Linux 虚拟机部署

### 4.0 文件上传到虚拟机

#### 推荐目录结构

```
# 虚拟机1（后端服务器）
/home/ubuntu/cinema/
└── backend/              # 后端代码目录

# 虚拟机2（前端服务器）
/home/ubuntu/cinema/
└── frontend/             # 前端代码目录
```

#### 方式1：使用 scp 命令上传（推荐）

**上传后端代码到虚拟机1：**
```bash
# 在 Windows PowerShell 中执行
scp -r "g:\人工智能\P2\cinema system\backend" ubuntu@<虚拟机1的IP>:/home/ubuntu/cinema/
```

**上传前端代码到虚拟机2：**
```bash
# 在 Windows PowerShell 中执行
scp -r "g:\人工智能\P2\cinema system\frontend" ubuntu@<虚拟机2的IP>:/home/ubuntu/cinema/
```

#### 方式2：使用 Git（如果已上传到仓库）

```bash
# 在虚拟机1中克隆后端
cd /home/ubuntu/cinema
git clone <你的仓库地址>
mv <仓库名>/backend .

# 在虚拟机2中克隆前端
cd /home/ubuntu/cinema
git clone <你的仓库地址>
mv <仓库名>/frontend .
```

### 4.1 后端部署（虚拟机1）

#### 环境准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python
sudo apt install python3 python3-pip python3-venv -y

# 安装 MySQL（如未安装）
sudo apt install mysql-server -y
```

#### 项目配置

```bash
# 进入后端目录
cd /home/ubuntu/cinema/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建上传目录
mkdir -p uploads

# 设置权限
chmod 755 uploads
```

#### 启动服务

```bash
# 开发模式
uvicorn main:app --host 0.0.0.0 --port 80 --reload

# 生产模式（推荐使用 supervisor 或 systemd）
uvicorn main:app --host 0.0.0.0 --port 80
```

### 4.2 前端部署（虚拟机2）

#### 环境准备

```bash
# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# 验证安装
node -v
npm -v
```

#### 项目配置

```bash
# 进入前端目录
cd /home/ubuntu/cinema/frontend

# 安装依赖
npm install

# 构建生产版本
npm run build
```

#### 使用 Nginx 部署

```bash
# 安装 Nginx
sudo apt install nginx -y

# 配置 Nginx
sudo nano /etc/nginx/sites-available/cinema

# 添加以下内容：
server {
    listen 80;
    server_name www.你的姓名全拼.com;

    root /home/ubuntu/cinema/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://api.你的姓名全拼.com/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /uploads/ {
        proxy_pass http://api.你的姓名全拼.com/uploads/;
    }
}

# 启用配置
sudo ln -s /etc/nginx/sites-available/cinema /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4.3 Host 配置

**虚拟机2（前端服务器）**：

```bash
sudo nano /etc/hosts
# 添加：
<虚拟机1的IP> api.你的姓名全拼.com
```

**宿主机**：

Windows：编辑 `C:\Windows\System32\drivers\etc\hosts`
```
<虚拟机2的IP> www.你的姓名全拼.com
```

Linux/Mac：编辑 `/etc/hosts`
```
<虚拟机2的IP> www.你的姓名全拼.com
```

---

## 五、功能详细说明

### 5.1 电影添加

- 支持完整电影信息录入
- 封面图片上传（自动保存到 uploads 目录）
- 分级选择（G/PG/PG-13/R/NC-17/NR）
- 自动关联地区和分类

### 5.2 电影编辑

- 预填充现有数据
- 支持修改所有字段
- 支持重新上传封面图片

### 5.3 电影删除

- 删除电影记录
- 自动删除关联的封面图片文件

### 5.4 电影列表

- **筛选功能**：
  - 按类型筛选（动作、喜剧、爱情等）
  - 按地区筛选（内地、港台、欧美等）
  - 按分级筛选（G、PG、PG-13、R、NC-17、NR）
  - 支持多条件联合筛选

- **排序功能**：
  - 按票房倒序
  - 按 IMDb 评分倒序
  - 按上映时间倒序

### 5.5 电影详情

- 完整展示电影所有信息
- 时长自动转换（秒 → 时分秒格式）
- 显示地区和分类名称
- 提供编辑入口

---

## 六、API 接口文档

### 6.1 基础地址

本地开发：`http://localhost:8000/api`  
生产环境：`http://api.你的姓名全拼.com/api`

### 6.2 接口列表

| 方法 | 路径 | 说明 | 参数 |
|------|------|------|------|
| GET | `/regions` | 获取地区列表 | 无 |
| GET | `/categories` | 获取分类列表 | 无 |
| GET | `/films` | 获取电影列表 | 筛选、排序参数 |
| GET | `/films/{id}` | 获取电影详情 | id（整数） |
| POST | `/films` | 添加电影 | JSON 数据 |
| PUT | `/films/{id}` | 更新电影 | JSON 数据 |
| DELETE | `/films/{id}` | 删除电影 | id（整数） |
| POST | `/upload` | 上传图片 | multipart/form-data |

### 6.3 接口详细说明

#### GET /api/films - 获取电影列表

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| category | int | 分类ID（可选） |
| region | int | 地区ID（可选） |
| grade | string | 分级（可选） |
| sort_by | string | 排序字段（profit/score/release_date） |

**响应示例**：
```json
{
  "total": 14,
  "items": [
    {
      "id": 1,
      "title": "西虹市首富",
      "synopsis": "剧情简介...",
      "pic": "abc123.jpg",
      "region": 1,
      "region_name": "内地",
      "director": "闫非、彭大魔",
      "release_date": "2018-07-27",
      "times": 9180,
      "score": 8.9,
      "grade": "PG-13",
      "category": 2,
      "category_name": "喜剧",
      "profit": 254759,
      "organization": "北京开心麻花影业",
      "created": "2024-01-01 12:00:00"
    }
  ]
}
```

#### POST /api/films - 添加电影

**请求体**：
```json
{
  "title": "新电影",
  "synopsis": "剧情介绍",
  "pic": "uploaded_file.jpg",
  "region": 1,
  "director": "导演名字",
  "release_date": "2024-01-01",
  "times": 7200,
  "score": 8.5,
  "grade": "PG-13",
  "category": 2,
  "profit": 100000,
  "organization": "制片公司"
}
```

#### PUT /api/films/{id} - 更新电影

**请求体**：与添加电影相同，可选字段

---

## 七、技术栈

### 后端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.8+ | 编程语言 |
| FastAPI | 0.100+ | 高性能 Web 框架 |
| SQLAlchemy | 2.0+ | ORM 框架 |
| PyMySQL | 1.1+ | MySQL 驱动 |
| Pydantic | 2.0+ | 数据验证 |
| Uvicorn | 0.23+ | ASGI 服务器 |

### 前端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | 3.4+ | 前端框架 |
| Vue Router | 4.2+ | 路由管理 |
| Axios | 1.6+ | HTTP 客户端 |
| Element Plus | 2.4+ | UI 组件库 |

---

## 八、测试数据

项目包含 14 部测试电影数据，执行以下命令添加：

```bash
cd backend
source venv/bin/activate
python add_test_data.py
```

测试数据包含：
- 国产电影：西虹市首富、流浪地球、哪吒之魔童降世、红海行动、战狼2等
- 欧美电影：复仇者联盟4、泰坦尼克号、肖申克的救赎、阿甘正传等
- 亚洲电影：千与千寻、寄生虫、釜山行等

---

## 九、开发说明

### 9.1 代码规范

- Python：遵循 PEP8 规范
- JavaScript：使用 ESLint 检查
- 代码注释：关键逻辑添加注释说明

### 9.2 安全注意事项

- 文件上传限制类型（仅允许图片）
- SQLAlchemy 防止 SQL 注入
- 输入数据验证（Pydantic）

### 9.3 常见问题

**Q1：前端无法连接后端？**

检查：
1. 后端服务是否启动
2. 防火墙是否允许 8000 端口
3. `vue.config.js` 代理配置是否正确

**Q2：图片上传失败？**

检查：
1. `uploads` 目录是否存在
2. 目录权限是否正确（755）
3. 文件大小是否超过限制

---

## 十、项目维护

- **作者**：王小帝
- **版本**：1.0.0
- **更新日期**：2026年

---

## 附录

### 电影分级说明

| 分级 | 说明 |
|------|------|
| G | 大众级，任何人都可以观看 |
| PG | 辅导级，部分内容可能不适合儿童 |
| PG-13 | 特别辅导级，建议13岁以上观看 |
| R | 限制级，建议17岁以上观看 |
| NC-17 | 17岁以下禁止观看 |
| NR | 未分级 |

### 时间格式转换

数据库存储总秒数，前端显示时自动转换为 `HH:MM:SS` 格式。

---

**项目已完成，欢迎使用！** 🎬
