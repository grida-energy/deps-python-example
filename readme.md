# DEPS (Distributed Energy Protocol System) Python 사용 예제

## 1 의존성 설치

pip 혹은 uv를 이용하여 의존성을 설치한다.

pip 이용 시

```bash
# 가상 환경 초기화
python3 -m venv path/to/venv
source path/to/venv/bin/activate
# 의존성 설치
python3 -m pip install .
# 실행
python3 sub_example.py ..."명령행 인자"
```

uv 이용 시

```bash
# uv로 실행시 의존성 자동 설치
uv run sub_example.py ..."명령행 인자"
```

## 2 실행

sub_example.py 실행 시 인자를 넣거나 혹은 환경변수에 인자를 명시한다.
혹은 .env 파일을 생성하여 환경변수를 오버라이드 하여 사용한다.

명령행 인자

```txt
usage: sub_example.py [-h] [--url URL] [--client_id CLIENT_ID] [--topic TOPIC] [--ca_cert CA_CERT] [--cert CERT] [--key KEY]

deps-python-example

options:
  -h, --help            show this help message and exit
  --url URL             mqtt url to connect including port.
  --client_id CLIENT_ID
                        mqtt client id. if use client certificate, this value usually needs to match the certificate's common name.
  --topic TOPIC         mqtt topic prefix to subscribe.
  --ca_cert CA_CERT     ca certificate file path. if not provided, connection will be made without tls.
  --cert CERT           client certificate file path. used with --ca_cert.
  --key KEY             client private key file path. used with --ca_cert.
```

.env 파일 이용시 (환경변수) 예제

```.env
MQTT_URL = mqtt 브로커 주소 # ex) "mqtt-server.com:1883"
MQTT_CLIENT_ID = 클라이언트 아이디 # ex) "python.example"
MQTT_TOPIC = mqtt 토픽 접두어 # ex) "test-lab/bess/pcs-0"

MQTT_CA_CERT = CA 인증서 (선택적) # ex) "cert.mqtt/ca.crt.pem"
MQTT_CERT = 클라이언트 인증서 (선택적) # ex) "cert.mqtt/client.crt.pem"
MQTT_KEY = 클라이언트 비밀키 (선택적) # ex) "cert.mqtt/client.key.pem"
```
