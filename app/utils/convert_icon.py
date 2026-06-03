from PIL import Image

# Load PNG image
img = Image.open("app/assets/projtrack_icon.png")

# Convert and save as ICO
img.save(
    "app/assets/projtrack_icon.ico",
    format="ICO",
    sizes=[(256, 256)]
)

print("Proj.Track icon converted successfully.")