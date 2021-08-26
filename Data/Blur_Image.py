def BlurImage(img,amount, repetitions=1):
    from PIL import Image, ImageFilter

    image = Image.open(img)

    for i in range(repetitions):
        boxImage = image.filter(ImageFilter.BoxBlur(amount))

    boxImage.save(img)

