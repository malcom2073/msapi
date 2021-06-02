#from dataclasses import dataclass
from dataclasses import field, asdict
#import db
#from typing import List
#from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, UniqueConstraint
#from sqlalchemy.orm import relationship
#from models.group import Group
#from models.usergroup import UserGroup
#from models.usermetadata import UserMetadata


from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
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
class MSBlogPost:
    def as_obj(self):
        return asdict(self)
    __tablename__ = "msblog_posts"
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(
        init=False, metadata={"sa": Column(Integer, primary_key=True)}
    )
    title: str = field(default=None, metadata={"sa": Column(String(50))})
    user_id: int = field(
        init=False,metadata={"sa": lambda: Column(ForeignKey("users.id"))}
    )
    timestamp: int = field(default=None, metadata={"sa": Column(Integer())})
    content: str = field(default=None, metadata={"sa": Column(String(1024))})
    published: bool = field(default=None, metadata={"sa": Column(Boolean())})

#    user = relationship("User",backref="msblog_posts")

#    def __repr__(self):
#        return "<User(id={}, name={}>".format(self.id, self.name)

db.main_table_list[MSBlogPost.__tablename__] = MSBlogPost

