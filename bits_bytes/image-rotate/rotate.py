
def rotate_image(bmp):
    # Extract metadata https://en.wikipedia.org/wiki/BMP_file_format
    pixel_start = int.from_bytes(bmp[10:14],'little')
    width = int.from_bytes(bmp[18:22],'little')
    height = int.from_bytes(bmp[22:26],'little')

    # Extract pixels
    pixel_size = 3 # RGB
    row_size = pixel_size * width
    column_size = pixel_size * height
    pixel_end = pixel_start + (row_size * column_size)
    pixels = bmp[pixel_start:pixel_end]

    # Rotate pixels
    rows = [pixels[i:i+row_size] for i in range(0, len(pixels), row_size)]
    rotated_rows = [b'' for _ in range(row_size)]
    for row in rows:
        for i in range(0, len(row), pixel_size):
            pixel = row[i:i+pixel_size]
            index = (row_size - pixel_size - i) // pixel_size
            rotated_rows[index] += pixel
    
    # Mash everything back together
    return bmp[:pixel_start] + b''.join(rotated_rows) + bmp[pixel_end:]

with open('teapot.bmp', 'rb') as f:
    bmp = f.read()

rotated_bmp = rotate_image(bmp)
with open('teapot-rotated.bmp', 'wb') as f2:
    f2.write(rotated_bmp)
