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
class MSServerChat:
    def as_obj(self):
        return asdict(self)
    __tablename__ = "msmc_chats"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(
        init=False, metadata={"sa": Column(Integer, primary_key=True)}
    )
    # unixtime of when the message arrived on-server.
    timestamp: int = field(default=None, metadata={"sa": Column(Integer())})
    # String representaiton of username.
    username: str = field(default=None, metadata={"sa": Column(String())})
    # UUID of the user. This is used for tying multiple chats together.
    uuid: str = field(default=None, metadata={"sa": Column(String())})
    # Type of message
    msgtype: str = field(default=None, metadata={"sa": Column(String())})
    # Actual text content.
    text: str = field(default=None, metadata={"sa": Column(String())})
    # Description, used for advancements
    description: str = field(default=None, metadata={"sa": Column(String())})
    # Source. ATM6, E2E, DISCORD, etc.
    source: str = field(default=None, metadata={"sa": Column(String())})

#    user = relationship("User",backref="msblog_posts")

#    def __repr__(self):
#        return "<User(id={}, name={}>".format(self.id, self.name)

db.main_table_list[MSServerChat.__tablename__] = MSServerChat

