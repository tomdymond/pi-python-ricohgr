#!/usr/bin/env python

import pyexiv2
import fractions
from PIL import Image
from PIL.ExifTags import TAGS
import sys
import datetime

# http://exiv2.org/tags.html

class Grimageexif(object):
  def __init__(self, image_file):
    self.image_file = image_file
    self.metadata = pyexiv2.ImageMetadata(self.image_file)
    self.metadata.read()

  def to_deg(self, value, loc):
    if value < 0:
      loc_value = loc[0]
    elif value > 0:
      loc_value = loc[1]
    else:
      loc_value = ""
    abs_value = abs(value)
    deg =  int(abs_value)
    t1 = (abs_value-deg)*60
    min = int(t1)
    sec = round((t1 - min)* 60, 5)
    return (deg, min, sec, loc_value)

  def get_taken_time(self):
    """ Return an epochs timestamp of when the picture was taken """
    t =  self.metadata['Exif.Image.DateTime'].value
    return t.strftime('%s')

  def view_gps_location(self, file_name, lat, lng):
    """Adds GPS position as EXIF metadata
    Keyword arguments:
    file_name -- image file 
    lat -- latitude (as float)
    lng -- longitude (as float)
    """
    lat_deg = to_deg(lat, ["S", "N"])
    lng_deg = to_deg(lng, ["W", "E"])
    
    print lat_deg
    print lng_deg
    
    # convert decimal coordinates into degrees, munutes and seconds
    exiv_lat = (pyexiv2.Rational(lat_deg[0]*60+lat_deg[1],60),pyexiv2.Rational(lat_deg[2]*100,6000))
    exiv_lng = (pyexiv2.Rational(lng_deg[0]*60+lng_deg[1],60),pyexiv2.Rational(lng_deg[2]*100,6000))

    exiv_image = pyexiv2.Image(file_name)
    exiv_image.readMetadata()
    exif_keys = exiv_image.exifKeys() 
    
    for key in exif_keys:
      print key, [exiv_image[key]]
    
  def set_gps_location(self, file_name, lat, lng):
    """Adds GPS position as EXIF metadata
    Keyword arguments:
    file_name -- image file 
    lat -- latitude (as float)
    lng -- longitude (as float)
    """
    lat_deg = to_deg(lat, ["S", "N"])
    lng_deg = to_deg(lng, ["W", "E"])
    
    print lat_deg
    print lng_deg
    
    # convert decimal coordinates into degrees, munutes and seconds
    exiv_lat = (pyexiv2.Rational(lat_deg[0]*60+lat_deg[1],60),pyexiv2.Rational(lat_deg[2]*100,6000), pyexiv2.Rational(0, 1))
    exiv_lng = (pyexiv2.Rational(lng_deg[0]*60+lng_deg[1],60),pyexiv2.Rational(lng_deg[2]*100,6000), pyexiv2.Rational(0, 1))

    exiv_image = pyexiv2.ImageMetadata(file_name)
    exiv_image.read()
    exif_keys = exiv_image.exif_keys
    
    exiv_image["Exif.GPSInfo.GPSLatitude"] = exiv_lat
    exiv_image["Exif.GPSInfo.GPSLatitudeRef"] = lat_deg[3]
    exiv_image["Exif.GPSInfo.GPSLongitude"] = exiv_lng
    exiv_image["Exif.GPSInfo.GPSLongitudeRef"] = lng_deg[3]
    exiv_image["Exif.Image.GPSTag"] = 654
    exiv_image["Exif.GPSInfo.GPSMapDatum"] = "WGS-84"
    exiv_image["Exif.GPSInfo.GPSVersionID"] = '2 0 0 0'
    
    exiv_image.write()
    # set_gps_location(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))

  def return_tags(self):
    """ Just for testing, return the tags """
    return self.metadata.keys()

  def update_add_key(self, k, v):
    """ Update metadata """
    self.metadata[k] = v
    self.metadata.write()
