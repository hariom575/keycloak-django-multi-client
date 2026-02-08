# Keycloak + Django Multi‑Client Dummy Project

This project is a **learning / dummy setup** to understand how an **Identity and Access Management (IAM)** tool like **Keycloak** works with **multiple clients** and **Django applications**.

The goal is to clearly understand the concepts of:

* Realm
* Clients (multiple apps)
* Users
* Roles & permissions
* Token‑based authentication (OAuth2 / OpenID Connect)

---

## 🧠 What this project demonstrates

* One **Keycloak Realm** managing identity
* Multiple **clients** inside the same realm
* Separate Django apps acting as **resource servers**
* Role‑based access control using **JWT access tokens**
* Token validation using Keycloak `/userinfo` endpoint

---

## 🏗 Architecture Overview

```
User
  ↓ (login)
Keycloak (Realm: universe-realm)
  ↓ (JWT Access Token)
Django App (student-client)
```

---

## 📦 Tech Stack

* **Keycloak** (Docker image)
* **Django** (Python 3.11)
* **Docker & Docker Compose**
* **Postman / curl** for testing

---

## 📁 Project Structure

```
keycloak-django-multi-client/
│
├── docker-compose.yml
│
├── student-app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   └── app/
│       ├── views.py
│       └── urls.py
├── faculty-app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   └── app/
│       ├── views.py
│       └── urls.py
│
└── README.md
```

---

## 🚀 Step 1: Start Keycloak

Run the containers:

```bash
docker-compose up --build
```

Keycloak will be available at:

```
http://localhost:8080
```

---

## 🔐 Step 2: Keycloak Setup (Admin UI)

### 1️⃣ Create Realm

* Realm name: `universe-realm`

### 2️⃣ Create Client

**Client ID:** `student-client`

Settings:

* Client type: `OpenID Connect`
* Access type: `Confidential`
* Direct Access Grants: ✅ Enabled

➡️ Save

### 3️⃣ Get Client Secret

* Open client → **Credentials tab**
* Copy the **Client Secret**

This is used by Django / Postman.

---

## 👤 Step 3: Create User

* Username: `hariom`
* Set password
* Disable **Temporary password**

⚠️ IMPORTANT:

> If password is temporary, login will fail with:
> `Account is not fully set up`

---

## 🏷 Step 4: Create Roles

Inside **student-client**:

* Role name: `view_courses`

Assign this role to the user `hariom`.

---

## 🧪 Step 5: Testing Login (Token Generation)

### Option A: Using curl

```bash
curl -X POST http://localhost:8080/realms/universe-realm/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=student-client" \
  -d "client_secret=<CLIENT_SECRET>" \
  -d "username=hariom" \
  -d "password=hariom"
```

### Successful Response

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "expires_in": 300,
  "token_type": "Bearer"
}
```

Copy the **access_token**.

---

## 🧪 Step 6: Testing via Postman

### 🔑 Login (Token Request)

**Method:** POST
**URL:**

```
http://localhost:8080/realms/universe-realm/protocol/openid-connect/token
```

**Headers:**

```
Content-Type: application/x-www-form-urlencoded
```

**Body (x-www-form-urlencoded):**

```
grant_type=password
client_id=student-client
client_secret=<CLIENT_SECRET>
username=hariom
password=hariom
```

---

### 🔒 Protected Endpoint Test

**Method:** GET
**URL:**

```
http://localhost:8000/protected/
```

**Headers:**

```
Authorization: Bearer <ACCESS_TOKEN>
```

### ✅ Expected Success Response

```json
{
  "message": "Student protected data",
  "user": "hariom",
  "roles": ["view_courses"]
}
```

---

## ❌ Common Errors & Fixes

### ❌ `invalid_grant: Account is not fully set up`

✔ Disable temporary password

---

### ❌ `401 Authorization header missing`

✔ Add Authorization header

---

### ❌ `401 Invalid Authorization header format`

✔ Header must be exactly:

```
Authorization: Bearer <token>
```

---

### ❌ `403 Forbidden`

✔ User does not have required role

---

## 🧠 Key Learnings

* Keycloak manages **authentication**, not your app
* Django validates **access tokens**
* Roles are client‑specific
* JWT tokens are the core of modern IAM

---

## 🔮 Next Improvements (Optional)

* Use JWT signature verification instead of `/userinfo`
* Create multiple Django apps (faculty, admin)
* Add role‑based decorators or middleware
* Replace password grant with Authorization Code flow

---

## 📌 Conclusion

This dummy project successfully demonstrates how **Keycloak integrates with Django** for **multi‑client identity management**, helping understand real‑world IAM systems used in production.

---

Happy experimenting with Keycloak 🚀

---

## Faculty Client & Endpoint Testing (Extended Scenario)

### Realm Setup

* **Global Realm**: `universe-realm`
* All clients, users, and roles exist inside this single realm.

### Clients

1. **student-client**
2. **faculty-client**

Each client represents a separate application protected by Keycloak.

---

## Role Design

### Student Roles (student-client)

* `view-course`

**Assigned Users**:

* `hariom` → view-course
* `aritra` → view-course

### Faculty Roles (faculty-client)

* `create-course`

**Assigned Users**:

* `aman` → create-course
* `farhan` → create-course

Roles are **client-level roles**, not realm roles.

---

## API Endpoints Design

### Student App Endpoints

| Endpoint      | Access Type | Description                               |
| ------------- | ----------- | ----------------------------------------- |
| `/public/`    | Public      | No authentication required                |
| `/protected/` | Protected   | Requires valid token + `view-course` role |

**Public Endpoint Response**:

```json
{
  "message": "Student public endpoint"
}
```

---

### Faculty App Endpoints

| Endpoint      | Access Type | Description                                 |
| ------------- | ----------- | ------------------------------------------- |
| `/public/`    | Public      | No authentication required                  |
| `/protected/` | Protected   | Requires valid token + `create-course` role |

**Public Endpoint Response**:

```json
{
  "message": "Faculty public endpoint"
}
```

---

## Authentication Testing (Failures & Success)

### 1. Realm Does Not Exist Error ❌

**Cause**:

* Wrong realm name in token URL

**Error**:

```json
{
  "error": "Realm does not exist"
}
```

**Fix**:

* Ensure realm name is exactly:

```
universe-realm
```

---

### 2. Account Is Not Fully Set Up ❌

**Cause**:

* User password marked as **Temporary**
* Required actions enabled (update password, verify email, OTP)

**Error**:

```json
{
  "error": "invalid_grant",
  "error_description": "Account is not fully set up"
}
```

**Fix**:

* Go to Keycloak Admin Console
* Users → Credentials → Set Password
* Set `Temporary = OFF`
* Disable all required actions

---

### 3. Successful Login (Password Grant) ✅

**Token Endpoint**:

```
POST http://localhost:8080/realms/universe-realm/protocol/openid-connect/token
```

**Payload (Student Example)**:

```
grant_type=password
client_id=student-client
client_secret=<student-client-secret>
username=hariom
password=hariom
```

**Payload (Faculty Example)**:

```
grant_type=password
client_id=faculty-client
client_secret=<faculty-client-secret>
username=aman
password=aman
```

**Success Response**:

* `access_token`
* `refresh_token`
* `expires_in`

---

## Authorization Testing

### Student Protected Endpoint

**Request**:

```
GET /protected/
Authorization: Bearer <access_token>
```

* Works for: `hariom`, `aritra`
* Fails for: `aman`, `farhan`

---

### Faculty Protected Endpoint

**Request**:

```
GET /protected/
Authorization: Bearer <access_token>
```

* Works for: `aman`, `farhan`
* Fails for: `hariom`, `aritra`

---

## Common Runtime Error (Django)

### Missing Authorization Header ❌

**Error**:

```
IndexError: list index out of range
```

**Cause**:

* Request sent without Authorization header

**Fix**:

* Always send:

```
Authorization: Bearer <token>
```

* Add defensive checks in Django view

---

## Key Learning Outcomes

* One realm can manage multiple applications
* Clients isolate roles and permissions
* Tokens are client-specific
* Role-based access control enforced via JWT
* IAM errors are mostly configuration issues

---

## Conclusion

This project demonstrates a real-world **multi-client IAM architecture** using Keycloak with Django:

* Centralized authentication
* Client-specific authorization
* Clear separation of student and faculty access
* Practical debugging of IAM failures

This setup mirrors production-grade identity systems used in enterprise applications.
