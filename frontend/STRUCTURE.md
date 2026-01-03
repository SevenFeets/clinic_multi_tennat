# Frontend Project Structure

This document explains the organization of the frontend codebase.

## 📁 Directory Structure

```
frontend/
├── public/                          # Static files
│   └── vite.svg
│
├── src/
│   ├── assets/                      # Images, icons, media files
│   │   └── react.svg
│   │
│   ├── components/                  # React components
│   │   ├── common/                  # Reusable UI components
│   │   │   └── .gitkeep             # (Button, Input, Modal, Card, etc.)
│   │   │
│   │   ├── layout/                  # Layout components
│   │   │   └── .gitkeep             # (Navbar, Sidebar, Footer, etc.)
│   │   │
│   │   ├── auth/                    # Authentication components
│   │   │   └── .gitkeep             # (LoginForm, RegisterForm, etc.)
│   │   │
│   │   ├── patients/                # Patient management components
│   │   │   └── .gitkeep             # (PatientList, PatientCard, etc.)
│   │   │
│   │   ├── appointments/            # Appointment components
│   │   │   └── .gitkeep             # (AppointmentList, Calendar, etc.)
│   │   │
│   │   └── dashboard/               # Dashboard specific components
│   │
│   ├── context/                     # React Context providers
│   │   └── .gitkeep                 # (AuthContext, TenantContext, etc.)
│   │
│   ├── hooks/                       # Custom React hooks
│   │   └── .gitkeep                 # (useAuth, useTenant, useApi, etc.)
│   │
│   ├── pages/                       # Page components (routes)
│   │   └── .gitkeep                 # (LoginPage, DashboardPage, etc.)
│   │
│   ├── services/                    # API services
│   │   ├── api.js                   # Base API client
│   │   ├── authService.js           # Authentication API calls
│   │   ├── patientService.js        # Patient API calls
│   │   ├── appointmentService.js    # Appointment API calls
│   │   └── index.js                 # Export all services
│   │
│   ├── styles/                      # Global styles
│   │   └── .gitkeep                 # (Theme, variables, global CSS)
│   │
│   ├── utils/                       # Utility functions
│   │   ├── constants.js             # App constants (API_URL, routes, etc.)
│   │   ├── storage.js               # localStorage helpers
│   │   ├── validators.js            # Validation functions
│   │   ├── formatters.js            # Data formatting functions
│   │   └── tests/                   # Utility tests
│   │
│   ├── App.jsx                      # Main App component with routes
│   ├── App.css                      # App-specific styles
│   ├── main.jsx                     # Entry point
│   └── index.css                    # Global CSS
│
├── .env                             # Environment variables (not in git)
├── .env.example                     # Environment template (in git)
├── .gitignore                       # Git ignore rules
├── index.html                       # HTML template
├── package.json                     # Dependencies
├── vite.config.js                   # Vite configuration
└── README.md                        # Project documentation

```

## 📋 Folder Purposes

### `/components`
**Purpose**: Reusable React components organized by feature/purpose

- **`common/`**: Generic, reusable UI components used throughout the app
  - Examples: Button, Input, Modal, Card, Badge, Spinner
  
- **`layout/`**: Components that define app layout and structure
  - Examples: Navbar, Sidebar, Footer, Header
  
- **`auth/`**: Authentication-related components
  - Examples: LoginForm, RegisterForm, ProtectedRoute
  
- **`patients/`**: Patient management specific components
  - Examples: PatientList, PatientCard, PatientForm, PatientDetails
  
- **`appointments/`**: Appointment management specific components
  - Examples: AppointmentList, AppointmentForm, AppointmentCalendar
  
- **`dashboard/`**: Dashboard-specific components
  - Examples: Stats cards, charts, quick actions

### `/context`
**Purpose**: React Context providers for global state management

- **AuthContext**: User authentication state (user, token, login, logout)
- **TenantContext**: Multi-tenant state (current clinic/tenant)

### `/hooks`
**Purpose**: Custom React hooks for reusable logic

- **useAuth**: Hook to access authentication context
- **useTenant**: Hook to access tenant context
- **useApi**: Hook for API calls with loading/error states

### `/pages`
**Purpose**: Top-level page components that map to routes

- LoginPage
- RegisterPage
- DashboardPage
- PatientsPage
- AppointmentsPage
- NotFoundPage

### `/services`
**Purpose**: API communication layer - all backend API calls

- **api.js**: Base HTTP client with auth headers
- **authService.js**: Authentication API (login, register, logout)
- **patientService.js**: Patient CRUD operations
- **appointmentService.js**: Appointment CRUD operations

### `/styles`
**Purpose**: Global styles, themes, and CSS variables

- Theme configuration
- CSS variables
- Global styles

### `/utils`
**Purpose**: Helper functions and utilities

- **constants.js**: App-wide constants (API URLs, routes, enums)
- **storage.js**: localStorage wrapper functions
- **validators.js**: Form validation functions
- **formatters.js**: Data formatting (dates, phones, etc.)

### `/assets`
**Purpose**: Static files like images, icons, fonts

## 🎯 Design Principles

### 1. **Feature-Based Organization**
Components are grouped by feature (patients, appointments) rather than type

### 2. **Separation of Concerns**
- UI components in `/components`
- Business logic in `/services`
- Global state in `/context`
- Reusable logic in `/hooks`
- Pure functions in `/utils`

### 3. **Clear Dependencies**
```
Pages → Components → Hooks → Context → Services → API
```

### 4. **Scalability**
Easy to add new features by adding new folders in components/

## 📝 Naming Conventions

### Files
- **Components**: PascalCase with `.jsx` extension
  - `LoginForm.jsx`, `PatientCard.jsx`
  
- **Services**: camelCase with `.js` extension
  - `authService.js`, `patientService.js`
  
- **Utils**: camelCase with `.js` extension
  - `validators.js`, `formatters.js`
  
- **Hooks**: camelCase starting with `use`
  - `useAuth.js`, `useApi.js`

### Folders
- **lowercase** for utilities and services
  - `utils/`, `services/`, `hooks/`
  
- **lowercase** for component categories
  - `components/common/`, `components/auth/`

## 🚀 Getting Started

### 1. Create a new component:
```
src/components/[category]/ComponentName.jsx
```

### 2. Create a new page:
```
src/pages/PageName.jsx
```

### 3. Create a new service:
```
src/services/featureService.js
```

### 4. Create a new hook:
```
src/hooks/useFeature.js
```

## ✅ Structure Benefits

1. **Easy Navigation**: Developers know exactly where to find code
2. **Scalability**: Easy to add new features without restructuring
3. **Maintainability**: Clear separation of concerns
4. **Team-Friendly**: Multiple developers can work without conflicts
5. **Professional**: Industry-standard organization

---

## 📚 Next Steps

Now that the structure is in place, you can start building:

1. **Context Providers** - Set up AuthContext and TenantContext
2. **Custom Hooks** - Create useAuth, useTenant, useApi
3. **Pages** - Build LoginPage, DashboardPage
4. **Components** - Create LoginForm, Navbar, etc.

Happy coding! 🎉

