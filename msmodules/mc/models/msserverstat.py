#from dataclasses import dataclass
from dataclasses import field, asdict
#import db
#from typing import List
#from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, UniqueConstraint
#from sqlalchemy.orm import relationship
#from models.group import Group
#from models.usergroup import UserGroup
#from models.usermetadata import UserMetadata


from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import db
#from app import db
#from app import main_table_list
#from app.models.user import User
from datetime import datetime
from dataclasses import dataclass
from typing import Type


@db.mapper_registry.mapped
@dataclass
class MSServerStat:
    def as_obj(self):
        return asdict(self)
    __tablename__ = "msmc_stats"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(
        init=False, metadata={"sa": Column(Integer, primary_key=True)}
    )
    timestamp: int = field(default=None, metadata={"sa": Column(Integer())})
    tps: int = field(default=None, metadata={"sa": Column(Float())})
    ticktime: int = field(default=None, metadata={"sa": Column(Float())})
    online: int = field(default=None, metadata={"sa": Column(Integer())})

#    user = relationship("User",backref="msblog_posts")

#    def __repr__(self):
#        return "<User(id={}, name={}>".format(self.id, self.name)

db.main_table_list[MSServerStat.__tablename__] = MSServerStat

