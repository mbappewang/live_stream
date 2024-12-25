import os

class Config:
    # 应用密钥，用于会话加密等安全功能
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    # 关闭SQLAlchemy的跟踪修改功能，提升性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def init_app(app):
        # 用于初始化应用的配置
        pass

class DevelopmentConfig(Config):
    # 开发环境配置
    DEBUG = True  # 启用调试模式
    # 开发环境数据库URI，连接到MySQL数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://fb_data:nLXirkxf6KPwLf5G@192.168.1.9/fb_data'

class ProductionConfig(Config):
    # 生产环境配置
    # 生产环境数据库URI，连接到MySQL数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://fb_data:nLXirkxf6KPwLf5G@192.168.1.9/fb_data'

# 配置字典，用于根据环境选择不同的配置
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
