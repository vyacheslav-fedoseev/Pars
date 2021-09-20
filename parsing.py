import sys
# pip install PyMuPDF
import fitz
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import re
import os.path

# аргументы из командной строки записываем в соответствующие переменные
path_pdf = sys.argv[1]
# если такого файла не существует, бросаем исключение
if not os.path.isfile(path_pdf):
    raise Exception("Incorrect path of pdf-file")
page_index = int(sys.argv[2])
page_width = int(sys.argv[3])
page_height = int(sys.argv[4])
is_show_matplotlib = True if sys.argv[5] == 'True' else False
save_path = sys.argv[6]
# если по шаблону не находим в названии файла перечень доступных расширений, также бросаем исключение
if re.search(r'\.png|\.jpeg|\.tiff$', save_path) is None:
    raise Exception("Incorrect image format! Use .jpeg, .png or .tiff")
page_format = sys.argv[7]

# получаем страницу в формате, который указал пользователь и сохраняем по указанному пути в случае верного индекса
doc = fitz.open(path_pdf)
if doc.pageCount <= page_index:
    raise Exception("Incorrect number of page!")
page = doc.loadPage(page_index)
pix = page.getPixmap()
pix.writePNG(save_path)

image_of_pdf = mpimg.imread(save_path)
image_height, image_width = image_of_pdf.shape[:2]
# находим центры картинки
image_height_div2 = round(image_height / 2)
image_width_div2 = round(image_width / 2)
# находим сдвиги относительно центра
page_width_div2 = round(page_width / 2)
page_height_div2 = round(page_height / 2)
# чтобы сдвиг картинки не вышел в отрицательную зону, делаем переменные равными, если это произошло
page_height_div2 = image_height_div2 if image_height_div2 - page_height_div2 < 0 else page_height_div2
page_width_div2 = image_width_div2 if image_width_div2 - page_width_div2 < 0 else page_width_div2
new_image = image_of_pdf[image_height_div2 - page_height_div2:image_height_div2 + page_height_div2,
            image_width_div2 - page_width_div2:image_width_div2 + page_width_div2]

# условия конечно было написать намного короче, но тогда добавлять другие форматы будет сложнее
# и придётся переписывать, поэтому под будущее
# else выполняется как бы по умолчанию, если указан не gray
if page_format == 'gray':
    gray = np.dot(new_image[..., :3], [0.2989, 0.5870, 0.1140])
    plt.imsave(save_path, gray, cmap='gray')
else:
    plt.imsave(save_path, new_image)

if is_show_matplotlib:
    if page_format == 'gray':
        plt.imshow(gray, cmap=plt.get_cmap('gray'))
    else:
        plt.imshow(new_image, vmin=0, vmax=1)
    plt.axis('off')
    plt.show()