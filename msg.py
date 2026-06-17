import requests
import datetime as dt


def send_to_discord(message):
  url = 'https://discord.com/api/webhooks/1516685405100052500'
  key = 'wfEAmZeZq2oHwPzNUsn2u2n-d60BApE8kSZgPWyDxaxbV2zbH_3z2j-HaPoCDI3MJRCr'
  payload = {'content': message}
  response = requests.post(f'{url}/{key}', json=payload)
  if response.status_code == 204: print('메시지가 성공적으로 전송되었습니다!')
  else: print(f'전송 실패: 상태 코드 {response.status_code}')


if __name__ == '__main__':
  at = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  send_to_discord(f'{at}, 라즈베리파이에서 보냅니다.')
