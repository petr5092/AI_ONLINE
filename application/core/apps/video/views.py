from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
import pygame # type: ignore

pygame.mixer.init()

def index(request):
	return render(request, 'video/main.html')

def show_drone(request):
	return render(request, 'video/show.html')

def stream_response(request):
    response = StreamingHttpResponse(ai_show(), content_type='multipart/x-mixed-replace; boundary=frame')
    return response

def ai_show():
    fire_cascade = cv2.CascadeClassifier('core/apps/video/fire_detection_cascade_model.xml')
    vid = cv2.VideoCapture('core/apps/video/videos/video.mp4')
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    while True:
        frame, flaq = ai_viedo(vid, fire_cascade)
        yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def ai_viedo(vid: cv2.VideoCapture, fire_cascade: cv2.CascadeClassifier):
    flaq = 0
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(gray, 1.2, 5)
    if len(fire) != 0:
        sound = pygame.mixer.Sound('core/apps/video/videos/mgs-alert.mp3')
        sound.play()
    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 2)
    frame_flip = cv2.flip(frame, 1)
    ret, jpeg = cv2.imencode('.jpg', frame_flip)
    return (jpeg.tobytes(), flaq)


def audio_generator(request):
    return StreamingHttpResponse(audio_generat(), content_type='audio/mpeg')


def audio_generat():
    print(1)
    with open('core/apps/video/videos/mgs-alert.mp3', 'rb') as f:
        while chunk := f.read(1024):
             yield chunk

'''def send_email():
    msg_content = create_alerts()
    server = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) 
    server.login("abobalox53@gmail.com", "Irina709")
    server.send_message(msg_content)


def create_alerts():
    email = EmailMessage()
    email["Subject"] = "Оповещение"
    email['From'] = "abobalox53@gmail.com"
    email['To'] = "payplayfish@gmail.com"
    email.set_content(
        f"""
            <h1>Оповещение</h1"
            Оповещение
        """
    )
    return email'''