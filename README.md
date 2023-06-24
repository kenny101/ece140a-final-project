# ECE140A Final Project: MVP Leaderboards
This is a final project for ECE140A at UCSD which "Builds on a solid foundation of electrical and computer engineer skills, this course strives to broaden student skills in software, full-stack engineering, and concrete understanding of methods related to the realistic development of a commercial product. Students will research, design, and develop an IOT device to serve an emerging market". [ECE Courses at UCSD Here](https://catalog.ucsd.edu/courses/ECE.html) 

The main feature of this website is to be able to view and comment on other student's ideas for ECE140a. This is not a real product, rather is used for learning full-stack engineering using [FastAPI](https://fastapi.tiangolo.com/) and MySQL database to implement a RESTful API as well as auth using [JWT (JSON Web Tokens)](https://jwt.io/). You can learn more about what makes an API RESTful [here.](https://www.youtube.com/watch?v=lsMQRaeKNDk)

### Features Implemented:
- [x] Auth: Login, account creation, deletion, update user information
- [x] Session Expiry - Auto Logout using JSON Web Tokens
- [x] Redirecting invalid pages (401/404 pages)
- [x] Edit/delete Comment in Leaderboard Commenting System
- [x] View different page content on the webpage

### Future Features:
- [ ] Make website more user-friendly/responsive for smaller screens
- [ ] Use ORM library such as [SQLAlcademy](https://www.sqlalchemy.org/) rather than executing raw SQL queries


https://github.com/kenny101/ece140a-final-project/assets/53395124/46653408-22fa-403e-9106-f7baf3479785


### File Structure
![file-structure](https://user-images.githubusercontent.com/53395124/227109115-d70cd3fd-19b2-43c6-a0b4-044b6c4ef1f1.png)

### Database Design
![database-design](https://user-images.githubusercontent.com/53395124/227106301-b4525c03-107f-4a94-a1a4-c7fec3e3ef2b.png)

![fast-api-routes](https://user-images.githubusercontent.com/53395124/227103902-23364591-fc28-4019-98d3-b553a3e036da.png)

### Information Architecture
![information-architecture](https://user-images.githubusercontent.com/53395124/227107375-ab6d17db-796e-4b16-adb4-8f8c5bed8947.png)

### Systems Design
![system-design](https://user-images.githubusercontent.com/53395124/227106332-e3fb694d-8f0f-4788-96ba-9c856e904483.png)
