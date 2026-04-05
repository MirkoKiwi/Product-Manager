import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from decimal import Decimal

from src.models.product import Product, ProductCreate




def test_signup(client: TestClient):
    """Signup test"""
    # Signup
    reg_res = client.post("/auth/register", json={
        "username":  "user",
        "password":  "password123",
        "email":     "test@test.com",
        "full_name": "name test",
    })
    assert reg_res.status_code == 201



def test_signup_already_exists(client: TestClient):
    """"""
    reg_res = client.post("/auth/register", json={
        "username":  "user",
        "password":  "password123",
        "email":     "test@test.com",
        "full_name": "name test",
    })

    reg_res2 = client.post("/auth/register", json={
        "username":  "user",
        "password":  "password123",
        "email":     "test2@test.com",
        "full_name": "second test",
    })
    assert reg_res2.status_code == 400




def test_login(client: TestClient):
    """Logging in after acquiring JWT Token"""
    client.post("/auth/register", json={
        "username": "user",
        "password": "password123",
        "email":    "test@test.com"
    })

    # Login
    login_res = client.post("/auth/token", data={
        "username": "user",
        "password": "password123"
    })
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()



def test_login_wrong_password(client: TestClient):
    """"""
    client.post("/auth/register", json={
        "username": "user",
        "password": "password123",
        "email":    "test@test.com"
    })

    login_res = client.post("/auth/token", data={
        "username": "user",
        "password": "wrongpassword123"
    })
    assert login_res.status_code == 401



def test_login_wrong_username(client: TestClient):
    """"""
    client.post("/auth/register", json={
        "username": "user",
        "password": "password123",
        "email":    "test@test.com"
    })

    login_res = client.post("/auth/token", data={
        "username": "user33",
        "password": "wrongpassword123"
    })
    assert login_res.status_code == 401



def test_get_products_list(client: TestClient, session: Session):
    """"""
    session.add(Product.model_validate(ProductCreate(name="TestItemGET", price=1.5, quantity=100)))
    session.commit()

    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "TestItemGET"



def test_get_filter_products(client: TestClient, session: Session):
    """"""
    session.add(Product.model_validate(ProductCreate(name="TestItem1", price=10, quantity=1)))
    session.add(Product.model_validate(ProductCreate(name="TestItem2", price=20, quantity=1)))
    session.add(Product.model_validate(ProductCreate(name="TestItem3", price=30, quantity=1)))
    session.commit()

    query = client.get("/products/?name=TestItem1")
    assert len(query.json()) == 1
    assert query.json()[0]["name"] == "TestItem1"

    query = client.get("/products/?min_price=15&max_price=25")
    assert len(query.json()) == 1
    assert query.json()[0]["name"] == "TestItem2"

    query = client.get("/products/?min_price=15")
    assert len(query.json()) == 2
    assert query.json()[0]["name"] == "TestItem2" and query.json()[1]["name"] == "TestItem3"

    query = client.get("/products/?max_price=25")
    assert len(query.json()) == 2
    assert query.json()[0]["name"] == "TestItem1" and query.json()[1]["name"] == "TestItem2"

    query = client.get("/products/?name=Test")
    names = [p["name"] for p in query.json()]
    assert len(query.json()) == 3
    assert "TestItem1" in names
    assert "TestItem2" in names
    assert "TestItem3" in names
    



def test_add_product_auth(client: TestClient):
    """"""
    client.post("/auth/register", json={"username": "user", "password": "password123"})
    login_res = client.post("/auth/token", data={"username": "user", "password": "password123"})
    token     = login_res.json()["access_token"]
    headers   = {"Authorization": f"Bearer {token}"}
    
    prod = {
        "name": "TestItem",
        "price": 50.00,
        "quantity": 5
    }
    response = client.post("/products/", headers=headers, json=prod)
    data = response.json()
    
    assert response.status_code == 201
    assert data["name"] == "TestItem"
    assert Decimal(data["price"]) == Decimal("50.00")
    assert data["quantity"] == 5
    assert "id" in data



def test_add_product_no_auth(client: TestClient):
    """"""
    prod = {
        "name": "TestItem",
        "price": 50.00,
        "quantity": 5
    }
    response = client.post("/products/", json=prod)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"



def test_add_product_already_existing(client: TestClient, session: Session):
    """"""
    client.post("/auth/register", json={"username": "user", "password": "password123"})
    login_res = client.post("/auth/token", data={"username": "user", "password": "password123"})
    token     = login_res.json()["access_token"]
    headers   = {"Authorization": f"Bearer {token}"}

    prod = {
        "name":     "TestItem", 
        "price":    10.00, 
        "quantity": 5
    }

    # First push
    response = client.post("/products/", headers=headers, json=prod)
    assert response.status_code == 201

    # Second push
    prod = {
        "name":     "TestItem", 
        "price":    10.00, 
        "quantity": 11
    }

    response = client.post("/products/", headers=headers, json=prod)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TestItem"
    assert Decimal(data["price"]) == 10.00
    assert response.json()["quantity"] == (5 + 11)



def test_patch_product_auth(client: TestClient, session: Session):
    """"""
    client.post("/auth/register", json={"username": "user", "password": "password123"})
    login_res = client.post("/auth/token", data={"username": "user", "password": "password123"})
    token     = login_res.json()["access_token"]
    headers   = {"Authorization": f"Bearer {token}"}

    prod = Product(name="TestItemPATCH", price=10.00, quantity=5)
    session.add(prod)
    session.commit()
    session.refresh(prod)

    updated_prod = {
        "name": "TestItemPATCH_NewName", 
        "price": 15.00
    }
    response = client.patch(f"/products/{prod.id}", json=updated_prod, headers=headers)

    assert response.status_code == 200
    assert response.json()["name"] == "TestItemPATCH_NewName"
    assert Decimal(response.json()["price"]) == Decimal("15.00")
    assert response.json()["quantity"] == 5



def test_patch_product_no_auth(client: TestClient, session: Session):
    """"""
    item = Product(name="TestItemPATCH", price=10.00, quantity=5)
    session.add(item)
    session.commit()
    session.refresh(item)

    prod = {
        "name": "TestItemPATCH_NewName", 
        "price": 15.00
    }
    response = client.patch(f"/products/{item.id}", json=prod)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"



def test_remove_product_auth(client: TestClient, session: Session):
    """"""
    client.post("/auth/register", json={"username": "user", "password": "password123"})
    login_res = client.post("/auth/token", data={"username": "user", "password": "password123"})
    token     = login_res.json()["access_token"]
    headers   = {"Authorization": f"Bearer {token}"}

    prod = Product.model_validate(ProductCreate(name="TestProd", price=50.03, quantity=7))
    session.add(prod)
    session.commit()
    session.refresh(prod)
    prod_id = prod.id

    deleted =  client.delete(f"/products/{prod.id}", headers=headers)
    assert deleted.status_code == 200

    check  = client.get("/products")
    db_ids = [p["id"] for p in check.json()]
    assert prod_id not in db_ids



def test_remove_product_no_auth(client: TestClient, session: Session):
    """"""
    prod = Product.model_validate(ProductCreate(name="TestProd", price=50.03, quantity=7))
    session.add(prod)
    session.commit()
    session.refresh(prod)
    prod_id = prod.id

    deleted =  client.delete(f"/products/{prod.id}")
    assert deleted.status_code == 401

    check  = client.get("/products")
    db_ids = [p["id"] for p in check.json()]
    assert prod_id in db_ids