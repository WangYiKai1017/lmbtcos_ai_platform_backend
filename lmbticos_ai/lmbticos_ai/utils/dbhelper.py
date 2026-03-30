from django.db import connection, transaction
from django.db.utils import OperationalError
import json


class PostgreSQLHelper:
    """
    PostgreSQL数据库操作辅助类，提供常用的CRUD操作方法
    """
    
    @staticmethod
    def execute_query(query, params=None, fetchall=True):
        """
        执行查询语句
        :param query: SQL查询语句
        :param params: 查询参数（可选）
        :param fetchall: 是否返回所有结果，True返回所有，False返回第一条
        :return: 查询结果
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                if fetchall:
                    return cursor.fetchall()
                else:
                    return cursor.fetchone()
        except OperationalError as e:
            print(f"数据库查询错误: {e}")
            return None
        except Exception as e:
            print(f"执行查询时发生错误: {e}")
            return None
    
    @staticmethod
    def execute_update(query, params=None):
        """
        执行更新语句（INSERT、UPDATE、DELETE）
        :param query: SQL更新语句
        :param params: 查询参数（可选）
        :return: 受影响的行数
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount
        except OperationalError as e:
            print(f"数据库更新错误: {e}")
            return 0
        except Exception as e:
            print(f"执行更新时发生错误: {e}")
            return 0
    
    @staticmethod
    def bulk_insert(table_name, columns, values):
        """
        批量插入数据
        :param table_name: 表名
        :param columns: 列名列表
        :param values: 值列表，格式为[(val1, val2, ...), (val1, val2, ...)]
        :return: 受影响的行数
        """
        try:
            if not values:
                return 0
                
            # 构建插入语句
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            
            with connection.cursor() as cursor:
                cursor.executemany(query, values)
                return cursor.rowcount
        except OperationalError as e:
            print(f"批量插入错误: {e}")
            return 0
        except Exception as e:
            print(f"执行批量插入时发生错误: {e}")
            return 0
    
    @staticmethod
    @transaction.atomic
    def execute_in_transaction(queries):
        """
        在事务中执行多个SQL语句
        :param queries: SQL语句列表，格式为[(query1, params1), (query2, params2), ...]
        :return: 所有语句执行成功返回True，否则返回False
        """
        try:
            with connection.cursor() as cursor:
                for query, params in queries:
                    cursor.execute(query, params)
            return True
        except OperationalError as e:
            print(f"事务执行错误: {e}")
            return False
        except Exception as e:
            print(f"执行事务时发生错误: {e}")
            return False
    
    @staticmethod
    def get_by_id(table_name, id_value, id_column='id'):
        """
        根据ID获取记录
        :param table_name: 表名
        :param id_value: ID值
        :param id_column: ID列名（默认id）
        :return: 记录字典或None
        """
        try:
            query = f"SELECT * FROM {table_name} WHERE {id_column} = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (id_value,))
                result = cursor.fetchone()
                if result:
                    # 获取列名
                    columns = [desc[0] for desc in cursor.description]
                    # 转换为字典
                    return dict(zip(columns, result))
                return None
        except OperationalError as e:
            print(f"根据ID查询错误: {e}")
            return None
        except Exception as e:
            print(f"执行ID查询时发生错误: {e}")
            return None
    
    @staticmethod
    def update_by_id(table_name, id_value, data, id_column='id'):
        """
        根据ID更新记录
        :param table_name: 表名
        :param id_value: ID值
        :param data: 要更新的数据字典
        :param id_column: ID列名（默认id）
        :return: 受影响的行数
        """
        try:
            # 构建更新语句
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            values = list(data.values()) + [id_value]
            query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = %s"
            
            with connection.cursor() as cursor:
                cursor.execute(query, values)
                return cursor.rowcount
        except OperationalError as e:
            print(f"更新记录错误: {e}")
            return 0
        except Exception as e:
            print(f"执行记录更新时发生错误: {e}")
            return 0
    
    @staticmethod
    def delete_by_id(table_name, id_value, id_column='id'):
        """
        根据ID删除记录
        :param table_name: 表名
        :param id_value: ID值
        :param id_column: ID列名（默认id）
        :return: 受影响的行数
        """
        try:
            query = f"DELETE FROM {table_name} WHERE {id_column} = %s"
            with connection.cursor() as cursor:
                cursor.execute(query, (id_value,))
                return cursor.rowcount
        except OperationalError as e:
            print(f"删除记录错误: {e}")
            return 0
        except Exception as e:
            print(f"执行记录删除时发生错误: {e}")
            return 0
    
    @staticmethod
    def pagination_query(query, params=None, page=1, page_size=10):
        """
        分页查询
        :param query: SQL查询语句
        :param params: 查询参数（可选）
        :param page: 当前页码（默认1）
        :param page_size: 每页记录数（默认10）
        :return: 分页结果，包含total、page、page_size和items
        """
        try:
            # 计算偏移量
            offset = (page - 1) * page_size
            
            # 获取总记录数
            count_query = f"SELECT COUNT(*) FROM ({query}) AS count_table"
            total = PostgreSQLHelper.execute_query(count_query, params, fetchall=False)[0]
            
            # 获取分页数据
            paginated_query = f"{query} LIMIT %s OFFSET %s"
            paginated_params = (params or []) + [page_size, offset]
            items = PostgreSQLHelper.execute_query(paginated_query, paginated_params)
            
            return {
                'total': total,
                'page': page,
                'page_size': page_size,
                'items': items
            }
        except OperationalError as e:
            print(f"分页查询错误: {e}")
            return {'total': 0, 'page': page, 'page_size': page_size, 'items': []}
        except Exception as e:
            print(f"执行分页查询时发生错误: {e}")
            return {'total': 0, 'page': page, 'page_size': page_size, 'items': []}
    
    @staticmethod
    def build_where_clause(filters):
        """
        构建WHERE子句
        :param filters: 过滤条件字典
        :return: WHERE子句字符串和参数列表
        """
        if not filters:
            return '', []
            
        conditions = []
        params = []
        
        for key, value in filters.items():
            if isinstance(value, dict):
                # 支持操作符，如{'gt': 10, 'lt': 20}
                for op, val in value.items():
                    if op == 'eq':
                        conditions.append(f"{key} = %s")
                    elif op == 'neq':
                        conditions.append(f"{key} != %s")
                    elif op == 'gt':
                        conditions.append(f"{key} > %s")
                    elif op == 'gte':
                        conditions.append(f"{key} >= %s")
                    elif op == 'lt':
                        conditions.append(f"{key} < %s")
                    elif op == 'lte':
                        conditions.append(f"{key} <= %s")
                    elif op == 'in':
                        placeholders = ', '.join(['%s'] * len(val))
                        conditions.append(f"{key} IN ({placeholders})")
                        params.extend(val)
                        continue
                    elif op == 'nin':
                        placeholders = ', '.join(['%s'] * len(val))
                        conditions.append(f"{key} NOT IN ({placeholders})")
                        params.extend(val)
                        continue
                    elif op == 'like':
                        conditions.append(f"{key} LIKE %s")
                    elif op == 'not_like':
                        conditions.append(f"{key} NOT LIKE %s")
                    elif op == 'is_null':
                        conditions.append(f"{key} IS NULL")
                        continue
                    elif op == 'is_not_null':
                        conditions.append(f"{key} IS NOT NULL")
                        continue
                    params.append(val)
            else:
                # 默认等于操作
                conditions.append(f"{key} = %s")
                params.append(value)
        
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
        return where_clause, params
    
    @staticmethod
    def build_order_by_clause(order_by):
        """
        构建ORDER BY子句
        :param order_by: 排序字段列表，格式为['+field1', '-field2']
        :return: ORDER BY子句字符串
        """
        if not order_by:
            return ''
            
        order_conditions = []
        for field in order_by:
            if field.startswith('+'):
                order_conditions.append(f"{field[1:]} ASC")
            elif field.startswith('-'):
                order_conditions.append(f"{field[1:]} DESC")
            else:
                order_conditions.append(f"{field} ASC")
        
        order_by_clause = "ORDER BY " + ", ".join(order_conditions)
        return order_by_clause
    
    @staticmethod
    def execute_raw_sql(sql, params=None):
        """
        执行原始SQL语句
        :param sql: SQL语句
        :param params: 查询参数（可选）
        :return: 执行结果，查询语句返回结果集，更新语句返回受影响行数
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                if sql.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                else:
                    return cursor.rowcount
        except OperationalError as e:
            print(f"执行SQL错误: {e}")
            return None if sql.strip().upper().startswith('SELECT') else 0
        except Exception as e:
            print(f"执行SQL时发生错误: {e}")
            return None if sql.strip().upper().startswith('SELECT') else 0
    
    @staticmethod
    def get_table_columns(table_name):
        """
        获取表的列信息
        :param table_name: 表名
        :return: 列信息列表
        """
        try:
            query = """
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """
            return PostgreSQLHelper.execute_query(query, (table_name,))
        except OperationalError as e:
            print(f"获取表结构错误: {e}")
            return []
        except Exception as e:
            print(f"获取表结构时发生错误: {e}")
            return []
    
    @staticmethod
    def to_dict_list(results, columns=None):
        """
        将查询结果转换为字典列表
        :param results: 查询结果
        :param columns: 列名列表（可选）
        :return: 字典列表
        """
        if not results:
            return []
            
        if columns:
            return [dict(zip(columns, row)) for row in results]
        else:
            return [dict(row) for row in results]


# 实例化一个全局DBHelper对象，方便使用
db_helper = PostgreSQLHelper()
