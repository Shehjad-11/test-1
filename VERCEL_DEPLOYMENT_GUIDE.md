# 🚀 Vercel Deployment Guide for CollabPlatform

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **PostgreSQL Database**: Set up a database (recommended: Neon, Supabase, or Railway)

## 🛠️ Step-by-Step Deployment

### 1. **Prepare Your Database**

#### Option A: Neon (Recommended - Free tier available)
1. Go to [neon.tech](https://neon.tech)
2. Create a free account
3. Create a new project
4. Copy the connection string (starts with `postgresql://`)

#### Option B: Supabase
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings → Database
4. Copy the connection string

#### Option C: Railway
1. Go to [railway.app](https://railway.app)
2. Create a PostgreSQL database
3. Copy the connection string

### 2. **Deploy to Vercel**

#### Method 1: Vercel Dashboard (Recommended)
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect it's a Python project

#### Method 2: Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from your project directory
vercel

# Follow the prompts
```

### 3. **Configure Environment Variables**

In your Vercel project dashboard, go to **Settings → Environment Variables** and add:

#### Required Variables:
```
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DATABASE_URL=postgresql://your-database-connection-string
POSTGRES_URL=postgresql://your-database-connection-string
VERCEL=1
FLASK_ENV=production
```

#### Optional Variables (for email functionality):
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 4. **Initialize Database**

After deployment, you need to create the database tables:

#### Option A: Using Vercel CLI
```bash
# Install Vercel CLI if not already installed
npm i -g vercel

# Run database migration
vercel env pull .env.local
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database tables created!')
"
```

#### Option B: Add initialization to your app
The app will automatically create tables on first run due to the existing code.

## 🔧 Files Created for Vercel

### `vercel.json`
- Configures Vercel deployment settings
- Routes all requests to the Flask app
- Sets Python runtime and timeout

### `api/index.py`
- Entry point for Vercel serverless functions
- Imports and runs your Flask app

### `requirements.txt`
- Lists all Python dependencies
- Vercel uses this to install packages

### Updated `config.py`
- Handles different database URLs for production/development
- Configures settings for Vercel environment

## 🌐 Access Your Deployed App

After successful deployment:
1. Vercel will provide a URL like: `https://your-app-name.vercel.app`
2. Your app will be live and accessible worldwide
3. Automatic HTTPS and CDN included

## 🔍 Troubleshooting

### Common Issues:

#### 1. **Database Connection Error**
- Ensure `DATABASE_URL` is correctly set in Vercel environment variables
- Check that your database allows external connections
- Verify the connection string format

#### 2. **Import Errors**
- Make sure all dependencies are in `requirements.txt`
- Check that file paths are correct in `api/index.py`

#### 3. **Static Files Not Loading**
- Vercel serves static files automatically from the project root
- CSS/JS files should load from `/static/` URLs

#### 4. **Database Tables Don't Exist**
- Run the database initialization commands above
- Or add this to your app to auto-create tables:

```python
# Add to app/__init__.py after db initialization
with app.app_context():
    db.create_all()
```

### 5. **Function Timeout**
- Vercel has a 10-second timeout for Hobby plan
- Optimize database queries if needed
- Consider upgrading to Pro plan for longer timeouts

## 📊 Monitoring Your App

1. **Vercel Dashboard**: Monitor deployments and function invocations
2. **Logs**: View real-time logs in Vercel dashboard
3. **Analytics**: Track performance and usage

## 🔄 Continuous Deployment

Once connected to GitHub:
1. Every push to main branch triggers automatic deployment
2. Preview deployments for pull requests
3. Rollback to previous versions if needed

## 💡 Production Tips

1. **Environment Variables**: Never commit secrets to Git
2. **Database Backups**: Set up regular backups for your database
3. **Monitoring**: Set up uptime monitoring (UptimeRobot, etc.)
4. **Custom Domain**: Add your own domain in Vercel settings
5. **Performance**: Monitor function execution times

## 🎉 Success!

Your Flask app should now be running on Vercel with:
- ✅ Working message system
- ✅ Functional notifications
- ✅ PostgreSQL database
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Continuous deployment

Visit your Vercel URL to see your live application!

## 🆘 Need Help?

If you encounter issues:
1. Check Vercel function logs in the dashboard
2. Verify all environment variables are set
3. Test database connection
4. Check the GitHub repository is properly connected

Your CollabPlatform is now ready for the world! 🌍