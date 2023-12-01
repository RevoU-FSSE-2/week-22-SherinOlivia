[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/DGzh2WKs)
# Project Milestone 5 Overview
For this week's assignment, we are tasked to convert our to-do-list app backend (from Project Milestone 3) to Flask and adjust the React frontend for compatibility.

The capabilities of the project are:
1. CRUD Implementation 
- Register
- Login
- User's Profile
- Create new Task
- Edit Task
- Update Task Status
- Delete task
2. Database 
- PostgreSQL (through Supabase)
3. Authentication and Authorization
- Authentication: JWT (& Bcrypt)
- Authorization: Role-Based Access Control (RBAC)
4. Documentation
- Swagger

## Tools used
- Flask
- SQLAlchemy
- Bcrypt
- JWT
- Marshmallow
- Injector
- flask-swagger-ui

## Front End Deployed Link & Repo
<p align="center">
<a href="https://github.com/SherinOlivia/to-do-list-app">FE Repository</a>
</p> 
<p align="center">
<a href="https://week22-44a31.web.app">week22-44a31.web.app</a>
</p> 

## API Endpoints

<p align="center">
<a href="https://sherinolivia-ttfsxqentq-uc.a.run.app">sherinolivia-ttfsxqentq-uc.a.run.app</a> || <a href="http://127.0.0.1:5000/swagger/">127.0.0.1:5000/swagger</a>
</p> 


## Sample Accounts
```JSON
CLIENT:
    "username": "dreya",
    "password":"dreya123"
```
```JSON
STAFF:
    "username":"zoyaaa",
    "password":"Zoyaa123"
```
```JSON
ADMIN:
    "username":"FChief",
    "password":"Chief123"
```
<br>

## Request Required Data:
**AUTH:**
```JSON
Register (ENUM: CLIENT/STAFF/ADMIN, if not provided -> default = CLIENT):
{
    "username":"yourUsername",
    "email": "your@email.com",
    "password":"yourP4ssw0rd",
    "name":"your name",
    "city":"your city",
    "about_me":"short self-description"
}
```
```JSON
Login:
{
    "username":"yourUsername",
    "password":"yourP4ssw0rd"
}
```
<br>

**TASKS:**
```JSON
Create New Task:
{
    "title": "Task Title",
    "description": "Task Description",
    "purpose": "WORK/STUDY/GENERAL/PERSONAL (ENUM)",
    "priority": "LOW/MEDIUM/HIGH (ENUM)",
    "due_date": "yyyy-mm-dd HH",
}
```
```JSON
Edit Task:
{
    "title": "New? Task Title",
    "description": "New? Task Description",
    "purpose": "Task Purpose (work/personal/finance/misc)",
    "due_date": "yyyy-mm-dd hh:mm:ss format (i.e: 2023-11-21 12:30:00)"
}
```
```JSON
Update Task Status:
{
    "status": "ONGOING/COMPLETED (ENUM)"
}
```
<br>

## API Endpoints

<p align="center">
<a href="https://sherinolivia-ttfsxqentq-uc.a.run.app">sherinolivia-ttfsxqentq-uc.a.run.app</a>
</p> 

**AUTH & USERS**
<div align="center">

| Name  | HTTP Method | Endpoint | Authentication | Authorization |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| **Homepage** | `GET` |[/](https://sherinolivia-ttfsxqentq-uc.a.run.app/) | ❌ | ❌ |
| **Register User** | `POST` | [/auth/registration](https://sherinolivia-ttfsxqentq-uc.a.run.app/auth/registration) | ❌ | ❌ |
| **Login User** | `POST` | [/auth/login](https://sherinolivia-ttfsxqentq-uc.a.run.app/auth/login) | ❌ | ❌ |
| **Logout User** | `POST` | [/auth/logout](https://sherinolivia-ttfsxqentq-uc.a.run.app/auth/logout) | ✔ | ❌ |
| **User Profile (each user sees their own)** | `GET` | [/users/profile](https://sherinolivia-ttfsxqentq-uc.a.run.app/user/profile) | ✔ | **CLIENT**, **STAFF**, **ADMIN** |
</div>

**TASKS**
<div align="center">

| Name  | HTTP Method | Endpoint | Authentication | Authorization |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| **Homepage** | `GET` |[/](https://sherinolivia-ttfsxqentq-uc.a.run.app/) | ❌ | ❌ |
| **Create New Taks** | `POST` | [/task/create](https://sherinolivia-ttfsxqentq-uc.a.run.app/task/create) | ✔ | **CLIENT**, **STAFF**, **ADMIN** |
| **List All Tasks ('CLIENT' can only see their own)** | `GET` | [/task/list](https://sherinolivia-ttfsxqentq-uc.a.run.app/task/list) | ✔ | **CLIENT**, **STAFF**, **ADMIN** |
| **Edit Task** | `PUT` | [/task/edit/{taskId}](https://sherinolivia-ttfsxqentq-uc.a.run.app/task/edit/2) | ✔ | **CLIENT**, **STAFF**, **ADMIN** |
| **Update Task Status** | `PATCH` | [/task/update/{taskId}](https://sherinolivia-ttfsxqentq-uc.a.run.app/task/update/2) | ✔ | **CLIENT**, **STAFF**, **ADMIN** |
| **Delete Task (Soft Delete)** | `DELETE` | [/task/delete/{taskId}](https://sherinolivia-ttfsxqentq-uc.a.run.app/task/delete/1) | ✔ | **CLIENT**, **STAFF**, **ADMIN** |

</div>

### Contact Me:

<img src="https://raw.githubusercontent.com/RevoU-FSSE-2/week-7-SherinOlivia/3dd7cdf0d5c9fc1828f0dfcac8ef2e9c057902be/assets/gmail-icon.svg" width="15px" background-color="none">[SOChronicle@gmail.com](mailto:SOChronicle@gmail.com) [Personal]

<img src="https://raw.githubusercontent.com/RevoU-FSSE-2/week-7-SherinOlivia/3dd7cdf0d5c9fc1828f0dfcac8ef2e9c057902be/assets/gmail-icon.svg" width="15px" background-color="none">[SOlivia198@gmail.com](mailto:SOlivia198@gmail.com) [Work]

[![Roo-Discord](https://raw.githubusercontent.com/RevoU-FSSE-2/week-5-SherinOlivia/bddf1eca3ee3ad82db2f228095d01912bf9c3de6/assets/MDimgs/icons8-discord.svg)](https://discord.com/users/shxdxr#7539)[![Roo-Instagram](https://raw.githubusercontent.com/RevoU-FSSE-2/week-5-SherinOlivia/bddf1eca3ee3ad82db2f228095d01912bf9c3de6/assets/MDimgs/icons8-instagram.svg)](https://instagram.com/shxdxr?igshid=MzRlODBiNWFlZA==)[![Roo-LinkedIn](https://raw.githubusercontent.com/RevoU-FSSE-2/week-5-SherinOlivia/bddf1eca3ee3ad82db2f228095d01912bf9c3de6/assets/MDimgs/icons8-linkedin-circled.svg)](https://www.linkedin.com/in/sherin-olivia-07311127a/)