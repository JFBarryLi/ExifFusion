# ExifFusion

Overlay EXIF metadata onto photos.

## Features
- Extract Exif metadata from photos
- Overlay metadata onto photos, such as datetime and location.
- Reverse geo-code GPS cordinates into addresses.
- Dynamically chooses overlay text color to maximize contrast.
- [TODO] QR Code for more information, link to map

## Usage
```bash
exiffusion fuse INPUT_PATH OUTPUT_PATH
```

For help:
```bash
exiffusion --help
exiffusion fuse --help
```

## TODO
- Summary report on success and failure at the end
- qr code
- Investigate london color-contrast

## Development
```bash
pip install -e .
```
