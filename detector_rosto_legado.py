import cv2
import numpy as np
import time

class DriverMonitor:
    def __init__(self):
        # Carregar classificadores Haar Cascade
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Limiares e Configurações
        self.CONSECUTIVE_FRAMES_SLEEP = 15  # Olhos não detectados
        self.CONSECUTIVE_FRAMES_DISTRACTED = 20 # Rosto não detectado
        
        # Estado
        self.sleep_counter = 0
        self.distraction_counter = 0
        self.is_sleeping = False
        self.is_distracted = False
        self.face_present = False

    def process_frame(self, frame, fps):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 1. Detecção de Rosto
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        status_text = "Status: Normal"
        status_color = (0, 255, 0)
        
        if len(faces) > 0:
            self.face_present = True
            self.distraction_counter = 0
            
            # Pegar o maior rosto (geralmente o motorista)
            (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # Região de Interesse (ROI) para os olhos (metade superior do rosto)
            roi_gray = gray[y:y + int(h/2), x:x + w]
            roi_color = frame[y:y + int(h/2), x:x + w]
            
            # 2. Detecção de Olhos
            eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
            
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            
            # Lógica de Sono: Se não detectar olhos dentro do rosto
            if len(eyes) == 0:
                self.sleep_counter += 1
            else:
                self.sleep_counter = 0
                
            if self.sleep_counter >= self.CONSECUTIVE_FRAMES_SLEEP:
                self.is_sleeping = True
            else:
                self.is_sleeping = False
                
        else:
            # Rosto não detectado
            self.face_present = False
            self.distraction_counter += 1
            self.sleep_counter = 0
            
            if self.distraction_counter >= self.CONSECUTIVE_FRAMES_DISTRACTED:
                self.is_distracted = True
            else:
                self.is_distracted = False

        # Definição de Texto e Cor baseado no estado
        if self.is_sleeping:
            status_text = "ALERTA: SONO (OLHOS FECHADOS)!"
            status_color = (0, 0, 255)
        elif self.is_distracted:
            status_text = "ALERTA: DISTRACAO (ROSTO AUSENTE)!"
            status_color = (0, 0, 255)

        # Overlay de Status e FPS
        cv2.rectangle(frame, (0, 0), (500, 40), (0, 0, 0), -1)
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        cv2.putText(frame, f"FPS: {int(fps)}", (400, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Instruções de Debug
        cv2.putText(frame, f"Contador Sono: {self.sleep_counter}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Contador Distracao: {self.distraction_counter}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return frame

def main():
    monitor = DriverMonitor()
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        print("Erro: Não foi possível acessar a câmera.")
        return

    prev_time = time.time()

    while True:
        ret, frame = camera.read()
        if not ret:
            break
            
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
        prev_time = curr_time

        frame = cv2.flip(frame, 1) # Espelhar a imagem
        frame = monitor.process_frame(frame, fps)
        
        cv2.imshow("Monitor de Motorista (OpenCV)", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
