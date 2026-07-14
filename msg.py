import os
import time
import requests
import datetime as dt

url = 'https://discord.com/api/webhooks/1516685405100052500'
key = 'wfEAmZeZq2oHwPzNUsn2u2n-d60BApE8kSZgPWyDxaxbV2zbH_3z2j-HaPoCDI3MJRCr'
webhook_url = f'{url}/{key}'


def send_message(message):
  payload = {'content': message}
  response = requests.post(webhook_url, json=payload)
  if response.status_code == 204: print('메시지가 성공적으로 전송되었습니다!')
  else: print(f'전송 실패: 상태 코드 {response.status_code}')


def send_image(filename, message=''):
  # 1. 보낼 파일 열기 (바이너리 읽기 모드)
  if os.path.isfile(filename):
    fp = open(filename, 'rb')
    # 2. 디스코드에서 요구하는 'files' 포맷 데이터 구성; 파일명, 파일객체, 파일타입
    files = {'file': (filename, fp, f'image/{filename[-3:]}')}
    # 3. 텍스트 메시지가 있다면 함께 전송할 데이터에 추가
    data = {'content': message}
    
    # 4. 웹훅 URL로 POST 요청 보내기
    response = requests.post(webhook_url, data=data, files=files)
    
    # 5. 전송 결과 확인
    if response.status_code in [200, 204]:
      print("메시지와 이미지가 성공적으로 전송되었습니다!")
    else:
      print(f"전송 실패. 상태 코드: {response.status_code}")
      print(response.text)
  else:
    print(f"지정한 경로에서 파일을 찾을 수 없습니다: {filename}")


def one_hour_stand_up():
  print('운동 알람을 시작합니다.')
  while True:
    now = dt.datetime.now()
    
    # 현재 시간이 09:00 ~ 18:00 사이인지 확인
    if now.hour in [10, 11, 14, 15, 16, 17]:
      send_message(f'{now.strftime('%H:%M:%S')}, 운동하실 시간입니다.')
    
    # 다음 정각(예: 10:00:00)까지 남은 시간(초) 계산
    next_hour = now + dt.timedelta(hours=1)
    next_hour = next_hour.replace(minute=0, second=0, microsecond=0)
    sleep_seconds = (next_hour - now).total_seconds()
    
    # 다음 정각까지 프로그램 대기
    time.sleep(sleep_seconds)


if __name__ == '__main__':
  # at = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  # send_to_discord(f'{at}, 라즈베리파이에서 보냅니다.')
  # one_hour_stand_up()
  send_image('../data/people/2026-07-13-133311.jpg', '시험')
