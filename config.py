# 配置文件
# 包含数据库连接信息和其他配置参数

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root123',
    'db': 'todo_db',
    'charset': 'utf8mb4'
}

# 应用配置
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key_for_todo_app')