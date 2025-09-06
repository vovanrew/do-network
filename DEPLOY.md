# Deployment Instructions for Render

## Prerequisites
- A GitHub account
- Your code pushed to a GitHub repository
- A Render account (free at https://render.com)

## Deployment Steps

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to https://dashboard.render.com
   - Click "New +" and select "Web Service"
   - Connect your GitHub account if not already connected
   - Select your repository
   - Render will automatically detect the `render.yaml` file
   - Click "Create Web Service"

3. **Environment Setup**
   - Render will automatically:
     - Install Python dependencies from `requirements.txt`
     - Run `build.py` to initialize the database
     - Generate a secure `SECRET_KEY`
     - Start your app with Gunicorn

4. **Access Your App**
   - After deployment (usually takes 2-5 minutes), your app will be available at:
     `https://reflection-game.onrender.com` (or similar URL)

## Important Notes

- **Free Tier Limitations**: 
  - Apps on free tier spin down after 15 minutes of inactivity
  - First request after spin down takes ~30 seconds
  - SQLite database is reset on each deployment

- **Database Persistence**: 
  - For production use with persistent data, consider upgrading to:
    - Render's paid tier with persistent disk
    - Or switch to PostgreSQL (Render provides free PostgreSQL)

- **Custom Domain**: 
  - You can add a custom domain in Render dashboard settings

## Troubleshooting

If deployment fails:
1. Check the deploy logs in Render dashboard
2. Ensure all dependencies are in `requirements.txt`
3. Verify Python version compatibility
4. Check that `build.py` runs without errors locally

### Common Issues

**"Failed to find attribute 'app' in 'app'" Error**
This error occurs when gunicorn can't find the Flask app. The application supports multiple entry points:
- `gunicorn application:app` - Uses application.py (recommended)
- `gunicorn app:app` - Uses app/__init__.py
- `gunicorn wsgi:app` - Uses wsgi.py

The Procfile and render.yaml are configured to use `application:app` for consistency.

## Local Testing Before Deploy

Test the production setup locally:
```bash
pip install -r requirements.txt
python build.py
gunicorn application:app
```

Then visit http://localhost:8000
