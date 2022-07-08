from flask import Flask, Response, render_template
import cv2
import model_process

app = Flask(__name__, template_folder="templates")
video = cv2.VideoCapture(0)


@app.route("/")
def index():
    return render_template("index_test.html")


@app.route("/dd")
def dd():
    return Response(model_process.get_gesture_text(), mimetype="text")


@app.route("/process_feed")
def process_feed():
    global video
    return Response(
        model_process.analyze(video,mode="count"),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2204, threaded=True)
