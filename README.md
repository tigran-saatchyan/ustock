# UStock – Unified Financial Platform

![UStock Logo](https://via.placeholder.com/300x100?text=UStock+Logo)
*Placeholder image for UStock logo*

UStock is a full-stack financial platform for tracking, analyzing, and managing stocks, options, cryptocurrencies, and personal finance. It features a Django backend (REST API, business logic, data management) and a Vue.js (TypeScript) frontend (modern UI, dashboards, charts). UStock is designed for individuals and investors seeking a unified, extensible solution for all their financial data and analytics needs.

---

## Table of Contents
- [UStock – Unified Financial Platform](#ustock--unified-financial-platform)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Key Features](#key-features)
  - [Tech Stack](#tech-stack)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
    - [Backend (Django)](#backend-django)
    - [Frontend (Vue.js)](#frontend-vuejs)
  - [API Endpoints](#api-endpoints)
  - [Documentation](#documentation)
  - [Testing](#testing)
  - [Progress \& Roadmap](#progress--roadmap)
  - [License and Terms of Service](#license-and-terms-of-service)
  - [Contributing](#contributing)
  - [Contact](#contact)

---

## Overview
UStock unifies financial data and tools for stocks, options, crypto, and personal finance. It provides:
- Real-time and historical market data
- Personal finance management
- Interactive dashboards and analytics
- Secure user authentication
- Extensible architecture for future financial tools

---

## Key Features
- **Unified Dashboard:** View and analyze stocks, options, crypto, and personal finance in one place
- **Comprehensive Data:** Real-time and historical data for multiple asset classes
- **Personal Finance Tools:** Track expenses, budgets, and financial goals
- **Interactive Charts:** Visualize trends and analytics with modern charting libraries
- **Modular Architecture:** Easily extend with new features or asset classes
- **Secure Authentication:** Robust user management and data privacy
- **RESTful API:** Django backend exposes endpoints for all core features
- **Responsive Frontend:** Vue.js UI for seamless experience across devices

---

## Tech Stack
- **Backend:** Python 3.12, Django, Django REST Framework
- **Frontend:** Vue.js (TypeScript), Vuex, Vue Router, Chart.js/ECharts
- **Database:** PostgreSQL (recommended)
- **Caching:** Redis (optional, for performance)
- **Testing:** pytest (backend), Vue Test Utils/Jest (frontend)
- **Other:** Axios (API calls), Poetry (backend deps), Node.js/NPM (frontend deps)

---

## Project Structure
```bash
UStock/
├── frontend/                  # Vue.js frontend (TypeScript)
│   ├── src/
│   │   ├── components/       # UI components (charts, finance, etc.)
│   │   ├── views/            # Page views
│   │   ├── store/            # Vuex modules
│   │   ├── router/           # Frontend routing
│   │   └── ...
│   └── public/
├── src/                      # Django backend
│   ├── apps/
│   │   ├── financials/       # Financial statements & market data
│   │   ├── options/          # Options data
│   │   ├── tickers/          # Ticker info & news
│   │   ├── personal_finance/ # Personal finance features
│   │   └── custom_auth/      # Authentication
│   ├── config/               # Django settings & URLs
│   ├── services/             # External API clients, helpers
│   └── utils/                # Shared utilities
├── memory-bank/              # Project documentation & context
├── README.md
├── LICENSE.md
├── TERMS_OF_SERVICE.md
├── pyproject.toml            # Backend dependencies
├── poetry.lock
├── package.json              # Frontend dependencies (in frontend/)
└── ...
```

---

## Getting Started

### Backend (Django)
1. **Install dependencies:**
   ```bash
   cd src
   poetry install
   ```
2. **Configure environment:**
   - Copy `.env.example` to `.env` and set variables as needed
3. **Apply migrations:**
   ```bash
   poetry run python manage.py migrate
   ```
4. **Run backend server:**
   ```bash
   poetry run python manage.py runserver
   ```
   The API will be available at `http://127.0.0.1:8000/api/v1/`

### Frontend (Vue.js)
1. **Install dependencies:**
   ```bash
   cd ../frontend
   npm install
   ```
2. **Run frontend dev server:**
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173/` (default Vite port)

---

## API Endpoints
See backend API documentation for full list. Example endpoints:
- `/api/v1/tickers/<ticker>/` – Ticker info
- `/api/v1/options/<ticker>/chain/` – Option chain data
- `/api/v1/financials/<ticker>/` – Financial statements
- `/api/v1/personal_finance/` – Personal finance data

Interactive docs:
- **Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc UI:** [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

---

## Documentation
- **Backend:** Auto-generated API docs (Swagger/ReDoc)
- **Frontend:** Modular code, with components and store modules organized by feature
- **Project Context:** See `memory-bank/` for project goals, architecture, and progress

---

## Testing
- **Backend:**
  ```bash
  poetry run pytest
  ```
- **Frontend:**
  ```bash
  npm run test
  ```

---

## Progress & Roadmap
- Modular backend and frontend structure in place
- Core features for stocks, options, crypto, and personal finance implemented or in progress
- Next: Expand analytics, improve error handling, enhance documentation, and refine UI/UX

---

## License and Terms of Service
UStock is licensed under the MIT License. See [LICENSE.md](./LICENSE.md) for details.
See [TERMS_OF_SERVICE.md](./TERMS_OF_SERVICE.md) for terms of service.

---

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Contact
For questions, suggestions, or support, contact:
- **Name:** Tigran Saatchyan
- **Email:** [mr.saatchyan@yandex.com](mailto:mr.saatchyan@yandex.com)
- **GitHub:** [tigran-saatchyan](https://github.com/tigran-saatchyan)

---

*Note: Replace placeholder images and add more detailed usage examples as the project evolves.*
