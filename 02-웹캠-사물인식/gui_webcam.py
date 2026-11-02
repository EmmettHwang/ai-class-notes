# 1부: 웹캠으로 사물인식 — GUI(창) 버전
# 실행: python gui_webcam.py   /   끝내기: 창을 누른 뒤 q 키

# OpenCV(파이썬에서 카메라·사진을 다루는 도구)를 cv2 라는 이름으로 불러온다
import cv2
# ultralytics 도구에서 YOLO(사진 속 물체를 찾아 주는 AI)를 불러온다
from ultralytics import YOLO

# AI 모델 파일을 읽는다. 처음 한 번은 인터넷에서 저절로 받는다(n = 가장 작고 빠른 것)
model = YOLO("yolo26n.pt")
# 0번 카메라(노트북 기본 웹캠)를 켠다. 안 되면 0 을 1 로 바꿔 본다
cap = cv2.VideoCapture(0)

# 카메라가 켜져 있는 동안 계속 되풀이한다
while cap.isOpened():
    # 카메라에서 프레임(영상의 사진 한 장)을 하나 읽는다. ok = 잘 읽었는지(참/거짓)
    ok, frame = cap.read()
    # 못 읽었으면(카메라가 꺼졌으면) 되풀이를 멈춘다
    if not ok:
        break
    # 사진 한 장을 AI 에게 보여 주고 무엇이 어디 있는지 결과를 받는다
    results = model(frame)
    # 결과를 사진 위에 네모 상자와 이름표로 그린다
    annotated = results[0].plot()
    # 그린 사진을 "YOLO" 라는 이름의 창에 띄운다
    cv2.imshow("YOLO", annotated)
    # 1밀리초 동안 키보드를 보고, q 키가 눌렸으면 멈춘다
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 카메라를 끈다(다른 프로그램이 쓸 수 있게 돌려준다)
cap.release()
# 열려 있는 창을 모두 닫는다
cv2.destroyAllWindows()
