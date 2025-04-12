from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import csv, io, zipfile, os, time
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

@app.route('/generate', methods=['POST'])
def generate_certificates():
    log("Received certificate generation request")

    template_file = request.files.get('template')
    font_file = request.files.get('font')
    csv_file = request.files.get('csv')
    fields = request.form.get('fields')

    if not template_file or not font_file or not csv_file or not fields:
        return jsonify({'error': 'Missing file or field data'}), 400

    fields = eval(fields)  # convert JSON string to list of dicts
    log(f"Fields received: {fields}")

    font_path = 'temp_font.ttf'
    template_path = 'temp_template.png'

    # Save template and font temporarily
    template_file.save(template_path)
    font_file.save(font_path)

    image = Image.open(template_path)
    width, height = image.size

    # Prepare ZIP in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        reader = csv.DictReader(io.StringIO(csv_file.read().decode()))
        for i, row in enumerate(reader):
            cert = image.copy()
            draw = ImageDraw.Draw(cert)

            for field in fields:
                name = field['name']
                x, y, size = field['x'], field['y'], field['size']
                text = row.get(name, '')

                log(f"[{i+1}] Adding '{text}' at ({x},{y}) with size {size}")

                font = ImageFont.truetype(font_path, size)
                draw.text((x, y), text, font=font, fill='white')

            filename = f"{i+1}_{row.get(fields[0]['name'], 'unknown').replace(' ', '_')}.png"
            buffer = io.BytesIO()
            cert.save(buffer, format="PNG")
            buffer.seek(0)
            zipf.writestr(filename, buffer.read())

    zip_buffer.seek(0)

    # Cleanup
    os.remove(template_path)
    os.remove(font_path)

    log("Certificates generated successfully. Sending ZIP file.")
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='certificates.zip')


def log(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

if __name__ == '__main__':
    app.run(debug=True, port=8030)
