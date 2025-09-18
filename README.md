# 🗒️ Django Notes App (Demo Project)

![Notes App Demo](demo.gif)

A demo **note-taking application** built with **Django, HTMX, and Bootstrap**.  
This project showcases full CRUD functionality, authentication, profile management, search, filtering, and server-driven interactivity.  

---

## 🚀 Features

### 🔐 Authentication & Profiles
- User registration, login, and logout  
- Profile update functionality  

### 🗒️ Notes Management (CRUD)
- Create, read, update, and delete notes  
- Responsive forms and layouts styled with Bootstrap  

### 🔍 Search & Filtering
- Live search using HTMX  
- Filter notes by favorites for quick access  

### ❤️ Favorites
- Mark notes as favorites  
- Filter favorite notes separately  

### ⚡ HTMX Integration
- Dynamic updates without full page reloads  
- Partial templates for smooth interactivity  

### 🎨 Bootstrap Styling
- Clean and responsive UI  
- Mobile-friendly layout  

---

## 🛠️ Tech Stack
- [Django](https://www.djangoproject.com/) – Web framework  
- [HTMX](https://htmx.org/) – Dynamic interactivity without heavy JS  
- [Bootstrap](https://getbootstrap.com/) – Responsive UI framework  
- SQLite (default) 

---

## 📦 Installation & Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/Minenhle-Ngubane/notes-app.git
   cd notes-app

2. **Create and activate a virtual environment**
    ```python -m venv venv
        # Activate virtual environment
        # On Linux/Mac:
        source venv/bin/activate
        # On Windows:
        venv\Scripts\activate
    ```

3. **Install dependencies**
    ```pip install -r requirements.txt```

4. **Apply migrations**
    ```python manage.py migrate```

5. **Create a superuser (admin)**
    ```python manage.py createsuperuser```

6. **Run the development server**
    ```python manage.py runserver```

7. **Access the app**
   - Open your browser and visit:
👉      http://127.0.0.1:8000/