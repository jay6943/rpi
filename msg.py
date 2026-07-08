import time
import requests
import datetime as dt


def one_hour_stand_up():
  print('운동 알람을 시작합니다.')
  while True:
    now = dt.datetime.now()
    
    # 현재 시간이 09:00 ~ 18:00 사이인지 확인
    if 9 <= now.hour <= 18:
        print(f"[{now.strftime('%H:%M:%S')}] 운동")
    
    # 다음 정각(예: 10:00:00)까지 남은 시간(초) 계산
    next_hour = (now + dt.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    sleep_seconds = (next_hour - now).total_seconds()
    
    # 다음 정각까지 프로그램 대기
    time.sleep(sleep_seconds)
    send_to_discord('운동하실 시간입니다.')


def send_to_discord(message):
  url = 'https://discord.com/api/webhooks/1516685405100052500'
  key = 'wfEAmZeZq2oHwPzNUsn2u2n-d60BApE8kSZgPWyDxaxbV2zbH_3z2j-HaPoCDI3MJRCr'
  payload = {'content': message}
  response = requests.post(f'{url}/{key}', json=payload)
  if response.status_code == 204: print('메시지가 성공적으로 전송되었습니다!')
  else: print(f'전송 실패: 상태 코드 {response.status_code}')


if __name__ == '__main__':
  # at = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  # send_to_discord(f'{at}, 라즈베리파이에서 보냅니다.')
  one_hour_stand_up()
