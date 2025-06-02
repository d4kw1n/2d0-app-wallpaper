from PIL import Image, ImageDraw

# Create a new image with a transparent background
img = Image.new('RGBA', (12, 12), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw the arrow
draw.line([(2, 4), (6, 8), (10, 4)], fill=(128, 128, 128, 255), width=2)

# Save the image
img.save('assets/down-arrow.png') 