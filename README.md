# ECE140A Final Project: MVP Leaderboards
Name: Kenny Chan
PID: A16138682

### Extra Credit Features Implemented:
- [x] Web Hosting on Provider
- [x] Added CSS to provide better UI 
- [x] Session Expiry - Auto Logout
- [x] Edit Comment in Leaderboard Commenting System

### Extra Credit Live Website: [Click here to see the live website.](https://0855-2603-8001-8e00-5e00-1d2e-19a6-9c85-8ddb.ngrok.io/)

https://user-images.githubusercontent.com/53395124/227124110-a16337dd-fb2d-4677-ab6d-2a4dd0db9792.mp4

### File Structure

<i>File structure differs from assignment outline, use the diagram below as an outline instead. </i>

![file-structure](https://user-images.githubusercontent.com/53395124/227109115-d70cd3fd-19b2-43c6-a0b4-044b6c4ef1f1.png)

### Database Design
![database-design](https://user-images.githubusercontent.com/53395124/227106301-b4525c03-107f-4a94-a1a4-c7fec3e3ef2b.png)

![fast-api-routes](https://user-images.githubusercontent.com/53395124/227103902-23364591-fc28-4019-98d3-b553a3e036da.png)

### Information Architecture
![information-architecture](https://user-images.githubusercontent.com/53395124/227107375-ab6d17db-796e-4b16-adb4-8f8c5bed8947.png)

### Systems Design
![system-design](https://user-images.githubusercontent.com/53395124/227106332-e3fb694d-8f0f-4788-96ba-9c856e904483.png)


### Challenges:
- Implementing Auth + Signing up + Sign In:
    - I found auth to be a real challenge at first as I had never implement auth for any website but found the use of JWT to be an interesting solution to auth. To autheticate the webpage I hashed passwords using passwordlib and create JWTs using the jose library as recommended on FastApi's docs. With this, I used dependency injections to reuse auth functions which made my code a lot more modular and readable.
- Home Page:
    - Getting the pages have a fullscreen scroll was inspired by Pinterest's design for their homepage and was a challenge to implement in HTML, using built in snapping attributes in HTML such as snap-start combined with tailwind's styling support for this, I was able to get it working
- MVP Updates page:
    - I was having difficulty deciding whether to dynamically load the MVP week comments or make them HTML pages. I resolved this problem by deciding to have each MVP week their own pages rather than dynamically updating with JavaScript as this would require a lot of DOM manipulation. I think that it was a fine solution for this assignment since we are only having 3 weeks of static content. 
- Profile Page:
    - I was having trouble coming up with what I should allow the user to edit and how I would implement the resetting of the password. For resetting the password, I came up with a simple solution where it just redirects to the forgot password page which allows the user to reset their password given their sign up information. I also allowed the user to change their email and student ID in the profile page.
- Leaderboard page + commenting system:
    - One major challenge was working with the SlideSpace API as it was limiting my requests since I was requesting all the data at once per page load. It also caused a lot of latency. I resolved the latency issue by asynchronously loading all the data with <code>Promise.all()</code> method and if the user had previous requests from SlideSpace API causing a request error, I would display a text dialog to tell the user to wait as too many requests were sent to the API.