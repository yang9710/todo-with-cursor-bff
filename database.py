# 数据库连接模块
# 负责创建和管理数据库连接

import pymysql
from pymysql.cursors import DictCursor
import logging
from config import DB_CONFIG

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_db_connection():
    """
    创建并返回数据库连接

    Returns:
        connection: 数据库连接对象
    """
    try:
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            db=DB_CONFIG['db'],
            charset=DB_CONFIG['charset'],
            cursorclass=DictCursor
        )
        return connection
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        raise

def init_db():
    """
    初始化数据库，创建必要的表
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 创建todo_items表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS todo_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                value VARCHAR(255) NOT NULL,
                isCompleted BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
        conn.commit()
        logger.info("数据库初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise
    finally:
        conn.close()