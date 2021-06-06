from dataclasses import dataclass
from dataclasses import field, asdict
import db
from typing import List
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
#from models.group import Group
#from models.usergroup import UserGroup
#from models.user import User

@db.mapper_registry.mapped
@dataclass
class Permission:
    def as_obj(self):
        return asdict(self)
    __tablename__ = "permissions"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(
        init=False, metadata={"sa": Column(Integer, primary_key=True)}
    )
    api_permission: str = field(default=None, metadata={"sa": Column(String(50))})
#    value: str = field(default=None, metadata={"sa": Column(String(50))})
    group_id: int = field(
        init=False,metadata={"sa": lambda: Column(ForeignKey("groups.id"))}
    )
db.main_table_list[Permission.__tablename__] = Permission