Extracting photos from my Ricoh GR camera is painful when on a motorbike trip. 

I want something in the lines of:

- Raspberry pi inside the bike connected via USB to the bike battery using a usb adaptor
- GPS tracking module attached to pi
- I turn on my camera and push the wifi button
- A python service running on the Pi will detect the presence of the camera SSID, connect to it and download all the photos
- Each photo downloaded to the pi will have geo-tagging information merged into the metadata
- Either when the download is complete or the camera SSID is no longer available, connect to the mobile phone SSID 
- Upload photos somewhere...


