# 🚗 **Crudcar-Django**  
![Python](https://img.shields.io/badge/Python-yellow?style=flat&logo=python&logoColor=white)  
![Django](https://img.shields.io/badge/Django-darkgreen?style=flat&logo=django&logoColor=white)  
![Bootstrap](https://img.shields.io/badge/Bootstrap-purple?style=flat&logo=bootstrap&logoColor=white)  
![SQLite](https://img.shields.io/badge/SQLite-blue?logo=sqlite&logoColor=white)  
![Platform](https://img.shields.io/badge/Platform-Web-blue?logo=google-chrome)  
![Last Commit](https://img.shields.io/github/last-commit/ander1code/djangoproject?color=yellow&logo=github)  

---

## 📌 **Project Description**
**Crudcar-Django** is a complete **CRUD web application** built using the **Django** framework, powered by an **SQLite** database and styled with a **responsive Bootstrap interface**.

🔐 The system enables users to register **customers** and manage **multiple cars per customer** in a secure and user-friendly way. It also includes an intuitive admin panel and a fully functional **authentication system** with access control.

---

## 🚀 **Main Features**
- 👤 **Customer-Car Relationship:**  
  Each customer can register and manage **multiple cars** under their profile.

- 🔐 **User Authentication:**  
  - Secure login system with password protection  
  - Restricted access to certain actions for logged-in users only

- 📱 **Responsive Design:**  
  Built with **Bootstrap** to ensure a smooth experience across **mobile** and **desktop** devices.

- ⚙️ **Admin Interface:**  
  - Access to the `/admin` panel for superusers  
  - Complete data management for customers, cars, and users

- 💾 **Data Persistence with SQLite:**  
  Lightweight and easy-to-use database — perfect for development and testing.

---

## 🛠️ **Technologies Used**

### ⚙️ Back-End
- **Framework:** Django `5.2.7`
- **Language:** Python `3.13.7`
- **Database:** SQLite `3`

### 🎨 Front-End
- **CSS Framework:** Bootstrap `3.3.7`
- **Templating:** HTML5 + CSS3 + Django Templating Engine

### 💻 Development Environment
- **IDE:** Visual Studio Code `1.67.2`
- **Recommended Extensions:**  
  - Python  
  - Django  
  - SQLite Viewer  
  - Prettier

---

## 📷 **Screenshots** *(optional)*
> You can add screenshots here such as:  
> - Login Page  
> - Dashboard  
> - Registration Forms  
> - Admin Panel

---

## 🧪 **How to Run This Project Locally**

```bash
# Clone the repository
git clone https://github.com/ander1code/djangoproject.git
cd djangoproject

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver

---

## 📁 Project Structure

C:.
│ db.sqlite3
│ manage.py
│ README.md
│
├───crud
│ │ admin.py
│ │ apps.py
│ │ forms.py
│ │ models.py
│ │ tests.py
│ │ urls.py
│ │ views.py
│ │ init.py
│ │
│ ├───migrations
│ │ │ 0001_initial.py
│ │ │ init.py
│ │
│ ├───static
│ │ ├───css
│ │ │ bootstrap-datepicker.css
│ │ │ bootstrap-datepicker.css.map
│ │ │ bootstrap-datepicker.min.css
│ │ │ bootstrap-datepicker.min.css.map
│ │ │ bootstrap-datepicker.standalone.css
│ │ │ bootstrap-datepicker.standalone.css.map
│ │ │ bootstrap-datepicker.standalone.min.css
│ │ │ bootstrap-datepicker.standalone.min.css.map
│ │ │ bootstrap-datepicker3.css
│ │ │ bootstrap-datepicker3.css.map
│ │ │ bootstrap-datepicker3.min.css
│ │ │ bootstrap-datepicker3.min.css.map
│ │ │ bootstrap-datepicker3.standalone.css
│ │ │ bootstrap-datepicker3.standalone.css.map
│ │ │ bootstrap-datepicker3.standalone.min.css
│ │ │ bootstrap-datepicker3.standalone.min.css.map
│ │ │ bootstrap.css
│ │ │ bootstrap.min.css
│ │ │ crud-css.css
│ │ │ jquery-ui.css
│ │ │
│ │ ├───fonts
│ │ │ glyphicons-halflings-regular.eot
│ │ │ glyphicons-halflings-regular.svg
│ │ │ glyphicons-halflings-regular.ttf
│ │ │ glyphicons-halflings-regular.woff
│ │ │ glyphicons-halflings-regular.woff2
│ │ │
│ │ ├───img
│ │ │ favicon.png
│ │ │ logob.png
│ │ │ logod.png
│ │ │ logop.png
│ │ │ logop.svg
│ │ │ logos.png
│ │ │ select.png
│ │ │
│ │ └───js
│ │ bootstrap-datepicker.js
│ │ bootstrap-datepicker.pt-BR.min.js
│ │ bootstrap.min.js
│ │ currency.js
│ │ datetime.js
│ │ jquery-3.2.1.min.js
│ │ jquery-ui.js
│ │ jquery.maskMoney.js
│ │
│ ├───templates
│ │ │ index.html
│ │ │
│ │ ├───car
│ │ │ catalog.html
│ │ │ create.html
│ │ │ edit.html
│ │ │ show.html
│ │ │
│ │ ├───customer
│ │ │ create.html
│ │ │ edit.html
│ │ │ list.html
│ │ │ show.html
│ │ │
│ │ ├───home
│ │ │ home.html
│ │ │
│ │ ├───login
│ │ │ login.html
│ │ │
│ │ └───partials
│ │ header.html
│ │ messages.html
│ │ paths_after.html
│ │ paths_before.html
│ │
│ ├───utils
│ │ │ validators.py
│
├───djangoproject
│ │ asgi.py
│ │ settings.py
│ │ urls.py
│ │ wsgi.py
│ │ init.py
│
└───media
