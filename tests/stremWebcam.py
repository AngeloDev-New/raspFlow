import cv2
from ultralytics import YOLO
import os
from threading import Thread

# Caminho do modelo
network = 'networks/network.pt'

#web cam
cap = cv2.VideoCapture(3)

if not cap.isOpened():
    print('Erro ao abrir WebCam')
    exit()

class Promisse(Thread):
    def __init__(self, frame_inicial):
        super().__init__()
        self.model = YOLO(network)
        self.frame = frame_inicial
        self.detecting = True
        self.result_frame = frame_inicial.copy()
        self.result = None
    
    def run(self):
        while self.detecting:
            results = self.model(self.frame, conf=0.30)
            self.result = results[0]
    
    def getFrame(self):
        # Desenha as detecções
        if not self.result:
            return self.frame
        
        # Cria uma cópia para não modificar o frame original durante a leitura
        display_frame = self.frame.copy()
        
        for box in self.result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = self.model.names[cls] if hasattr(self.model, "names") else str(cls)
            
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                display_frame,
                f"{label} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
        
        return display_frame
    
    def atualize(self, novo_frame):
        self.frame = novo_frame
    
    def release(self):
        self.detecting = False

# Captura o primeiro frame
ret, frame = cap.read()
if not ret:
    print("Erro ao capturar o primeiro frame")
    cap.release()
    exit()

# Inicia a thread de detecção
promisse = Promisse(frame)
promisse.start()

# Loop principal
print("Processando vídeo... Pressione 'q' para sair")
while True:
    ret, frame = cap.read()
    if not ret:
        print('Fim do vídeo ou erro ao capturar frame')
        break
    
    # Atualiza o frame no objeto Promisse
    promisse.atualize(frame)
    
    # Mostra o frame processado
    cv2.imshow('WebCam Video Detection', promisse.getFrame())
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

promisse.release()
promisse.join()
cap.release()
cv2.destroyAllWindows()