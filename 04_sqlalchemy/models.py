from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from base import Base

"""
部门模型(一对多：一个部门包含多个员工)
"""
class Department(Base):
  # 定义表,声明表名
  __tablename__ = "departments"

  #定义表中的列名以及数据类型以及约束
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False, unique=True) # 部门名称
  location = Column(String(100)) # 部门位置(如"北京总部")

  # 一对多关联员工：返回员工列表,显式指定外键(可选,但更清晰)
  employees = relationship(
    "Employee",
    back_populates="department",
    # 可选：级联删除(删除部门时自动删除下属员工,根据业务选择)
    # cascade="all, delete-orphan",
    # 可选：懒加载策略,优化查询性能
    lazy="selectin"
  )

""" 
员工模型(多对一：多个员工属于一个部门)
"""
class Employee(Base):
  # 定义表,声明表名
  __tablename__ = "employees"

  # 定义表中的列名以及数据类型以及约束
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False) # 姓名
  age = Column(Integer) # 年龄
  hire_date = Column(Date) # 入职日期

  #添加外键约束,绑定到departments.id
  department_id = Column(
    Integer,
    ForeignKey("departments.id", ondelete="RESTRICT"), # 禁止删除有员工的部门
    nullable=False # 员工必须归属一个部门(根据业务可改为True,允许无部门)
  )

  # 核心修正：多对一关联,指定uselist=False(返回单个部门对象)
  department = relationship(
    "Department",
    back_populates="employees",
    lazy="joined" # 可选：立即加载部门数据,减少查询次数
  )