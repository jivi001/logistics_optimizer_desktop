# 🚚 Nexus Route AI - Smart Logistics Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Google Gemini](https://img.shields.io/badge/Gemini_AI-Enabled-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> **Next-generation AI-powered logistics route optimization platform** combining Dijkstra's algorithm with Google Gemini AI for intelligent delivery planning across Indian cities.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Prerequisites](#-prerequisites)
- [Installation Guide](#-installation-guide)
  - [Windows](#windows-installation)
  - [macOS](#macos-installation)
  - [Linux](#linux-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [License](#-license)

---

## 🎯 Overview

**Nexus Route AI** is a production-ready logistics optimization platform that leverages:

- **Graph Theory**: Dijkstra's algorithm for optimal path calculation
- **AI Intelligence**: Google Gemini AI for natural language insights
- **Real-time Calculations**: Toll estimation, cost analysis, and ETA predictions
- **Premium UX**: Elegant glassmorphism design with responsive interface

### Key Capabilities

✅ **Route Optimization** - Find shortest paths between 20+ Indian cities  
✅ **AI Assistant** - Natural language logistics queries  
✅ **Cost Estimation** - Fuel, toll, and operational expenses  
✅ **ETA Prediction** - AI-powered delivery time estimates  
✅ **Multi-Stop Planning** - Optimize sequences for multiple destinations  
✅ **Toll Calculator** - NHAI-based toll cost estimation  
✅ **Weather Analysis** - Seasonal route planning recommendations  
✅ **Safety Compliance** - Cargo-specific regulations and documentation  

---

## ✨ Features

### 🗺️ Core Features

| Feature | Description |
|---------|-------------|
| **Intelligent Route Planning** | Dijkstra's algorithm with interactive map visualization |
| **20+ City Network** | Pre-configured network of major Indian cities |
| **Real-time Calculations** | Distance, time, toll, and cost estimates |
| **Interactive Maps** | Leaflet.js integration with custom markers |

### 🤖 AI Command Center (6 Tools)

1. **💬 AI Assistant** - Conversational logistics advisor
2. **⚡ ETA Prediction** - Smart delivery time estimation with risk analysis
3. **🗺️ Multi-Stop Optimizer** - Route sequencing for multiple deliveries
4. **💰 Cost Analysis** - Comprehensive expense breakdown (fuel, tolls, maintenance)
5. **🌦️ Weather Impact** - Seasonal route analysis and precautions
6. **🛡️ Safety Check** - Compliance verification and documentation requirements

### 🛣️ Toll Calculator

- Vehicle-specific rates (Car, LCV, Truck, Multi-Axle)
- Route segment breakdown
- NHAI-based estimates
- Plaza count prediction
- Cost per 100km analysis

### 🎨 Premium UI/UX

- Elegant dark theme with glassmorphism effects
- Fully responsive (mobile, tablet, desktop)
- Collapsible AI Command Center
- Smooth animations and transitions
- Persistent UI state with localStorage

---

## 🎬 Demo

**Live Demo**: [Coming Soon]  
**Video Demo**: [Coming Soon]

### Screenshots

| Route Planning | AI Command Center | Toll Calculator |
|---------------|-------------------|-----------------|
| ![Route](https://via.placeholder.com/300x200/667eea/ffffff?text=Route+Planning) | ![AI](https://via.placeholder.com/300x200/764ba2/ffffff?text=AI+Features) | ![Toll](https://via.placeholder.com/300x200/8b5cf6/ffffff?text=Toll+Calculator) |

---

## 📋 Prerequisites

Before installation, ensure you have:

### Required Software

| Software | Version | Download Link |
|----------|---------|---------------|
| **Python** | 3.8 or higher | [python.org](https://www.python.org/downloads/) |
| **pip** | Latest | Comes with Python |
| **Git** | Latest | [git-scm.com](https://git-scm.com/downloads) |

### Required API Keys

- **Google Gemini API Key** (Free tier available)
  - Get it at: [Google AI Studio](https://makersuite.google.com/app/apikey)
  - Required for AI features

### System Requirements

- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **RAM**: Minimum 2GB
- **Storage**: 500MB free space
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

---

## 🚀 Installation Guide

### Quick Start (All Platforms)

1. Clone the repository
git clone https://github.com/yourusername/nexus-route-ai.git
cd nexus-route-ai

2. Create virtual environment
python -m venv venv

3. Activate virtual environment
On Windows:
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate

4. Install dependencies
pip install -r requirements.txt

5. Configure environment variables
Create .env file (see Configuration section)
6. Run the application
python app.py

text

---

### Windows Installation

#### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer and **check "Add Python to PATH"**
3. Verify installation:
python --version
pip --version

text

#### Step 2: Install Git (Optional but Recommended)

1. Download from [git-scm.com](https://git-scm.com/download/win)
2. Install with default settings

#### Step 3: Clone Repository

**Option A: Using Git**
git clone https://github.com/yourusername/nexus-route-ai.git
cd nexus-route-ai

text

**Option B: Download ZIP**
1. Download ZIP from GitHub
2. Extract to desired location
3. Open Command Prompt in extracted folder

#### Step 4: Create Virtual Environment

python -m venv venv
venv\Scripts\activate

text

You should see `(venv)` in your command prompt.

#### Step 5: Install Dependencies

pip install --upgrade pip
pip install -r requirements.txt

text

#### Step 6: Configure Environment

Create `.env` file in project root:
type nul > .env
notepad .env

text

Add to `.env`:
GEMINI_API_KEY=your_api_key_here
FLASK_DEBUG=true
PORT=5001

text

#### Step 7: Run Application

python app.py

text

Open browser: `http://localhost:5001`

---

### macOS Installation

#### Step 1: Install Homebrew (if not installed)

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

text

#### Step 2: Install Python

brew install python@3.11
python3 --version

text

#### Step 3: Install Git

brew install git

text

#### Step 4: Clone Repository

git clone https://github.com/yourusername/nexus-route-ai.git
cd nexus-route-ai

text

#### Step 5: Create Virtual Environment

python3 -m venv venv
source venv/bin/activate

text

#### Step 6: Install Dependencies

pip install --upgrade pip
pip install -r requirements.txt

text

#### Step 7: Configure Environment

touch .env
nano .env

text

Add configuration:
GEMINI_API_KEY=your_api_key_here
FLASK_DEBUG=true
PORT=5001

text

Save with `Ctrl+O`, Exit with `Ctrl+X`

#### Step 8: Run Application

python app.py

text

Open browser: `http://localhost:5001`

---

### Linux Installation

#### Step 1: Update System

sudo apt update
sudo apt upgrade -y

text

#### Step 2: Install Python and Dependencies

Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip git -y

Verify installation
python3 --version
pip3 --version

text

#### Step 3: Clone Repository

git clone https://github.com/yourusername/nexus-route-ai.git
cd nexus-route-ai

text

#### Step 4: Create Virtual Environment

python3 -m venv venv
source venv/bin/activate

text

#### Step 5: Install Dependencies

pip install --upgrade pip
pip install -r requirements.txt

text

#### Step 6: Configure Environment

touch .env
nano .env

text

Add configuration:
GEMINI_API_KEY=your_api_key_here
FLASK_DEBUG=true
PORT=5001

text

Save with `Ctrl+O`, Exit with `Ctrl+X`

#### Step 7: Run Application

python app.py

text

Open browser: `http://localhost:5001`

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

============================================
REQUIRED CONFIGURATION
============================================
Google Gemini AI API Key
Get your key at: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

============================================
OPTIONAL CONFIGURATION
============================================
Flask Debug Mode (true/false)
FLASK_DEBUG=true

Server Port (default: 5001)
PORT=5001

Flask Secret Key (for sessions)
SECRET_KEY=your_random_secret_key_here
text

### Getting Gemini API Key

1. **Visit**: [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Sign in** with your Google account
3. **Create API Key**: Click "Create API Key"
4. **Copy the key** and paste into `.env` file
5. **Important**: Keep your API key secret (don't commit to Git)

### Configuring for Production

For production deployment, update `.env`:

GEMINI_API_KEY=your_production_api_key
FLASK_DEBUG=false
PORT=8000
SECRET_KEY=generate_strong_random_secret_key

text

Generate secret key:
python -c "import secrets; print(secrets.token_hex(32))"

text

---

## 🏃 Running the Application

### Development Mode

Activate virtual environment
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows

Run the application
python app.py

text

Application will be available at: `http://localhost:5001`

### Production Mode

For production deployment, use Gunicorn:

Install Gunicorn
pip install gunicorn

Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

text

### Running in Background (Linux/macOS)

nohup python app.py > app.log 2>&1 &

text

### Docker Deployment (Optional)

Create `Dockerfile`:
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "app.py"]

text

Build and run:
docker build -t nexus-route-ai .
docker run -p 5001:5001 --env-file .env nexus-route-ai

text

---

## 📁 Project Structure

nexus-route-ai/
│
├── 📄 app.py # Flask application (main entry point)
├── 📄 route_optimizer.py # Dijkstra's algorithm implementation
├── 📄 requirements.txt # Python dependencies
├── 📄 .env # Environment variables (create this)
├── 📄 .gitignore # Git ignore rules
├── 📄 README.md # This file
├── 📄 LICENSE # MIT License
│
├── 📁 templates/
│ └── 📄 index.html # Main HTML template
│
├── 📁 static/
│ ├── 📁 css/
│ │ └── 📄 style.css # Premium styling
│ ├── 📁 js/
│ │ └── 📄 script.js # Frontend logic
│ └── 📁 images/ # (Optional) Images/logos
│
├── 📁 venv/ # Virtual environment (auto-generated)
└── 📁 pycache/ # Python cache (auto-generated)

text

---

## 📖 Usage Guide

### 1. Basic Route Planning

1. **Select Origin City**: Choose starting point from dropdown
2. **Select Destination City**: Choose endpoint
3. **Calculate Route**: Click "Calculate Optimal Route" button
4. **View Results**:
   - Route displayed on interactive map
   - Distance and time estimates
   - AI-powered insights
   - Toll cost breakdown

### 2. Using AI Command Center

#### Accessing AI Features

1. **Toggle Section**: Click "AI Command Center" header to expand/collapse
2. **Select Tool**: Click on any of the 6 feature pills
3. **Fill Form**: Enter required information
4. **Get Results**: Click action button to generate AI insights

#### AI Assistant Chat

Example queries:

"What's the best route from Mumbai to Delhi?"

"Tips for monsoon season driving"

"How to reduce fuel costs?"

"Safety measures for transporting electronics"

text

#### ETA Prediction

Required inputs:
- Vehicle Type (Heavy Truck/Mini Truck/Van)
- Cargo Weight (kg)
- Departure Time

Output:
- Estimated delivery time
- Best departure window
- Risk factors and delays

#### Multi-Stop Optimizer

1. Select starting city
2. Add multiple delivery stops
3. Click "Optimize Route"
4. Get suggested optimal sequence

#### Cost Estimation

Required inputs:
- Vehicle type
- Cargo weight
- Current fuel price (₹/liter)

Output:
- Total cost breakdown (fuel, tolls, driver, maintenance)
- Cost per kilometer
- Cost-saving recommendations

### 3. Toll Calculator

- **Automatic**: Appears after route calculation
- **Interactive**: Change vehicle type to update costs
- **Detailed**: View segment-wise breakdown
- **Accurate**: Based on NHAI rates

---

## 📡 API Documentation

### Base URL

http://localhost:5001/api

text

### Endpoints

#### 1. Get Cities

GET /api/get_cities

text

**Response:**
{
"cities": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", ...],
"coordinates": {
"Mumbai": [19.0760, 72.8777],
"Delhi": [28.7041, 77.1025],
...
}
}

text

#### 2. Calculate Shortest Route

GET /api/get_shortest_route?src=Mumbai&dest=Delhi

text

**Parameters:**
- `src`: Source city name
- `dest`: Destination city name

**Response:**
{
"path": ["Mumbai", "Surat", "Ahmedabad", "Jaipur", "Delhi"],
"distance": 1420.5,
"time_hours": 23.67,
"coordinates": {
"Mumbai": [19.0760, 72.8777],
...
}
}

text

#### 3. Get AI Insights

POST /api/get_gemini_insights
Content-Type: application/json

{
"path": ["Mumbai", "Delhi"],
"distance": 1420
}

text

**Response:**
{
"insights": "Route Summary: Direct highway route...\nChallenges: Heavy traffic in urban areas..."
}

text

#### 4. AI Chat

POST /api/ai/chat
Content-Type: application/json

{
"message": "Best time to travel from Mumbai to Delhi?",
"context": {
"current_route": "Mumbai → Delhi",
"distance": 1420
}
}

text

#### 5. Predict Delivery Time

POST /api/ai/predict_delivery_time
Content-Type: application/json

{
"path": ["Mumbai", "Delhi"],
"distance": 1420,
"vehicle_type": "truck",
"cargo_weight": 5000,
"departure_time": "2025-11-02T06:00"
}

text

#### 6. Cost Estimation

POST /api/ai/cost_estimate
Content-Type: application/json

{
"distance": 1420,
"vehicle_type": "truck",
"cargo_weight": 5000,
"fuel_price": 100
}

text

#### 7. Calculate Toll

POST /api/calculate_toll
Content-Type: application/json

{
"distance": 1420,
"vehicle_type": "truck"
}

text

---

## 🤝 Contributing

We welcome contributions! Follow these steps:

### Fork & Clone

1. Fork the repository on GitHub
2. Clone your fork
git clone https://github.com/YOUR-USERNAME/nexus-route-ai.git
cd nexus-route-ai

3. Add upstream remote
git remote add upstream https://github.com/original-repo/nexus-route-ai.git

text

### Create Branch

Create feature branch
git checkout -b feature/amazing-feature

Or bug fix branch
git checkout -b fix/bug-description

text

### Make Changes

1. **Code**: Make your changes
2. **Test**: Ensure everything works
3. **Commit**: Write clear commit messages

git add .
git commit -m "feat: add amazing new feature"

text

### Commit Message Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

### Push & Pull Request

Push to your fork
git push origin feature/amazing-feature

Create Pull Request on GitHub
text

### Development Guidelines

✅ **Code Style**
- Follow PEP 8 for Python
- Use meaningful variable names
- Add docstrings for functions
- Comment complex logic

✅ **Testing**
- Test all features locally
- Verify on different browsers
- Check responsive design

✅ **Documentation**
- Update README if needed
- Add API documentation for new endpoints
- Include code comments

---

## 🔧 Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
Activate virtual environment first
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows

Then install dependencies
pip install -r requirements.txt

text

#### 2. Gemini API Error

**Error:** `Gemini API is not configured`

**Solution:**
- Verify `.env` file exists
- Check `GEMINI_API_KEY` is set correctly
- Get new API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

#### 3. Port Already in Use

**Error:** `Address already in use`

**Solution:**
Change port in .env
PORT=5002

Or kill process using port (Linux/macOS)
lsof -ti:5001 | xargs kill -9

Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F

text

#### 4. Map Not Displaying

**Solution:**
- Check internet connection (Leaflet.js needs CDN access)
- Clear browser cache
- Check browser console for errors

#### 5. Virtual Environment Issues

**Windows Error:** `venv\Scripts\activate : File cannot be loaded`

**Solution:**
Run PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

Then activate
venv\Scripts\activate

text

---

## ❓ FAQ

**Q: Is this free to use?**  
A: Yes, completely free and open-source under MIT License.

**Q: Do I need a paid Google account for Gemini API?**  
A: No, free tier is available with generous quota.

**Q: Can I add more cities?**  
A: Yes! Edit `route_optimizer.py` and add cities to the graph.

**Q: How accurate are toll estimates?**  
A: Based on NHAI rates; actual charges may vary by ±10%.

**Q: Can I deploy this commercially?**  
A: Yes, MIT License allows commercial use with attribution.

**Q: Does it work offline?**  
A: Partially. Route calculation works offline, but AI features need internet.

**Q: What browsers are supported?**  
A: All modern browsers (Chrome, Firefox, Safari, Edge).

**Q: Can I customize the UI?**  
A: Yes! All CSS is in `static/css/style.css`.

---

## 📄 License

This project is licensed under the **MIT License**.

MIT License

Copyright (c) 2025 Jivi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

text

---

## 👨‍💻 Author

**Jivi** - AI & Data Science Engineer

- 🌐 GitHub: [@yourusername](https://github.com/yourusername)
- 💼 LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- 📧 Email: your.email@example.com
- 🐦 Twitter: [@yourhandle](https://twitter.com/yourhandle)

---

## 🙏 Acknowledgments

Special thanks to:

- **Google Gemini AI** - Natural language processing capabilities
- **OpenStreetMap** - Map data and tile services
- **Leaflet.js** - Interactive mapping library
- **Flask Community** - Excellent framework and documentation
- **NHAI** - Toll rate reference data
- **Open Source Community** - Inspiration and support

---

## 📊 Project Stats

![GitHub Stars](https://img.shields.io/github/stars/yourusername/nexus-route-ai?style=social)
![GitHub Forks](https://img.shields.io/github/forks/yourusername/nexus-route-ai?style=social)
![GitHub Issues](https://img.shields.io/github/issues/yourusername/nexus-route-ai)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/yourusername/nexus-route-ai)

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/nexus-route-ai&type=Date)](https://star-history.com/#yourusername/nexus-route-ai&Date)

---

## 🚀 Roadmap

### Version 2.0 (Planned)

- [ ] Real-time traffic integration
- [ ] Live weather API
- [ ] Expand to 50+ cities
- [ ] Route comparison feature
- [ ] User authentication
- [ ] Save and share routes
- [ ] Mobile app (React Native)
- [ ] Fleet management dashboard

### Version 3.0 (Future)

- [ ] Machine learning for route prediction
- [ ] Integration with GPS devices
- [ ] Multi-language support
- [ ] API rate limiting
- [ ] Database integration
- [ ] Analytics dashboard

---

## 📞 Support & Contact

### Get Help

- 📖 **Documentation**: Read this README
- 🐛 **Bug Reports**: [Open an Issue](https://github.com/yourusername/nexus-route-ai/issues)
- 💡 **Feature Requests**: [Submit Request](https://github.com/yourusername/nexus-route-ai/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/nexus-route-ai/discussions)
- 📧 **Email**: your.email@example.com

### Stay Updated

- ⭐ Star the repository
- 👁️ Watch for updates
- 🍴 Fork for your own use

---

## 🎓 Learning Resources

### For Beginners

- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Flask Quickstart](https://flask.palletsprojects.com/quickstart/)
- [JavaScript Basics](https://developer.mozilla.org/en-US/docs/Learn/JavaScript)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)

### Advanced Topics

- [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Leaflet.js Documentation](https://leafletjs.com/reference.html)
- [REST API Design](https://restfulapi.net/)

---

**Built with ❤️ for the logistics industry**

© 2025 Nexus Route AI. All rights reserved.

---

**Last Updated**: November 1, 2025  
**Version**: 1.0.0  
**Maintained**: Yes ✅