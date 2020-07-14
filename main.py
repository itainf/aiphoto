
from u_2_net import my_u2net_test
from to_background import to_background
from to_background import to_standard_trimap
from m_dlib import ai_crop

import numpy as np
from PIL import Image
if __name__ == "__main__":
    org_img = "..\\aiphoto\\img\\meinv.jpg"
    alpha_img = "..\\aiphoto\\img\\meinv_alpha.png"
    alpha_resize_img = "..\\aiphoto\\img\\meinv_alpha_resize.png"
    # #
    # 通过u_2_net 获取 alpha
    my_u2net_test.test_seg_trimap(org_img, alpha_img, alpha_resize_img)
    #
    # # 通过alpha 获取 trimap
    trimap = "..\\aiphoto\\img\\meinv_trimap_resize.png"
    to_standard_trimap.to_standard_trimap(alpha_resize_img, trimap)
    #
    # 证件照添加蓝底纯色背景
    id_image = "..\\aiphoto\\img\\meinv_id.png"
    to_background.to_background(org_img, trimap, id_image, "blue")
    #id_image = "..\\aiphoto\\img\\meinv_id_grid.png"
    #to_background.to_background_grid(org_img, trimap, id_image)
    # image = Image.open(id_image)
    # data = image.getdata()
    # np.savetxt("data6.txt", data,fmt='%d',delimiter=',')

    # 20200719
    # 通过识别人脸关键点，裁剪图像
    ai_crop.crop_photo("..\\aiphoto\\img\\meinv_id.png", "..\\aiphoto\\img\\2in.jpg")
