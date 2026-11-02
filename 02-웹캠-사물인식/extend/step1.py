# 2부 확장 1단계: 화면에 사람 수 표시
# 실행: python extend/step1.py  →  브라우저 주소창에 http://127.0.0.1:5000   /   끝내기: 터미널에서 Ctrl+C

# OpenCV(파이썬에서 카메라·사진을 다루는 도구)를 cv2 라는 이름으로 불러온다
import cv2
# Flask(파이썬으로 작은 웹사이트를 만드는 도구)와 Response(브라우저에 보낼 답장)를 불러온다
from flask import Flask, Response
# ultralytics 도구에서 YOLO(사진 속 물체를 찾아 주는 AI)를 불러온다
from ultralytics import YOLO

# 웹앱(웹사이트 프로그램)을 하나 만든다
app = Flask(__name__)
# AI 모델 파일을 읽는다. 처음 한 번은 인터넷에서 저절로 받는다
model = YOLO("yolo26n.pt")
# 0번 카메라(노트북 기본 웹캠)를 켠다. 안 되면 0 을 1 로 바꿔 본다
cap = cv2.VideoCapture(0)

# 첫 화면에 보여 줄 HTML(웹페이지 글). <img> 칸이 /video 주소의 영상을 받아 보여 준다
PAGE = """<h1>웹캠 사물인식</h1>
<img src="/video" width="640">"""


# 사진을 한 장씩 끝없이 만들어 내보내는 함수(이렇게 계속 내보내는 함수를 '제너레이터'라고 한다)
def frames():
    # 계속 되풀이한다
    while True:
        # 카메라에서 프레임(영상의 사진 한 장)을 하나 읽는다. ok = 잘 읽었는지
        ok, frame = cap.read()
        # 못 읽었으면 멈춘다
        if not ok:
            break
        # AI 에게 보여 주고 첫 번째 결과를 받는다
        result = model(frame)[0]
        # 결과를 사진 위에 네모 상자와 이름표로 그린다
        annotated = result.plot()
        # 결과 안의 물체 번호 목록에서 0번(사람)이 몇 개인지 센다
        people = result.boxes.cls.tolist().count(0)
        # 사진 왼쪽 위(20, 40 자리)에 사람 수를 초록 글씨로 쓴다(영어만 된다)
        cv2.putText(annotated, f"People: {people}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        # 그린 사진을 JPG(인터넷에서 흔히 쓰는 사진 형식)로 바꾼다
        ok, jpg = cv2.imencode(".jpg", annotated)
        # 브라우저가 알아듣는 모양(구분선 + 사진 종류 + 사진 내용)으로 한 장을 내보낸다
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg.tobytes() + b"\r\n"


# 누군가 첫 화면(/) 주소로 들어오면 아래 함수를 실행한다
@app.route("/")
# 첫 화면 함수
def index():
    # 위에서 만든 웹페이지 글을 돌려준다
    return PAGE


# 누군가 /video 주소로 들어오면 아래 함수를 실행한다
@app.route("/video")
# 영상 함수
def video():
    # 사진을 줄줄이 이어 보내 영상처럼 보이게 한다(MJPEG = 사진을 이어 붙인 영상)
    return Response(frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


# 이 파일을 직접 실행했을 때만 웹앱을 켠다
if __name__ == "__main__":
    # 내 컴퓨터(127.0.0.1)의 5000번 문으로 웹앱을 켠다
    app.run(host="127.0.0.1", port=5000)
