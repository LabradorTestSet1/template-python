# labcrawler template project #

python을 사용하여 구현하는 툴의 템플릿 프로젝트

### Python Coding Convention
* 영문:  https://www.python.org/dev/peps/pep-0008/
* 번역본:  https://luavis.me/python/python-convention

### 아이오티큐브 Python Program 개발 가이드 ###
1. 기본적인 코딩컨벤션은 위에 링크한 python coding convention 을 사용한다.

2. 아래와 같은 템플릿을 사용하여 기본 프로젝트를 생성한다.
```
template_project
├── README.md
├── Dockerfile
├── docker.build.sh
├── docker.install.sh
├── docker.run.in.background.mode.sh
├── docker.run.in.interactive.mode.sh
└── src
    ├── com
    │   └── iotcube
    │       ├── app
    │       │   └── [PROJECT_NAME]
    │       │       └── main.py
    │       ├── db
    │       └── util
    ├── config.ini
    └── requirements.txt
```

3. 1. Dockerfile
* python3.9만 사용한다.
* 도커 파일
* python:3-alpine을 기본이미지로 작성하고, 변경이 필요한 경우에만 변경해서 사용한다.

3. 2. Dockerfile.java+python3
* sort gen을 사용하기 위한 가상 환경 (가벼운 환경)
* sort gen을 사용하려면 비트버켓의 sortgen 검색..후 사용법 확인바람
* 백그라운드 실행시 python => python3 로 교체

3. 3. Dockerfile.ubuntu
* 여러 명령어와 실행이 잘 안될 때, ubuntu용 도커 파일
* 현재 java11, python3, golang이 자동으로 설치된다.
* 필요한 환경을 자유로 구상하여 사용 가능!
* 백그라운드 실행시 python => python3 로 교체

4. docker.build.sh
* 도커 빌드 스크립트
* 편집해서 사용하지 않는다.
* config.ini 파일에 정의된 이름으로 도커 이미지가 생성된다.

5. docker.install.sh
* 도커 설치 스크립트
* 편집해서 사용하지 않는다.
* config.ini 파일에 정의된 이름의 도커 이미지를 설치한다.

6. docker.run.in.background.mode.sh 
* 배포하여 백드라운드로 실행하기 위한 스크립트

7. docker.run.in.interactive.mode.sh
* 개발중 docker 환경 내에서 프로그램을 구동하기 위한 실행 스크립트 

8. config.ini
* 설정 파일(db 연결정보, 도커 이미지 이름 등)이 정의되어 있다.
* 기본 설정외의 프로그램이 사용할 설정은 추가로 정의해서 사용한다.

9. src
* 파이선 프로그램이 저장될 소스 폴더
* com/iotcube 형태로 폴더 구조를 사용한다.
* db 폴더에 공통적으로 사용할 DB 클래스가 구현되어 있다.
* util 폴더에 공통적으로 사용한 유틸리티 클래스가 구현되어 있다.
* requirements.txt

10. 가상환경
* 각 프로그램에 해당하는 python 가상환경(예: 아나콘다)을 따로 사용하지 않는다.
* docker 내에서 가상환경을 만들어서 사용한다.
* docker.run.in.interactive.mode.sh 파일 참조
* requirements.txt도 docker 이미지 내부에서 생성한다.

11. DB 유틸리티
* Class로 작성
* sqlalchemy 라이브러리를 사용
* 기본적인 db 설정과 연결/해제에 대한 base 클래스만 제공한다.
* 실제 쿼리와 모델 연동은 각자 프로그램에서 구현한다.

12. LOG 유틸리티
* 콘솔과 파일로 로그 메세지를 출력하는 유틸리티

### 프로그램 작성과 배포 방법 ###
1. template project를 클론한다.

2. template project를 기반으로 원하는 프로그램을 작성한다.

3. 배포와 프로그램 실행은 docker로 진행한다.

### 템플릿 프로젝트를 사용한 생성 & 업데이트 방법

1. labcrawler_template를 포크해서 새로운 레포지토리를 생성

2. 원격저장소 등록
```
$ git remote add upstream git@bitbucket.org:iotcubedev/template-python.git
```

3. 등록된 원격 저장소 확인
```
$ git remote -v
origin	git@bitbucket.org:iotcubedev/MY_NEW.git (fetch)
origin	git@bitbucket.org:iotcubedev/MY_NEW.git (push)
upstream	git@bitbucket.org:iotcubedev/template-python.git (fetch)
upstream	git@bitbucket.org:iotcubedev/template-python.git (push)
```

4. labcrawler_template의 수정사항 머지
```
$ git fetch upstream
$ git merge upstream/master
```