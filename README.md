# Recipe Journal API

## Overview
Recipe Journal is a backend REST API that allows users to create, manage, and analyze recipes. 
The application helps users understand the nutritional benefits of their meals by analyzing ingredients using the Edamam Food Database API.

## Problem Statement
Many people cook meals without understanding their nutritional value. Recipe Journal solves this by allowing users to document recipes and automatically analyze nutritional content such as calories, fiber, and protein levels.

## Features
- User authentication (JWT)
- Recipe CRUD operations
- Ingredient management
- Recipe–Ingredient relationship
- Nutrition analysis using Edamam API
- Personalized data per user

## Tech Stack
- Python
- Django
- Django REST Framework
- SQLite (development)
- Edamam Food Database API
- JWT Authentication

## Database:
- SQLite (development)
- PostgreSQL recommended for production

## Installation
1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Set environment variables
5. Run migrations
6. Start server

## API Documentation
See detailed API endpoints below.
## API Endpoints

### Authentication
POST /api/auth/register/  
POST /api/auth/login/

### Recipes
GET /api/recipes/  
POST /api/recipes/  
GET /api/recipes/{id}/  
PUT /api/recipes/{id}/  
DELETE /api/recipes/{id}/  

### Recipe Ingredients
POST /api/recipe-ingredients/  
PUT /api/recipe-ingredients/{id}/  
DELETE /api/recipe-ingredients/{id}/  

### Recipe Analysis
POST /api/recipes/{id}/analyze/

## Note:
* Requires JWT access token
* Tested using Postman


## Author
**Miracle Adakole**  
Backend Engineering Student – ALX Africa (Cohort 7)

