# Kodbank - Banking Application

A full-stack banking application with Flask backend and HTML/CSS/JS frontend.

## Features
- User Registration (default balance ₹100,000)
- Login with JWT Token Authentication
- Check Balance with token verification
- Beautiful UI with party popper animation

## Tech Stack
- **Backend**: Flask (Python)
- **Database**: MySQL (Aiven)
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: JWT (JSON Web Tokens)

## Quick Start (Local)

1. Install dependencies:
```
bash
pip install -r requirements.txt
```

2. Configure database in `.env` file:
```
DB_HOST=your-aiven-host
DB_PORT=3306
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=kodbank
JWT_SECRET_KEY=your-secret-key
```

3. Initialize database:
```
Visit: http://localhost:5000/init
```

4. Run the app:
```
bash
python app.py
```

5. Open: http://localhost:5000

## Deploy to Render.com (FREE)

### Steps:

1. **Push code to GitHub:**
```
bash
git init
git add .
git commit -m "Initial commit"
# Create a new repo on GitHub and push
```

2. **Deploy on Render:**
   - Go to https://render.com
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Name: kodbank
     - Build Command: (leave empty)
     - Start Command: python app.py
   - Add Environment Variables:
     - DB_HOST: your-aiven-host
     - DB_PORT: 3306
     - DB_USER: your-aiven-username
     - DB_PASSWORD: your-aiven-password
     - DB_NAME: kodbank
     - JWT_SECRET_KEY: any-random-string
   - Click "Deploy"

3. **Initialize Database:**
   - Visit: `https://your-app-name.onrender.com/init`

4. **Your app is live!**

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| /init | GET | Initialize database |
| /register | POST | Register new user |
| /login | POST | Login & get JWT token |
| /getBalance | POST | Get balance (requires token) |
| /logout | POST | Logout |
| /verify | GET | Verify token |

## Screenshots
- Login Page with KodNest Logo
- Registration Page
- Dashboard with Check Balance

## License
MIT
