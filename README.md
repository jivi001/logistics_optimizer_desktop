text
# 🚚 Nexus Route AI - Smart Logistics Platform

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Google Gemini](https://img.shields.io/badge/Gemini_AI-Enabled-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> AI-powered logistics route optimization platform combining Dijkstra's algorithm with Google Gemini AI for intelligent delivery planning across Indian cities.

## 🎯 Overview

Nexus Route AI is a production-ready logistics platform that delivers:

- **Smart Route Planning** using Dijkstra's algorithm
- **AI-Powered Insights** via Google Gemini
- **Real-time Cost Analysis** including tolls, fuel, and operational expenses
- **Interactive Maps** with Leaflet.js visualization
- **Premium UI/UX** with elegant glassmorphism design

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🗺️ **Route Optimization** | Find shortest paths between 20+ Indian cities |
| 💬 **AI Assistant** | Natural language logistics queries |
| ⚡ **ETA Prediction** | Smart delivery time estimates with risk analysis |
| 💰 **Cost Estimation** | Fuel, toll, driver, and maintenance breakdown |
| 🛣️ **Toll Calculator** | NHAI-based estimates with vehicle-specific rates |
| 🌦️ **Weather Analysis** | Seasonal route planning recommendations |
| 🛡️ **Safety Compliance** | Cargo-specific regulations and documentation |

## 📋 Prerequisites

| Requirement | Version | Notes |
|------------|---------|-------|
| Python | 3.8+ | [Download](https://www.python.org/downloads/) |
| pip | Latest | Comes with Python |
| Git | Latest | [Download](https://git-scm.com/downloads) |
| Google Gemini API | Free tier | [Get key](https://makersuite.google.com/app/apikey) |

**System Requirements:**
- OS: Windows 10+, macOS 10.14+, or Linux (Ubuntu 20.04+)
- RAM: Minimum 2GB
- Storage: 500MB free space
- Browser: Chrome, Firefox, Safari, or Edge (latest)

## 🚀 Quick Start

1. **Clone repository**:
git clone https://github.com/jivi001/logistics_optimizer_desktop.git
cd logistics_optimizer_desktop

2. **Create virtual environment**:
python -m venv venv

3. **Activate virtual environment**:
Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate

4. **Install dependencies**:
pip install -r requirements.txt

5. **Configure environment**
**Create**.env file and add:
GEMINI_API_KEY=your_api_key_here
FLASK_DEBUG=true
PORT=5001
6. **Run application**:
python app.py

7. **Open browser**
Navigate to: http://localhost:5001


## ⚙️ Configuration

Create `.env` file in project root:

Required
GEMINI_API_KEY=your_gemini_api_key_here

Optional
FLASK_DEBUG=true
PORT=5001

text

**Get Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy key to `.env` file

## 📁 Project Structure

nexus-route-ai/
- ├── app.py # Flask application entry point
- ├── route_optimizer.py # Dijkstra's algorithm engine
- ├── requirements.txt # Python dependencies
- ├── .env # Environment variables
- ├── templates/
- │ └── index.html # Main HTML template
- └── static/
-  ├── css/
-  │ └── style.css # Styling
-  └── js/
-  └── script.js # Frontend logic

text

## 📖 Usage

### Basic Route Planning

1. Select origin and destination cities from dropdowns
2. Click "Calculate Optimal Route"
3. View route on interactive map with distance and time
4. Review AI-powered insights and toll estimates

### AI Command Center (6 Tools)

Click "AI Command Center" header to access:

1. **AI Assistant** - Natural language logistics queries
2. **ETA Prediction** - Delivery time estimates with risk factors
3. **Multi-Stop Optimizer** - Sequence planning for multiple deliveries
4. **Cost Analysis** - Comprehensive expense breakdown
5. **Weather Impact** - Seasonal route analysis
6. **Safety Check** - Compliance and documentation requirements

### Toll Calculator

Automatically displays after route calculation:
- Change vehicle type to update estimates
- View segment-wise breakdown
- Based on NHAI rates

## 📡 API Endpoints

### Core Routes

- GET /api/get_cities
- GET /api/get_shortest_route?src={city}&dest={city}
- POST /api/get_gemini_insights

text

### AI Features

- POST /api/ai/chat
- POST /api/ai/predict_delivery_time
- POST /api/ai/optimize_multi_stop
- POST /api/ai/cost_estimate
- POST /api/ai/weather_impact
- POST /api/ai/safety_check
- POST /api/calculate_toll


## 🔧 Troubleshooting

### Common Issues

**ModuleNotFoundError**
Solution: Activate virtual environment first
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
pip install -r requirements.txt

text

**Gemini API Error**
- Verify `.env` file exists
- Check `GEMINI_API_KEY` is correct
- Get new key from [Google AI Studio](https://makersuite.google.com/app/apikey)

**Port Already in Use**
Change port in .env
PORT=5002

Or kill process (Linux/macOS)
lsof -ti:5001 | xargs kill -9


## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'feat: add feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

**Commit Convention:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Maintenance

## 📄 License

MIT License - Copyright (c) 2025 Jivi

Permission is granted to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software.

## 👨‍💻 Author

**Jivi** - AI & Data Science Engineer

- 🌐 GitHub: [@jivi001](https://github.com/jivi001)
- 💼 LinkedIn: [jivi001](https://www.linkedin.com/in/jivi001)
- 🐦 Twitter: [@1Jivitesh](https://x.com/1Jivitesh)
- 📧 Email: jiviteshgd28@gmail.com

## 🙏 Acknowledgments

- **Google Gemini AI** - Natural language processing
- **OpenStreetMap** - Map data
- **Leaflet.js** - Interactive mapping
- **Flask Community** - Framework and documentation
- **NHAI** - Toll rate reference

## 🚀 Roadmap

**v2.0 (Planned)**
- [ ] Real-time traffic integration
- [ ] Live weather API
- [ ] 50+ cities
- [ ] Route comparison
- [ ] User authentication
- [ ] Save and share routes
- [ ] Mobile app

**v3.0 (Future)**
- [ ] ML route prediction
- [ ] GPS device integration
- [ ] Multi-language support
- [ ] Database integration
- [ ] Analytics dashboard

## 📞 Support

- 📖 **Documentation**: Read this README
- 🐛 **Bug Reports**: [Open Issue](https://github.com/jivi001/logistics_optimizer_desktop/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/jivi001/logistics_optimizer_desktop/discussions)
- 📧 **Email**: jiviteshgd28@gmail.com

---

**Built with ❤️ for the logistics industry**

© 2025 Nexus Route AI. All rights reserved.

**Version**: 1.0.0 | **Last Updated**: November 1, 2025