import os
import tornado.web
import shortuuid
from u_2_net import my_u2net_test
from to_background import to_background
from to_background import to_standard_trimap
from m_dlib import ai_crop

# import PILImageMy as mypil


class UploadHandler(tornado.web.RequestHandler):

    def post(self, *args, **kwargs):

        filename=shortuuid.uuid()
        print(os.path.dirname(__file__))
        parent_path = os.path.dirname(os.path.dirname(__file__))
        filePath =""
        # 查看上传文件的完整格式，files以字典形式返回
        print(self.request.files)
        # {'file1':
        # [{'filename': '新建文本文档.txt', 'body': b'61 60 -83\r\n-445 64 -259', 'content_type': 'text/plain'}],
        # 'file2':
        filesDict = self.request.files
        for inputname in filesDict:
            # 第一层循环取出最外层信息，即input标签传回的name值
            # 用过filename键值对对应，取出对应的上传文件的真实属性
            http_file = filesDict[inputname]
            for fileObj in http_file:

                # 第二层循环取出完整的对象
                # 取得当前路径下的 upfiles 文件夹+上fileObj.filename属性(即真实文件名)
                filePath = os.path.join(parent_path, "static", filename+".jpg")
                print(filePath)
                with open(filePath, 'wb') as f:
                    f.write(fileObj.body)



        org_img = filePath

        id_image = os.path.join(parent_path, "static", filename+"_meinv_id.png")
        # 20200719
        # 通过识别人脸关键点，裁剪图像
        ai_crop.crop_photo(org_img,id_image )


        print(org_img)
        alpha_img = os.path.join(parent_path, "static", filename+"_alpha.png")
        print(alpha_img)
        alpha_resize_img = os.path.join(parent_path, "static", filename+"_alpha_resize.png")
        print(alpha_resize_img)
        #
        # 通过u_2_net 获取 alpha
        my_u2net_test.test_seg_trimap(id_image, alpha_img, alpha_resize_img)
        #
        # # 通过alpha 获取 trimap
        trimap = os.path.join(parent_path, "static", filename+"_trimap_resize.png")
        to_standard_trimap.to_standard_trimap(alpha_resize_img, trimap)
        print(trimap)

        id_image_org = os.path.join(parent_path, "static", filename+"_meinv_id_2in.png")

        #
        # 证件照添加蓝底纯色背景//"..\\aiphoto\\img\\meinv_trimap_resize.png"
        #         to_standard_trimap.to_standard_trimap(alpha_resize_img, trimap)
        to_background.to_background(id_image, trimap, id_image_org, "blue")
        print(id_image_org)
        self.write( "static/"+filename+"_meinv_id_2in.png")



