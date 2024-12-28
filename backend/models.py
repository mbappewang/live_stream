from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from . import db

class FbSport(db.Model):
    __tablename__ = 'fb'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String(100), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    nm = db.Column(db.Text, nullable=True)
    match_time_unix = db.Column(db.BigInteger, nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    animation = db.Column(db.JSON, nullable=True)
    fid = db.Column(db.Integer, nullable=True)
    fmt = db.Column(db.Integer, nullable=True)
    lg = db.Column(db.JSON, nullable=True)
    mc = db.Column(db.JSON, nullable=True)
    mg = db.Column(db.JSON, nullable=True)
    ms = db.Column(db.Integer, nullable=True)
    ne = db.Column(db.Integer, nullable=True)
    nsg = db.Column(db.JSON, nullable=True)
    pl = db.Column(db.Integer, nullable=True)
    sb = db.Column(db.JSON, nullable=True)
    sid = db.Column(db.Integer, nullable=True)
    smt = db.Column(db.Integer, nullable=True)
    tms = db.Column(db.Integer, nullable=True)
    tps = db.Column(db.JSON, nullable=True)
    ts = db.Column(db.JSON, nullable=True)
    ty = db.Column(db.Integer, nullable=True)
    vs = db.Column(db.JSON, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'lang': self.lang,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'nm': self.nm,
            'match_time_unix': self.match_time_unix,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'animation': self.animation,
            'fid': self.fid,
            'fmt': self.fmt,
            'lg': self.lg,
            'mc': self.mc,
            'mg': self.mg,
            'ms': self.ms,
            'ne': self.ne,
            'nsg': self.nsg,
            'pl': self.pl,
            'sb': self.sb,
            'sid': self.sid,
            'smt': self.smt,
            'tms': self.tms,
            'tps': self.tps,
            'ts': self.ts,
            'ty': self.ty,
            'vs': self.vs
        }

class Animation(db.Model):
    __tablename__ = 'animation'

    id = db.Column(db.Integer, primary_key=True)
    animation1 = db.Column(db.Text, nullable=True)
    animation2 = db.Column(db.Text, nullable=True)
    statscore_id = db.Column(db.Integer, nullable=True)

