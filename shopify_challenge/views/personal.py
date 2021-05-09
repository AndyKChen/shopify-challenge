import os

from flask import render_template, session
from flask.views import MethodView

from shopify_challenge.helpers.decorators import login_required
from shopify_challenge.models.image import ImageModel

class Personal(MethodView):
    
    @login_required
    def get(self):
        public_images = ImageModel.get_public_images_by_username(session['username'])
        private_images = ImageModel.get_private_images_by_username(session['username'])
        cloudfront = os.environ.get('CLOUDFRONT_DOMAIN')
        return render_template("personal.html", public_images=public_images, private_images=private_images, cloudfront=cloudfront)