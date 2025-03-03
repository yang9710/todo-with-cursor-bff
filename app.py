# 主应用入口
# 初始化Flask应用并注册路由

import logging
from flask import Flask
from routes import api
from database import init_db
from flask_cors import CORS

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """
    创建并配置Flask应用

    Returns:
        Flask: 配置好的Flask应用实例
    """
    app = Flask(__name__)
    CORS(app)

    # 从配置文件加载配置
    app.config.from_pyfile('config.py')

    # 注册蓝图
    app.register_blueprint(api)

    # 初始化数据库
    with app.app_context():
        init_db()

    return app

if __name__ == '__main__':
    app = create_app()
    logger.info("Todo List 后端应用启动")
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)