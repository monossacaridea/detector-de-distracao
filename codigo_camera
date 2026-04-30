import cv2

caminho = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

detector_rosto = cv2.CascadeClassifier(caminho)
camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Camera", frame)
    rostos = detector_rosto.detectMultiScale(cinza)
    for (x, y, w, h) in rostos:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
