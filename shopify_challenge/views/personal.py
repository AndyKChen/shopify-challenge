import os
from io import BytesIO

import requests
from flask import Response, redirect, render_template, request, session
from flask.views import MethodView

from shopify_challenge.helpers.config import CLOUDFRONT
from shopify_challenge.helpers.decorators import login_required
from shopify_challenge.helpers.s3_helpers import (create_presigned_url,
                                                  delete_image)
from shopify_challenge.models.image import ImageModel


class Personal(MethodView):
    
    @login_required
    def get(self):
        public_images = ImageModel.get_public_images_by_username(session['username'])
        private_images = ImageModel.get_private_images_by_username(session['username'])
        return render_template("personal.html", public_images=public_images, private_images=private_images, cloudfront=CLOUDFRONT), 200
    
    @login_required
    def post(self):
        action = request.form.get('action')
        identifier = request.form['identifier']
        image = ImageModel.get_image_by_identifier(identifier)
        if action == "make public" or action == "make private":
            image.change_privacy()
        elif action == "delete":
            delete_image(identifier)
            image.delete_from_database()
        elif action == "download":
            url = create_presigned_url(identifier)
            return Response(
                BytesIO(requests.get(url).content),
                mimetype='image/jpeg',
                headers={"Content-Disposition": "attachment;filename=" + identifier}
            )
        return redirect('/personal'), 200