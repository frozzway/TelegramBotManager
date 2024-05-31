from pydantic import BaseModel

from .auth import *
from .elements import *


class BaseModelWithId(BaseModel):
    id: int
