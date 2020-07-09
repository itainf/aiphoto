from PIL import Image


def to_standard_trimap(alpha, trimap):
    #  Alpha图生成 trimap
    print(alpha)
    image = Image.open(alpha)
    print(image)
    # image = image.convert("P")
    # image_file.save('meinv_resize_trimap.png')
    sp = image.size
    width = sp[0]
    height = sp[1]

    for yh in range(height):
        for xw in range(width):
            dot = (xw, yh)
            color_d_arr = image.getpixel(dot)
            color_d=color_d_arr[0]

            if 0 < color_d <= 60:
                image.putpixel(dot, (0,0,0))
            if 60 < color_d <= 200:
                image.putpixel(dot, (128,128,128))
            if 200 < color_d <= 255:
                image.putpixel(dot, (255,255,255))

    image.save(trimap)





# to_standard_trimap("..\\img\\trimap\\meinv_resize_trimap.png", "meinv_resize_bz_trimap.png")
#
#
# image = Image.open("meinv_resize_bz_trimap.png")
# data = image.getdata()
# np.savetxt("data4.txt", data,fmt='%d',delimiter=',')
