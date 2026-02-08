# Image Analysis API

A robust FastAPI-based backend service for analyzing skin images. This API allows users to upload images and receive detailed analysis regarding skin type, issues, and health metrics.

## Features

- **Image Upload**: securely upload JPEG or PNG images.
- **AI Analysis**: automated skin analysis for type (Oily, Dry, etc.), issues (Acne, Wrinkles), and confidence scores.
- **Detailed Metrics**: optional detailed report including hydration, oil index, elasticity, and specific recommendations.
- **Docker Support**: fully containerized for easy deployment.
- **API Key Security**: simple header-based authentication.

## Prerequisites

- **Python**: 3.11+
- **Docker**: (Optional, for containerized deployment)

## Local Development Setup

1.  **Clone the repository**
    ```bash
    git clone <repository_url>
    cd image-analysis-api
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

## Docker Setup

1.  **Build the image**
    ```bash
    docker build -t image-analysis-api .
    ```

2.  **Run the container**
    ```bash
    docker run -d -p 8000:8000 --name image-analysis-container image-analysis-api
    ```

3.  **Check logs**
    ```bash
    docker logs -f image-analysis-container
    ```

## API Documentation

Once the app is running, interactive documentation is available at:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### Key Endpoints

**Base URL**: `http://127.0.0.1:8000`

#### 1. Upload Image
*   **Endpoint**: `/upload`
*   **Method**: `POST`
*   **Header**: `x-api-key: dev-api-key-12345` (default)
*   **Body**: Form-data with key `file`

#### 2. Analyze Image
*   **Endpoint**: `/analyze`
*   **Method**: `POST`
*   **Header**: `x-api-key: dev-api-key-12345`
*   **Body (JSON)**:
    ```json
    {
      "image_id": "<your_image_id>",
      "detailed": true
    }
    ```

#### 3. Health Check
*   **Endpoint**: `/health`
*   **Method**: `GET`

## Configuration

The application uses the following default configuration (can be overridden via environment variables):

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEY` | `dev-api-key-12345` | Simple authentication key |

## Project Structure

```
image-analysis-api/
├── app/
│   ├── routes/         # API endpoints (upload, analyze)
│   ├── services/       # Business logic (analysis, storage)
│   ├── utils/          # Helpers (logging, validation)
│   ├── config.py       # App configuration
│   └── main.py         # App entry point
├── uploads/            # Local storage for uploaded images
├── Dockerfile          # Container definition
├── requirements.txt    # Python dependencies
└── README.md           # Documentation.
```
