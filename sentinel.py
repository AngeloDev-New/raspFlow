from ultralytics import YOLO
import cv2
import re
import torch
import io
from fast_plate_ocr import LicensePlateRecognizer

class Sentinel():
    def __init__(self,model,Observer,FluxOrientation,Persistence,decoder,output = False):
        self.model = YOLO(model)
        self.observer = Observer
        self.orientation = FluxOrientation
        self.Persistence = Persistence
        self.decoder = decoder
        self.run()

    def run(self):
        for frame in self.observer():
            print('captura')
            results = self.model.predict(
                source = frame,
                imgsz=608,
                conf=0.25
            )
            for r in results:
                for box in r.boxes.xyxy:
                    xmin, ymin, xmax, ymax = map(int, box)
    
        

if __name__=='__main__':
    def decoder(plate):
        m = LicensePlateRecognizer('cct-xs-v1-global-model')
        plateString = m.run(plate)
        text = plateString.strip().upper()
        pattern = r"[A-Z]{3}[- ]?\d{4}|[A-Z]{3}\d[A-Z]\d{2}"
        match = re.search(pattern, text)
        if match:
            return match.group(0).replace(" ", "").replace("-", "")
        return None

    def observer(c = 0):
        cam = cv2.VideoCapture(c)
        ret = True
        while ret:
            ret,frame = cam.read()
            print('Entregando Frame')
            yield frame

    sentinel = Sentinel(
        model='v8n_augmentado_plate_vecicle.pt',
        Observer=observer,
        FluxOrientation=0,
        Persistence='/src',
        decoder = decoder,
        output = True        
    )
    
