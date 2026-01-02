# Recipe_Journal-app

Recipe Journal is a Django REST API that allows users to create, manage, and analyze recipes and ingredients. The application is designed to provide a seamless experience for recipe management and nutritional analysis using the Edamam Food Database API.

Key Features:

-User authentication (signup and login) with JWT.

-CRUD operations for Recipes and Ingredients.

-Link ingredients to recipes with quantity and units.

-Nutritional analysis of recipes with external API integration (Edamam).

-Summary generation (e.g., protein-rich, high-fiber, low-carb).

Technology Stack:

* Backend: Python 3.11, Django 5.2.9, Django REST Framework

* Database: SQLite3 (default, lightweight for testing)

* Authentication: JWT via djangorestframework-simplejwt

* External API: Edamam Food Database API (for nutritional analysis)

Testing: Postman

Installation & Setup:

Clone the repository

git clone http://
cd Recipe_Journal-app

Create a virtual environment:
venv\Scripts\activate       # Windows

Install dependencies

pip install -r requirements.txt


Set up .env file

# .env file
EDAMAM_APP_ID=<edamam-app-id>
EDAMAM_APP_KEY=<edamam-api-key>

Apply migrations:
python manage.py migrate

Run the server

python manage.py runserver


Server will start at http://127.0.0.1:8000/.

Authentication Flow

Signup

Endpoint: POST /api/signup/

Body:

{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password"
}


Login / Get JWT Token

Endpoint: POST /api/token/

Body:

{
  "username": "your_username",
  "password": "your_password"
}


Response:

{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}


Include Access Token in Requests

Use header:

Authorization: Bearer <access_token>

API Endpoints
Welcome

GET /api/Welcome/

Returns a simple welcome message for users.

Ingredients

GET /api/ingredients/ – List all ingredients for logged-in user.

POST /api/ingredients/ – Add new ingredient.

Body:

{
  "name": "Carrot",
  "description": "Fresh carrot"
}


GET /api/ingredients/{id}/ – Get single ingredient details.

PUT /api/ingredients/{id}/ – Update ingredient.

DELETE /api/ingredients/{id}/ – Delete ingredient.

Special Action:

GET /api/ingredients/{id}/benefits/ – Fetch nutritional benefits from external API.

Recipes

GET /api/recipes/ – List all recipes for logged-in user.

POST /api/recipes/ – Create a recipe.

Body:

{
  "name": "Fried Rice",
  "description": "Delicious fried rice recipe"
}


GET /api/recipes/{id}/ – Get recipe details.

PUT /api/recipes/{id}/ – Update recipe.

DELETE /api/recipes/{id}/ – Delete recipe.

Custom Action:

POST /api/recipes/{id}/analyze/ – Analyze recipe ingredients and return nutritional summary.

Response:

{
  "recipe": "Fried Rice",
  "ingredients_sent": [
    "2 cups Carrot",
    "1 cup Peas"
  ],
  "calories": 350,
  "dietLabels": ["Balanced"],
  "healthLabels": ["High-Fiber", "Low-Sugar"],
  "totalNutrients": {
    "ENERC_KCAL": {"label": "Energy", "quantity": 350, "unit": "kcal"}
  },
  "summary": ["high-fiber", "low-carb"],
  "status": "Nutrition successfully analyzed"
}

Recipe Ingredients

GET /api/recipe-ingredients/ – List all ingredients linked to recipes.

POST /api/recipe-ingredients/ – Add ingredient to recipe.

Body:

{
  "recipe": 1,
  "ingredient": 2,
  "quantity": "2",
  "unit": "cups"
}


PUT / PATCH / DELETE – Update or remove ingredient from recipe.

Notes

Only the logged-in user can access their recipes and ingredients.

RecipeIngredient ensures unique recipe-ingredient combination.

Nutritional analysis requires valid Edamam API credentials.

Currently using SQLite, which is sufficient for local testing and submission. Switching to PostgreSQL is optional.

Testing the API

Use Postman to test all endpoints:

Signup → Login → Get JWT → Add Ingredients → Add Recipe → Add Recipe Ingredients → Analyze Recipe.

Include JWT in the Authorization header for protected endpoints.

Test multiple ingredients per recipe to validate analyzer.

Future Improvements

Switch to PostgreSQL for production.

Frontend interface for easier navigation (React/Vue).

More advanced nutrition insights.

Save analyzed summary for each recipe.
