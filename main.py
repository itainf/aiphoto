
from u_2_net import my_u2net_test
from to_background import to_background
from to_background import to_standard_trimap
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
    # # 证件照添加纯色背景
    id_image = "..\\aiphoto\\img\\meinv_id_grid.png"
    # to_background.to_background(org_img, trimap, id_image, "blue")
    to_background.to_background_grid(org_img, trimap, id_image)
    # image = Image.open(id_image)
    # data = image.getdata()
    # np.savetxt("data6.txt", data,fmt='%d',delimiter=',')
