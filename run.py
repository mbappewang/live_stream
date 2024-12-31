import os
from backend import create_app, db
from flask_migrate import Migrate
# from backend.models import FbSport
import threading
from backend.tasks import update_live_streams, update_upcoming_streams, update_prematch_streams, update_animation, update_hub88_event
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量中获取FLASK_CONFIG的值，默认为'default'
config_name = os.getenv('FLASK_CONFIG')

# 创建Flask应用实例
app = create_app(config_name)
# 初始化数据库迁移
migrate = Migrate(app, db)

def run_with_app_context(target):
    with app.app_context():
        target()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 20000))  # 默认端口为20000
    # 创建并启动后台状态更新线程
    def run_with_app_context(target):
        with app.app_context():
            target()

    try:
        live_thread = threading.Thread(target=lambda: run_with_app_context(update_live_streams))
        live_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
        live_thread.start()
        logger.info("Started live stream update thread")

        upcoming_thread = threading.Thread(target=lambda: run_with_app_context(update_upcoming_streams))
        upcoming_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
        upcoming_thread.start()
        logger.info("Started upcoming stream update thread")

        prematch_thread = threading.Thread(target=lambda: run_with_app_context(update_prematch_streams))
        prematch_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
        prematch_thread.start()
        logger.info("Started prematch stream update thread")

        animation_thread = threading.Thread(target=lambda: run_with_app_context(update_animation))
        animation_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
        animation_thread.start()
        logger.info("Started animation update thread")

        # hub88_thread = threading.Thread(target=lambda: run_with_app_context(update_hub88_event))
        # hub88_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
        # hub88_thread.start()
        # logger.info("Started hub88 update thread")
        
        # 启动Flask Web服务器
        app.run(port=port, debug=True, use_reloader=True)
        logger.info("Flask web server started")
    except Exception as e:
        logger.error(f"Error starting threads or web server: {e}")
