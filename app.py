from flask import Flask, render_template, request, redirect, url_for
import os
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Butterfly species data
BUTTERFLY_SPECIES = {
    'monarch': {
        'name': 'Monarch Butterfly',
        'fact': 'Migrates up to 3,000 miles each year!',
        'image': 'monarch.jpg'
    },
    'swallowtail': {
        'name': 'Swallowtail Butterfly',
        'fact': 'Named for the distinctive tail-like extensions on their hindwings.',
        'image': 'swallowtail.jpg'
    },
    'blue-morpho': {
        'name': 'Blue Morpho',
        'fact': 'Their wings reflect light to create an iridescent blue color.',
        'image': 'blue-morpho.jpg'
    },
    'painted-lady': {
        'name': 'Painted Lady',
        'fact': 'One of the most widespread butterfly species in the world.',
        'image': 'painted-lady.jpg'
    }
}

def get_random_species():
    """Return a random butterfly species"""
    return random.choice(list(BUTTERFLY_SPECIES.values()))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'butterfly-image' not in request.files:
            return redirect(request.url)
        
        file = request.files['butterfly-image']
        
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            # Save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Get a random species (in a real app, this would be ML prediction)
            species = get_random_species()
            
            return render_template('index.html', 
                                uploaded_image=filepath,
                                species=species)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
