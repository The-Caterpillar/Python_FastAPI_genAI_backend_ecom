import re
from typing import Any
 
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base, DeclarativeBase, Mapped, mapped_column
 
Base = declarative_base # check check
class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls: Any) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
 
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
