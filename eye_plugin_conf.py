from talon.track.geom import Point2d
from talon_plugins import eye_mouse, eye_zoom_mouse

eye_mouse.config.velocity = Point2d(100, 200)


eye_zoom_mouse.config.screen_area = Point2d(400, 300)
eye_zoom_mouse.config.img_scale = 4
eye_zoom_mouse.config.eye_avg = 100

