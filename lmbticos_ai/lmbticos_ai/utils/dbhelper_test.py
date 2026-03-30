"""
PostgreSQLHelper测试文件
展示如何使用dbhelper类的各种方法
"""

from .dbhelper import PostgreSQLHelper, db_helper


def test_dbhelper():
    """
    测试dbhelper的各种方法
    """
    print("=== PostgreSQLHelper测试 ===")
    
    # 1. 测试基本查询
    print("\n1. 测试基本查询:")
    # 注意：需要替换为实际存在的表名
    # result = db_helper.execute_query("SELECT * FROM your_table_name LIMIT 5")
    # print(f"查询结果: {result}")
    
    # 2. 测试参数化查询
    print("\n2. 测试参数化查询:")
    # 注意：需要替换为实际存在的表名和字段
    # result = db_helper.execute_query("SELECT * FROM your_table_name WHERE id > %s", (10,))
    # print(f"参数化查询结果: {result}")
    
    # 3. 测试获取单条记录
    print("\n3. 测试获取单条记录:")
    # 注意：需要替换为实际存在的表名和ID
    # result = db_helper.get_by_id("your_table_name", 1)
    # print(f"获取单条记录: {result}")
    
    # 4. 测试构建WHERE子句
    print("\n4. 测试构建WHERE子句:")
    filters = {
        'id': {'gt': 10, 'lt': 20},
        'name': {'like': 'test%'},
        'status': {'in': ['active', 'pending']},
        'deleted_at': {'is_null': True}
    }
    where_clause, params = db_helper.build_where_clause(filters)
    print(f"WHERE子句: {where_clause}")
    print(f"参数: {params}")
    
    # 5. 测试构建ORDER BY子句
    print("\n5. 测试构建ORDER BY子句:")
    order_by = ['+created_at', '-id']
    order_by_clause = db_helper.build_order_by_clause(order_by)
    print(f"ORDER BY子句: {order_by_clause}")
    
    # 6. 测试分页查询
    print("\n6. 测试分页查询:")
    # 注意：需要替换为实际存在的表名
    # pagination_result = db_helper.pagination_query(
    #     "SELECT * FROM your_table_name", 
    #     page=2, 
    #     page_size=5
    # )
    # print(f"分页结果: {pagination_result}")
    
    # 7. 测试获取表结构
    print("\n7. 测试获取表结构:")
    # 注意：需要替换为实际存在的表名
    # columns = db_helper.get_table_columns("your_table_name")
    # print(f"表结构: {columns}")
    
    # 8. 测试事务处理
    print("\n8. 测试事务处理:")
    # 注意：需要替换为实际存在的表名和字段
    # queries = [
    #     ("INSERT INTO your_table_name (name, status) VALUES (%s, %s)", ("test1", "active")),
    #     ("INSERT INTO your_table_name (name, status) VALUES (%s, %s)", ("test2", "pending")),
    #     ("UPDATE your_table_name SET status = %s WHERE name = %s", ("inactive", "test1"))
    # ]
    # result = db_helper.execute_in_transaction(queries)
    # print(f"事务执行结果: {result}")
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    test_dbhelper()
