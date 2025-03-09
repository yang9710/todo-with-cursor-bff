# 数据库连接模块
# 负责创建和管理数据库连接

import pymysql
from pymysql.cursors import DictCursor
import logging
from config import DB_CONFIG
import random
from datetime import datetime, timedelta

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

def generate_sample_data():
    """
    生成100条随机的待办事项数据
    """
    # 示例任务前缀列表
    task_prefixes = [
        "完成", "检查", "审核", "更新", "准备", "开发", "测试", "部署",
        "优化", "修复", "设计", "评审", "分析", "整理", "撰写"
    ]

    # 示例任务内容列表
    task_contents = [
        "项目文档", "代码审查", "数据库优化", "性能测试", "用户界面",
        "系统架构", "测试用例", "项目计划", "技术方案", "bug修复",
        "需求分析", "接口文档", "代码重构", "安全检查", "备份方案"
    ]

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 生成100条随机数据
            for i in range(100):
                # 随机生成任务内容
                task = f"{random.choice(task_prefixes)}{random.choice(task_contents)}{i+1}"

                # 随机生成完成状态
                is_completed = random.choice([True, False])

                # 随机生成创建时间（最近30天内）
                random_days = random.randint(0, 30)
                random_hours = random.randint(0, 23)
                random_minutes = random.randint(0, 59)
                created_at = datetime.now() - timedelta(
                    days=random_days,
                    hours=random_hours,
                    minutes=random_minutes
                )

                # 插入数据
                sql = """
                INSERT INTO todo_items (value, isCompleted, created_at)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (task, is_completed, created_at))

            conn.commit()
            logger.info("成功生成100条随机待办事项数据")
    except Exception as e:
        conn.rollback()
        logger.error(f"生成随机数据失败: {e}")
        raise
    finally:
        conn.close()

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

        # 检查是否需要生成示例数据
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM todo_items")
            result = cursor.fetchone()
            if result['count'] == 0:
                # 如果表为空，生成示例数据
                generate_sample_data()

    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise
    finally:
        conn.close()