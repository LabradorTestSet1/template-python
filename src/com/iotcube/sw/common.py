#-*- coding: utf-8 -*-
from typing import Dict
from pydantic import BaseModel
import json

class DBConfig(BaseModel):
    key: str = None
    value: str = None

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def getKey(self) -> str:
        return self.key
    
    def getValue(self) -> str:
        return self.value

