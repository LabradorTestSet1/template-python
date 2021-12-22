#-*- coding: utf-8 -*-

from pathlib import Path
import sys
sys.path.insert(0, str( Path(Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute()) ))

from com.iotcube.util.logger import Logger
from com.iotcube.util.config import Config
from com.iotcube.db.cdbvdb import LabradorDB
from com.iotcube.util.macher import Macher

import schedule
import time
import json
import jpype

def main():
    # #Logger 선언해서 사용하기 예제
    logger = Logger()
    logger.getLogger().warning('warn message')
    logger.getLogger().info('info message')
    logger.getLogger().error('error message')
    logger.getLogger().debug('debug message')

    #Config 가져오기 예제
    config = Config()
    logger.getLogger().info('\n' + config.toString())

    #DB 연동 예제
    cdbvdb = LabradorDB()
    cdbvdb.open()
    compactFilter = json.loads(cdbvdb.getDBConfig('COMPACT_FILTER')[0].getValue())
    cdbvdb.close()

    #Macher 테스트
    macher = Macher()
    macher.init(compactFilter)
    logger.getLogger().info(f"match : {macher.match('/test/bin/test.cpp')}\n")
    logger.getLogger().info(f"match : {macher.match('/test/test.cpp')}\n")

if __name__ == "__main__":
    schedule.every().friday.at("17:25").do(main)          # monday, tuesday, wednesday, thursday, friday, saturday, sunday 요일 정하고 시간 정하면 한 주에 한번 지정 요일 시간에 실행 됨
    # schedule.every(1).minutes.do(main)                    # 숫자 부분에 숫자 지정하면 지정 숫자 분마다 실행됨
    # schedule.every().day.at("11:00").do(main)             # 매일 지정 시간에 실행됨
    # schedule.every(7).days.do(main)                       # 7일마다 job 실행  * 첫 실행은 7일 후 ex) 20일 2시에 프로그램을 실행하면 main의 첫 실행은 27일에 실행됨
    # schedule.every(1).weeks.do(main)                      # 1주마다 job 실행
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            pass
