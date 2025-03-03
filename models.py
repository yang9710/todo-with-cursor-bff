# 数据模型模块
# 定义Todo项目的数据模型和数据库操作

import logging
from database import get_db_connection

# 配置日志
logger = logging.getLogger(__name__)

class TodoItem:
    """Todo项目的数据模型类"""

    @staticmethod
    async def get_all():
        """
        获取所有待办事项

        Returns:
            list: 包含所有待办事项的列表
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM todo_items ORDER BY created_at DESC")
                items = cursor.fetchall()
                return items
        except Exception as e:
            logger.error(f"获取待办事项失败: {e}")
            raise
        finally:
            conn.close()

    @staticmethod
    async def add(value, is_completed=False):
        """
        添加新的待办事项

        Args:
            value (str): 待办事项内容
            is_completed (bool, optional): 完成状态. 默认为 False.

        Returns:
            dict: 新添加的待办事项
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO todo_items (value, isCompleted) VALUES (%s, %s)"
                cursor.execute(sql, (value, is_completed))
                todo_id = cursor.lastrowid
            conn.commit()

            # 获取新添加的待办事项
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM todo_items WHERE id = %s", (todo_id,))
                new_todo = cursor.fetchone()
                return new_todo
        except Exception as e:
            conn.rollback()
            logger.error(f"添加待办事项失败: {e}")
            raise
        finally:
            conn.close()

    @staticmethod
    async def update_status(todo_id):
        """
        更新待办事项的完成状态

        Args:
            todo_id (int): 待办事项ID

        Returns:
            dict: 更新后的待办事项
        """
        conn = get_db_connection()
        try:
            # 先获取当前状态
            with conn.cursor() as cursor:
                cursor.execute("SELECT isCompleted FROM todo_items WHERE id = %s", (todo_id,))
                result = cursor.fetchone()
                if not result:
                    raise ValueError(f"ID为{todo_id}的待办事项不存在")

                current_status = result['isCompleted']
                new_status = not current_status

                # 更新状态
                sql = "UPDATE todo_items SET isCompleted = %s WHERE id = %s"
                cursor.execute(sql, (new_status, todo_id))
            conn.commit()

            # 获取更新后的待办事项
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM todo_items WHERE id = %s", (todo_id,))
                updated_todo = cursor.fetchone()
                return updated_todo
        except Exception as e:
            conn.rollback()
            logger.error(f"更新待办事项状态失败: {e}")
            raise
        finally:
            conn.close()

    @staticmethod
    async def delete(todo_id):
        """
        删除待办事项

        Args:
            todo_id (int): 待办事项ID

        Returns:
            bool: 删除是否成功
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # 检查待办事项是否存在
                cursor.execute("SELECT id FROM todo_items WHERE id = %s", (todo_id,))
                if not cursor.fetchone():
                    raise ValueError(f"ID为{todo_id}的待办事项不存在")

                # 删除待办事项
                sql = "DELETE FROM todo_items WHERE id = %s"
                cursor.execute(sql, (todo_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"删除待办事项失败: {e}")
            raise
        finally:
            conn.close()