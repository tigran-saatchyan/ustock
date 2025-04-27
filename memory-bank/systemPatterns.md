# System Patterns

## System Architecture

- Backend: Django REST API, modular apps for financials, options, personal finance, tickers, and authentication
- Frontend: Vue.js with TypeScript, modular components for charts, finance, authentication, and navigation

## Key Technical Decisions

- Use of Django for rapid backend development and robust ORM
- RESTful API design for frontend-backend communication
- Vue.js with TypeScript for scalable, maintainable frontend
- Modularization of both backend and frontend for extensibility

## Design Patterns in Use

- MVC (Model-View-Controller) in Django backend
- Component-based architecture in Vue.js frontend
- Service and store modules for state management and API calls

## Component Relationships

- Backend apps expose REST endpoints consumed by frontend services
- Frontend components interact via Vuex store and service modules
- Charts and dashboards aggregate data from multiple backend sources 