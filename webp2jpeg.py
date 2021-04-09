from PIL import Image

for image in range(31):
    path = f"./uploads/room_photos/{image+1}.webp"
    img = Image.open(path)
    img.save(path, "jpeg")
