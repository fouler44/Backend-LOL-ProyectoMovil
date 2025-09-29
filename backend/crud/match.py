from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.match import LolMatch, MatchParticipation

def upsert_match(db: Session, **kwargs):
    """Inserta o actualiza una partida"""
    match = db.query(LolMatch).filter(LolMatch.match_id == kwargs["match_id"]).first()
    
    if match:
        for k, v in kwargs.items():
            setattr(match, k, v)
    else:
        match = LolMatch(**kwargs)
        db.add(match)
    
    return match


def insert_participation(db: Session, **kwargs):
    """
    Inserta una participación.
    Si ya existe (match_id + puuid), no hace nada por el UniqueConstraint.
    """
    # Verificar si ya existe
    existing = db.query(MatchParticipation).filter(
        and_(
            MatchParticipation.match_id == kwargs["match_id"],
            MatchParticipation.puuid == kwargs["puuid"]
        )
    ).first()
    
    if existing:
        return existing
    
    participation = MatchParticipation(**kwargs)
    db.add(participation)
    return participation


def get_match_by_id(db: Session, match_id: str):
    """Obtiene una partida por ID"""
    return db.query(LolMatch).filter(LolMatch.match_id == match_id).first()


def get_participations_by_match(db: Session, match_id: str):
    """Obtiene todas las participaciones de una partida"""
    return db.query(MatchParticipation).filter(
        MatchParticipation.match_id == match_id
    ).all()


def get_participations_by_puuid(db: Session, puuid: str, limit: int = 20):
    """Obtiene las últimas participaciones de un jugador"""
    return db.query(MatchParticipation).filter(
        MatchParticipation.puuid == puuid
    ).order_by(MatchParticipation.participation_id.desc()).limit(limit).all()


def match_exists(db: Session, match_id: str) -> bool:
    """Verifica si una partida ya está guardada"""
    return db.query(LolMatch).filter(LolMatch.match_id == match_id).first() is not None