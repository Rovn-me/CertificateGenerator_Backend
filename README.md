# Certificate Generator Backend (Flask)

This is a Flask-based backend that generates certificates from a template image, custom font, and CSV data. The output is a downloadable ZIP archive containing the generated certificates in image format.

## Features

- Upload template image
- Upload font file (.ttf)
- Upload CSV file with recipient data
- Define multiple dynamic text fields with custom positions and sizes
- Specify text color in HEX format
- Returns all certificates as a ZIP archive
- Supports CORS for frontend integration

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/certificate-generator-backend.git
cd certificate-generator-backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

Using Flask:

```bash
flask run --port=8030
```

Using Gunicorn (for production):

```bash
gunicorn -w 1 -b 0.0.0.0:8030 app:app
```

## API Endpoint

### POST `/generate`

Accepts a multipart/form-data request with the following fields:

| Field     | Type            | Required | Description                                  |
|-----------|-----------------|----------|----------------------------------------------|
| template  | File (.png/.jpg)| Yes      | The certificate background image             |
| font      | File (.ttf)     | Yes      | The font file used for rendering text        |
| csv       | File (.csv)     | Yes      | CSV file with column headers matching field names |
| fields    | JSON string     | Yes      | List of field definitions with coordinates   |
| color     | String (hex)    | Yes      | Text color in HEX format (e.g., `#000000`)   |

### Sample Field Data

```json
[
  { "name": "Name", "x": 200, "y": 300, "size": 40 },
  { "name": "Course", "x": 200, "y": 400, "size": 30 }
]
```

### Sample Curl Request

```bash
curl -X POST http://localhost:8030/generate \
  -F "template=@template.png" \
  -F "font=@Poppins-Regular.ttf" \
  -F "csv=@participants.csv" \
  -F "fields=$(cat fields.json)" \
  -F "color=#000000" \
  --output certificates.zip
```

## CORS Support

The server is CORS-enabled using Flask-CORS to allow frontend integration from different origins.

## Technologies Used

- Python
- Flask
- Pillow (PIL)
- Flask-CORS
- Gunicorn (optional)

## License

MIT License
