# Manas Hospital Management System

A comprehensive web-based Hospital Management System designed to streamline healthcare operations and patient care. This system provides role-based access for administrators, doctors, and patients with a clean, intuitive interface.

## 🏥 Features

### Admin Features
- Manage doctors, patients, and staff
- Handle bed allocation and management
- Oversee hospital facilities and resources
- Monitor medication inventory
- Generate reports and analytics

### Doctor Features
- View and manage appointments
- Access patient medical records
- Update patient treatment status
- View assigned patients

### Patient Features
- Book and manage appointments
- View medical history
- Check bed availability
- Access doctor information
- View hospital facilities and services

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Database**: MongoDB (via PyMongo)
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- MongoDB
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Anand-303/Manas-Hospital-Management-System.git
   cd Manas-Hospital-Management-System
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add your configuration:
   ```
   SECRET_KEY=your-secret-key
   MONGO_URI=your-mongodb-uri
   ```

5. Run the application:
   ```bash
   python run.py
   ```

6. Open your browser and navigate to `http://localhost:5000`

## 📝 Usage

1. Register a new account or log in with existing credentials
2. Access the dashboard based on your role (Admin/Doctor/Patient)
3. Use the navigation menu to access different features
4. For admin accounts, you can manage users, beds, and hospital resources


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For any queries or support, please contact anskp3073@gmail.com or open an issue on the repository.

---

<div align="center">
  Made with ❤️ by Anand Singh
</div>
