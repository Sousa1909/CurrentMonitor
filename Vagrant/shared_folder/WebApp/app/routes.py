from app import app

@app.route('/')
def index():
    return render_template('index.html')
    
# Other routes and API endpoints