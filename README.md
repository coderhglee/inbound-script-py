# image-wires-agent

## 소스 패키징
```shell script
python setup.py sdist bdist_wheel 
```

## 서버 초기 세팅
```shell script
# setup 가상 환경
python3 -m venv venv
#
source venv/bin/activate
# install package
pip install -r requirements.txt

pip3 install wires-{version}.tar.gz
```