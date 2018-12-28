import datetime

from sqlalchemy import Column, String, PickleType, DateTime
from sqlalchemy.ext.declarative import declarative_base

from model.histogram import Histogram

Base = declarative_base()


class Site(Base):

    __tablename__ = 'sites'

    url = Column(String, primary_key=True)
    tag_histogram = Column(PickleType)
    date_of_visit = Column(DateTime)

    def __init__(self, url: str, tag_histogram: Histogram[str] = None, date_of_visit: datetime = None) -> None:
        self.url, self.tag_histogram = url, tag_histogram
        self.date_of_visit = date_of_visit or datetime.datetime.now()

    def __hash__(self) -> int:
        return hash(self.url)

    def __eq__(self, o: 'Site') -> bool:
        return self.url == o.url

