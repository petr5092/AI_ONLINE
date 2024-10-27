from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2

def index(request):
	return render(request, 'video/main.html')

def show_drone(request):
	return render(request, 'video/show.html')

def stream_response(request):
    response = StreamingHttpResponse(ai_show(), content_type='multipart/x-mixed-replace; boundary=frame')
    return response

def ai_show():
    fire_cascade = cv2.CascadeClassifier('core/apps/video/fire_detection_cascade_model.xml')
    vid = cv2.VideoCapture('core/apps/video/videos/video6.mp4')
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    while True:
        frame = ai_viedo(vid, fire_cascade)
        yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def ai_viedo(vid: cv2.VideoCapture, fire_cascade: cv2.CascadeClassifier):
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(gray, 1.2, 5)
    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 2)
    frame_flip = cv2.flip(frame, 1)
    ret, jpeg = cv2.imencode('.jpg', frame_flip)
    return jpeg.tobytes()

