# BlogSiteAPI
- Backend RESTful API for a social media type application that allows users to create, read, update, and delete posts
- Security features include user creation, user authentication, password hashing, and protected routes utilizing JWT tokens
- Made in Python with FastAPI, Pydantic, SQLAlchemy, PostgreSQL
- Future features: adding testing with pytest, building out a CI/CD pipeline using GitHub actions

- Below are screenshots of the interactive UI for my backend API (courtesy of Swagger UI)
![blogsiteapi_screenshot_1](https://user-images.githubusercontent.com/51379562/167350568-f0967a28-2e8d-4257-a88a-93db94040611.png)

- This shows me attempting to access a protected route without a JWT token and getting denied by the server
![blogsiteapi_screenshot_2](https://user-images.githubusercontent.com/51379562/167350584-af6fefb4-4660-4db2-8e59-7b501b69cfdd.png)
