from app.main import create_app
from front.main import mount_path

app = create_app()
mount_path(app, "front/static")

