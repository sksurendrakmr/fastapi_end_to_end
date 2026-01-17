# FastAPI Tutorial

## Installation

```bash
uv add "fastapi[standard]"
```

The `[standard]` extra includes commonly-used dependencies:

- **uvicorn** - ASGI web server to run your FastAPI application
- **pydantic-settings** - Configuration management
- **python-multipart** - Form data and file upload handling
- **email-validator** - Email validation support
- **fastapi-cli** - Used to run our app
- **jinja2** - Template engine for rendering HTML responses

This gives you a complete setup without needing to install additional packages manually.

## Running the Application

### Development Mode

```bash
uv run fastapi dev main.py
```

This starts the development server with auto-reload enabled, perfect for development and testing.

### Production Mode

```bash
uv run fastapi run main.py
```

This runs the application in production mode without auto-reload, optimized for performance and stability.

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI** - `/docs`
- **ReDoc** - `/redoc`

Visit these endpoints in your browser to explore and test your API endpoints.
