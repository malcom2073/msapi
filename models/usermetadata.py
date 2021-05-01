from dataclasses import dataclass
from dataclasses import field, asdict
import db
from typing import List
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from models.group import Group
from models.usergroup import UserGroup
#from models.user import User

@db.mapper_registry.mapped
@dataclass
class UserMetadata:
    def as_obj(self):
        return asdict(self)
    # Dataclass definitions
#    id: int
#    username: str
#    name: str
#    groupname: str
#    password: str
#    email: str
    __tablename__ = "users_metadata"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(
        init=False, metadata={"sa": Column(Integer, primary_key=True)}
    )
    key: str = field(default=None, metadata={"sa": Column(String(50))})
    value: str = field(default=None, metadata={"sa": Column(String(50))})
    user_id: int = field(
        init=False,metadata={"sa": lambda: Column(ForeignKey("users.id"))}
    )
#    id = Column(Integer, primary_key=True)
#    username = Column(String)
#    name = Column(String)
#    password = Column(String)
#    email = Column(String)


#    timezone = Column(String)
#    lastip = Column(String)
#    nickname = Column(String)
#    validated = Column(Boolean,nullable=False)

#    primary_group_id = Column(Integer, ForeignKey(Group.id))
#    primary_group = relationship("Group",back_populates="users",lazy="joined")

    #secondary_groups = db.relationship("Group",secondary="user_secondary_group_assoc")


#    profilefields = relationship("UserProfileField", back_populates="user")

#    registered_date = Column(DateTime, nullable=False,default=datetime.utcnow)

#    def __init__(self,id,username,name,groupname,password,state):
#        self.id = id
#        self.username = username
#        self.name = name
#        self.groupname = groupname
#        self.password = password
#        self.state = state
db.main_table_list[UserMetadata.__tablename__] = UserMetadata