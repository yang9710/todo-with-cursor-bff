# API路由模块
# 定义所有RESTful API端点

from flask import Blueprint, request, jsonify
import logging
from models import TodoItem

# 创建蓝图
api = Blueprint('api', __name__, url_prefix='/api')

# 配置日志
logger = logging.getLogger(__name__)

@api.route('/get-todo', methods=['GET'])
async def get_all_todos():
    """
    获取所有待办事项的API端点

    Returns:
        JSON: 包含所有待办事项的数组
    """
    try:
        todos = await TodoItem.get_all()
        return jsonify(todos), 200
    except Exception as e:
        logger.error(f"获取待办事项失败: {e}")
        return jsonify({"error": "获取待办事项失败", "message": str(e)}), 500

@api.route('/add-todo', methods=['POST'])
async def add_todo():
    """
    添加新待办事项的API端点

    JSON Body:
        value (str): 待办事项内容
        isCompleted (bool, optional): 完成状态

    Returns:
        JSON: 新添加的待办事项
    """
    try:
        # 增加错误处理，确保能正确解析JSON
        try:
            data = request.get_json(force=True)
        except Exception as e:
            logger.error(f"JSON解析失败: {e}")
            return jsonify({"error": "无效的JSON格式", "message": str(e)}), 400

        # 验证输入
        if not data or 'value' not in data:
            return jsonify({"error": "缺少必要参数"}), 400

        value = data['value']
        is_completed = data.get('isCompleted', False)

        # 添加待办事项
        new_todo = await TodoItem.add(value, is_completed)
        return jsonify(new_todo), 201
    except Exception as e:
        logger.error(f"添加待办事项失败: {e}")
        return jsonify({"error": "添加待办事项失败", "message": str(e)}), 500

@api.route('/update-todo/<int:todo_id>', methods=['POST'])
async def update_todo(todo_id):
    """
    更新待办事项状态的API端点

    Args:
        todo_id (int): 待办事项ID

    Returns:
        JSON: 更新后的待办事项
    """
    try:
        updated_todo = await TodoItem.update_status(todo_id)
        return jsonify(updated_todo), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"更新待办事项失败: {e}")
        return jsonify({"error": "更新待办事项失败", "message": str(e)}), 500

@api.route('/del-todo/<int:todo_id>', methods=['POST'])
async def delete_todo(todo_id):
    """
    删除待办事项的API端点

    Args:
        todo_id (int): 待办事项ID

    Returns:
        JSON: 删除操作结果
    """
    try:
        await TodoItem.delete(todo_id)
        return jsonify({"success": True, "message": f"ID为{todo_id}的待办事项已删除"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        logger.error(f"删除待办事项失败: {e}")
        return jsonify({"error": "删除待办事项失败", "message": str(e)}), 500