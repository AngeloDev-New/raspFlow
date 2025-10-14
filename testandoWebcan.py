from flask import Flask, Response, jsonify
import cv2
import threading
import pyaudio
import wave
import io

app = Flask(__name__)

# Dicionário global com câmeras abertas
cameras = {}
locks = {}

# Configuração de áudio
audio_devices = []
p = pyaudio.PyAudio()

def get_audio_devices():
    """Lista todos os dispositivos de áudio disponíveis"""
    devices = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:  # Apenas dispositivos de entrada
            devices.append({
                'index': i,
                'name': info['name'],
                'channels': info['maxInputChannels']
            })
    return devices

def generate_frames(camera_index):
    """Gera frames MJPEG da câmera"""
    if camera_index not in cameras:
        cameras[camera_index] = cv2.VideoCapture(camera_index)
        locks[camera_index] = threading.Lock()
    
    while True:
        with locks[camera_index]:
            success, frame = cameras[camera_index].read()
            if not success:
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_audio(device_index, channels=1, rate=44100):
    """Gera stream de áudio do microfone"""
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    
    try:
        stream = p.open(
            format=FORMAT,
            channels=channels,
            rate=rate,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=CHUNK
        )
        
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            yield data
            
    except Exception as e:
        print(f"Erro no áudio: {e}")
    finally:
        if stream:
            stream.stop_stream()
            stream.close()

@app.route('/frame/<int:num>')
def video_feed(num):
    """Endpoint para stream de vídeo"""
    return Response(
        generate_frames(num),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/audio/<int:device_index>')
def audio_feed(device_index):
    """Endpoint para stream de áudio"""
    return Response(
        generate_audio(device_index),
        mimetype='audio/x-raw'
    )

@app.route('/audio/devices')
def list_audio_devices():
    """Lista dispositivos de áudio disponíveis"""
    devices = get_audio_devices()
    return jsonify(devices)

@app.route('/')
def home():
    """Página principal"""
    with open('index.html', 'r', encoding='utf-8') as HTML:
        html = HTML.read()
    return Response(html, mimetype='text/html')

if __name__ == '__main__':
    print("Dispositivos de áudio disponíveis:")
    for dev in get_audio_devices():
        print(f"  [{dev['index']}] {dev['name']} ({dev['channels']} canais)")
    
    app.run(host='0.0.0.0', port=8080, threaded=True)