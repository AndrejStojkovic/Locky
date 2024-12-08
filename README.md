
# 🔒 **Locky - The Funny Lock Screen App**

Locky is a simple, yet powerful, **screen lock application** built using **Python** and **PyQt5**. It provides a fun and interactive way to lock your screen after a specified delay. If you try to move the mouse or press any key, you'll be greeted with a lock screen that requires a password to unlock.

Locky is perfect for anyone looking to **secure their PC when they're away** and maintain privacy while keeping it light, functional, and amusing.

---

## 📋 **Table of Contents**
- [🔧 Features](#-features)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation](#️-installation)
- [🚀 Usage](#-usage)
- [🔑 Password Management](#-password-management)
- [📜 Configuration](#-configuration)
- [📦 Dependencies](#-dependencies)
- [💻 Technologies Used](#-technologies-used)
- [📚 License](#-license)
- [🤝 Contributing](#-contributing)
- [📧 Contact](#-contact)

---

## 🔧 **Features**
- **Custom Delay**: Set a delay time (in seconds) before Locky activates the lock screen.
- **Interactive Lock Screen**: The screen locks and displays a **custom animated cool message** & **funny anime animation**.
- **Secure Unlock**: Enter a **password** to unlock the screen.
- **Password Protection**: Passwords are securely saved in a **local SQLite database**.
- **Switch Control**: Easily activate/deactivate the lock with a single **switch button**.
- **Customizable UI**: You can change the **delay** **language**  **set password** also you can customize the **animation** and **bacground color**.
- **Minimalistic UI**: Simple, intuitive, and clean design.

---

## 📂 **Project Structure**
```
Locky/
│
├── app/
│    ├── dialogs/
│    │    ├── about_dialog.py      # About dialog module
│    │    ├── lock_screen.py       # Lock screen logic and UI
│    │    └── options_dialog.py    # Options dialog for settings
│    ├── utils/                    # Utility functions and helpers
│    └── app.py                    # Main application entry point
├── characters/                    # Folder for character-related assets
├── icon.png                       # App icon
├── .gitignore                     # Git ignore rules
├── locky.py                       # Locky startup script
├── locky.spec                     # PyInstaller spec file
├── locky_db.db                    # SQLite database for storing user data
└── README.md                      # Project documentation
```

---

## ⚙️ **Installation**

To get started with **Locky**, follow these steps:

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/kalco/Locky.git
cd locky
```

### 2️⃣ **Install Dependencies**
Make sure you have **Python 3.7+** installed on your machine. Then, install the dependencies using pip:

```bash
pip install -r requirements.txt
```

### 3️⃣ **Run the Application**
Start the application using:

```bash
python locky.py
```

That's it! 🎉 Locky is now up and running!

---

## 🚀 **Usage**
1. **Launch the app**: Run `python locky.py`.
2. **Set the delay**: Use the input field to set the delay (in seconds) before Locky activates.
3. **Switch on lock**: Click Run to enable the lockscreen.
4. **Lock triggers**: If activity (mouse movement or keypress) occurs for the specified delay, **Locky will activate**.
5. **Unlock the screen**: To regain access, type in your **password** and press **Enter**.

---

## 🔑 **Password Management**
When you first run **Locky**, you need to change the default password. This password will be required every time you unlock the screen. Here’s how you can manage your password:

- **Default password**: Default password is **admin**.
- **Change password**: Go to **Options** and change your password.
- **Reset password**: If you forget your password, you will need to **change the password in options**.

---

## 📜 **Configuration**
Locky can be customized to suit your needs. Here’s how you can configure it:

| **Option**       | **Description**                                  | **Default** |
|-----------------|-------------------------------------------------|-------------|
| `Lock Delay`    | Delay before lock screen activates (in seconds)  | 30 seconds  |
| `Password`      | Your personal unlock password                    | admin       |
| `Language`      | Interface default language                       | English     |
| `Character`     | Choose the animated character                    | 1           |
| `Background`    | Set the bacground of lockscreen                  | 2           |

You can customize these settings directly from the **UI dialog**.

---

## 📦 **Dependencies**
Here are the main dependencies required to run Locky:

- **Python 3.7+**
- **PyQt5** (for GUI)
- **QT-PyQt-PySide-Custom-Widgets** (for custom switch widget)
- **SQLite** (for password storage)

To install them all, simply run:
```bash
pip install -r requirements.txt
```

---

## 💻 **Technologies Used**
- **Programming Language**: Python
- **GUI Framework**: PyQt5
- **Database**: SQLite (for password storage)

---

## 📚 **License**
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🤝 **Contributing**
We welcome contributions from the community! Here's how you can help:

1. **Fork the repo**: [Fork it](https://github.com/kalco/Locky)
2. **Create a new branch**: 
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make changes**: Write your awesome new features!
4. **Test changes**: Run the app to make sure everything works.
5. **Submit a pull request**: We’ll review and merge your changes.

---

## 📧 **Contact**
If you have any issues, suggestions, or feedback, feel free to reach out!

**Email**: martinrajovski@mai.ru  
**GitHub**: [kalco](https://github.com/kalco/Locky)  

We hope you enjoy using **Locky**! ❤️🚀

---
**Made with ❤️ by [Martin Rayovski]**  
**Version: 1.0.0**

---

## ☕ **Support**
If you like **Locky** and want to support its development, consider buying me a coffee. Your support keeps this project alive and motivates us to add more features and improvements!

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/kalco)





