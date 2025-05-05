# 🗃️ Inventory Management System

A simple web-based Inventory Management System built with Flask and SQLite. This application allows users to manage products, warehouse locations, stock levels, and product movements between locations. It also provides basic reporting features.

---

## 🚀 Features

- ✅ Add, View, and Edit Products
- ✅ Add, View, and Edit Locations
- ✅ Manage Stock Quantities per Product per Location
- ✅ Move Products Between Locations
- ✅ Generate Reports by Product or Location

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (`inventory.db`)
- **Frontend**: HTML, Jinja2 Templates, Bootstrap (optional)

---
```sql
CREATE TABLE products (
    P_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    P_NAME TEXT NOT NULL,
    PRICE INTEGER
);

CREATE TABLE locations (
    L_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    L_NAME TEXT NOT NULL
);

CREATE TABLE stocks (
    P_ID INTEGER,
    P_NAME TEXT,
    L_NAME TEXT,
    QTY INTEGER
);

CREATE TABLE movements (
    M_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TIMESTAMP TIME DEFAULT CURRENT_TIMESTAMP
    P_ID INTEGER,
    QTY INTEGER,
    FROM_LOCATION TEXT,
    TO_LOCATION TEXT
);
```
## 📁 Project Structure
```bash
.
├── app.py # Main Flask application
├── inventory.db # SQLite database
├── templates/ # HTML templates
│ ├── add_locations.html
│ ├── add_products.html
│ ├── edit_locations.html
│ ├── edit_products.html
│ ├── index.html
│ ├── layout.html
│ ├── move_products.html
│ ├── product_report.html
│ ├── report.html
│ ├── view_locations.html
│ ├── view_productmovements.html
│ ├── view_products.html
│ ├── view_report.html
│ └── view_stocks.html
```

## SCREENSHOTS:



![Screenshot 2025-05-05 212125](https://github.com/user-attachments/assets/b64fd7ad-ea0e-4b71-b552-fef719cae768)
![Screenshot 2025-05-05 212049](https://github.com/user-attachments/assets/27e87200-9e4a-4aec-9a51-5a05a4cfa45a)
![Screenshot 2025-05-05 212038](https://github.com/user-attachments/assets/a43baf2a-53f2-45e1-ac4f-79a704f2e281)
![Screenshot 2025-05-05 212021](https://github.com/user-attachments/assets/0cefc3fc-1209-4b7a-819b-1e542a5f6255)
![Screenshot 2025-05-05 211941](https://github.com/user-attachments/assets/15b98ad8-b1fb-41f4-8176-c140bc6c6a8e)
![Screenshot 2025-05-05 211927](https://github.com/user-attachments/assets/2b48ee36-ccc7-42db-b35d-9cb8c851547b)
![Screenshot 2025-05-05 211914](https://github.com/user-attachments/assets/9e40dfb2-1d1a-4851-9487-20ad33dbcaf2)
![Screenshot 2025-05-05 211900](https://github.com/user-attachments/assets/ab9a3301-7c50-41b2-8879-a0467f8efb3a)
![Screenshot 2025-05-05 211658](https://github.com/user-attachments/assets/80fb78fe-0401-48ac-b252-6498c3198601)
![Screenshot 2025-05-05 211645](https://github.com/user-attachments/assets/523bb223-7dee-4c0e-bda8-31886a979a03)

## SCREEN RECORDING:

https://drive.google.com/file/d/14YW6oT13cZP7a3kHEFFRcm2fOvWRRm0Y/view?usp=sharing
