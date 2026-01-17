# CollabPlatform Deployment Guide

## Quick Start (Local Development)

1. **Install Dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Initialize Database**
   ```bash
   python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
   ```

3. **Create Sample Data (Optional)**
   ```bash
   python setup.py
   ```

4. **Run Application**
   ```bash
   python run.py
   ```

5. **Access Application**
   - Open http://localhost:5000
   - Use sample credentials from setup output

## Production Deployment

### Option 1: Docker (Recommended)

1. **Build and Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Access Application**
   - Application: http://localhost
   - Database: PostgreSQL on port 5432

### Option 2: Render.com

1. **Connect GitHub Repository**
   - Fork/clone this repository
   - Connect to Render.com

2. **Create Web Service**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn run:app`

3. **Add Environment Variables**
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://...
   FLASK_ENV=production
   ```

4. **Create PostgreSQL Database**
   - Add PostgreSQL service in Render
   - Copy DATABASE_URL to web service

### Option 3: Railway

1. **Deploy from GitHub**
   ```bash
   railway login
   railway init
   railway add postgresql
   railway deploy
   ```

2. **Set Environment Variables**
   ```bash
   railway variables set SECRET_KEY=your-secret-key
   railway variables set FLASK_ENV=production
   ```

### Option 4: AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t2.micro or larger
   - Security group: HTTP (80), HTTPS (443), SSH (22)

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip postgresql nginx
   ```

3. **Clone and Setup**
   ```bash
   git clone <your-repo>
   cd collabplatform
   pip3 install -r requirements.txt
   ```

4. **Configure PostgreSQL**
   ```bash
   sudo -u postgres createdb collabplatform
   sudo -u postgres createuser collabuser
   ```

5. **Setup Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

6. **Run with Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:5000 run:app
   ```

7. **Configure Nginx** (Optional)
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SECRET_KEY` | Flask secret key | Yes | - |
| `DATABASE_URL` | Database connection | No | SQLite |
| `FLASK_ENV` | Environment | No | development |
| `MAIL_SERVER` | SMTP server | No | - |
| `MAIL_USERNAME` | Email username | No | - |
| `MAIL_PASSWORD` | Email password | No | - |

## Database Setup

### SQLite (Development)
```bash
# Automatic - no setup required
python run.py
```

### PostgreSQL (Production)
```bash
# Create database
createdb collabplatform

# Set DATABASE_URL
export DATABASE_URL=postgresql://user:pass@localhost/collabplatform

# Initialize
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use PostgreSQL in production
- [ ] Enable HTTPS
- [ ] Set strong passwords
- [ ] Configure firewall
- [ ] Regular backups
- [ ] Monitor logs

## Monitoring

### Health Check
```bash
curl http://localhost:5000/
```

### Logs
```bash
# Docker
docker-compose logs -f web

# Direct
tail -f app.log
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check DATABASE_URL format
   - Verify database exists
   - Check credentials

2. **Import Errors**
   - Verify all dependencies installed
   - Check Python version (3.8+)

3. **Permission Errors**
   - Check file permissions
   - Verify user has write access

4. **Port Already in Use**
   - Change PORT environment variable
   - Kill existing processes

### Debug Mode
```bash
export FLASK_ENV=development
python run.py
```

## Backup & Recovery

### Database Backup
```bash
# PostgreSQL
pg_dump collabplatform > backup.sql

# Restore
psql collabplatform < backup.sql
```

### File Backup
```bash
# Backup uploads
tar -czf uploads_backup.tar.gz app/static/uploads/
```

## Performance Optimization

1. **Use Production WSGI Server**
   ```bash
   gunicorn --workers 4 --bind 0.0.0.0:5000 run:app
   ```

2. **Enable Caching**
   - Redis for session storage
   - CDN for static files

3. **Database Optimization**
   - Add indexes
   - Connection pooling
   - Query optimization

## Support

- **Documentation**: README.md
- **Issues**: GitHub Issues
- **Email**: support@collabplatform.com