from flask import Blueprint, render_template, flash, redirect, url_for, send_file
from .forms import UploadForm
from werkzeug.utils import secure_filename
import io
import mimetypes

from .utils.compress import compress_image, compress_video

main = Blueprint('main', __name__)

@main.route("/", methods=["GET","POST"])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        upload = form.file.data
        filename = secure_filename(upload.filename)
        data = upload.read()
        mime_type, _ = mimetypes.guess_type(filename)
        try:
            if mime_type and mime_type.startswith('image'):
                out_bytes = compress_image(data)
            elif mime_type and mime_type.startswith('video'):
                out_bytes = compress_video(data, filename)
            else:
                flash('Unsupported file type.', 'error')
                return redirect(url_for('main.index'))
        except Exception as e:
            flash(f'Compression failed: {e}', 'error')
            return redirect(url_for('main.index'))
        return send_file(io.BytesIO(out_bytes),
                         as_attachment=True,
                         download_name=filename,
                         mimetype=mime_type or 'application/octet-stream')
    return render_template("upload.html", form=form)
