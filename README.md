# Lawvriksh Backend API

## Endpoints

### 1. Admin Login
- **POST** `/adminlogin`
- **Body (form):**
  - `username`: admin email
  - `password`: admin password
- **Response:** `{ "access_token": "...", "token_type": "bearer" }`

### 2. Register User
- **POST** `/userdata`
- **Body (JSON):**
  ```json
  { "name": "User Name", "email": "user@email.com", "phone": "1234567890" }
  ```
- **Response:** User object

### 3. Register Creator
- **POST** `/creatordata`
- **Body (JSON):**
  ```json
  { "name": "Creator Name", "email": "creator@email.com", "phone": "1234567890" }
  ```
- **Response:** Creator object

### 4. Not Interested
- **POST** `/notinteresteddata`
- **Body (JSON):**
  ```json
  { "email": "user@email.com", "reason": "Not interested" }
  ```
- **Response:** NotInterested object

### 5. Feedback
- **POST** `/feedback`
- **Body (JSON):**
  ```json
  { "contact_email": "user@email.com", "feedback": { "message": "Great!" } }
  ```
- **Response:** Feedback object

### 6. Get Registered Users (Admin)
- **GET** `/registereduserdata`
- **Headers:** `Authorization: Bearer <token>`
- **Response:** List of users

### 7. Get Registered Creators (Admin)
- **GET** `/registeredcreatordata`
- **Headers:** `Authorization: Bearer <token>`
- **Response:** List of creators

### 8. Download Data (Admin)
- **POST** `/downloaddata`
- **Headers:** `Authorization: Bearer <token>`
- **Body (form):**
  - `table`: `users` or `creators`
- **Response:** Excel file download

---

## Testing
- Use [httpie](https://httpie.io/), [curl](https://curl.se/), or [Postman](https://www.postman.com/) for API testing.
- Ensure your `.env` is configured and MySQL is running.
- Start the server: `uvicorn app.main:app --reload`

---

## Example: Admin Login (httpie)
```sh
http -f POST http://localhost:8000/adminlogin username==sahilsaurav2507@gmail.com password==Lawvriksh@2507//
```

## Example: Register User (httpie)
```sh
http POST http://localhost:8000/userdata name='Test User' email='test@user.com' phone='1234567890'
```