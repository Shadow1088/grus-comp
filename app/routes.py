from flask import Blueprint, render_template, flash, redirect, url_for, send_file
from .forms import UploadForm
from werkzeug.utils import secure_filename
import io

from .utils.compress import compress_file  # stub for now

main = Blueprint('main', __name__)

@main.route("/", methods=["GET","POST"])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        upload = form.file.data
        filename = secure_filename(upload.filename)
        data = upload.read()
        out_bytes, out_name = compress_file(data, filename)  # currently returns same bytes
        return send_file(io.BytesIO(out_bytes),
                         as_attachment=True,
                         download_name=out_name,
                         mimetype='application/octet-stream')
    return render_template("upload.html", form=form)
