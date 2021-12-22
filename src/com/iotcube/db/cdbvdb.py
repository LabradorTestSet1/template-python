#-*- coding: utf-8 -*-
from enum import Enum
from typing import List
from sqlalchemy.sql.expression import text

from pathlib import Path
import sys
sys.path.insert(0, str( Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute() ))

from com.iotcube.db.base import Database
from com.iotcube.sw.common import DBConfig
from com.iotcube.util.logger import Logger


class LabradorDB(Database):
    logger = Logger()

    def getDBConfig(self, key) -> DBConfig:
        with self._getDB().connect() as connection:
            try:
                statement = text("""SELECT * from TB_CONFIG where `KEY` = '%s'""" % key)
                self.logger.getLogger().info(statement)
                resultProxy = connection.execute(statement)

                rows = resultProxy.fetchall()
                if rows is None:
                    self.logger.getLogger().info('data is null')
                    return None
                
                configList = []
                for r in rows:
                    config = DBConfig()
                    config.key = r[1]
                    config.value = r[2]
                    configList.append(config)
                return configList
            except Exception as e:
                self.logger.getLogger().error(e)
                raise e

           
