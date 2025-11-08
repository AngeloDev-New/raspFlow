from flask import Flask, render_template,request,Response,jsonify,url_for
# from scripts import ...
# import 
app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def home():
    if request.method == "POST":
        files = request.files
        data = request.json
        print(files,data)
        return Response("Imagens Recebitadas",status=200,mimetype='text/plain')
    print('#############')
    return render_template("index.html")



@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "Controle de fluxo",
        "short_name": "TransitControll",
        "start_url": "/",
        "display": "fullscreen",
        "background_color": "#000000",
        "theme_color": "#000000",
        "icons": [
            {"src": url_for('static', filename='icons/icon-192.png'), "sizes": "192x192", "type": "image/png"},
            {"src": url_for('static', filename='icons/icon-512.png'), "sizes": "512x512", "type": "image/png"}
        ]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
