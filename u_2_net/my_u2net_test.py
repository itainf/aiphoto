import torch
from torch.autograd import Variable
from torchvision import transforms#, utils
# import torch.optim as optim
import numpy as np
from u_2_net.data_loader import RescaleT
from u_2_net.data_loader import ToTensorLab
from u_2_net.model import U2NET # full size version 173.6 MB
from PIL import Image


# normalize the predicted SOD probability map
def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)
    dn = (d-mi)/(ma-mi)
    return dn


def preprocess(image):
    label_3 = np.zeros(image.shape)
    label = np.zeros(label_3.shape[0:2])

    if (3 == len(label_3.shape)):
        label = label_3[:, :, 0]
    elif (2 == len(label_3.shape)):
        label = label_3
    if (3 == len(image.shape) and 2 == len(label.shape)):
        label = label[:, :, np.newaxis]
    elif (2 == len(image.shape) and 2 == len(label.shape)):
        image = image[:, :, np.newaxis]
        label = label[:, :, np.newaxis]

    transform = transforms.Compose([RescaleT(320), ToTensorLab(flag=0)])
    sample = transform({
        'imidx': np.array([0]),
        'image': image,
        'label': label
    })

    return sample


def pre_net():
    # 采用n2net 模型数据
    model_name = 'u2net'
    model_dir = 'saved_models/'+ model_name + '/' + model_name + '.pth'
    print("...load U2NET---173.6 MB")
    net = U2NET(3,1)
    # 指定cpu
    net.load_state_dict(torch.load(model_dir, map_location=torch.device('cpu')))
    if torch.cuda.is_available():
        net.cuda()
    net.eval()
    return net


def pre_test_data(img):
    torch.cuda.empty_cache()
    sample = preprocess(img)
    inputs_test = sample['image'].unsqueeze(0)
    inputs_test = inputs_test.type(torch.FloatTensor)
    if torch.cuda.is_available():
        inputs_test = Variable(inputs_test.cuda())
    else:
        inputs_test = Variable(inputs_test)
    return inputs_test


def get_im(pred):
    predict = pred
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()
    im = Image.fromarray(predict_np*255).convert('RGB')
    return im


def test_seg_trimap(org,org_trimap,resize_trimap):
    # 将原始图片转换成trimap
    # org：原始图片
    # org_trimap:
    # resize_trimap: 调整尺寸的trimap
    image = Image.open(org)
    print(image)
    img = np.array(image)
    net = pre_net()
    inputs_test = pre_test_data(img)
    d1, d2, d3, d4, d5, d6, d7 = net(inputs_test)
    # normalization
    pred = d1[:, 0, :, :]
    pred = normPRED(pred)
    # 将数据转换成图片
    im = get_im(pred)
    im.save(org_trimap)
    sp = image.size
    # 根据原始图片调整尺寸
    imo = im.resize((sp[0], sp[1]), resample=Image.BILINEAR)
    imo.save(resize_trimap)


if __name__ == "__main__":
    test_seg_trimap("..\\img\\meinv.jpg","..\\img\\trimap\\meinv_org_trimap.png","..\\img\\trimap\\meinv_resize_trimap.png")
    #pil_wait_blue()
