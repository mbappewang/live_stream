from flask import jsonify, request
from . import api  # 确保 api 蓝图已正确注册
from ..models import FbSport  # 确保 FbSport 模型已正确定义
from .. import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@api.route('/streams', methods=['GET'])
def get_streams():
    """获取所有直播流列表
    返回: JSON格式的直播流列表
    """
    try:
        streams = FbSport.query.all()  # 确保数据库连接正常，并且 FbSport 模型中有数据
        logger.info(f"Fetched {len(streams)} streams")
        return jsonify({'streams': [stream.to_json() for stream in streams]})  # 确保 FbSport 模型中有 to_json 方法
    except Exception as e:
        logger.error(f"Error fetching streams: {e}")
        return jsonify({'error': 'Error fetching streams'}), 500

@api.route('/streams/search', methods=['GET'])
def search_streams():
    """根据regionId和leagueId请求比赛信息
    参数: regionId - 地区ID, leagueId - 联赛ID
    返回: JSON格式的比赛信息列表
    """
    region_id = request.args.get('regionId', type=int)
    league_id = request.args.get('leagueId', type=int)
    
    if region_id is None or league_id is None:
        logger.error("Missing regionId or leagueId")
        return jsonify({'error': 'Missing regionId or leagueId'}), 400
    
    try:
        streams = FbSport.query.filter_by(regionId=region_id, leagueId=league_id).all()
        logger.info(f"Fetched {len(streams)} streams for regionId {region_id} and leagueId {league_id}")
        return jsonify({'streams': [stream.to_json() for stream in streams]})
    except Exception as e:
        logger.error(f"Error searching streams: {e}")
        return jsonify({'error': 'Error searching streams'}), 500

@api.route('/streams/match/<int:match_id>', methods=['GET'])
def get_stream_by_match_id(match_id):
    """根据match_id请求比赛信息
    参数: match_id - 比赛ID
    返回: JSON格式的比赛信息
    """
    try:
        stream = FbSport.query.filter_by(match_id=match_id).first()
        if stream is None:
            logger.error(f"Match with match_id {match_id} not found")
            return jsonify({'error': 'Match not found'}), 404
        logger.info(f"Fetched stream for match_id {match_id}")
        return jsonify(stream.to_json())
    except Exception as e:
        logger.error(f"Error fetching stream by match_id: {e}")
        return jsonify({'error': 'Error fetching stream by match_id'}), 500

@api.route('/helloworld', methods=['GET'])
def hello_world():
    """简单的Hello World API
    返回: JSON格式的Hello World消息
    """
    logger.info("Hello World API called")
    return jsonify({'message': 'Hello, World!'})
