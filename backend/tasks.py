from . import db
from .models import FbSport,Animation,FbResult,Hub88
from datetime import datetime
from .spiders.my_spider import fetch_data,getStatscore_id,fetch_hub88,fetch_basic_data,get_sports,get_token
import logging
import time
from sqlalchemy import and_
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

def update_streams(data):
    """更新直播流数据
    
    参数:
        data: 从爬虫获取的数据列表
    """
    if data:
        logger.info(f"Updating streams with {len(data)} items")
        # 获取数据库中已有的直播流记录，以(id, lang)为键，存储在字典中
        existing_streams = {(stream.id): stream for stream in FbSport.query.filter(
            and_(
                FbSport.id.in_([item['id'] for item in data])
            )
        ).all()}
        
        # 用于存储新的直播流记录
        new_streams = []
        
        for item in data:
            key = (item['id'])
            if key in existing_streams:
                # 如果数据库中已有该(id, lang)的记录，则更新该记录
                stream = existing_streams[key]
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
                # stream.mg = item.get('mg', stream.mg)
                stream.ms = item.get('ms', stream.ms)
                stream.ne = item.get('ne', stream.ne)
                stream.nsg = item.get('nsg', stream.nsg)
                stream.pl = item.get('pl', stream.pl)
                stream.sb = item.get('sb', stream.sb)
                stream.sid = item.get('sid', stream.sid)
                stream.tms = item.get('tms', stream.tms)
                stream.tps = item.get('tps', stream.tps)
                stream.ts = item.get('ts', stream.ts)
                stream.ty = item.get('ty', stream.ty)
                stream.vs = item.get('vs', stream.vs)
                # logger.info(f"Updated stream with id {item['id']} and lang {item['lang']}")
            else:
                # 如果数据库中没有该(id, lang)的记录，则创建新记录
                new_stream = FbSport(
                    id=item['id'],
                    # lang=item['lang'],
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
                    # mg=item.get('mg', ''),
                    ms=item.get('ms', ''),
                    ne=item.get('ne', ''),
                    nsg=item.get('nsg', ''),
                    pl=item.get('pl', ''),
                    sb=item.get('sb', ''),
                    sid=item.get('sid', ''),
                    tms=item.get('tms', ''),
                    tps=item.get('tps', ''),
                    ts=item.get('ts', ''),
                    ty=item.get('ty', ''),
                    vs=item.get('vs', '')
                )
                new_streams.append(new_stream)
                # logger.info(f"Created new stream with id {item['id']} and lang {item['lang']}")
        
        # 批量插入新记录
        if new_streams:
            db.session.bulk_save_objects(new_streams)
            # logger.info(f"Inserted {len(new_streams)} new streams")
        
        # 提交所有更改到数据库
        db.session.commit()
        logger.info("Committed all changes to the database")


def update_result_streams(data):
    """更新直播流数据
    
    参数:
        data: 从爬虫获取的数据列表
    """
    if data:
        logger.info(f"Updating result with {len(data)} items")
        # 获取数据库中已有的直播流记录，以(id, lang)为键，存储在字典中
        existing_streams = {(stream.id): stream for stream in FbResult.query.filter(
            and_(
                FbResult.id.in_([item['id'] for item in data])
            )
        ).all()}
        
        # 用于存储新的直播流记录
        new_streams = []
        
        for item in data:
            key = (item['id'])
            if key in existing_streams:
                # 如果数据库中已有该(id, lang)的记录，则更新该记录
                stream = existing_streams[key]
                stream.created_at = item.get('created_at', stream.created_at)
                stream.updated_at = datetime.utcnow()
                stream.ms = item.get('ms', stream.ms)
                stream.nsg = item.get('nsg', stream.nsg)
                stream.sid = item.get('sid', stream.sid)
                # logger.info(f"Updated stream with id {item['id']} and lang {item['lang']}")
            else:
                # 如果数据库中没有该(id, lang)的记录，则创建新记录
                new_stream = FbResult(
                    id=item['id'],
                    # lang=item['lang'],
                    created_at=item.get('created_at', datetime.utcnow()),
                    updated_at=datetime.utcnow(),
                    ms=item.get('ms', ''),
                    nsg=item.get('nsg', ''),
                    sid=item.get('sid', None)
                )
                new_streams.append(new_stream)
                # logger.info(f"Created new stream with id {item['id']} and lang {item['lang']}")
        
        # 批量插入新记录
        if new_streams:
            db.session.bulk_save_objects(new_streams)
            # logger.info(f"Inserted {len(new_streams)} new streams")
        
        # 提交所有更改到数据库
        db.session.commit()
        logger.info("Committed all changes to the database")        

lang_dict = {
    "BRA": "pt-BR",
    "CMN": "zh-CN",
    "DEU": "de",
    "ENG": "en",
    "FRA": "fr",
    "HIN": "hi",
    "IND": "id",
    "JPN": "ja",
    "KOR": "ko",
    "MSA": "ms",
    "RUS": "ru",
    "SAU": "ar",
    "SPA": "es",
    "THA": "th",
    "TR": "tr",
    "VIE": "vi",
    "ZHO": "zh"
}


def update_live_streams():
    """后台任务：定期更新直播流状态（live）
    
    运行间隔：每60秒执行一次
    """
    while True:
        try:
            # 调用爬虫程序获取数据
            data = fetch_data('滚球',"ENG","en")
            update_streams(data)
        except Exception as e:
            logger.error(f"Error updating live stream status: {e}")
        time.sleep(1)

def update_finish_streams():
    """后台任务：定期更新直播流状态（live）
    
    运行间隔：每60秒执行一次
    """
    while True:
        try:
            # 调用爬虫程序获取数据
            data = fetch_data('结束',"ENG","en")
            update_result_streams(data)
        except Exception as e:
            logger.error(f"Error updating result stream status: {e}")
        time.sleep(60)

def update_upcoming_streams():
    """后台任务：定期更新即将到来的直播流状态（upcoming）
    
    运行间隔：每3600秒（1小时）执行一次
    """
    while True:
        try:
            # 调用爬虫程序获取数据
            data = fetch_data('今日',"ENG","en")
            update_streams(data)
        except Exception as e:
            logger.error(f"Error updating upcoming stream status: {e}")
        time.sleep(120)

def update_prematch_streams():
    """后台任务：定期更新预赛直播流状态（prematch）
    
    运行间隔：每天执行一次
    """
    while True:
        try:
            # 调用爬虫程序获取数据
            data = fetch_data('早盘',"ENG","en")
            update_streams(data)
        except Exception as e:
            logger.error(f"Error updating prematch stream status: {e}")
        time.sleep(1200)

def update_animation():
    """后台任务：定期更新预赛直播流状态（prematch）
    
    运行间隔：每天执行一次
    """
    while True:
        try:
            # 调用爬虫程序获取数据
            data = getAnimations()
            update_statscore_id(data)
        except Exception as e:
            logger.error(f"Error updating statscore_id: {e}")
        time.sleep(60)


def getAnimations():
    """获取animation1有值且不为空字符串，同时statscore_id不为null的行"""
    db.session.commit()
    query = db.session.query(Animation.id, Animation.animation1).filter(
        and_(
            Animation.animation1.isnot(None),
            Animation.animation1 != '',
            Animation.statscore_id.is_(None)
        )
    )

    # query = query.limit(10)

    animations = query.all()
    logger.info(f"Found {len(animations)} animations with non-empty animation1 and null statscore_id.")
    if not animations:
        logger.info("No animations found with non-empty animation1 and non-null statscore_id.")
        return []
    statscore_id_list = []

    for animation in animations:
        id_as = {}
        id_as['id'] = animation.id
        id_as['statscore_id'] = getStatscore_id(animation.id,animation.animation1)
        statscore_id_list.append(id_as)
        # time.sleep(1)

    return statscore_id_list

def update_statscore_id(data):
    """更新直播流数据
    
    参数:
        data: 从爬虫获取的数据列表
    """
    if data:
        logger.info(f"Updating streams with {len(data)} items")
        # 获取数据库中已有的直播流记录，以(id, lang)为键，存储在字典中
        existing_streams = {(stream.id): stream for stream in Animation.query.filter(
            and_(
                Animation.id.in_([item['id'] for item in data])
            )
        ).all()}
        
        # 用于存储新的直播流记录
        new_streams = []
        
        for item in data:
            key = (item['id'])
            if key in existing_streams:
                # 如果数据库中已有该(id, lang)的记录，则更新该记录
                stream = existing_streams[key]
                stream.statscore_id = item.get('statscore_id', stream.statscore_id)
                logger.info(f"Updated id with id {item['id']} and statscore_id {item['statscore_id']}")
            else:
                # 如果数据库中没有该(id, lang)的记录，则创建新记录
                new_stream = Animation(
                    id=item['id'],
                    statscore_id=item['statscore_id']
                )
                new_streams.append(new_stream)
                logger.info(f"Created new id with id {item['id']} and statscore_id {item['statscore_id']}")
        
        # 批量插入新记录
        if new_streams:
            db.session.bulk_save_objects(new_streams)
            logger.info(f"Inserted {len(new_streams)} statscore_id")
        
        # 提交所有更改到数据库
        db.session.commit()
        logger.info("Committed all changes to the database")
        # update_hub88_event()
    

def update_hub88_event():
    """后台任务：定期更新预赛直播流状态（hub88event）
    
    运行间隔：每天执行一次
    """
    logger.info("Starting hub88 event update thread")
    existing_streams = [stream.eventId for stream in Hub88.query.all()]
    # print(existing_streams)
    # if not existing_streams:
    #     logger.info("No animations found with non-empty animation1 and non-null statscore_id.")
    #     return
# fetch_hub88(existing_streams,sportId,date,token):
    # while not existing_streams:
    try:
        token = get_token()
        # sportdata = get_sports(token)
        # blacklist = [457,458,459,820,358,26,787,1216,853]
        # sportIds = [i.get('id') for i in sportdata if i.get('id') not in blacklist]
        sportIds = [1,8,2,4,27,11,53,14,17,25]
        today = datetime.today()
        future_dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
        # 调用爬虫程序获取数据
        # logger.info(f"开始抓取hub88:{len(existing_streams)},{existing_streams}")
        for sportId in sportIds:
            for date in future_dates:
                data = fetch_hub88(existing_streams,sportId,date,token)
                update_hub88(data)
    except Exception as e:
        logger.error(f"Error updating statscore_id: {e}")
    time.sleep(60)
    return

def update_hub88(data):
    """更新直播流数据
    
    参数:
        data: 从爬虫获取的数据列表
    """
    if data:
        logger.info(f"Updating streams with {len(data)} items")
        # 获取数据库中已有的直播流记录，以(id, lang)为键，存储在字典中
        existing_streams = {(stream.eventId): stream for stream in Hub88.query.all()}
        
        # 用于存储新的直播流记录
        new_streams = []
        
        for item in data:
            key = (item['eventId'])
            if key in existing_streams:
                # 如果数据库中已有该(id, lang)的记录，则更新该记录
                stream = existing_streams[key]
                stream.statscore_id = item.get('statscore_id', stream.statscore_id)
                logger.info(f"Updated id with statscore_id {item['statscore_id']} and eventId {item['eventId']}")
            else:
                # 如果数据库中没有该(id, lang)的记录，则创建新记录
                new_stream = Hub88(
                    statscore_id=item['statscore_id'],
                    eventId=item['eventId']
                )
                new_streams.append(new_stream)
                logger.info(f"Created new id with statscore_id {item['statscore_id']} and eventId {item['eventId']}")
        
        # 批量插入新记录
        if new_streams:
            db.session.bulk_save_objects(new_streams)
            logger.info(f"Inserted {len(new_streams)} statscore_id")
        
        # 提交所有更改到数据库
        db.session.commit()
        logger.info("Committed all changes to the database")
