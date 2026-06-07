# ✦ QuoteAlpha — Random Quote Generator

> **CodeAlpha Python Internship Project** · Built with Python 3 & Streamlit

---

## 📌 Project Description

**QuoteAlpha** is a professional Random Quote Generator web application developed as part of the **CodeAlpha Python Programming Internship**. The app delivers curated, categorised wisdom at the click of a button — wrapped in a polished, responsive dark/light-mode UI built entirely with Streamlit and custom CSS.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎲 Random Quote | Displays a new unique quote every time |
| 🗂 Category Filter | Motivation · Success · Life · Study |
| 🔍 Live Search | Search by quote text or author name |
| 🌙 Dark / Light Mode | One-click theme toggle, persisted in session |
| 📋 Copy Quote | Native clipboard copy via Streamlit code block |
| ⭐ Favourites | Add, view, and remove quotes (session-persistent) |
| 📊 Statistics | Total quotes, per-category counts, favourite breakdown |
| 🃏 Animated Cards | Hover effects, fade-in animations, accent stripe |
| 🔢 Quote Counter | Live count badge updates with filters |
| 📱 Responsive | Works on desktop, tablet, and mobile browsers |
| 🧭 Sidebar Navigation | Home · Favourites · Statistics |
| 🔖 Author Attribution | Each quote shows author name and category tag |

---

## 📁 Folder Structure

```
CodeAlpha_RandomQuoteGenerator/
│
├── app.py              # Main Streamlit application
├── quotes.json         # Quote database (60+ quotes, 4 categories)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation (this file)
```

---

## ⚙️ Installation Steps

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/CodeAlpha_RandomQuoteGenerator.git
cd CodeAlpha_RandomQuoteGenerator
```

### 2. (Optional) Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Run Command

```bash
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

---

## 🖼 Screenshots

> _Add screenshots after running the app locally._

| Dark Mode — Home | Light Mode — Favourites | Statistics Page |
|---|---|---|
| _(screenshot)_ | _(screenshot)_ | _(screenshot)_ |

**How to take screenshots:**
1. Run `streamlit run app.py`
2. Press `F12` → Device Toolbar for mobile view
3. Use your OS screenshot tool or Streamlit's built-in camera icon

---

## 🛠 Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3.10+** | Core programming language |
| **Streamlit 1.32+** | Web application framework |
| **JSON** | Quote data storage format |
| **CSS3** | Custom styling, animations, responsive layout |
| **Google Fonts** | Playfair Display + DM Sans typography |
| **Streamlit Session State** | Favourites persistence, theme state |

---

## 🔮 Future Enhancements

- [ ] User authentication with personalised favourites stored in a database
- [ ] Export favourites as PDF or image card
- [ ] Share quote directly to Twitter / LinkedIn
- [ ] Quote of the Day with daily auto-rotation
- [ ] User-submitted quotes with moderation workflow
- [ ] Text-to-speech reading of quotes
- [ ] Animated quote card transitions
- [ ] REST API backend with FastAPI for quote management
- [ ] PWA (Progressive Web App) support for mobile install

---

## 👤 Author

**Your Name**
- 🌐 Portfolio: [yourwebsite.com](https://yourwebsite.com)
- 💼 LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- 🐙 GitHub: [github.com/yourusername](https://github.com/yourusername)
- 📧 Email: your.email@example.com

---

## 📤 GitHub Repository Setup

```bash
# 1. Initialise git (if not cloned)
git init

# 2. Add all files
git add .

# 3. Initial commit
git commit -m "feat: initial release — CodeAlpha Random Quote Generator"

# 4. Add remote origin
git remote add origin https://github.com/yourusername/CodeAlpha_RandomQuoteGenerator.git

# 5. Push
git branch -M main
git push -u origin main
```

**Recommended repository settings:**
- ✅ Add a description: *"Random Quote Generator — CodeAlpha Python Internship Project"*
- ✅ Add topics: `python`, `streamlit`, `quotes`, `codealpha`, `internship`, `web-app`
- ✅ Enable GitHub Pages if you deploy via Streamlit Cloud

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<div align="center">
  Made with ❤️ for the <strong>CodeAlpha Python Internship</strong> · 2024
</div>
