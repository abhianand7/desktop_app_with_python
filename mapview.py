# from kivy.garden.mapview import MapView
# from kivy.app import App
#
# class MapViewApp(App):
#     def build(self):
#         mapview = MapView(zoom=11, lat=50.6394, lon=3.057)
#         return mapview
#
# MapViewApp().run()

import gmplot

gmap = gmplot.GoogleMapPlotter(19.7, 79.2, 16)

gmap.draw('my_html.html')