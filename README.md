# Product Manager

Product Manager web application developed with FastAPI. It is implemented following CRUD logics


---



## Technology Stack

**Backend**
* [FastAPI 0.115.12](https://fastapi.tiangolo.com/) for the Python backend API
* [SQLModel 0.0.24](https://sqlmodel.tiangolo.com/) for the Python SQL interactions (ORM)
* [Pydantic 2.11.5](https://docs.pydantic.dev/2.11/) used by FastAPI for data validation & [Environment/Config management (.env)](https://fastapi.tiangolo.com/advanced/settings/) 
* [SQLlite](https://fastapi.tiangolo.com/tutorial/sql-databases/) as local SQL database
* [FastAPI convenience tool](https://fastapi.tiangolo.com/tutorial/bigger-applications/) as a bluepring for the folder management

**Frontend**
* [Jinja2](https://jinja.palletsprojects.com/en/stable/) for the frontend
* [Bootstrap 5.3.1](https://getbootstrap.com/docs/5.3/) for responsive UI elements
* [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) and [Web API](https://developer.mozilla.org/en-US/docs/Web/API) for asynchronous interactions
*  [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) & [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) for content structure and network protocols

**Authentication & Security**
* OAuth2 implementation (with FastAPI) for authentication using JWT tokens
* [Pwdlib (with Argon2)](https://fastapi.tiangolo.com/tutorial/security/) for secure password hashing

**Test suite**
* [Pytest 9.0.2](https://docs.pytest.org/en/9.0.x/) for automated API testing, using [FastAPI integration](https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/)
* [Pytest fixtures](https://docs.pytest.org/en/6.2.x/fixture.html) for dependency injection in test setup



---



## API Reference

All API endpoints return data in JSON format. 
<br> Protected endpoints require authentication via the (`Authorization: Bearer <token>`) header. 
<br> The base URL for the examples is `http://localhost:8000`.

### Product Management (`/products`)

| Verb | Endpoint | Description | Input | Output | Auth |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **GET** | `/products/` | Retrieves the list of products | *Query params (opzional):*<br>`name` (str), `min_price` (Decimal), `max_price` (Decimal) | `List[ProductRead]` | X |
| **POST** | `/products/` | Adds a new product to the Database or update quantity if already existing | *JSON Body:*<br>`ProductCreate` (name, price, quantity) | `ProductRead`<br>The new product data | ✓ |
| **PATCH** | `/products/{id}` | Updates an existing product | *Path:* `product_id`<br>*JSON Body:* `ProductUpdate` | `ProductRead`<br>Updated product | ✓ |
| **DELETE** | `/products/{id}` | Removes a product by its ID | *Path:* `product_id` | `ProductRead`<br>Removed | ✓ |
| **DELETE** | `/products/` | Removes all products stored in the Database (debug) | *None* | `dict`<br>Confirmation | ✓ |

### Authentication (`/auth`)

| Verb | Endpoint | Description | Input | Output |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/auth/register` | Registers a new user in the system | *JSON Body:* `UserCreate`<br>(username, password, email, full_name) | `dict`<br>Confirmation message |
| **POST** | `/auth/token` | Generates a JWT Access Token for login | *Form-Data:* `OAuth2PasswordRequestForm`<br>(username, password) | `Token`<br>Token JWT and Token type |

### Frontend (`/`)
The front-end endpoints return `HTMLResponse` instances
* `GET /` - Homepage
* `GET /products_list` - Product catalog with a dedicated UI for filtering and editing
* `GET /signup` - Sign-up page
* `GET /login` - Login page

---

### **GET** `/products/`

```bash
curl --request GET \
  --url 'http://localhost:8000/products/?name=<product_name>&min_price=<min_value>&max_price=<max_value>' \
  --header 'Accept: application/json'
```

#### Retrieves a list of products from the database based on the applied filters. <br> If no parameters are provided, it returns the entire catalog.

<br>

<**name**> `string` (*optional*)
<br> Partial text search filter

<**min_price**> `Decimal` (*optional*)
<br> Minimum price of the product (must be `>= 0`)

<**max_price**> `Decimal` (*optional*)
<br> Maximum price of the product (must be `>= 0`)

#### Responses
*   **`200 OK`** - Returns a list of `ProductRead` objects
*   **`500 Internal Server Error`** - Error retrieving products from the database

---

### **POST** `/products/`

```bash
curl --request POST \
  --url http://localhost:8000/products/ \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
  "name": "New Product",
  "price": 25.50,
  "quantity": 10
}'
```

#### Adds a new product to the Database or update quantity if already existing.

<br>

<**name**> `string` (*required*)
<br> The name of the product

<**price**> `Decimal` (*required*)
<br> The selling price of the product (must be `> 0`)

<**quantity**> `int` (*required*)
<br> The inventory quantity to add (must be `>= 0`)

#### Responses
*   **`200 OK`** - Returns the updated `ProductRead` object (if the product already existed)
*   **`201 Created`** - Returns the newly created `ProductRead` object
*   **`401 Unauthorized`** - Missing or invalid JWT Token
*   **`500 Internal Server Error`** - Database transaction error

---

### **PATCH** `/products/{product_id}`

```bash
curl --request PATCH \
  --url http://localhost:8000/products/34 \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
  "price": 19.99,
  "quantity": 50
}'
```

#### Updates an existing product

<br>

<**product_id**> `int` (*required*) - (Path parameter)
<br> The ID of the product to update

<**name**> `string` (*optional*)
<br> The new name of the product

<**price**> `Decimal` (*optional*)
<br> The new price of the product

<**quantity**> `int` (*optional*)
<br> The new inventory quantity

#### Responses
*   **`200 OK`** - Returns the updated `ProductRead` object
*   **`401 Unauthorized`** - Missing or invalid JWT Token
*   **`404 Not Found`** - Product with the specified <`product_id`> does not exist
*   **`500 Internal Server Error`** - Error updating the product in the database

---

### **DELETE** `/products/{product_id}`

```bash
curl --request DELETE \
  --url http://localhost:8000/products/1 \
  --header 'Authorization: Bearer <token>'
```

#### Permanently removes a product by its ID

<br>

<**product_id**> `int` (*required*) - (Path parameter)
<br> The ID of the product you want to delete.

#### Responses
*   **`200 OK`** - Returns the deleted `ProductRead` object
*   **`401 Unauthorized`** - Missing or invalid JWT Token
*   **`404 Not Found`** - Product with the specified <`product_id`> does not exist
*   **`500 Internal Server Error`** - Error deleting the product from the database

---

### **DELETE** `/products/`

```bash
curl --request DELETE \
  --url http://localhost:8000/products/ \
  --header 'Authorization: Bearer <token>'
```

#### Clear the whole catalog (Debug)

#### Responses
*   **`200 OK`** - Returns a success confirmation message
*   **`401 Unauthorized`** - Missing or invalid JWT Token.
*   **`500 Internal Server Error`** 

---

### **POST** `/auth/register`

```bash
curl --request POST \
  --url http://localhost:8000/auth/register \
  --header 'Content-Type: application/json' \
  --data '{
  "username": "user",
  "password": "Password123.",
  "email": "name@mail.com",
  "full_name": "FirstNome LastName"
}'
```

#### User Registration, the password is hashed before being stored

<br>

<**username**> `string` (*required*)
<br> Username, must be unique

<**password**> `string` (*required*)
<br> Plaintext password

<**email**> `string` (*optional*)
<br> User's email address

<**full_name**> `string` (*optional*)
<br> User's full name

#### Responses
*   **`201 Created`** - Returns a success message
*   **`400 Bad Request`** - The provided `username` is already registered
*   **`500 Internal Server Error`** - Could not save the user in the system

---

### **POST** `/auth/token`

```bash
curl --request POST \
  --url http://localhost:8000/auth/token \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data 'username=user&password=Password123.'
```

#### Generate a JWT Access Token if the login credentials are valid 

<br>

<**username**> `string` (*required*) - (Form Data)
<br> The registered username

<**password**> `string` (*required*) - (Form Data)
<br> User's password

---

### Frontend Routes (`/`)

The endpoints return `HTMLResponse` instances rendered with Jinja2

*   `GET /` - Renders the Homepage.
*   `GET /products_list` - Renders the product catalog
*   `GET /signup` - Renders the user registration page
*   `GET /login` - Renders the login page




---

# Configure

#### First, clone the repository and set the name of the project, for example `product-manager`:

```bash
git clone https://github.com/MirkoKiwi/Product-Manager.git product-manager
```

#### Navigate into the new directory:
```bash
cd product-manager
```


#### Create a virtual environment to isolate dependencies:
```bash
python -m venv venv
```
#### Activate it on macOS/Linux:
```bash
source venv/bin/activate
```
#### Activate it on Windows:
```bash
venv\Scripts\activate
```
### Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment Variables Configuration

### Update the configs in the .env files with the following:
```env
AUTH_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20
```

### Generate Secret Keys
Some environment variables in the .env file have a default value of `changethis`.
<br> To generate a secret key you can run:
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
or either, in a bash terminal:
```bash
openssl rand -hex 32
```
Copy the content and use it as password / secret key.

### Launch the application by running the main script:
```bash
python main.py
```
or alternatively, run the server directly via `Uvicorn`:
```bash
uvicorn main:app --reload --port 8000
```
The server should run in localhost at `http://127.0.0.1:8000/`. (Swagger documentation on `/docs`).


## Test Suite

The project uses **Pytest** for automated unit tests. <br>
To run the full test suite:
```bash
pytest -v
```