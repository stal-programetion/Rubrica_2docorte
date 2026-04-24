from app.routes.routes import app

# Vercel buscará automáticamente la variable "app" dentro de index.py
if __name__ == '__main__':
    app.run(debug=True, port=5000)
