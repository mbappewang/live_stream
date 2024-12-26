from . import db
from .models import FbSport
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
        # 获取数据库中已有的直播流记录，以match_id为键，存储在字典中
        existing_streams = {stream.match_id: stream for stream in FbSport.query.filter(FbSport.match_id.in_([item['match_id'] for item in data])).all()}
        
        # 用于存储新的直播流记录
        new_streams = []
        
        for item in data:
            if item['match_id'] in existing_streams:
                # 如果数据库中已有该match_id的记录，则更新该记录
                stream = existing_streams[item['match_id']]
                stream.match_time = item['match_time']
                stream.match_time_utc = item['match_time_utc']
                stream.regionName = item['regionName']
                stream.regionId = item['regionId']
                stream.regionUrl = item['regionUrl']
                stream.leagueName = item['leagueName']
                stream.leagueId = item['leagueId']
                stream.leagueUrl = item['leagueUrl']
                stream.match_name = item['match_name']
                stream.homeTeam = item['homeTeam']
                stream.homeTeamUrl = item['homeTeamUrl']
                stream.homeTeamId = item['homeTeamId']
                stream.awayTeam = item['awayTeam']
                stream.awayTeamUrl = item['awayTeamUrl']
                stream.awayTeamId = item['awayTeamId']
                stream.animation1 = item.get('animation1', '')
                stream.animation2 = item.get('animation2', '')
                stream.web = item.get('web', '')
                stream.flvHD = item.get('flvHD', '')
                stream.flvSD = item.get('flvSD', '')
                stream.m3u8HD = item.get('m3u8HD', '')
                stream.m3u8SD = item.get('m3u8SD', '')
                stream.status = item.get('status', '')
                stream.statscore_id = item.get('statscore_id', '')
                stream.updated_at = datetime.utcnow()  # 更新最后更新时间
                logger.info(f"Updated stream with match_id {item['match_id']}")
            else:
                # 如果数据库中没有该match_id的记录，则创建新记录
                new_stream = FbSport(
                    match_id=item['match_id'],
                    match_time=item['match_time'],
                    match_time_utc=item['match_time_utc'],
                    regionName=item['regionName'],
                    regionId=item['regionId'],
                    regionUrl=item['regionUrl'],
                    leagueName=item['leagueName'],
                    leagueId=item['leagueId'],
                    leagueUrl=item['leagueUrl'],
                    match_name=item['match_name'],
                    homeTeam=item['homeTeam'],
                    homeTeamUrl=item['homeTeamUrl'],
                    homeTeamId=item['homeTeamId'],
                    awayTeam=item['awayTeam'],
                    awayTeamUrl=item['awayTeamUrl'],
                    awayTeamId=item['awayTeamId'],
                    animation1=item.get('animation1', ''),
                    animation2=item.get('animation2', ''),
                    web=item.get('web', ''),
                    flvHD=item.get('flvHD', ''),
                    flvSD=item.get('flvSD', ''),
                    m3u8HD=item.get('m3u8HD', ''),
                    m3u8SD=item.get('m3u8SD', ''),
                    status = item.get('status', ''),
                    statscore_id=item.get('statscore_id', ''),
                    created_at=datetime.utcnow(),  # 设置创建时间
                    updated_at=datetime.utcnow()   # 设置最后更新时间
                )
                new_streams.append(new_stream)  # 将新记录添加到列表中
                logger.info(f"Created new stream with match_id {item['match_id']}")
        
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
        time.sleep(60)  # 休眠60秒

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
