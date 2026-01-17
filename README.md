# CollabPlatform - Fair Project Collaboration Platform

A transparent, ethical platform connecting companies with developers and designers through fair project-based collaboration. Built with Flask, PostgreSQL, and modern web technologies.

## 🎯 Mission

Create a fair, transparent platform where companies post short-term projects and developers/designers collaborate by submitting real work, not free labor. Supporting SDG-8: Decent Work & Economic Growth.

## ✨ Features

### For Companies
- **Project Management**: Post projects with clear requirements and fair compensation
- **Transparent Process**: Shortlist candidates, review submissions, provide feedback
- **Fair Rewards**: Winner rewards + optional participation compensation
- **Quality Control**: Score submissions and give constructive feedback

### For Developers/Designers
- **Portfolio Building**: Work on real projects and build reputation
- **Fair Compensation**: Get paid for quality work, even if not selected as winner
- **Skill Development**: Apply to projects matching your expertise
- **Transparent Feedback**: Receive constructive feedback on submissions

### Platform Features
- **Role-based Authentication**: Company, Developer, Admin roles
- **Real-time Notifications**: Stay updated on project status
- **Messaging System**: Direct communication between companies and shortlisted candidates
- **Reputation System**: Build credibility through successful projects
- **Responsive Design**: Works seamlessly on desktop and mobile

## 🛠 Technology Stack

- **Backend**: Python Flask Framework
- **Database**: PostgreSQL (SQLite for development)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Flask-Login with secure password hashing
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Migrations**: Flask-Migrate
- **Deployment**: Docker, Gunicorn, Nginx

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL (for production) or SQLite (for development)
- Node.js (optional, for frontend build tools)
- Docker & Docker Compose (for containerized deployment)

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd collabplatform
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Create sample data (optional)**
   ```bash
   flask deploy
   ```

7. **Run the application**
   ```bash
   python run.py
   ```

Visit `http://localhost:5000` to access the application.

### Docker Deployment

1. **Using Docker Compose (Recommended)**
   ```bash
   docker-compose up -d
   ```

2. **Using Docker only**
   ```bash
   docker build -t collabplatform .
   docker run -p 5000:5000 collabplatform
   ```

## 📁 Project Structure

```
collabplatform/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models
│   ├── auth/                    # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── routes.py            # Auth routes
│   │   └── forms.py             # Auth forms
│   ├── routes/                  # Main application routes
│   │   ├── __init__.py
│   │   ├── main.py              # Main routes
│   │   └── forms.py             # Application forms
│   ├── services/                # Business logic services
│   │   ├── __init__.py
│   │   └── notification_service.py
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/                # Authentication templates
│   │   ├── company/             # Company dashboard templates
│   │   ├── developer/           # Developer dashboard templates
│   │   └── projects/            # Project-related templates
│   └── static/                  # Static files
│       ├── css/
│       ├── js/
│       └── uploads/
├── migrations/                  # Database migrations
├── config.py                    # Configuration settings
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
└── README.md                    # This file
```

## 🗄 Database Schema

### Core Models

- **User**: Authentication and basic user info
- **CompanyProfile**: Company-specific information
- **DeveloperProfile**: Developer/designer profiles
- **Project**: Project details and requirements
- **Application**: Developer applications to projects
- **Submission**: Work submissions from shortlisted candidates
- **Message**: Internal messaging system
- **Notification**: System notifications

### Relationships

- Users have profiles (Company or Developer)
- Companies create Projects
- Developers submit Applications
- Shortlisted Applications can have Submissions
- Messages link Users within Project context

## 🔐 Security Features

- **Password Hashing**: Werkzeug secure password hashing
- **CSRF Protection**: Flask-WTF CSRF tokens
- **Input Validation**: Server-side form validation
- **Role-based Access**: Proper authorization checks
- **Secure Sessions**: Flask-Login session management

## 🌐 Deployment Options

### 1. Render (Recommended for beginners)
```bash
# Connect your GitHub repo to Render
# Set environment variables in Render dashboard
# Deploy automatically on git push
```

### 2. Railway
```bash
railway login
railway init
railway add postgresql
railway deploy
```

### 3. AWS EC2
```bash
# Launch EC2 instance
# Install Docker and Docker Compose
# Clone repository and run docker-compose
```

### 4. DigitalOcean Droplet
```bash
# Create droplet with Docker
# Clone repository
# Run docker-compose up -d
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |
| `DATABASE_URL` | Database connection string | SQLite |
| `FLASK_ENV` | Environment (development/production) | `development` |
| `MAIL_SERVER` | SMTP server for emails | None |
| `MAIL_USERNAME` | Email username | None |
| `MAIL_PASSWORD` | Email password | None |

### Database Configuration

**Development (SQLite):**
```
DATABASE_URL=sqlite:///collaboration_platform.db
```

**Production (PostgreSQL):**
```
DATABASE_URL=postgresql://username:password@host:port/database
```

## 👥 User Roles & Workflows

### Company Workflow
1. Register and complete company profile
2. Post project with requirements and rewards
3. Review applications and shortlist candidates
4. Review submissions and provide feedback
5. Select winner and distribute rewards

### Developer Workflow
1. Register and complete developer profile
2. Browse and apply to relevant projects
3. If shortlisted, submit work within deadline
4. Receive feedback and potential rewards
5. Build reputation through successful projects

## 🧪 Testing

### Sample Users (Development)
- **Admin**: admin@collabplatform.com / admin123
- **Company**: hr@techcorp.com / company123
- **Developer**: john@example.com / dev123
- **Designer**: jane@example.com / dev123

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and code comments
- **Issues**: Open GitHub issues for bugs and feature requests
- **Email**: support@collabplatform.com

## 🌟 Acknowledgments

- Built to support SDG-8: Decent Work & Economic Growth
- Inspired by the need for fair, ethical freelance platforms
- Thanks to the Flask and open-source community

## 🚀 Future Enhancements

- [ ] Payment integration (Stripe/PayPal)
- [ ] Advanced search and filtering
- [ ] Project categories and tags
- [ ] Video submission support
- [ ] Mobile app (React Native)
- [ ] API for third-party integrations
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

---

**CollabPlatform** - Building a fairer future for project collaboration 🌟