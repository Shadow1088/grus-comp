# 📦 File Compressor

A modern Flask web application for compressing images and videos with an intuitive UI and powerful compression algorithms.

## 🛠 Technologies Used

### Backend
- **Flask** (3.1.2) - Lightweight Python web framework for building the server
- **Flask-WTF** (1.2.2) - Form handling and CSRF protection
- **WTForms** (3.2.1) - Robust form validation
- **Pillow** (12.1.0) - Python Imaging Library for image processing and compression
- **ffmpeg-python** - Python wrapper for FFmpeg for video compression
- **Gunicorn** (23.0.0) - Production WSGI server for deploying Flask

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients, animations, and responsive design
- **Jinja2** (3.1.6) - Template engine for dynamic HTML generation

### DevOps & Deployment
- **Docker** - Containerization for easy deployment
- **Docker Compose** - Multi-container orchestration

### System Dependencies
- **FFmpeg** - Multimedia framework for video processing and re-encoding

## ✨ Features

### Image Compression
- **Quality Optimization**: Intelligently reduces JPEG quality (starting at 85, down to 40) to achieve target file size
- **Resolution Scaling**: Dynamically shrinks image dimensions (90% proportional scaling) if quality reduction isn't enough
- **Format Support**: JPG, JPEG, PNG, GIF
- **Alpha Channel Handling**: Automatically converts RGBA and palletted images to RGB for JPEG compatibility
- **Configurable Size Limit**: Default 8MB max, easily adjustable

### Video Compression
- **Bitrate Calculation**: Intelligently calculates optimal bitrate based on video duration and target size
- **Resolution Scaling**: Automatically scales videos down to 720p maximum
- **Audio Preservation**: Maintains 128k audio bitrate for quality
- **Codec Optimization**: Uses libx264 video codec with "faster" preset for speed
- **Format Support**: MP4, MOV, AVI, and other FFmpeg-compatible formats
- **Muxing Overhead**: Accounts for 10% overhead in calculations

### Web Interface
- **Modern UI**: Beautiful gradient-based design with smooth animations
- **File Type Detection**: Automatically routes images to image compressor, videos to video compressor
- **Flash Messages**: User-friendly error and success notifications
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Feedback**: Download compressed files instantly after processing

### Error Handling
- **Try-Catch Protection**: Graceful error handling with user-friendly messages
- **File Type Validation**: Rejects unsupported file types
- **Size Validation**: Enforces maximum file size limits

## 📋 Limitations

1. **Video Processing Time**: Video compression can be slow depending on video length and bitrate. The app has a 120-second timeout per request.

2. **Minimum Dimensions**: Images cannot be shrunk below 2x2 pixels; videos scaled proportionally to maintain aspect ratio.

3. **Audio-Only Content**: Videos with very long durations may result in very low video bitrates to stay within size limits.

4. **Single File Processing**: Can only compress one file per upload request (no batch processing).

5. **Memory Usage**: Large files may consume significant RAM during processing. Consider increasing Docker memory limits for very large files.

6. **No Progressive Upload**: Files must be completely uploaded before processing begins.

7. **Temporary File Storage**: Intermediate files are created in system temp directory during processing.

8. **Format Limitations**: Some rare video codecs may not be supported by FFmpeg.

## 🚀 Installation & Setup

### Prerequisites
- Python 3.13+
- Docker & Docker Compose (for containerized deployment)
- FFmpeg (required for video compression)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Shadow1088/grus-comp.git
   cd grus-comp
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg:**
   - **Ubuntu/Debian:**
     ```bash
     sudo apt-get install ffmpeg
     ```
   - **macOS (Homebrew):**
     ```bash
     brew install ffmpeg
     ```
   - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use:
     ```bash
     choco install ffmpeg
     ```

5. **Run the Flask development server:**
   ```bash
   python run.py
   ```
   The app will be available at `http://localhost:5000`

### Docker Deployment

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Or build manually:**
   ```bash
   docker build -t file-compressor .
   docker run -p 5000:5000 file-compressor
   ```

3. **Access the application:**
   Open `http://localhost:5000` in your browser

### Environment Variables

Create a `.env` file for configuration (optional):
```
FLASK_ENV=development
FLASK_DEBUG=True
MAX_CONTENT_LENGTH=104857600  # 100MB
```

## 📁 Project Structure

```
grus-comp/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── routes.py             # URL routing and request handling
│   ├── forms.py              # WTForms form definitions
│   ├── utils/
│   │   └── compress.py       # Compression logic (images & videos)
│   ├── templates/
│   │   ├── base.html         # Base template
│   │   ├── upload.html       # Upload page
│   │   └── macros.html       # Reusable template components
│   └── static/
│       └── styles.css        # Modern CSS styling
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
├── .dockerignore             # Files to exclude from Docker build
└── README.md                 # This file
```

## 🔧 Configuration

### Max File Size
Edit `run.py` to change the maximum upload size:
```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

### Compression Targets
Edit `app/utils/compress.py` to adjust:
- `max_bytes` - Target compression size (default: 8MB for images, 8MB for videos)
- Image quality starting point and minimum quality
- Video resolution and bitrate settings

## 📊 How It Works

### Image Compression Flow
1. User uploads an image
2. App converts to RGB if needed (RGBA → RGB for JPEG)
3. Compresses with high quality (85) to BytesIO
4. If file size > target:
   - Reduce quality in 5-point increments
   - If still over, shrink dimensions by 10% proportionally
   - Repeat until size target is met
5. Return compressed image

### Video Compression Flow
1. User uploads a video
2. App creates temporary files for input/output
3. Uses FFprobe to get video duration
4. Calculates optimal bitrate: `(max_bytes * 8 * 0.9) / duration`
5. Runs FFmpeg with libx264 codec at calculated bitrate
6. Scales video to 720p maximum resolution
7. Returns compressed video

## 🐛 Troubleshooting

**FFmpeg not found:**
- Ensure FFmpeg is installed and in your PATH
- Restart the application after installing FFmpeg

**Video compression is slow:**
- This is normal for large videos. Consider increasing the timeout or using lower resolution/bitrate targets.

**Memory errors with large files:**
- Reduce `MAX_CONTENT_LENGTH` or increase Docker memory limits

**Import errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- For ffmpeg-python: `pip install ffmpeg-python`

## 👤 Author

Created by Shadow1088
