from typing import Optional
import datetime

from sqlalchemy import Date, DateTime, ForeignKeyConstraint, Index, Integer, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Departments(Base):
    __tablename__ = 'departments'
    __table_args__ = (
        Index('name', 'name', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='部门名称')
    location: Mapped[Optional[str]] = mapped_column(String(100), comment='部门位置')
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    employees: Mapped[list['Employees']] = relationship('Employees', back_populates='department')


class Employees(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        ForeignKeyConstraint(['department_id'], ['departments.id'], ondelete='SET NULL', name='employees_ibfk_1'),
        Index('idx_dept', 'department_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment='员工姓名')
    age: Mapped[Optional[int]] = mapped_column(Integer, comment='年龄')
    hire_date: Mapped[Optional[datetime.date]] = mapped_column(Date, comment='入职日期')
    department_id: Mapped[Optional[int]] = mapped_column(Integer, comment='所属部门ID')

    department: Mapped[Optional['Departments']] = relationship('Departments', back_populates='employees')
