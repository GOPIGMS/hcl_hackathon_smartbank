# 🏦 SmartBank — User Registration, KYC & Core Banking Module

## 📘 Overview
**SmartBank** is a modular, secure backend system designed for hackathon banking operations.  
This module focuses on **User Registration**, **KYC verification**, **Loan management**, and **Transaction logging** with full **Admin & Auditor access control**.

The system is built using **Django 5.x**, **Django REST Framework (DRF)**, **JWT authentication**, and **role-based access control (RBAC)**.  
All key operations (registration, transactions, verifications) are tracked via a **centralized audit log** for transparency and compliance.

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| Framework | **Django 5.x** |
| REST API | **Django REST Framework (DRF)** |
| Authentication | **JWT (SimpleJWT)** |
| Database | **MySQL** |
| File Uploads | **Django FileField (Media)** |
| Logging | **Custom AuditLog Model + Python Logging** |
| Testing | **pytest, pytest-django (Unit & Integration Tests)** |
| API Browsing | **DRF API Browser (via ViewSets)** |
| Rate Limiting | **DRF Throttling** |

---

### Module Name
**1. User Registration and KYC**


### Description
This module allows:
- Customers to register using their basic details.
- Upload KYC documents for verification.
- Automatically assign UUIDs and roles.
- Authentication using **JWT tokens**.
- Enforced **rate limits** to prevent abuse.
- **Audit logging** for all registration and verification activities.

Admins and auditors can later verify KYC, manage roles, and access logs through secure endpoints.

---

---

## 🧩 Database Schema

# 🧩 Core Database Tables

---

## 1️⃣ User Table

| Field | Type | Description |
|--------|------|-------------|
| id | Auto | Primary key |
| username | CharField | Unique login ID |
| email | EmailField | User email |
| password | CharField | Encrypted password |
| is_active | Boolean | Determines if the user can log in |
| role | CharField | Role assigned → customer / admin / auditor |
| date_joined | DateTime | Account creation date |
| last_login | DateTime | Last login timestamp |

**Purpose:**  
Base authentication table used by Django. Every user (customer, admin, auditor) originates from here.

---

##  Customer Table

| Field | Type | Description | Access |
|--------|------|-------------|---------|
| user | OneToOne(User) | Linked user account | System |
| address | TextField | Customer address | Customer |
| phone | CharField(15) | Contact number | Customer |
| kyc_file | FileField | Uploaded KYC document | Customer |
| is_verified | Boolean | KYC approved by admin | Admin only |
| account_status | CharField | active / suspended / closed | Admin only |
| created_at | DateTime | Record creation timestamp | System |
| updated_at | DateTime | Record update timestamp | System |

**Purpose:**  
Stores customer-specific profile and KYC information.  
Customers can only see and modify their personal info — KYC approval and account status are managed by Admins.

---

##  CustomerVerification Table

| Field | Type | Description | Access |
|--------|------|-------------|---------|
| id | Auto | Primary key | System |
| customer | FK(Customer) | Customer being verified | System |
| verified_by | FK(Admin) | Admin who reviewed KYC | Admin |
| verified_at | DateTime | Time of verification | System |
| status | CharField | approved / pending / rejected | Admin |
| remarks | TextField | Admin remarks on verification | Admin |

**Purpose:**  
Keeps a record of every KYC verification performed by an Admin.  
Used for auditing and traceability — accessible to Auditors for read-only review.

---

##  Admin Table

| Field | Type | Description | Access |
|--------|------|-------------|---------|
| user | OneToOne(User) | Linked user account | System |
| employee_id | CharField | Unique admin ID | System |
| department | CharField | Department name (e.g., Compliance, KYC) | System |
| verified_count | Integer | Number of customers verified | Admin |
| last_activity | DateTime | Recent admin activity | System |
| created_at | DateTime | Created timestamp | System |

**Purpose:**  
Represents system administrators who manage customer verifications and account statuses.  
Each admin’s activity is logged and reviewable by auditors.

---

##  Auditor Table

| Field | Type | Description | Access |
|--------|------|-------------|---------|
| user | OneToOne(User) | Linked user account | System |
| auditor_id | CharField | Unique auditor code | System |
| access_scope | CharField | full / regional / limited | System |
| last_audit_date | DateTime | Last audit performed | Auditor |
| remarks | TextField | Optional notes | Auditor |
| created_at | DateTime | Created timestamp | System |

**Purpose:**  
Auditors have read-only access to key operational data (KYC, verifications, audit logs).  
They ensure compliance and transparency across the system.

---

### **2️⃣ Account Table**

| Field | Type | Description |
|--------|------|-------------|
| `account_number` | CharField | Unique account number |
| `customer` | OneToOne(Customer) | Account owner |
| `balance` | Decimal | Current balance |
| `account_type` | CharField | savings/current |
| `is_active` | Boolean | Account active flag |
| `created_at` | DateTime | Timestamp |
| `updated_at` | DateTime | Timestamp |

---

### **3️⃣ Transaction Table**

| Field | Type | Description |
|--------|------|-------------|
| `transaction_id` | UUID | Primary key |
| `account` | FK(Account) | Linked account |
| `amount` | Decimal | Transaction amount |
| `transaction_type` | CharField | debit / credit |
| `description` | TextField | Transaction details |
| `timestamp` | DateTime | Time of transaction |
| `status` | CharField | success / failed / pending |
| `flag` | CharField | normal / suspicious / reviewed |
| `reference_id` | UUID | Optional reference link |
| `logged_by` | FK(User) | User who initiated |

#### ⚙️ Flag Usage
- **normal** → Standard transaction  
- **suspicious** → Auto-flagged (large or rapid transaction)  
- **reviewed** → Reviewed by admin/auditor  

Admins and auditors can filter transactions via:  
`/api/transactions/?flag=suspicious`

---

### **4️⃣ Account_Verify Table**

| Field | Type | Description |
|--------|------|-------------|
| `id` | Auto | Primary key |
| `account` | FK(Account) | Verified account |
| `verified_by` | FK(Admin User) | Who verified |
| `status` | CharField | pending/approved/rejected |
| `verified_at` | DateTime | When verified |
| `remarks` | TextField | Comments |

---

### **5️⃣ Loan_Verify Table**

| Field | Type | Description |
|--------|------|-------------|
| `id` | Auto | Primary key |
| `customer` | FK(Customer) | Applicant |
| `loan_amount` | Decimal | Requested loan amount |
| `loan_type` | CharField | home/personal/education |
| `status` | CharField | pending/approved/rejected |
| `verified_by` | FK(Admin) | Admin verifier |
| `verified_at` | DateTime | Verification timestamp |
| `remarks` | TextField | Comments |

---

### **6️⃣ Fraud_Verify Table**

| Field | Type | Description |
|--------|------|-------------|
| `id` | Auto | Primary key |
| `account` | FK(Account) | Related account |
| `reported_by` | FK(User/System) | Who raised the alert |
| `report_details` | TextField | Description |
| `status` | CharField | under_review/confirmed/false_positive |
| `resolved_by` | FK(Admin) | Who resolved |
| `resolved_at` | DateTime | Resolution time |

---

### **7️⃣ Promotion Table**

| Field | Type | Description |
|--------|------|-------------|
| `id` | Auto | Primary key |
| `promoter` | FK(User) | Who promoted |
| `promoted_user` | FK(User) | Who was promoted |
| `promoted_role` | CharField | admin/auditor/customer |
| `timestamp` | DateTime | Promotion time |

---

### **8️⃣ AuditLog Table**

| Field | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `user` | FK(User) | Who performed the action |
| `role` | CharField | admin/auditor/customer |
| `action` | CharField | e.g., LOGIN_SUCCESS, KYC_UPLOADED |
| `description` | TextField | Action details |
| `ip_address` | IP | Source IP |
| `timestamp` | DateTime | Action time |
| `status` | CharField | success/failed |
| `reference_id` | UUID | Optional FK to transaction/loan |

---

## 🔒 Access Control

| Role | Permissions |
|------|--------------|
| **Customer** | Register, login, update address/KYC, view own transactions/loans |
| **Admin** | Approve/reject KYC, verify accounts/loans, update roles, access all logs |
| **Auditor** | Read-only access to all logs, cannot modify data |
| **System** | Auto-creates logs, verifies fraud alerts |

---

## 🧾 Logging & Audit Access

### Storage
- All logs are stored in the **`AuditLog`** database table.
- Python logging optionally writes a backup at `/logs/audit.log`.

### Access
- **Admin** → Full access (`GET`, `PATCH`, `DELETE`)  
- **Auditor** → Read-only (`GET`)  
- **Customer** → ❌ No access  

### DRF Permission Example
```python
class IsAuditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='auditor_group').exists()

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='admin_group').exists()
