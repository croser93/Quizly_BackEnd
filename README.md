[![Python](https://img.shields.io/badge/Python-3.14.4-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0.6-092E20?style=for-the-badge&logo=django&labelColor=092E20)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django_REST_Framework-3.17.1-red?style=for-the-badge&logo=django)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT-black?style=for-the-badge&logo=jsonwebtokens)](https://jwt.io/)

# Quizly_Backend
A Django REST API that turns any YouTube video into a quiz: it downloads the audio, transcribes it, and uses an LLM to generate multiple-choice questions.
Learning project as part of the Developer Akademie — built to practice Test-Driven Development (TDD) with Django REST Framework.

## About the Project

Quizly lets an authenticated user submit a YouTube URL and receive a ready-to-use quiz in return. The backend downloads the video's audio track, transcribes it with OpenAI Whisper, and sends the transcript to Google Gemini to generate a title, description, and a set of multiple-choice questions. Users can list, retrieve, partially update, and delete their own quizzes; authentication is handled via JWT stored in HttpOnly cookies.

## Tech Stack

| Technology | Version |
|------------|---------|
| Python | 3.14.4 |
| Django | 6.0.6 |
| Django REST Framework | 3.17.1 |
| djangorestframework-simplejwt | 5.5.1 |
| yt-dlp | 2026.7.4 |
| openai-whisper | 20250625 |
| google-genai | 2.13.0 |
| python-dotenv | 1.2.2 |
| Database | SQLite (dev) |
| Authentication | JWT (HttpOnly cookies, custom auth class) |

## Installation & Setup

**Prerequisite:** [ffmpeg](https://ffmpeg.org/) must be installed and available on your system `PATH` (required by `openai-whisper` to decode downloaded audio).

```bash
# 1. Clone repository
git clone https://github.com/croser93/Quizly_BackEnd.git
```

```bash
# 2. Go to project
cd Quizly_BackEnd
```

```bash
# 3. Create virtual environment
python -m venv .venv
```

```bash
# 4. Activate virtual environment — Linux/Mac
source .venv/bin/activate
```

```bash
# 4. Activate virtual environment — Windows
.venv\Scripts\activate
```

```bash
# 5. Install dependencies
pip install -r requirements.txt
```

```bash
# 6. Generate a Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

```bash
# 7. Create migration files
python manage.py makemigrations
```

```bash
# 8. Run database migrations
python manage.py migrate
```

```bash
# 9. Start development server
python manage.py runserver
```

Create a `.env` file in the project root and add the generated key together with your Gemini API key:

```env
SECRET_KEY='your_generated_key_here'
GEMINI_API_KEY='your_gemini_api_key_here'
```
## Project Structure

```
Quizly_Backend/
├── core/               # Project configuration (settings, urls, wsgi)
├── auth_app/           # Registration, login, logout & cookie-based JWT token refresh
├── quizzes_app/        # Quiz creation (yt-dlp + Whisper + Gemini) and quiz CRUD endpoints
└── media/               # Temporary downloaded audio files (gitignored)
```

---
**Maik G.** — Learning project as part of the Developer Akademie
