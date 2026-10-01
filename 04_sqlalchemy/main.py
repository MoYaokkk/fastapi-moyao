from base import Base
from database import engine,SessionLocal
from models import Employee,Department #必须要加
from datetime import date

# 创建表
def create_table():
  print("注册的表名:", Base.metadata.tables.keys())
  # 创建所有模型对应的表
  Base.metadata.create_all(bind=engine)
  print("表创建成功")




#添加功能
def insert_data():
    # 获取数据库会话
    db = SessionLocal()

    try:
        # =========== 第一步：新增部门 =============
        new_dept = Department(
            name="研发部",  # 部门名称(唯一)
            location="北京总部"  # 部门位置
        )
        db.add(new_dept)  # 将部门对象加入会话
        db.commit()  # 提交到数据库(执行 INSERT 语句)
        db.refresh(new_dept)  # 刷新对象,获取自增的 id 等字段

        # =========== 第二步：新增关联的员工 ===========
        # 员工1：关联上面创建的研发部
        emp1 = Employee(
            name="张三",
            age=30,
            hire_date=date(2023, 1, 1),  # 入职日期(datetime.date 类型)
            department_id=new_dept.id  # 关联部门 ID(外键)
        )
        # 员工2：同部门的另一个员工
        emp2 = Employee(
            name="李四",
            age=28,
            hire_date=date(2023, 3, 15),
            department_id=new_dept.id
        )

        # 批量添加员工(也可逐个 add)
        db.add_all([emp1, emp2])
        db.commit()  # 提交员工数据
        # 刷新员工对象,获取自增 ID
        db.refresh(emp1)
        db.refresh(emp2)

        # ===================== 输出结果 =====================
        print(f"新增部门：ID={new_dept.id},名称={new_dept.name},位置={new_dept.location}")
        print(f"新增员工1：ID={emp1.id},姓名={emp1.name},所属部门={new_dept.name}")
        print(f"新增员工2：ID={emp2.id},姓名={emp2.name},所属部门={new_dept.name}")

        # 验证关联关系(通过 ORM 关联查询)
        print("\n【验证关联关系】")
        # 从员工查部门
        print(f"员工{emp1.name}的部门名称：{emp1.department.name}")
        # 从部门查员工
        dept_employees = new_dept.employees
        print(f"部门{new_dept.name}的员工列表：{[emp.name for emp in dept_employees]}")

    except Exception as e:
        db.rollback()  # 出错时回滚
        print(f"新增失败：{e}")
    finally:
        db.close()  # 关闭会话



def delete_data():
    # 获取会话
    session = SessionLocal()

    try:
        # 删除单个员工
        emp = session.query(Employee).filter(Employee.name == "李四").first()
        if emp:
            session.delete(emp)
            session.commit()
            print(f"已删除员工：{emp.name}")

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"刪除失败：{e}")
    finally:
        session.close()  # 关闭会话



def update_data():
    # 获取会话
    session = SessionLocal()
    try:
        # 修改员工年龄
        emp = session.query(Employee).filter(Employee.name == "张三").first()
        if emp:
            emp.age = 31  # 直接修改属性
            session.commit()  # 提交更新
            print(f"修改后 {emp.name} 的年龄：{emp.age}")

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"修改失败：{e}")
    finally:
        session.close()  # 关闭会话







def find_data():
    # 获取会话
    session = SessionLocal()
    try:
        # ======按主键查询 get========
        #  查询id=1的部门
        dept = session.get(Department, 1)
        print(f"部门 ID=1：{dept.name}({dept.location})")

        # ======过滤(filter)查询========
        # 查询研发部的所有员工
        rd_employees = session.query(Employee).filter(
            Employee.department_id == 1  # 按部门ID过滤
        ).all()
        print("研发部员工：", [emp.name for emp in rd_employees])  # 输出：['张三']

        # 查询年龄>30的员工
        old_employees = session.query(Employee).filter(Employee.age > 30).all()
        print("年龄>30的员工：", [emp.name for emp in old_employees])  # 输出：['张三', '王五']

        # ======逻辑运算(and_/or_)查询========
        from sqlalchemy import and_, or_

        # 年龄30-40且属于研发部的员工(and_)
        emp = session.query(Employee).filter(
            and_(Employee.age.between(30, 40), Employee.department_id == 1)
        ).first()
        print("符合条件的员工：", emp.name)  # 输出：张三

        # 属于市场部或年龄>32的员工(or_)
        emps = session.query(Employee).filter(
            or_(Employee.department_id == 2, Employee.age > 32)
        ).all()
        print("符合条件的员工：", [emp.name for emp in emps])  # 输出：['张三', '王五']

        # ======表连接(join)查询========
        # 内连接：查询员工及其所属部门名称
        # 语法：query(主表, 关联表).join(关联表, 连接条件)
        result = session.query(Employee, Department).join(
            Department, Employee.department_id == Department.id
        ).all()

        for emp, dept in result:
            print(f"员工 {emp.name} 属于 {dept.name}")
        # 输出：
        # 员工 张三 属于 研发部
        # 员工 王五 属于 市场部

        # ======预加载关联数据(joinedload)查询========
        from sqlalchemy.orm import joinedload

        # 加载员工时同时加载部门信息(避免多次查询)
        employees = session.query(Employee).options(
            joinedload(Employee.department)  # 预加载关联的 department
        ).all()

        # 直接访问关联数据,不会触发新查询
        for emp in employees:
            print(f"{emp.name} 的部门：{emp.department.name}")
        # 输出：
        # 张三 的部门：研发部
        # 王五 的部门：市场部

        # ======子查询(subquery)========
        from sqlalchemy import func
        # 子查询：统计每个部门的员工数,再查询员工数>0的部门
        # 步骤1：创建子查询(统计部门员工数)
        dept_emp_count = session.query(
            Employee.department_id,
            func.count(Employee.id).label("count")  # 别名 count
        ).group_by(Employee.department_id).subquery()  # 转为子查询

        # 步骤2：主查询(关联子查询结果)
        depts = session.query(Department).join(
            dept_emp_count, Department.id == dept_emp_count.c.department_id
        ).filter(dept_emp_count.c.count > 0).all()  # 筛选员工数>0的部门

        print("有员工的部门：", [dept.name for dept in depts])  # 输出：['研发部', '市场部']

        # ======去重(distinct)========
        # 查询所有有员工的部门位置(去重)
        locations = session.query(Department.location).join(
            Employee
        ).distinct().all()  # distinct() 去重

        print("部门位置：", [loc[0] for loc in locations])  # 输出：['北京', '广州']

        # ======结果获取(first/all)========
        # first()：返回第一条结果(适合唯一查询)
        first_emp = session.query(Employee).first()
        print("第一个员工：", first_emp.name)  # 输出：张三

        # all()：返回所有结果(列表)
        all_depts = session.query(Department).all()
        print("所有部门：", [dept.name for dept in all_depts])  # 输出：['研发部', '市场部']

    except Exception as e:
        session.rollback()  # 出错时回滚
        print(f"查询失败：{e}")
    finally:
        session.close()  # 关闭会话

if __name__ == '__main__':
  # create_table()
  #   insert_data()
  # delete_data()
  # update_data()
  find_data()