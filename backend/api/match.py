from flask import jsonify, request, send_from_directory
from . import api  # 确保 api 蓝图已正确注册
from ..models import FbSport, MatchInfo, Animation,Hub88,Stream
from .. import db
from datetime import datetime
import logging
from sqlalchemy import func
import os

logger = logging.getLogger(__name__)

@api.route('matchlist', methods=['GET'])
def get_home():
    """获取首页数据"""
    logger.info("Fetching home data")
    
    # 执行查询
    sports = db.session.query(FbSport).join(
            MatchInfo, MatchInfo.id == FbSport.id
        ).filter(
            MatchInfo.status_id.in_([4, 5]),
            MatchInfo.match_time_unix.isnot(None),
            MatchInfo.match_time_unix <= datetime.now().timestamp() + 86400
        ).order_by(
            MatchInfo.match_time_unix.asc()
        ).limit(500)

    # 构建返回结果
    result = []
    for sport in sports:
        result.append(sport.to_json())

    return jsonify(result)

@api.route('/matchdetail', methods=['GET'])
def get_match_detail():
    """获取比赛详情"""
    match_id = request.args.get('match_id')
    logger.info(f"Fetching match detail for match_id {match_id}")
    
    # 执行查询
    match = db.session.query(FbSport).filter_by(id=match_id).first()

    # 构建返回结果
    result = match.to_json()
    return jsonify(result)

@api.route('/fb_hub88', methods=['GET'])
def get_fb_hub88():
    logger.info("Fetching animation and hub88 data")
    
    # 执行查询
    results = db.session.query(Animation.id, Hub88.eventId
                               ).join(Hub88, Hub88.statscore_id == Animation.statscore_id
                                      ).filter(
        Animation.match_time_unix > datetime.now().timestamp(),
                                      ).all()

    # 构建返回结果
    result_list = []
    for result in results:
        id = str(result.id)
        eventId = str(result.eventId)
        result_list.append(f"{id}*{eventId}")
    result_dict = {'count': len(result_list),'data': result_list}
    return jsonify(result_dict)


@api.route('/hello', methods=['GET'])
def hello_world():
    """返回Hello World"""
    return jsonify(message="Hello, World!")