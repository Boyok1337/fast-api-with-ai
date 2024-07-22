# Test task for Python Developer


## 👩‍💻 _Installation & Run_
### 🧠 Set up the environment 


 On Windows:
```python
python -m venv venv 
venv\Scripts\activate
 ```

 On UNIX or macOS:
```python
python3 -m venv venv 
source venv/bin/activate
 ```

### 👯 Install requirements 
```python
pip install -r requirements.txt
```


### 🗃️ Database setup

```python
alembic revision --autogenerate -m "initial migrations"
alembic upgrade head
```

### 📝 Set enviroment variable
- Copy and rename the **.env.sample** file to **.env** 
- Open the .env file and edit the environment variables 
- Save the .env file securely 
- Add the .env file to .gitignore 

### 📫 Install VPN service(optional)
1. If your location not included in free use zone for AI API from Google.
2. https://hide-me-vpn.ru.uptodown.com/windows
3. Set United States as location.

### 🚀 Run the project
```python
python -m uvicorn main:app --reload 
```

## 🛡️ Testing
You can run tests for the project using the following command (put into terminal):
```python
pytest tests/test.py
```