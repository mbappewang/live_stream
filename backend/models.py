from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from . import db

class FbSport(db.Model):
    __tablename__ = 'fb'

    match_id = db.Column(db.Integer, primary_key=True)
    match_time = db.Column(db.BigInteger)
    match_time_utc = db.Column(db.DateTime, default=datetime.utcnow)
    match_period  = db.Column(db.Integer)
    match_status = db.Column(db.Integer)
    match_group = db.Column(db.JSON)
    match_stats = db.Column(db.JSON)
    regionName = db.Column(db.String(100))
    regionId = db.Column(db.Integer)
    regionUrl = db.Column(db.Text)
    leagueName = db.Column(db.String(100))
    leagueId = db.Column(db.Integer)
    leagueUrl = db.Column(db.Text)
    leagueOrder = db.Column(db.Integer)
    leagueHot = db.Column(db.Boolean)
    match_name = db.Column(db.String(100))
    homeTeam = db.Column(db.String(100))
    homeTeamUrl = db.Column(db.Text)
    homeTeamId = db.Column(db.Integer)
    awayTeam = db.Column(db.String(100))
    awayTeamUrl = db.Column(db.Text)
    awayTeamId = db.Column(db.Integer)
    animation1 = db.Column(db.Text)
    animation2 = db.Column(db.Text)
    web = db.Column(db.Text)
    flvHD = db.Column(db.Text)
    flvSD = db.Column(db.Text)
    m3u8HD = db.Column(db.Text)
    m3u8SD = db.Column(db.Text)
    statscore_id = db.Column(db.Integer)
    status = db.Column(db.String(100))  # 比赛状态字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)  # 更新时间

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting match_id {self.match_id} to JSON")
        return {
            'match_id': self.match_id,
            'match_time': self.match_time,
            'regionName': self.regionName,
            'regionId': self.regionId,
            'regionUrl': self.regionUrl,
            'leagueName': self.leagueName,
            'leagueId': self.leagueId,
            'leagueUrl': self.leagueUrl,
            'match_name': self.match_name,
            'homeTeam': self.homeTeam,
            'homeTeamUrl': self.homeTeamUrl,
            'homeTeamId': self.homeTeamId,
            'awayTeam': self.awayTeam,
            'awayTeamUrl': self.awayTeamUrl,
            'awayTeamId': self.awayTeamId,
            'animation1': self.animation1,
            'animation2': self.animation2,
            'web': self.web,
            'flvHD': self.flvHD,
            'flvSD': self.flvSD,
            'm3u8HD': self.m3u8HD,
            'm3u8SD': self.m3u8SD,
            'statscore_id': self.statscore_id,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class MatchInfo(db.Model):
    __tablename__ = 'match_info'

    match_id = db.Column(db.Integer, primary_key=True)
    match_time_unix = db.Column(db.BigInteger, nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    match_name = db.Column(db.String(100), nullable=True)
    period_id = db.Column(db.Integer, nullable=True)
    status_id = db.Column(db.Integer, nullable=True)
    sportId = db.Column(db.Integer, nullable=True)
    regionId = db.Column(db.Integer, nullable=True)
    leagueId = db.Column(db.Integer, nullable=True)
    is_hot = db.Column(db.Boolean, nullable=True)
    hometeamId = db.Column(db.Integer, nullable=True)
    awayteamId = db.Column(db.Integer, nullable=True)
    match_stats = db.Column(db.JSON, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting match_id {self.match_id} to JSON")
        return {
            'match_id': self.match_id,
            'match_time_unix': self.match_time_unix,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'match_name': self.match_name,
            'period_id': self.period_id,
            'status_id': self.status_id,
            'sportId': self.sportId,
            'regionId': self.regionId,
            'leagueId': self.leagueId,
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
    as1 = db.Column(db.Text, nullable=True)
    as2 = db.Column(db.Text, nullable=True)
    statscore_id = db.Column(db.Integer, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'as1': self.as1,
            'as2': self.as2,
            'statscore_id': self.statscore_id
        }

class Stream(db.Model):
    __tablename__ = 'stream'

    id = db.Column(db.Integer, primary_key=True)
    web = db.Column(db.Text, nullable=True)
    flvsd = db.Column(db.Text, nullable=True)
    flvhd = db.Column(db.Text, nullable=True)
    m3u8sd = db.Column(db.Integer, nullable=True)
    m3u8hd = db.Column(db.Text, nullable=True)

    def to_json(self):
        """将模型转换为JSON格式，用于API响应"""
        logger.info(f"Converting id {self.id} to JSON")
        return {
            'id': self.id,
            'web': self.web,
            'flvsd': self.flvsd,
            'flvhd': self.flvhd,
            'm3u8sd': self.m3u8sd,
            'm3u8hd': self.m3u8hd
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


