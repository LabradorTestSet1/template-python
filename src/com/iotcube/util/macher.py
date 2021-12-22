#-*- coding: utf-8 -*-
import re

from pathlib import Path
import sys
sys.path.insert(0, str( Path(Path(Path(Path(Path(__file__).parent.absolute()).parent.absolute()).parent.absolute()).parent.absolute()) ))

from com.iotcube.util.timeout import Timeout

class Macher():
    patterns = []

    '''
    필터 리스트를 입력해서 Macher를 초기화 한다.
    '''
    def init(self, filterList: None):
        try:
            for b in filterList:
                self.patterns.append(re.compile(b, re.IGNORECASE))

            #add more(.xxx/ | .xxx)
            self.patterns.append(re.compile('(?:^|[\\\/])(\.(?!\.)[^\\\/]+)$'))
            self.patterns.append(re.compile('(?<=\/)\.')) 
            self.patterns.append(re.compile('(?:^|[\\\/])(\.(?!\.)[^\\\/]+)/'))
        except Exception as e:
            raise(e)

    '''
    filter list와 일치하는 패턴이 있는지 확인하고 결과를 돌려준다.
    True: 일치
    False: 불일치 
    '''
    def match(self, text):
        retval = self.matchInnder(text)
        if retval == None:
            return True
        else:
            return retval
    
    '''
    패턴이 일치하는 경우 간혹 'findall'이 오래 걸리는 문제가 발생해서 타임아웃 10초를 둔다.
    이 경우, None이 리턴되고 패턴 일치로 처리된다. 
    '''
    def matchInnder(self, text):
        with Timeout(10):
            try:
                for p in self.patterns:
                    out = re.findall(p, text)
                    if out != None and len(out) != 0:
                        return True
                return False
            except Exception as e:
                raise(e)
    
