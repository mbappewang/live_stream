from . import db
from .models import FbSport, MatchInfo, MarketInfo, MarketType, MatchPeriod, MatchStatus, MarketName, Period, StatsType, SportType, TournamentPhase, Animation, Stream, Region, League, Team
import time
from datetime import datetime
from .spiders.my_spider import fetch_data
import logging

logger = logging.getLogger(__name__)

def update_streams(data):
    """更新直播流数据
    
    参数:
        data: 从爬虫获取的数据列表
    """
    if data:
        logger.info(f"Updating streams with {len(data)} items")
        # 获取数据库中已有的直播流记录，以id为键，存储在字典中
        existing_streams = {stream.id: stream for stream in FbSport.query.filter(FbSport.id.in_([item['id'] for item in data])).all()}
        
        # 用于存储新的直播流记录
        new_streams = []
        
        for item in data:
            if item['id'] in existing_streams:
                # 如果数据库中已有该id的记录，则更新该记录
                stream = existing_streams[item['id']]
                stream.created_at = item.get('created_at', stream.created_at)
                stream.updated_at = datetime.utcnow()
                stream.nm = item.get('nm', stream.nm)
                stream.match_time_unix = item.get('match_time_unix', stream.match_time_unix)
                stream.start_time = item.get('start_time', stream.start_time)
                stream.animation = item.get('animation', stream.animation)
                stream.fid = item.get('fid', stream.fid)
                stream.fmt = item.get('fmt', stream.fmt)
                stream.lg = item.get('lg', stream.lg)
                stream.mc = item.get('mc', stream.mc)
                stream.mg = item.get('mg', stream.mg)
                stream.ms = item.get('ms', stream.ms)
                stream.ne = item.get('ne', stream.ne)
                stream.nsg = item.get('nsg', stream.nsg)
                stream.pl = item.get('pl', stream.pl)
                stream.sb = item.get('sb', stream.sb)
                stream.sid = item.get('sid', stream.sid)
                stream.smt = item.get('smt', stream.smt)
                stream.tms = item.get('tms', stream.tms)
                stream.tps = item.get('tps', stream.tps)
                stream.ts = item.get('ts', stream.ts)
                stream.ty = item.get('ty', stream.ty)
                stream.vs = item.get('vs', stream.vs)
                logger.info(f"Updated stream with id {item['id']}")
            else:
                # 如果数据库中没有该id的记录，则创建新记录
                new_stream = FbSport(
                    id=item['id'],
                    created_at=item.get('created_at', datetime.utcnow()),
                    updated_at=datetime.utcnow(),
                    nm=item.get('nm', ''),
                    match_time_unix=item.get('match_time_unix', ''),
                    start_time=item.get('start_time', ''),
                    animation=item.get('animation', ''),
                    fid=item.get('fid', ''),
                    fmt=item.get('fmt', ''),
                    lg=item.get('lg', ''),
                    mc=item.get('mc', ''),
                    mg=item.get('mg', ''),
                    ms=item.get('ms', ''),
                    ne=item.get('ne', ''),
                    nsg=item.get('nsg', ''),
                    pl=item.get('pl', ''),
                    sb=item.get('sb', ''),
                    sid=item.get('sid', ''),
                    smt=item.get('smt', ''),
                    tms=item.get('tms', ''),
                    tps=item.get('tps', ''),
                    ts=item.get('ts', ''),
                    ty=item.get('ty', ''),
                    vs=item.get('vs', '')
                )
                new_streams.append(new_stream)
                logger.info(f"Created new stream with id {item['id']}")
        
        # 批量插入新记录
        if new_streams:
            db.session.bulk_save_objects(new_streams)
            logger.info(f"Inserted {len(new_streams)} new streams")
        
        # 提交所有更改到数据库
        db.session.commit()
        logger.info("Committed all changes to the database")

def update_live_streams():
    """后台任务：定期更新直播流状态（live）
    
    运行间隔：每60秒执行一次
    """
    while True:
        try:
            # 调用爬虫程序获取数据
            data = fetch_data('滚球')
            update_streams(data)
        except Exception as e:
            logger.error(f"Error updating live stream status: {e}")
        time.sleep(0)  # 休眠60秒

def update_upcoming_streams():
    """后台任务：定期更新即将到来的直播流状态（upcoming）
    
    运行间隔：每3600秒（1小时）执行一次
    """
    while True:
        try:
            # 调用爬虫程序获取数据
            data = fetch_data('今日')
            update_streams(data)
        except Exception as e:
            logger.error(f"Error updating upcoming stream status: {e}")
        time.sleep(3600)  # 休眠3600秒（1小时）

def update_prematch_streams():
    """后台任务：定期更新预赛直播流状态（prematch）
    
    运行间隔：每天执行一次
    """
    while True:
        try:
            # 调用爬虫程序获取数据
            data = fetch_data('早盘')
            update_streams(data)
        except Exception as e:
            logger.error(f"Error updating prematch stream status: {e}")
        time.sleep(86400)  # 休眠86400秒（1天）

# def update_finished_streams():
#     """后台任务：定期更新已结束的比赛状态
#     
#     运行间隔：每天执行一次
#     """
#     while True:
#         try:
#             # 获取当前时间
#             now = datetime.utcnow().timestamp()
#             # 查找所有已结束的比赛（假设比赛结束时间在当前时间之前）
#             finished_streams = FbSport.query.filter(FbSport.match_time < now).all()
#             for stream in finished_streams:
#                 # 更新比赛状态为已结束
#                 stream.status = 'finished'
#                 stream.updated_at = datetime.utcnow()
#             db.session.commit()
#         except Exception as e:
#             logger.error(f"Error updating finished stream status: {e}")
#         time.sleep(86400)  # 休眠86400秒（1天）
