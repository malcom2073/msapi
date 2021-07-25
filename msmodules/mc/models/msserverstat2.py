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
#[?] TPS from last 5s, 10s, 1m, 5m, 15m:
#[?]  *20.0, 18.07, 19.65, 19.92, 20.0
#[?] 
#[?] Tick durations (min/med/95%ile/max ms) from last 10s, 1m:
#[?]  34.7/40.5/88.0/620.4;  30.0/39.3/69.8/620.4
#[?] 
#[?] CPU usage from last 10s, 1m, 15m:
#[?]  37%, 31%, 30%  (system)
#[?]  37%, 31%, 30%  (process)

@db.mapper_registry.mapped
@dataclass
class MSServerStat2:
    def as_obj(self):
        return asdict(self)
    __tablename__ = "msmc_stats2"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(
        init=False, metadata={"sa": Column(Integer, primary_key=True)}
    )
    timestamp: int = field(default=None, metadata={"sa": Column(Integer())})
    tps: int = field(default=None, metadata={"sa": Column(Float())})
    tps5s: float = field(default=None, metadata={"sa": Column(Float())})
    tps10s: float = field(default=None, metadata={"sa": Column(Float())})
    tps1m: float = field(default=None, metadata={"sa": Column(Float())})
    tps5m: float = field(default=None, metadata={"sa": Column(Float())})
    tps15m: float = field(default=None, metadata={"sa": Column(Float())})
    tick10smin: float = field(default=None, metadata={"sa": Column(Float())})
    tick10smed: float = field(default=None, metadata={"sa": Column(Float())})
    tick10s95: float = field(default=None, metadata={"sa": Column(Float())})
    tick10smax: float = field(default=None, metadata={"sa": Column(Float())})
    tick1mmin: float = field(default=None, metadata={"sa": Column(Float())})
    tick1mmed: float = field(default=None, metadata={"sa": Column(Float())})
    tick1m95: float = field(default=None, metadata={"sa": Column(Float())})
    tick1mmax: float = field(default=None, metadata={"sa": Column(Float())})
    cpusys10s: float = field(default=None, metadata={"sa": Column(Float())})
    cpusys1m: float = field(default=None, metadata={"sa": Column(Float())})
    cpusys15m: float = field(default=None, metadata={"sa": Column(Float())})
    cpuproc10s: float = field(default=None, metadata={"sa": Column(Float())})
    cpuproc1m: float = field(default=None, metadata={"sa": Column(Float())})
    cpuproc15m: float = field(default=None, metadata={"sa": Column(Float())})
    online: int = field(default=None, metadata={"sa": Column(Integer())})

#    user = relationship("User",backref="msblog_posts")

#    def __repr__(self):
#        return "<User(id={}, name={}>".format(self.id, self.name)

db.main_table_list[MSServerStat2.__tablename__] = MSServerStat2

