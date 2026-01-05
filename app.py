from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import datetime

# 初始化 Flask 应用
app = Flask(__name__)
CORS(app)  # 允许所有跨域请求，生产环境可指定前端地址

# PostgreSQL 连接配置（根据你的实际配置修改）
PG_CONFIG = {
    "user": "root",
    "password": "root@202601",
    "host": "localhost",
    "port": "5432",
    "database": "postgres"  # 替换为你的数据库名
}

# 获取 PostgreSQL 连接
def get_db_connection():
    conn = psycopg2.connect(**PG_CONFIG)
    conn.autocommit = True  # 自动提交事务
    return conn

# 接口1：新增打卡记录
@app.route('/api/clock/add', methods=['POST'])
def add_clock_record():
    try:
        print(1)
        # 获取前端传递的参数
        data = request.get_json()
        record_day = data.get('record_day')  # 日期：YYYY-MM-DD
        record_time = data.get('record_time')  # 时间：HH:MM:SS
        record_type = data.get('record_type')  # 上班/下班
        print(2)
        # 校验参数
        if not all([record_day, record_time, record_type]):
            return jsonify({"code": 400, "msg": "参数不完整"}), 400

        # 连接数据库并插入数据
        conn = get_db_connection()
        print(3)
        cur = conn.cursor()
        sql = """
            INSERT INTO clock_record (record_day, record_time, record_type)
            VALUES (%s, %s, %s)
        """
        cur.execute(sql, (record_day, record_time, record_type))
        cur.close()
        conn.close()

        return jsonify({"code": 200, "msg": "打卡记录添加成功"}), 200
    except Exception as e:
        print(f"错误信息：{e}")
        return jsonify({"code": 500, "msg": f"服务器错误：{str(e)}"}), 500

# 接口2：按日期查询打卡记录
@app.route('/api/clock/query', methods=['GET'])
def query_clock_record():
    try:
        # 获取前端传递的日期参数
        target_day = request.args.get('date')  # YYYY-MM-DD
        if not target_day:
            return jsonify({"code": 400, "msg": "请指定查询日期"}), 400

        # 连接数据库查询
        conn = get_db_connection()
        cur = conn.cursor()
        # 原有SQL查询逻辑不变
        sql = """
            SELECT id, record_day, record_time, record_type
            FROM clock_record
            WHERE record_day = %s
            ORDER BY record_time DESC 
        """
        # print(sql)
        cur.execute(sql, (target_day,))

        # 获取查询结果并转为字典格式（新增类型判断和转换）
        columns = [desc[0] for desc in cur.description]
        records = []
        for row in cur.fetchall():
            row_dict = {}
            for col, val in zip(columns, row):
                # 判断是否为date或time类型，若是则转为字符串
                if isinstance(val, (datetime.date, datetime.time)):
                    row_dict[col] = str(val)
                else:
                    row_dict[col] = val
            records.append(row_dict)

        # print(records)
        cur.close()
        conn.close()

        return jsonify({
            "code": 200,
            "msg": "查询成功",
            "data": records
        }), 200
    except Exception as e:
        print(f"错误信息：{e}")
        return jsonify({"code": 500, "msg": f"服务器错误：{str(e)}"}), 500

# 启动服务
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)