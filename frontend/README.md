# 🏥 Clinic Management - Frontend

A modern, responsive React frontend for the Multi-Tenant Clinic Management System.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- Backend running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Visit http://localhost:5173 in your browser

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── auth/           # Authentication components
│   ├── common/         # Common UI components
│   ├── layout/         # Layout components
│   └── ...
├── context/            # React Context (global state)
│   └── AuthContext.jsx # Authentication state management
├── pages/              # Page components (routes)
│   ├── LoginPage.jsx   # Login screen
│   └── DashboardPage.jsx # Main dashboard
├── services/           # API services
├── styles/             # CSS files
├── utils/              # Utility functions
├── App.jsx             # Main app with routing
└── main.jsx            # Entry point
```

## 🎯 Features

### ✅ Implemented
- **Authentication System**: Login/logout with JWT tokens
- **Login Page**: Modern, responsive login interface
- **Dashboard**: Professional dashboard with stats and quick actions
- **Protected Routes**: Automatic redirect for unauthorized access
- **Multi-tenant Support**: X-Tenant-ID header support
- **Persistent Sessions**: Stays logged in after page refresh

### 🚧 Coming Soon
- Patient Management
- Appointment Scheduling
- Calendar View
- Reports & Analytics
- User Profile Management

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
VITE_API_URL=http://localhost:8000
VITE_DEFAULT_TENANT=cityclinic
VITE_ENV=development
```

**Important:** 
- Restart dev server after changing `.env`
- All env variables must start with `VITE_`

## 🎨 Customization

### Change Colors

Edit color schemes in:
- `src/styles/LoginPage.css` - Login page colors
- `src/styles/DashboardPage.css` - Dashboard colors
- `src/index.css` - Global colors

### Add New Pages

1. Create page component in `src/pages/`
2. Add route in `src/App.jsx`
3. Add navigation link

Example:
```javascript
// 1. Create src/pages/PatientsPage.jsx
function PatientsPage() {
  return <div>Patients</div>;
}

// 2. Add route in App.jsx
<Route 
  path="/patients" 
  element={
    <ProtectedRoute>
      <PatientsPage />
    </ProtectedRoute>
  } 
/>
```

## 📖 Documentation

- **[FRONTEND_GUIDE.md](./FRONTEND_GUIDE.md)** - Complete guide with explanations
- **[STRUCTURE.md](./STRUCTURE.md)** - Project structure details

## 🛠️ Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

## 🧪 Testing the App

### 1. Start Backend
```bash
cd "d:\clinic multi tennant SaaS"
python manage.py runserver
```

### 2. Start Frontend
```bash
cd frontend
npm run dev
```

### 3. Create Test User

Visit http://localhost:8000/admin and create a user with:
- Email: `doctor@clinic.com`
- Password: `yourpassword`

### 4. Login

Visit http://localhost:5173 and login with the credentials above.

## 🐛 Troubleshooting

### Login not working?
- ✅ Check backend is running on port 8000
- ✅ Check `.env` file has correct `VITE_API_URL`
- ✅ Check browser console (F12) for errors
- ✅ Verify user exists in Django admin

### Styles not showing?
- ✅ Hard refresh: `Ctrl + Shift + R`
- ✅ Check CSS files are imported
- ✅ Clear browser cache

### Environment variables not working?
- ✅ Restart dev server
- ✅ Make sure variables start with `VITE_`
- ✅ Access with `import.meta.env.VITE_VARIABLE_NAME`

## 🎓 Learning Resources

- [React Documentation](https://react.dev)
- [React Router](https://reactrouter.com)
- [Vite Guide](https://vite.dev/guide/)

## 📝 Tech Stack

- **React 19** - UI framework
- **Vite 7** - Build tool & dev server
- **React Router 6** - Client-side routing
- **CSS3** - Styling (no framework, custom CSS)
- **Fetch API** - HTTP requests

## 🤝 Contributing

When adding new features:
1. Follow the existing folder structure
2. Add comments explaining your code
3. Test with backend before committing
4. Update documentation if needed

## 📄 License

Part of the Multi-Tenant Clinic Management System project.

---

**Built with ❤️ for modern clinic management**
