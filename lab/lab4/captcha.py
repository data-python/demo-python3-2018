import os,sys;
from PIL import Image, ImageDraw, ImageFont
from skimage import transform as tf
import numpy as np

def create_captcha(text, shear=0, size=(100, 24)):

    im = Image.new("L", size, "black")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(r"Coval-Regular.otf", 22)
    draw.text((1, 1), text, fill=1, font=font)
    image = np.array(im)
    affine_tf = tf.AffineTransform(shear=shear)
    image = tf.warp(image, affine_tf)
    return image / image.max()

from matplotlib import pyplot as plt
image = create_captcha("GENE", shear=0.5)
plt.imshow(image, cmap='Greys')
#plt.show()

from skimage.measure import label, regionprops
def segment_image(image):
    #联通区域的图像标记为一组(相当于找联通块)
    labeled_image = label(image > 0)
    subimages = []
    #regionprops指的是标为同一组的联通块取它的范围
    for region in regionprops(labeled_image):
        #取得某一联通块的大小的左上角以及右下角坐标
        start_x, start_y, end_x, end_y = region.bbox
        subimages.append(image[start_x:end_x,start_y:end_y])
    #切分失败
    if len(subimages) == 0:
        return [image,]
    return subimages

#获得切分后的图像集合
subimages = segment_image(image)
#subplots，设置绘图区域,1到子图个数.figsize设置的是切割后figure显示框大小
f, axes = plt.subplots(1, len(subimages), figsize=(10,1))
for i in range(len(subimages)):
    axes[i].imshow(subimages[i], cmap="gray")
#plt.show()

from sklearn.utils import check_random_state
random_state = check_random_state(14)
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
shear_values = np.arange(0, 0.5, 0.05)

def generate_sample(random_state=None):
    random_state = check_random_state(random_state)
    letter = random_state.choice(letters)
    shear = random_state.choice(shear_values)
    #生成一个训练集，但是因为需要输入值和输出值。所以，把图片和这个字符所在的字母表位置相对应
    return create_captcha(letter, shear=shear, size=(20, 20)),letters.index(letter)

image, target = generate_sample(random_state)
plt.imshow(image, cmap="Greys")
print("The target for this image is: {0}".format(target))

#调用几千次该函数，生成足够的训练数据，把这些数据传入到numpy的数组
dataset, targets = zip(*(generate_sample(random_state) for i in range(3000)))
dataset = np.array(dataset, dtype='float')
targets = np.array(targets)

#共有26个类别，每个类别（字母）用从0到25之间的一个整数表示。用多个神经元有多个输出，每个输出值在0到1之间。因此，对类别使用一位有效码编码方法，每条数据就能得到26个输出。如果结果像某字母，使用近似于1的值；如果不像，就用近似于0的值。
from sklearn.preprocessing import OneHotEncoder
#使用N位状态寄存器来对N个状态进行编码，每个状态都由他独立的寄存器位，并且在任意时候，其中只有一位有效
onehot = OneHotEncoder()
y = onehot.fit_transform(targets.reshape(targets.shape[0],1))

#我们用的库不支持稀疏矩阵，因此，需要将稀疏矩阵转换为密集矩阵。
y = y.todense()

#需要用到scikit-image库中的resize函数，因为我们得到的小图像并不总是20像素见方
from skimage.transform import resize
#使用for循环将所有图像全部转换为20*20大小的，并重新扔给dataset
dataset = np.array([resize(segment_image(sample)[0], (20, 20)) for sample in dataset])
#创建一个改变了尺寸的新数组，原数组的shape保持不变
X = dataset.reshape((dataset.shape[0], dataset.shape[1] * dataset.shape[2]))

#使用scikit-learn中的train_test_split函数，把数据集切分为训练集和测试集。代码如下：
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.9)

from pybrain.datasets import SupervisedDataSet

#首先，遍历我们的训练集，把每条数据添加到一个新的SupervisedDataSet实例中：
training = SupervisedDataSet(X.shape[1], y.shape[1])
for i in range(X_train.shape[0]):
    training.addSample(X_train[i], y_train[i])

#然后，遍历测试集，同样把每条数据添加到一个新的SupervisedDataSet实例中：
testing = SupervisedDataSet(X.shape[1], y.shape[1])
for i in range(X_test.shape[0]):
    testing.addSample(X_test[i], y_test[i])

#导入buildNetwork函数，指定维度，创建神经网络。
#第一个参数X.shape[1]为输入层神经元的数量，也就是特征数（数据集X的列数）。
#第二个参数指隐含层的神经元数量，这里设置为100。
#第三个参数为输出层神经元数量，由类别数组y的形状来确定。
#最后，除去输出层外，我们每层使用一个一直处于激活状态的偏置神经元（bias neuron，它与下一层神经元之间有边连接，边的权重经过训练得到）。
from pybrain.tools.shortcuts import buildNetwork
net = buildNetwork(X.shape[1], 100, y.shape[1], bias=True)

#反向传播算法（back propagation，backprop）的工作机制为对预测错误的神经元施以惩罚。从输出层开始，向上层层查找预测错误的神经元，微调这些神经元输入值的权重，以达到修复输出错误的目的。
# PyBrain提供了backprop算法的一种实现，在神经网络上调用trainer类即可。
from pybrain.supervised.trainers import BackpropTrainer
trainer = BackpropTrainer(net, training, learningrate=0.01,weightdecay=0.01)

from pybrain.supervised.trainers import BackpropTrainer
trainer = BackpropTrainer(net, training, learningrate=0.01,weightdecay=0.01)

trainer.trainEpochs(epochs=20)

#在测试集上进行预测
predictions = trainer.testOnClassData(dataset=testing)

#得到预测值后，可以用scikit-learn计算F1值。
from sklearn.metrics import f1_score
print("F-score: {0:.2f}".format(f1_score(predictions,y_test.argmax(axis=1), average='micro' )))
