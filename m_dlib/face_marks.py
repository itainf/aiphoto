import dlib
import cv2


def predictor_face(path):
    """
    :param path:   原始图片路径
    :return shape 关键点
    """
    # 模型路径 --》修改成自己的路径
    predictor_path = "E:\\python\\az\\dlib-19.19.0.tar\\shape_predictor_68_face_landmarks.dat"

    # 获取一个探测器
    detector = dlib.get_frontal_face_detector()
    # 获取一个预测模型
    predictor = dlib.shape_predictor(predictor_path)
    # 加载图片
    img = dlib.load_rgb_image(path)

    # 探测到的人脸
    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    # 取一个人脸
    d = dets[0]

    print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(0, d.left(), d.top(), d.right(), d.bottom()))

    # Get the landmarks/parts for the face in box d.
    shape = predictor(img, d)

    print("Part 0: {}, Part 1: {} ...".format(shape.part(0), shape.part(1)))
    return shape, d

# 显示人脸关键点
def test_landmarks(path,target_path):
    path = path
    img = cv2.imread(path)
    font=cv2.FONT_HERSHEY_SIMPLEX
    i = 0
    shape, d = predictor_face(path)
    for pt in shape.parts():
        i = i+1
        pt_pos = (pt.x, pt.y)
        cv2.putText(img, str(i), pt_pos, font, 0.3, (0, 255, 0))

    cv2.imshow("image", img)
    cv2.imwrite(target_path,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 打印人脸特征点
# test_landmarks("..//img//meinv_id.png","..//img//meinv_id_landmarks.png")
