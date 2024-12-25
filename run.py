import os
from backend import create_app, db
from flask_migrate import Migrate
from backend.models import FbSport
import threading
from backend.tasks import update_live_streams, update_upcoming_streams, update_prematch_streams, update_finished_streams

# 创建Flask应用实例
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# 初始化数据库迁移
migrate = Migrate(app, db)

@app.cli.command()
def init_db():
    """命令行命令：初始化数据库
    使用方法: flask init_db
    """
    db.create_all()
    print('Initialized database.')

if __name__ == '__main__':
    # 创建并启动后台状态更新线程
    live_thread = threading.Thread(target=update_live_streams)
    live_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
    live_thread.start()

    upcoming_thread = threading.Thread(target=update_upcoming_streams)
    upcoming_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
    upcoming_thread.start()

    prematch_thread = threading.Thread(target=update_prematch_streams)
    prematch_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
    prematch_thread.start()
    
    finished_thread = threading.Thread(target=update_finished_streams)
    finished_thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
    finished_thread.start()
    
    # 启动Flask Web服务器
    app.run(debug=True)
