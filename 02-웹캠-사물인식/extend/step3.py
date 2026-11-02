# 2부 확장 3단계: 사람 수 + 신뢰도 슬라이더 + 물체 고르기
# 실행: python extend/step3.py  →  브라우저 주소창에 http://127.0.0.1:5000   /   끝내기: 터미널에서 Ctrl+C

# OpenCV(파이썬에서 카메라·사진을 다루는 도구)를 cv2 라는 이름으로 불러온다
import cv2
# Flask(웹사이트를 만드는 도구), Response(브라우저에 보낼 답장), request(브라우저가 보낸 값)를 불러온다
from flask import Flask, Response, request
# ultralytics 도구에서 YOLO(사진 속 물체를 찾아 주는 AI)를 불러온다
from ultralytics import YOLO

# 웹앱(웹사이트 프로그램)을 하나 만든다
app = Flask(__name__)
# AI 모델 파일을 읽는다. 처음 한 번은 인터넷에서 저절로 받는다
model = YOLO("yolo26n.pt")
# 0번 카메라(노트북 기본 웹캠)를 켠다. 안 되면 0 을 1 로 바꿔 본다
cap = cv2.VideoCapture(0)

# 신뢰도 기준(0~1). AI 가 「이게 맞다」고 믿는 정도가 이보다 낮으면 화면에 안 그린다
CONF = 0.25
# 찾을 물체 번호 목록. None 이면 전부 찾는다(0 = 사람, 41 = 컵, 67 = 휴대폰)
CLASSES = None

# 첫 화면 HTML. 슬라이더로 신뢰도를, 고르기 칸으로 찾을 물체를 바꾼다
PAGE = """<h1>웹캠 사물인식</h1>
<p>신뢰도 <input type="range" min="0.05" max="0.95" step="0.05" value="0.25"
 oninput="fetch('/conf?v=' + this.value); c.textContent = this.value"> <b id="c">0.25</b></p>
<p>찾을 물체 <select onchange="fetch('/only?id=' + this.value)">
 <option value="">전부</option><option value="0">사람</option>
 <option value="41">컵</option><option value="67">휴대폰</option></select></p>
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
        # AI 에게 보여 주되, 신뢰도는 CONF 이상, 물체는 CLASSES 에 든 것만 찾는다(None 이면 전부)
        result = model(frame, conf=CONF, classes=CLASSES)[0]
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


# 누군가 /conf 주소로 값을 보내면 아래 함수를 실행한다
@app.route("/conf")
# 신뢰도 바꾸기 함수
def set_conf():
    # 함수 밖의 CONF 를 고치겠다고 알린다
    global CONF
    # 주소 뒤 ?v= 에 붙어 온 글자를 숫자로 바꿔 CONF 에 넣는다
    CONF = float(request.args["v"])
    # 잘 받았다고 답한다
    return "ok"


# 누군가 /only 주소로 물체 번호를 보내면 아래 함수를 실행한다
@app.route("/only")
# 찾을 물체 바꾸기 함수
def set_only():
    # 함수 밖의 CLASSES 를 고치겠다고 알린다
    global CLASSES
    # 주소 뒤 ?id= 에 붙어 온 글자를 꺼낸다
    v = request.args["id"]
    # 비어 있으면(「전부」) None, 아니면 그 번호 하나만 든 목록으로 정한다
    CLASSES = None if v == "" else [int(v)]
    # 잘 받았다고 답한다
    return "ok"


# 이 파일을 직접 실행했을 때만 웹앱을 켠다
if __name__ == "__main__":
    # 내 컴퓨터(127.0.0.1)의 5000번 문으로 웹앱을 켠다
    app.run(host="127.0.0.1", port=5000)
