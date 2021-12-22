#-*- coding: utf-8 -*-
from pydantic import BaseModel
import sqlalchemy as db
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.engine.base import Engine

from pathlib import Path
import sys
sys.path.insert(0, str( Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute() ))

from com.iotcube.util.config import Config
from com.iotcube.util.logger import Logger

class Database(BaseModel):
    uri: str = None
    engine: Engine = None
    metadata: MetaData = None
    logger = Logger()
    
    class Config:
        arbitrary_types_allowed = True

    def open(self):
        config = Config()
        self.uri = config.getConfig('DB', 'DbUrl')
        try:
            self.logger.getLogger().info('[Database]open:' + self.uri)
            self.engine = db.create_engine(self.uri, pool_pre_ping=True)
            self.metadata = db.MetaData()
        except Exception as e:
            self.close()
            self.logger.getLogger().error(e)
            raise e

    def _getDB(self) -> Engine:
        try:
            self.engine = db.create_engine(self.uri, pool_pre_ping=True)
            self.metadata = db.MetaData()
            
            return self.engine
        except Exception as e:
            self.close()
            self.logger.getLogger().error(e)
            raise e

    def close(self):
        if self.engine is not None:
            self.logger.getLogger().info('[Database]close')
            self.engine.dispose()
            self.engine = None
        