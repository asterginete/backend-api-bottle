from bottle import Bottle, mount
from .routes import auth_routes, item_routes, category_routes, comment_routes, notification_routes

app = Bottle()

app.mount('/auth', auth_routes)
app.mount('/items', item_routes)
app.mount('/categories', category_routes)
app.mount('/comments', comment_routes)
app.mount('/notifications', notification_routes)
