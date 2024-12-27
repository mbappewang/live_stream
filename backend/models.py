from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from . import db

class FbSport(db.Model):
    __tablename__ = 'fb'

    id = db.Column(db.Integer, primary_key=True)
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
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'nm': self.nm,
            'match_time_unix': self.match_time_unix,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'as': self.as_,
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

class MatchInfo(db.Model):
    __tablename__ = 'match_info'

    id = db.Column(db.Integer, primary_key=True)
    match_time_unix = db.Column(db.BigInteger, nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    match_name = db.Column(db.String(100), nullable=True)
    period_id = db.Column(db.Integer, nullable=True)
    status_id = db.Column(db.Integer, nullable=True)
    sportId = db.Column(db.Integer, nullable=True)
    regionId = db.Column(db.Integer, nullable=True)
    leagueId = db.Column(db.Integer, nullable=True)
    league_order = db.Column(db.Integer, nullable=True)
    is_hot = db.Column(db.Boolean, nullable=True)
    hometeamId = db.Column(db.Integer, nullable=True)
    awayteamId = db.Column(db.Integer, nullable=True)
    match_stats = db.Column(db.JSON, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting match_id {self.match_id} to JSON")
        return {
            'id': self.id,
            'match_time_unix': self.match_time_unix,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'match_name': self.match_name,
            'period_id': self.period_id,
            'status_id': self.status_id,
            'sportId': self.sportId,
            'regionId': self.regionId,
            'leagueId': self.leagueId,
            "league_order": self.league_order,
            'is_hot': self.is_hot,
            'hometeamId': self.hometeamId,
            'awayteamId': self.awayteamId,
            'match_stats': self.match_stats
        }

class MarketInfo(db.Model):
    __tablename__ = 'market_info'

    match_id = db.Column(db.Integer, primary_key=True)
    market = db.Column(db.JSON, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting match_id {self.match_id} to JSON")
        return {
            'match_id': self.match_id,
            'market': self.market
        }

class MarketType(db.Model):
    __tablename__ = 'market_type'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'lang': self.lang,
            'name': self.name
        }

class MatchPeriod(db.Model):
    __tablename__ = 'match_period'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'lang': self.lang,
            'name': self.name
        }

class MatchStatus(db.Model):
    __tablename__ = 'match_status'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'lang': self.lang,
            'name': self.name
        }

class MarketName(db.Model):
    __tablename__ = 'market_name'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'lang': self.lang,
            'name': self.name
        }

class Period(db.Model):
    __tablename__ = 'period'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'lang': self.lang,
            'name': self.name
        }

class StatsType(db.Model):
    __tablename__ = 'stats_type'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'lang': self.lang,
            'name': self.name
        }

class SportType(db.Model):
    __tablename__ = 'sport_type'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'lang': self.lang,
            'name': self.name
        }

class TournamentPhase(db.Model):
    __tablename__ = 'tournament_phase'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'lang': self.lang,
            'name': self.name
        }

class Animation(db.Model):
    __tablename__ = 'animation'

    id = db.Column(db.Integer, primary_key=True)
    animation1 = db.Column(db.Text, nullable=True)
    animation2 = db.Column(db.Text, nullable=True)
    statscore_id = db.Column(db.Integer, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'animation1': self.animation1,
            'animation2': self.animation2,
            'statscore_id': self.statscore_id
        }

class Stream(db.Model):
    __tablename__ = 'stream'

    id = db.Column(db.Integer, primary_key=True)
    web = db.Column(db.Text, nullable=True)
    flvSD = db.Column(db.Text, nullable=True)
    flvHD = db.Column(db.Text, nullable=True)
    m3u8SD = db.Column(db.Integer, nullable=True)
    m3u8HD = db.Column(db.Text, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'web': self.web,
            'flvSD': self.flvSD,
            'flvHD': self.flvHD,
            'm3u8SD': self.m3u8SD,
            'm3u8HD': self.m3u8HD
        }

class Region(db.Model):
    __tablename__ = 'region'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'lang': self.lang,
            'name': self.name
        }

class League(db.Model):
    __tablename__ = 'league'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'lang': self.lang,
            'name': self.name
        }

class Team(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'lang': self.lang,
            'name': self.name
        }


