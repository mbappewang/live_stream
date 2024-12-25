from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config
import logging

logger = logging.getLogger(__name__)

# 创建SQLAlchemy实例
db = SQLAlchemy()

def create_app(config_name):
    """工厂函数：创建Flask应用实例
    
    参数:
        config_name: 配置名称，用于选择不同的配置环境
    
    返回:
        配置完成的Flask应用实例
    """
    app = Flask(__name__)
    CORS(app)  # 启用跨域资源共享
    
    # 加载配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    logger.info(f"App created with {config_name} configuration")

    # 初始化扩展
    db.init_app(app)
    logger.info("Database initialized")

    # 注册蓝图
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    logger.info("API blueprint registered")

    return app
