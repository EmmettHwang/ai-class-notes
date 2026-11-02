# 01. 코랩에서 YOLO 사물인식(detect)

> 🎯 **대상: 비전공 · 프로그래밍 처음인 학생**

[← 목차로](../README.md) · 다음 시간: [02 웹캠 사물인식](../02-웹캠-사물인식/README.md)

## 지난 시간에 한 것

- Colab(인터넷 속 컴퓨터에서 파이썬을 돌리는 곳) 둘러보기 — <https://colab.research.google.com/notebooks/intro.ipynb>
- 간편한 표준 에디터 **마크다운** 보기 — <https://colab.research.google.com/notebooks/markdown_guide.ipynb>
- YOLO 를 이용한 사물인식 — 「객체 탐지 (Object Detection) - YOLO의 모든것」 노트북 <https://colab.research.google.com/drive/1dtJG0gzXJD4R5dXePizcTcal_lXdIYS2>

## 배운 것

1. **객체 탐지란?**
   > 사진 속에서 **무엇이**(사람·버스·컵…) **어디에** 있는지 찾아 네모 상자로 표시하는 것입니다.
   > 상자 옆 숫자는 AI 가 「이게 맞다」고 믿는 정도(신뢰도)입니다.
   > YOLO 는 이 일을 아주 빠르게 하는 AI 의 이름입니다.
2. `detect.py` 라는 소스코드에 몇 가지 파라미터(실행할 때 넣어 주는 설정값)를 넣어서 **내 사진까지** 인식해 보았습니다.

## 다음에 할 것 (보류해 둔 것)

- **나만의 모델 만들기** — 포트홀(도로 파임) 감지, 산불 감지, 헬멧 미착용자 감지 등
