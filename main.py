from pymongo import MongoClient
from urllib.parse import quote_plus
# 方式1：直接传入连接参数
def connect_mongodb():
    # 配置连接信息（对应Docker启动时的账号、密码、主机、端口）
    username = "root"  # 你的MongoDB管理员用户名
    password = "root@202601"  # 你的MongoDB密码（替换为实际密码）
    host = "localhost"  # 本地部署填localhost，远程服务器填服务器IP
    port = 27017  # MongoDB默认端口（已通过Docker映射）

    # 建立连接
    try:
        # 构建连接字符串
        client = MongoClient(
            host=host,
            port=port,
            username=username,
            password=password,
            authSource="admin"  # 认证数据库（Docker初始化时默认在admin库认证）
        )

        # 验证连接是否成功（通过访问数据库列表验证）
        db_list = client.list_database_names()
        print(f"连接成功！当前MongoDB包含的数据库：{db_list}")
        return client
    except Exception as e:
        print(f"连接失败！错误信息：{e}")
        return None

# 方式2：使用MongoDB连接字符串（URI格式，更简洁）
def connect_mongodb_by_uri():
    # URI格式：mongodb://用户名:密码@主机:端口/认证数据库?参数
    mongo_uri = f"mongodb://root:{quote_plus('root@202601')}@localhost:27017/?authSource=admin"
    try:
        client = MongoClient(mongo_uri)
        # 验证连接
        client.admin.command("ping")  # 发送ping命令验证连接可用性
        print("MongoDB连接成功！")
        return client
    except Exception as e:
        print(f"连接失败！错误信息：{e}")
        return None

# 初始化连接
if __name__ == "__main__":
    # 选择一种连接方式即可
    client = connect_mongodb()
    client = connect_mongodb_by_uri()