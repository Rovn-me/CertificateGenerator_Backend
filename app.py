from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import csv
import io
import zipfile
import json

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate_certificates():
    try:
        print("[Server] Received request...")

        # Get files and data
        template_file = request.files.get('template')
        font_file = request.files.get('font')
        csv_file = request.files.get('csv')
        color_hex = request.form.get('color', '#000000')
        fields = json.loads(request.form.get('fields', '[]'))

        print(f"[Server] Color: {color_hex}")
        print(f"[Server] Fields: {fields}")

        if not template_file or not font_file or not csv_file:
            return {"error": "Missing one or more required files"}, 400

        # Read input files
        template_data = template_file.read()
        font_data = io.BytesIO(font_file.read())
        csv_data = csv.DictReader(io.StringIO(csv_file.read().decode('utf-8')))
        entries = list(csv_data)

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            for idx, row in enumerate(entries):
                print(f"[Server] Generating for: {row}")
                img = Image.open(io.BytesIO(template_data)).convert("RGBA")
                draw = ImageDraw.Draw(img)

                for field in fields:
                    value = row.get(field['name'], '')
                    if not value:
                        continue
                    
                    font_data.seek(0)  # ✅ Reset pointer before loading
                    font = ImageFont.truetype(font_data, size=int(field['size']))
                    draw.text((int(field['x']), int(field['y'])), value, font=font, fill=color_hex)
                    print(f"    ↳ {field['name']}: '{value}' at ({field['x']}, {field['y']})")


                img_io = io.BytesIO()
                filename = f"{idx+1}_{row[fields[0]['name']].replace(' ', '_')}.png"
                img.save(img_io, format='PNG')
                img_io.seek(0)
                zipf.writestr(filename, img_io.read())

        zip_buffer.seek(0)
        print("[Server] ZIP ready. Sending to frontend.")
        return send_file(zip_buffer, download_name='certificates.zip', as_attachment=True)

    except Exception as e:
        print(f"[Server] ❌ Error: {e}")
        return {"error": str(e)}, 500

if __name__ == '__main__':
    print("🚀 Flask backend running at http://localhost:8030")
    app.run(port=8030, debug=True)
