import asyncio
import edge_tts
from pydub import AudioSegment
import os

# 1부터 100까지의 숫자를 순우리말(하나, 둘, 셋...)로 변환하는 함수
def get_korean_number(n):
  if n == 100: return '백'
  
  units = ['', '하나', '둘', '셋', '넷', '다섯', '여섯', '일곱', '여덟', '아홉']
  tens = ['', '열', '스물', '서른', '마흔', '쉰', '예순', '일흔', '여든', '아흔']
  
  t = n // 10
  u = n % 10
  
  result = tens[t]
  if u > 0: result += units[u]
      
  return result

async def generate_squat_audio_with_bgm():
  print('경쾌한 여성 목소리로 오디오 생성 중... 시간이 조금 걸릴 수 있습니다.')

  # 음성 트랙 초기화 (시작 전 1초 대기)
  voice_track = AudioSegment.silent(duration=1000)
  
  # 간격 조절용 묵음 설정: 1.5초 (1500 밀리초)
  pause = AudioSegment.silent(duration=1500)

  # edge-tts 보이스 설정 (경쾌한 한국어 여성 목소리)
  voice_model = 'ko-KR-SunHiNeural'

  for i in range(1, 101):
    # 숫자를 순우리말 텍스트로 변환
    korean_text = get_korean_number(i)
    
    # edge-tts로 음성 파일 생성 및 저장
    temp_file = f'../data/audio/temp_{i}.mp3'
    communicate = edge_tts.Communicate(korean_text, voice_model, rate='+10%') # 약간 빠르게 설정하여 경쾌함 추가
    await communicate.save(temp_file)

    # 생성된 음성 파일을 pydub 오디오 객체로 불러오기
    voice = AudioSegment.from_mp3(temp_file)

    # [숫자음성] + [1.5초 대기] 순서로 이어붙이기
    voice_track += voice + pause

    # 임시 파일 삭제
    os.remove(temp_file)

    # 진행 상황 출력
    if i % 10 == 0:
      print(f'{i}개 음성 생성 완료...')

  # 배경음악 추가 파트
  bgm_file = '../data/audio/bgm.mp3'  # 사용자가 준비한 배경음악 파일 이름
  
  if os.path.exists(bgm_file):
    print('배경음악을 합성하는 중입니다...')
    bgm = AudioSegment.from_file(bgm_file)
    
    # 목소리가 잘 들리도록 배경음악 볼륨 감소 (예: -15dB)
    bgm = bgm - 15
    
    # 배경음악 길이가 음성 트랙보다 짧으면 반복해서 이어붙이기
    while len(bgm) < len(voice_track):
        bgm += bgm
        
    # 음성 트랙의 길이에 맞춰 배경음악 자르기
    bgm = bgm[:len(voice_track)]
    
    # 배경음악과 음성 트랙 합성
    final_audio = bgm.overlay(voice_track)
  else:
    print(f'{bgm_file} 파일이 없어 배경음악 없이 목소리만 저장합니다.')
    final_audio = voice_track

  # 최종 오디오 파일 저장
  output_filename = '../data/audio/squat_100_cheerful_female.mp3'
  final_audio.export(output_filename, format='mp3')
  print(f'완료! {output_filename} 파일이 성공적으로 저장되었습니다.')

if __name__ == '__main__':
  # 비동기 함수 실행
  asyncio.run(generate_squat_audio_with_bgm())