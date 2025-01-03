from flask import jsonify, request
from . import api  # 确保 api 蓝图已正确注册
from ..models import FbSport, MatchInfo, Animation
from .. import db
from datetime import datetime
import logging
from sqlalchemy import func

logger = logging.getLogger(__name__)

@api.route('/match/<int:id>/<string:lang>', methods=['GET'])
def get_stream(id, lang):
    """根据ID和语言获取单个流媒体记录"""
    logger.info(f"Fetching stream with id {id} and lang {lang}")
    stream = FbSport.query.get_or_404((id, lang))
    return jsonify(stream.to_json())

@api.route('/match', methods=['GET'])
def get_sport_count():
    """根据sid和ms对FbSport进行group by"""
    # logger.info(f"Fetching matches with lang {lang}")
    
    matches = db.session.query(
        MatchInfo.sportId,
        MatchInfo.status_id,
        func.count(MatchInfo.id).label('count')
    ).group_by(
        MatchInfo.sportId,
        MatchInfo.status_id,
    ).all()

    result = {}
    for match in matches:
        sportId = match.sportId
        if sportId is None:
            continue
        status_id = match.status_id
        if sportId not in result:
            result[sportId] = []
        result[sportId].append({
            status_id: match.count
        })

    return jsonify(result)

@api.route('/match_list/<int:sportId>/<int:status_id>', methods=['GET'])
def get_league(sportId, status_id):
    """根据sportId和status_id获取leagueId"""
    logger.info(f"Fetching league with sportId {sportId} and status_id {status_id}")
    matches = db.session.query(
        MatchInfo.status_id,
        MatchInfo.regionId,
        MatchInfo.leagueId,
        MatchInfo.league_order,
        MatchInfo.id,
        MatchInfo.match_time_unix,
        MatchInfo.is_hot,
        MatchInfo.run_time,
        MatchInfo.period_id,
        MatchInfo.hometeamId,
        MatchInfo.awayteamId,
        MatchInfo.match_stats
    ).filter(
        MatchInfo.sportId == sportId,
        MatchInfo.status_id == status_id
    ).all()

    result = {}
    for match in matches:
        leagueId = match.leagueId
        league_order = match.league_order
        if leagueId not in result:
            result[leagueId] = {'league_order': league_order, 'match_count': 0, 'match_list': []}
        result[leagueId]['match_count'] += 1
        result[leagueId]['match_list'].append({
            'status_id': match.status_id,
            'regionId': match.regionId,
            'leagueId': match.leagueId,
            'league_order': match.league_order,
            'id': match.id,
            'match_time_unix': match.match_time_unix,
            'is_hot': match.is_hot,
            'run_time': match.run_time,
            'period_id': match.period_id,
            'hometeamId': match.hometeamId,
            'awayteamId': match.awayteamId,
            'match_stats': match.match_stats
        })

    return jsonify(result)

@api.route('/match_detail/<int:id>', methods=['GET'])
def get_match_detail(id):
    """根据ID获取比赛详情"""
    logger.info(f"Fetching match detail with id {id}")
    match = MatchInfo.query.get_or_404(id)
    return jsonify(match.to_json())

@api.route('/fb_hub88', methods=['GET'])
def get_fb_hub88():
    logger.info(f"Fetching fb_hub88")
    match_data = db.session.query(
        Animation.id,
        Animation.eventId
    ).filter(
        Animation.eventId.isnot(None),
        Animation.match_time_unix >= int(datetime.now().timestamp())
    ).all()

    match_ids = []
    for match in match_data:
        match_id = str(match.id)
        event_id = str(match.eventId)
        match_ids.append(f"{match_id}*{event_id}")
    return jsonify(match_ids)


@api.route('/hello', methods=['GET'])
def hello_world():
    """返回Hello World"""
    return jsonify(message="Hello, World!")
