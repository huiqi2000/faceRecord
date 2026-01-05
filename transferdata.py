import json
import psycopg2
from datetime import datetime

def migrate_time_data_to_postgres(json_file_path, db_config):
    """
    将 time.json 中的打卡数据迁移到 PostgreSQL 数据库
    
    Args:
        json_file_path: JSON 文件路径
        db_config: 数据库配置字典，包含 host, port, database, user, password
    """
    
    # 连接数据库
    conn = psycopg2.connect(
        host=db_config['host'],
        port=db_config['port'],
        database=db_config['database'],
        user=db_config['user'],
        password=db_config['password']
    )
    
    cursor = conn.cursor()
    
    try:
        # 读取 JSON 文件
        with open(json_file_path, 'r', encoding='utf-8') as file:
            time_data = json.load(file)
        
        # 准备 SQL 插入语句
        insert_sql = """
        INSERT INTO clock_record (record_day, record_time, record_type)
        VALUES (%s, %s, %s)
        """
        
        # 遍历 JSON 数据
        for record_day, records in time_data.items():
            for record in records:
                if len(record) >= 2:
                    record_type = record[0]  # "上班" 或 "下班"
                    record_time_str = record[1]  # 时间字符串
                    
                    # 将时间字符串转换为 datetime 对象
                    record_time = datetime.strptime(record_time_str, '%Y-%m-%d %H:%M:%S')
                    
                    # 执行插入
                    cursor.execute(insert_sql, (record_day, record_time, record_type))
        
        # 提交事务
        conn.commit()
        print(f"成功迁移 {cursor.rowcount} 条记录到数据库")
        
    except Exception as e:
        # 回滚事务
        conn.rollback()
        print(f"迁移过程中发生错误: {e}")
        raise
    
    finally:
        # 关闭连接
        cursor.close()
        conn.close()

# 使用示例
if __name__ == "__main__":
    # 数据库配置
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'postgres',
        'user': 'root',
        'password': 'root@202601'
    }
    
    # 执行迁移
    migrate_time_data_to_postgres('time.json', db_config)