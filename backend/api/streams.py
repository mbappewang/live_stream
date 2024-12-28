from flask import jsonify, request
from . import api  # 确保 api 蓝图已正确注册
from ..models import FbSport
from .. import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@api.route('/streams', methods=['GET'])
def get_streams():
    """获取所有流媒体记录"""
    logger.info("Fetching all streams")
    streams = FbSport.query.all()
    return jsonify([stream.to_json() for stream in streams])

@api.route('/streams/<int:id>', methods=['GET'])
def get_stream(id):
    """根据ID获取单个流媒体记录"""
    logger.info(f"Fetching stream with id {id}")
    stream = FbSport.query.get_or_404(id)
    return jsonify(stream.to_json())

@api.route('/streams', methods=['POST'])
def create_stream():
    """创建新的流媒体记录"""
    data = request.get_json()
    logger.info("Creating a new stream with data: %s", data)
    stream = FbSport(
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        nm=data.get('nm'),
        match_time_unix=data.get('match_time_unix'),
        start_time=datetime.fromisoformat(data.get('start_time')) if data.get('start_time') else None,
        animation=data.get('animation'),
        fid=data.get('fid'),
        fmt=data.get('fmt'),
        lg=data.get('lg'),
        mc=data.get('mc'),
        mg=data.get('mg'),
        ms=data.get('ms'),
        ne=data.get('ne'),
        nsg=data.get('nsg'),
        pl=data.get('pl'),
        sb=data.get('sb'),
        sid=data.get('sid'),
        smt=data.get('smt'),
        tms=data.get('tms'),
        tps=data.get('tps'),
        ts=data.get('ts'),
        ty=data.get('ty'),
        vs=data.get('vs')
    )
    db.session.add(stream)
    db.session.commit()
    return jsonify(stream.to_json()), 201

@api.route('/streams/<int:id>', methods=['PUT'])
def update_stream(id):
    """更新现有的流媒体记录"""
    data = request.get_json()
    logger.info(f"Updating stream with id {id} with data: %s", data)
    stream = FbSport.query.get_or_404(id)
    stream.updated_at = datetime.utcnow()
    stream.nm = data.get('nm', stream.nm)
    stream.match_time_unix = data.get('match_time_unix', stream.match_time_unix)
    stream.start_time = datetime.fromisoformat(data.get('start_time')) if data.get('start_time') else stream.start_time
    stream.animation = data.get('animation', stream.animation)
    stream.fid = data.get('fid', stream.fid)
    stream.fmt = data.get('fmt', stream.fmt)
    stream.lg = data.get('lg', stream.lg)
    stream.mc = data.get('mc', stream.mc)
    stream.mg = data.get('mg', stream.mg)
    stream.ms = data.get('ms', stream.ms)
    stream.ne = data.get('ne', stream.ne)
    stream.nsg = data.get('nsg', stream.nsg)
    stream.pl = data.get('pl', stream.pl)
    stream.sb = data.get('sb', stream.sb)
    stream.sid = data.get('sid', stream.sid)
    stream.smt = data.get('smt', stream.smt)
    stream.tms = data.get('tms', stream.tms)
    stream.tps = data.get('tps', stream.tps)
    stream.ts = data.get('ts', stream.ts)
    stream.ty = data.get('ty', stream.ty)
    stream.vs = data.get('vs', stream.vs)
    db.session.commit()
    return jsonify(stream.to_json())

@api.route('/streams/<int:id>', methods=['DELETE'])
def delete_stream(id):
    """删除流媒体记录"""
    logger.info(f"Deleting stream with id {id}")
    stream = FbSport.query.get_or_404(id)
    db.session.delete(stream)
    db.session.commit()
    return '', 204


