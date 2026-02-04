# 🔐 VulnERP – Vulnerable College ERP

VulnERP is an **intentionally vulnerable college ERP web application** created for **cybersecurity education and hands-on learning**.

The project is designed to simulate a **realistic ERP environment** used in educational institutions, while deliberately introducing security weaknesses to help students understand how authentication and access control failures occur in real systems.


## 🎯 Project Purpose

The main goal of VulnERP is to provide a **practical learning platform** where users can:

- Understand how ERP authentication systems work  
- Learn how security flaws arise due to poor design and logic errors  
- Practice identifying vulnerabilities in a controlled environment  
- Develop a real-world penetration testing mindset  

This project focuses on **learning by breaking**, not automated scanning.


## 🧩 What This Project Includes

VulnERP is being developed with the following key concepts:

### 🔑 Authentication Vulnerabilities
- Weak authentication mechanisms  
- Improper validation of login workflows  
- Poor implementation of security controls  

### 🧑‍💼 Role-Based Access Model
The application simulates multiple user roles commonly found in a college ERP:

- Student  
- Faculty  
- Admin  

Each role is designed with a **different difficulty level**, ensuring gradual learning from basic to advanced security concepts.


## 📈 Role-Based Difficulty Progression

| Role    | Difficulty | Focus |
|--------|------------|-------|
| Student | Easy | Basic authentication weaknesses |
| Faculty | Medium | Logic flaws and multi-factor issues |
| Admin | Hard | Critical authentication and authorization failures |

As the privilege level increases, vulnerabilities become:
- Less obvious  
- More logic-driven  
- More impactful  


## 🚫 Access Control Focus

Apart from authentication, VulnERP also highlights **Broken Access Control** issues such as:

- Missing server-side authorization checks  
- Over-trusting client-side data  
- Improper role validation  

These issues reflect common mistakes seen in real ERP systems.


## 🧠 Learning Philosophy

VulnERP is built with the belief that:

- Security is more about **logic** than tools  
- Client-side controls cannot be trusted  
- Proper authentication design is critical  
- Access control failures can lead to severe impact  

Automated vulnerability scanners are intentionally avoided to encourage **manual analysis and reasoning**.


## 🛠️ Intended Learning Outcomes

By working with VulnERP, learners will be able to:

- Understand ERP authentication architecture  
- Identify role-based security weaknesses  
- Analyze flawed authentication logic  
- Recognize the impact of broken access control  
- Think like an attacker in real-world scenarios  


## 🚧 Project Status

VulnERP is currently under development.  
Future updates will expand the project to cover more security concepts and OWASP Top 10 vulnerabilities.


## ⚠️ Disclaimer

This application is intentionally insecure and must be used **only for educational purposes**.  
Do not deploy this project in a production environment.
