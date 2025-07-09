# AI Business Name Generator - Complete Deployment Guide

## 📋 Project Structure

```
ai-business-name-generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version (optional)
├── .env                  # Environment variables (local only)
├── .gitignore           # Git ignore file
├── render.yaml          # Render deployment config
├── Procfile             # Heroku deployment (optional)
└── README.md            # Project documentation
```

## 🚀 Deployment Steps

### Step 1: Prepare Your Local Environment

1. **Create a new directory for your project:**
```bash
mkdir ai-business-name-generator
cd ai-business-name-generator
```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Create the project files:**
   - Copy the `app.py` code from the first artifact
   - Copy the `requirements.txt` and other config files from the second artifact

### Step 2: Test Locally

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python app.py
```

3. **Test in browser:**
   - Open `http://localhost:5000`
   - Test the name generation functionality

### Step 3: Set Up Git Repository

1. **Initialize Git:**
```bash
git init
git add .
git commit -m "Initial commit: AI Business Name Generator"
```

2. **Create GitHub repository:**
   - Go to GitHub and create a new repository
   - Follow the instructions to push your code

```bash
git remote add origin https://github.com/yourusername/ai-business-name-generator.git
git branch -M main
git push -u origin main
```

### Step 4: Deploy to Render

#### Option A: Using Render Dashboard (Recommended)

1. **Go to Render Dashboard:**
   - Visit [render.com](https://render.com)
   - Sign up or log in
   - Click "New +" → "Web Service"

2. **Connect Repository:**
   - Select "Connect a repository"
   - Choose your GitHub repository
   - Click "Connect"

3. **Configure Deployment:**
   - **Name:** `ai-business-name-generator`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type:** `Free`

4. **Environment Variables:**
   - Add `FLASK_ENV` = `production`
   - Add `SECRET_KEY` = `your-secret-key-here`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment to complete

#### Option B: Using render.yaml (Infrastructure as Code)

1. **Create render.yaml file** (already provided in the config files)

2. **Deploy using Render Blueprint:**
   - Go to Render Dashboard
   - Click "New +" → "Blueprint"
   - Connect your repository
   - Render will automatically use the `render.yaml` configuration

### Step 5: Alternative Deployment Options

#### Deploy to Heroku

1. **Install Heroku CLI:**
   - Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login and create app:**
```bash
heroku login
heroku create ai-business-name-generator
```

3. **Set environment variables:**
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key-here
```

4. **Deploy:**
```bash
git push heroku main
```

#### Deploy to Vercel

1. **Install Vercel CLI:**
```bash
npm i -g vercel
```

2. **Create vercel.json:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

3. **Deploy:**
```bash
vercel --prod
```

## 🔧 Configuration Details

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `FLASK_ENV` | Flask environment | Yes | `production` |
| `SECRET_KEY` | Flask secret key