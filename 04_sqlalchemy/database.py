from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL 连接格式：mysql+pymysql://用户名:密码@主机地址:端口/数据库名
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/fastapi_db"

# 创建引擎(echo=True 会打印执行的 SQL,方便调试),相当于创建Connection连接
engine = create_engine(
  DATABASE_URL,
  echo=True, # 是否启用日志输出 开发环境启用,生产环境关闭
  pool_pre_ping=True # 连接前检查有效性,避免连接失效
)

# 创建会话工厂(绑定引擎),相当于创建的cursor对象,用于执行sql
SessionLocal = sessionmaker(
  autocommit=False, # 关闭自动提交,需手动 commit()
  bind=engine
)