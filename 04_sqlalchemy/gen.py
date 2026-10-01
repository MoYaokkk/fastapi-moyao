import subprocess
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# from table_2_models import Departments, Employees

# 创建数据库引擎
db_host = "localhost"
db_port = 3306
db_name = "fastapi_db"
db_user_name = "root"
db_password = "123456"
url = f"mysql+pymysql://{db_user_name}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
engine = create_engine(url, echo=True)

# 配置会话工厂
engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 生成模型类
def table_2_model(run=False):
  """将数据库表映射为Python类"""
  if not run:
    return
  output_path = "table_2_models.py"

  venv_python = sys.executable # 若PyCharm使用虚拟环境，这里会返回.venv下的python.exe
  print("当前使用的Python路径：", venv_python) # 确认输出是.venv/Scripts/python.exe

  cmd = [venv_python, "-m", "sqlacodegen", url]
  result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

  # 打印执行结果（定位问题核心）
  print("=== 命令执行结果 ===")
  print(f"返回码（0=成功，非0=失败）：{result.returncode}")
  print(f"标准输出：\n{result.stdout}")
  print(f"错误输出：\n{result.stderr}") # 重点看这里，会显示失败原因

  with open(output_path, "w", encoding="utf-8") as f:
    f.write(result.stdout)

# 向员工和部门表中插入数据
def insert_dept_emp():
  # 1. 创建员工对象（用关键字参数，日期转换为date类型）
  emp = Employees(
    id=100, # 显式指定参数名
    name='zs',
    age=20,
    # hire_date=date(2025, 10, 10) # 字符串转date对象
    hire_date='2025-10-10' # 字符串转date对象
  )

  # 2. 创建部门对象（关键字参数，日期转换为datetime类型）
  dept = Departments(
    id=10,
    name='研发部',
    location='北京',
    created_at='2025-10-10', # 字符串转datetime对象
    employees=[emp] # 关联员工
  )

  # 3. 插入数据库
  with Session(engine) as session:
    session.add(dept)
    try:
      session.commit()
      print(f"插入成功！部门ID：{dept.id}，员工ID：{emp.id}")
    except Exception as e:
      session.rollback()
      print(f"插入失败：{e}")

if __name__ == "__main__":
  table_2_model(True)
  # insert_dept_emp()
