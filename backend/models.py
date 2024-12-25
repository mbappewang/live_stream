from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

db = SQLAlchemy()

class FbSport(db.Model):
    __tablename__ = 'fb_sport'

    match_id = db.Column(db.Integer, primary_key=True)
    match_time = db.Column(db.BigInteger)
    regionName = db.Column(db.String(100))
    regionId = db.Column(db.Integer)
    regionUrl = db.Column(db.Text)
    leagueName = db.Column(db.String(100))
    leagueId = db.Column(db.Integer)
    leagueUrl = db.Column(db.Text)
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
    status = db.Column(db.String(50))  # 比赛状态字段
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