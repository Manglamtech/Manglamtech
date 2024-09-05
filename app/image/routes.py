from database.database import db
from flask import request,jsonify,send_file
from . import bp
from database.database import db
import os
from app.model.image import Image


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@bp.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Save the image metadata to the database
        new_image = Image(filename=file.filename)
        db.session.add(new_image)
        db.session.commit()

        return jsonify({'message': 'Image uploaded successfully', 'image_id': new_image.id}), 200

# @bp.route('/get_image', methods=['GET'])
# def get_image():
#     image_id = request.args.get('image_id')
    
#     if not image_id:
#         return jsonify({'error': 'No image ID provided'}), 400
    
#     image = Image.query.get(image_id)
    
#     if image:
#         image_path = os.path.join(UPLOAD_FOLDER, image.filename)
#         return send_file(image_path, mimetype='image/jpeg')
#     else:
#         return jsonify({'error': 'Image not found'}), 404
    

@bp.route('/get_all_images', methods=['GET'])
def get_all_images():
    try:
        images = Image.query.all()
        
        if not images:
            return jsonify({'message': 'No images found'}), 404

    
        images_data = []
        for image in images:
            images_data.append({
                'image_id': image.id,
                'filename': image.filename,
            })

        return jsonify({'images': images_data}), 200

    except Exception as e:

        return jsonify({'error': str(e)}), 500