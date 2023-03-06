#import structlog
from app_manager import get_app_manager

#logger = structlog.get_logger()

app = get_app_manager()
x=app.get_playlists()
app.play_pause()

print(x)
