from typing import Optional, List

from sqlalchemy.orm import Session

import log
from model.entities import Site

logger = log.get_logger(__name__)


def load_all_sites(session: Session) -> List[Site]:
    return session.query(Site).all()


def load_site_by_url(site_url: str, session: Session) -> Optional[Site]:
    return session.query(Site)\
        .filter(Site.url == site_url)\
        .first()


def save_or_update(site: Site, session: Session) -> Site:
    existing_site = session.query(Site)\
        .filter(Site.url == site.url)\
        .first()
    if existing_site:
        session.delete(existing_site)

    session.add(site)

    return site
