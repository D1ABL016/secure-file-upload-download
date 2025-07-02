# File Share Project

A Django-based file sharing platform with JWT authentication, supporting two user roles: **ops** (operations) and **client**. Ops users can upload files, and client users can view and download them after email verification.

---

## Features
- JWT authentication (email & password login)
- Custom user model with roles: `ops` and `client`
- Email verification for client users
- File upload (ops only, supports pptx, docx, xlsx)
- File listing and download (client only)

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <project-directory>
```

### 2. Create a virtual environment and activate it
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (for admin access)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

---

## API Endpoints

### **User Signup**
- **Client Signup:**
  - `POST /client/signup/`
  - Body: `{ "email": "client@example.com", "password": "yourpassword" }`
- **Ops Signup:**
  - `POST /ops/signup/`
  - Body: `{ "email": "ops@example.com", "password": "yourpassword" }`

### **Email Verification (Client Only)**
- After signup, client receives a verification URL in the response. Visit the URL to verify the email.

### **Login (JWT Token)**
- `POST /login/`
- Body: `{ "email": "user@example.com", "password": "yourpassword" }`
- Response: `{ "refresh": "...", "access": "..." }`

### **File Upload (Ops Only)**
- `POST /ops/upload-file/`
- Header: `Authorization: Bearer <access_token>`
- Body: `form-data` with key `file` (pptx, docx, xlsx only)

### **List Files (Client Only)**
- `GET /client/files/`
- Header: `Authorization: Bearer <access_token>`
- Response: List of all uploaded files

### **Download File (Client Only)**
- `GET /client/files/<file_id>/download/`
- Header: `Authorization: Bearer <access_token>`
- Downloads the file with the given ID

---

## Authentication
- All endpoints (except signup and email verification) require JWT authentication.
- Obtain your access token via `/login/` and include it in the `Authorization` header as `Bearer <access_token>`.

---

## User Roles
- **Ops User:** Can upload files.
- **Client User:** Can view and download files after verifying their email.

---

## Notes
- Uploaded files are stored in the `media/uploads/` directory.
- Only pptx, docx, and xlsx files are allowed for upload.
- Use Django admin (`/admin/`) to manage users and files if needed.

---

## Development
- Default database: SQLite (`db.sqlite3`)
- Custom user model: `file_share.User`
- Media files: `media/`

---

## License
MIT (or specify your license) 