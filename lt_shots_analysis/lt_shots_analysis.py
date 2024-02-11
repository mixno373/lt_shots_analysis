import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as mfm

import numpy as np

from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from enum import Enum



plt.rcParams.update({'figure.max_open_warning': 0})

fig, ax = plt.subplots(figsize=(9, 4.5))
plt.margins(x=0.01, y=0.01)
plt.box(on=None)



y_cord = 1.9
bar_height = 0.1
shot_y_shift = 0.125
toptext_y_shift = 0.15
undertext_y_shift = 0.08

# Добавляем данные в график
series1 = 3
series2 = 2
series3 = 1
plt.axis([0, 15, 0, 2])
plt.barh(y_cord, series1, height=bar_height, color='r')
plt.barh(y_cord, series2, height=bar_height, color='b', left=3)
plt.barh(y_cord, series3, height=bar_height, color='g', left=6)

plt.text(series1, y_cord-shot_y_shift, "•", ha='center', va='bottom', fontsize=30, color="#FFFFFF")
plt.text(1, y_cord+toptext_y_shift, "СИБЗ - 1 класс | 0.8 с. ШОК, 0.5 с. НЕУЯЗВИМОСТЬ", ha='left', va='top', fontsize=10, color="#FFFFFF")
plt.text(series1 / 2, y_cord-undertext_y_shift, "неуязвим", ha='center', va='top', fontsize=10, color="#FFFFFF")

# get the axes object
ax = plt.gca()
# hide the y-axis
ax.get_yaxis().set_visible(False)

plt.yticks(color="#FFFFFF")
plt.xticks(color="#FFFFFF")
ax.set_axisbelow(True)
fig.tight_layout()
ax.set_facecolor('#36393f')
fig.patch.set_facecolor('#36393f')



# Конвертировать график в объект изображения
f_name = f"plot.png"
img_buf = BytesIO()
plt.savefig(img_buf, format='png', facecolor=fig.get_facecolor(), transparent=True)
plot_img = Image.open(img_buf)
plot_img.save(f_name, "PNG")
plt.show()

plt.clf()
fig.clf()
ax.cla()