''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Necessary Imports
# The main FastAPI import and Request object, Depends for Auth
from fastapi import FastAPI, Request, Depends, HTTPException, status
# Used to define the model matching the DB Schema
from pydantic import BaseModel
# Used for returning HTML responses (JSON is default)
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
# Used for generating HTML from templatized files
from fastapi.templating import Jinja2Templates
# Used for making static resources available to server
from fastapi.staticfiles import StaticFiles
# Used for running the app directly through Python
import uvicorn
# Used for interacting with the MySQL database
import mysql.connector as mysql
# Used for interacting with the system environment
import os
# Used to read the credentials
from dotenv import load_dotenv
# Used for Auth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Used for regex expressions
import re

# Use for parsing html files
from bs4 import BeautifulSoup

def readHtmlBody(filename:str):
    with open('./auth-templates/'+filename, 'r') as file:
        html = file.read()
    soup = BeautifulSoup(html, 'html.parser')
    return str(soup.body)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Configuration
load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# Connect to the db and create a cursor object
db = mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()
cursor.execute("USE leaderboard")


app = FastAPI()
views = Jinja2Templates(directory='../frontend/templates')

app.mount("/public", StaticFiles(directory="../frontend/public"), name="public")
app.mount("/assets", StaticFiles(directory="../frontend/assets"), name="assets")
app.mount("/templates",StaticFiles(directory="../frontend/templates"), name="templates")
app.mount("/auth-templates",StaticFiles(directory="./auth-templates"), name="auth-templates")

# Custom 404 Error Page
@app.exception_handler(404)
async def custom_404_handler(_, __):
    return FileResponse('./auth-templates/404.html')

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Pydantic Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    student_id: str | None = None
    hashed_password: str | None = None
    comments: str | None = None

class Comments(BaseModel):
    username: str
    comment: str
    comment_id: str
    date: str

class CommentDelete(BaseModel):
    comment_id: str

class CommentEdit(BaseModel):
    username: str
    comment: str
    comment_id: str
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Auth Config
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    cursor.execute("SELECT username, first_name, last_name, email, student_id, hashed_password FROM users WHERE username=%s", (username,))
    record = cursor.fetchone()
    if record is not None:
        return User(
            username=record[0],
            first_name=record[1],
            last_name=record[2],
            email=record[3],
            student_id=record[4],
            hashed_password=record[5],
        )

# Return the user BaseModel if password hashes match, else return false
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user



@app.post("/create-account")
async def create_account(form_data: User):    
    # Create and return the JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    # hash the password
    hashed_pwd = get_password_hash(form_data.hashed_password)
    try:
        # store created user in the database
        query = "INSERT INTO users (username, first_name, last_name, email, student_id, hashed_password) VALUES (%s, %s, %s, %s, %s, %s)"
        values = [
            (form_data.username, form_data.first_name, form_data.last_name, form_data.email, form_data.student_id, hashed_pwd),
        ]
        cursor.executemany(query, values)
        db.commit()
        print(cursor.rowcount, " rows created.")
    except:
        print("Error: Account Already Exists")
        return
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/post-comment")
async def post_comment(comments: Comments, user: User = Depends(get_current_user)):
    try:
        # store created comment in the database
        query = "INSERT INTO comments (username, comment, comment_id, date) VALUES (%s, %s, %s, %s)"
        values = [
            (comments.username, comments.comment, comments.comment_id, comments.date),
        ]   
        cursor.executemany(query, values)
        db.commit()
        print(cursor.rowcount, " rows created.")


    except mysql.Error as err:
        print("MySQL error: {0}".format(err))
        db.rollback()
        return
    
    try:
        cursor.execute("SELECT id FROM comments WHERE username=%s AND comment=%s AND comment_id=%s AND date=%s", (comments.username, comments.comment, comments.comment_id, comments.date))
        records = cursor.fetchall()
        db.commit()

        print("Successful creation of comment. Returning ID of: ",records[0][0])
        return JSONResponse({"comment_id": records[0][0]})
    
    except mysql.Error as err:
        print("MySQL error: {0}".format(err))
        db.rollback()
        return


@app.put("/edit-comment")
async def edit_comment(comments: CommentEdit, user: User = Depends(get_current_user)):
    print("comment debug", comments)
    try:
        query = "UPDATE comments SET comment=%s WHERE username=%s AND id=%s"
        values = (comments.comment, comments.username, comments.comment_id)
        cursor.execute(query, values)
        db.commit()
        print(cursor.rowcount, " rows created. Comment was updated")
    except mysql.Error as err:
        print("MySQL error: {0}".format(err))
        db.rollback()
        return
        
@app.delete("/delete-comment", response_class=JSONResponse)
async def delete_comment(comments: CommentDelete, user: User = Depends(get_current_user)):
    try:
        # delete comment with id=2 from the database
        query = "DELETE FROM comments WHERE id = %s"
        value = (comments.comment_id,)
        cursor.execute(query, value)
        db.commit()
        print(cursor.rowcount, " rows deleted.")
    except mysql.Error as err:
        print("MySQL error: {0}".format(err))
        db.rollback()
        return JSONResponse({"details":"err"})
    return JSONResponse({"details":"success"})

@app.get("/load-comments-{id}", response_class=JSONResponse)
async def load_comments(id: str, current_user: User = Depends(get_current_user)):
    cursor.execute("SELECT username, comment, date, id FROM comments WHERE comment_id=%s", (id,))
    records = cursor.fetchall()
    response = {}
    for index, row in enumerate(records):
        response[index] = {
            "username": str(row[0]),
            "comment": str(row[1]),
            "date": str(row[2]),
            "id": str(row[3]),
        }
    print("Response was:", response)
    return JSONResponse(response)

@app.post("/update-profile", response_class=JSONResponse)
async def update_profile(userProfile: User, current_user: User = Depends(get_current_user)):
    # Update account information
    try:
        query = "UPDATE users SET username=%s, student_id=%s, email=%s WHERE username=%s"
        values = (userProfile.username, userProfile.student_id, userProfile.email, userProfile.username)
        cursor.execute(query, values)
        db.commit()
        print(cursor.rowcount, " rows created. Profile was Updated")
    except mysql.Error as err:
        print("MySQL error: {0}".format(err))
        db.rollback()

@app.post("/reset-password", response_class=JSONResponse)
async def reset_password(user: User):
    hashed_pwd = get_password_hash(user.hashed_password)
    try:
        query = "UPDATE users SET hashed_password=%s WHERE first_name=%s AND last_name=%s AND username=%s AND student_id=%s AND email=%s"
        values = (hashed_pwd, user.first_name, user.last_name, user.username, user.student_id, user.email)
        cursor.execute(query, values)
        db.commit()
        print(cursor.rowcount, "password updated.")

        if cursor.rowcount == 0:
            return {"detail":"error"}
    except mysql.Error as err:
        print("MySQL error: {0}".format(err))
        db.rollback()
        return {"detail":"error"}
    return {"detail":"success"}

@app.get("/get-profile", response_class=JSONResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    cursor.execute("SELECT username, email, student_id, id FROM users WHERE username=%s", (current_user.username,))
    records = cursor.fetchall()
    response = {}
    for index, row in enumerate(records):
        response[index] = {
            "username": str(row[0]),
            "email": str(row[1]),
            "student_id": str(row[2]),
        }
    print("Response was:", response)
    return JSONResponse(response)
    

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    def getUsername(email: str):
        cursor.execute(
            "SELECT username FROM users WHERE email=%s", (email,))
        records = cursor.fetchall()
        if len(records) == 0:
            return None
        else:
            return records[0][0]

    def isEmail(string: str):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, string):
            return True
        else:
            return False
    
    if isEmail(form_data.username):
        form_data.username = getUsername(form_data.username)

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Routes that return HTML body strings
@app.get("/updates-html/")
async def get_updates_page_html(current_user: User = Depends(get_current_user)):
    return {"html":readHtmlBody("updates.html")}

@app.get("/leaderboard-html/")
async def get_leaderboard_page_html(current_user: User = Depends(get_current_user)):
    return {"html":readHtmlBody("leaderboard.html")}

@app.get("/profile-html/")
async def get_profile_page_html(current_user: User = Depends(get_current_user)):
    return {"html":readHtmlBody("profile.html")}

@app.get("/blog-1-html/")
async def get_blog_week_1_html(current_user: User = Depends(get_current_user)):
    return {"html":readHtmlBody("blog-1.html")}

@app.get("/blog-2-html/")
async def get_blog_week_2_html(current_user: User = Depends(get_current_user)):
    return {"html":readHtmlBody("blog-2.html")}

@app.get("/blog-3-html/")
async def get_blog_week_3_html(current_user: User = Depends(get_current_user)):
    return {"html":readHtmlBody("blog-3.html")}

@app.get("/comments-html/")
async def get_comments_page_html(current_user: User = Depends(get_current_user)):
    return {"html":readHtmlBody("comments.html")}
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# HTML Page Routes
@app.get('/', response_class=HTMLResponse)
def get_homepage(request: Request) -> HTMLResponse:
    return views.TemplateResponse('homepage.html', {"request": request})

@app.get('/reset', response_class=HTMLResponse)
def get_reset_page(request: Request) -> HTMLResponse:
    return views.TemplateResponse('reset.html', {"request": request})


@app.get('/signin', response_class=HTMLResponse)
def get_sign_in_page(request: Request) -> HTMLResponse:
    return views.TemplateResponse('signin.html', {"request": request})


@app.get('/signup', response_class=HTMLResponse)
def get_sign_up_page(request: Request) -> HTMLResponse:
    return views.TemplateResponse('signup.html', {"request": request})


@app.get('/leaderboard', response_class=HTMLResponse)
def get_leaderboard_page(request: Request) -> HTMLResponse:
    return views.TemplateResponse('leaderboard.html', {"request": request})


@app.get('/profile', response_class=HTMLResponse)
def get_profile_page(request: Request) -> HTMLResponse:
    return views.TemplateResponse('profile.html', {"request": request})


@app.get('/updates', response_class=HTMLResponse)
def get_updates_page(request: Request) -> HTMLResponse:
    return views.TemplateResponse('updates.html', {"request": request})


@app.get('/blog-1', response_class=HTMLResponse)
def get_blog_1(request: Request) -> HTMLResponse:
    return views.TemplateResponse('blog-1.html', {"request": request})

@app.get('/blog-2', response_class=HTMLResponse)
def get_blog_2(request: Request) -> HTMLResponse:
    return views.TemplateResponse('blog-2.html', {"request": request})

@app.get('/blog-3', response_class=HTMLResponse)
def get_blog_3(request: Request) -> HTMLResponse:
    return views.TemplateResponse('blog-3.html', {"request": request})

@app.get('/comments-{id}', response_class=HTMLResponse)
def get_comments(request: Request, id) -> HTMLResponse:
    if int(id) <= 0 or int(id) >= 27:
        return views.TemplateResponse('404.html', {"request": request})
    return views.TemplateResponse('comments.html', {"request": request})

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
if __name__ == "__main__":
    while True:
        try:
            uvicorn.run(app, host="localhost", port=6543)
        except Exception as e:
            print(f"Error occurred at {datetime.datetime.now()}: {e}")
            continue
