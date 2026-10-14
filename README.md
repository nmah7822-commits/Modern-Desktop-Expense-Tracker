# 💰 SpendWise: Modern Desktop Expense Tracker

## 📌 Brief One Line Summary
A sleek, modern, and lightweight desktop application to track daily expenses, manage monthly budgets, and visualize financial habits in real-time.

##  Overview
**SpendWise** is a personal finance management tool built with Python. It allows users to log their daily spending, set monthly budget limits, and get instant visual feedback through progress bars and interactive pie charts. It also features data filtering, searching, and one-click CSV export for external analysis.

## ⚠️ Problem Statement
Most people struggle to track their small daily expenses, which leads to budget overruns by the end of the month. Existing financial software is often too heavy, expensive, or requires an internet connection. There is a need for a lightweight, private, and easy-to-use offline desktop tool.

## 🗄️ Data Storage (Dataset)
Instead of a cloud dataset, this application uses a **Local SQLite Database (`expenses.db`)**. 
*   **Why SQLite?** It ensures 100% data privacy, requires no internet connection, and provides lightning-fast query performance for filtering and sorting expenses.

## ️ Tools and Technologies
*   **Programming Language:** Python 3.x
*   **GUI Framework:** CustomTkinter (For modern, responsive, and aesthetic UI)
*   **Database:** SQLite3 (Built-in relational database)
*   **Data Visualization:** Matplotlib (For generating interactive Pie Charts)
*   **Data Handling:** CSV Module (For data export)

## ⚙️ Methods & Architecture
The project follows an **Object-Oriented Programming (OOP)** approach with a clean separation of concerns:
1.  **`database.py`:** Handles all backend logic, SQL queries, and database connections.
2.  **`main.py`:** Handles the frontend UI, user events, and rendering charts.
3.  **Event-Driven Programming:** Real-time updates to the budget dashboard whenever an expense is added or deleted.

## 💡 Key Insights
*   **Visual Feedback:** The dynamic progress bar changes color (Green -> Orange -> Red) as the user approaches their budget limit, providing immediate psychological feedback.
*   **Data Filtering:** Users can instantly filter expenses by category or search keywords to analyze specific spending habits.
*   **Portability:** The CSV export feature allows users to take their data to Excel for deeper financial planning.

##  Dashboard / Model / Output
*(Note: Yahan aap apni app ki 3 screenshots lagayengi. Neeche instructions hain)*

### 1. Main Dashboard & Budget Tracker
![Main Dashboard](screenshots/dashboard.png)

### 2. Interactive Pie Chart
![Pie Chart](screenshots/chart.png)

### 3. Filter & Search Functionality
![Filter Search](screenshots/filter.png)

## 🚀 How to Run This Project?
Follow these simple steps to run the application on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/Modern-Desktop-Expense-Tracker.git
    cd Modern-Desktop-Expense-Tracker
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application:**
    ```bash
    python main.py
    ```

## 🎯 Results & Conclusion
The project successfully delivers a fully functional, aesthetically pleasing desktop application that solves the problem of personal expense tracking. It demonstrates strong skills in GUI development, database management, and data visualization without relying on heavy external frameworks.

## 🔮 Future Work
*   **Dark/Light Mode Toggle:** Adding a switch to change the app theme dynamically.
*   **Recurring Expenses:** Automating monthly bills like rent or subscriptions.
*   **Cloud Sync:** Optional integration with Firebase for cross-device data syncing.

