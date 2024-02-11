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


firerate = 300
firemode = "ОД"
# firemode = "АВ"

tth_alldata = {
    "Здание": [
        {
            "shock": 300,
            "invulnerability": 200,
            "title": "Без СИБЗ"
        },
        {
            "shock": 300,
            "invulnerability": 300,
            "title": "СИБЗ - 1 класс"
        },
        {
            "shock": 300,
            "invulnerability": 400,
            "title": "СИБЗ - 2 класс"
        },
        {
            "shock": 300,
            "invulnerability": 500,
            "title": "СИБЗ - 3 класс"
        }
    ],
    "Лес": [
        {
            "shock": 800,
            "invulnerability": 500,
            "title": "Без СИБЗ"
        },
        {
            "shock": 800,
            "invulnerability": 700,
            "title": "СИБЗ - 1 класс"
        },
        {
            "shock": 800,
            "invulnerability": 900,
            "title": "СИБЗ - 2 класс"
        },
        {
            "shock": 800,
            "invulnerability": 1100,
            "title": "СИБЗ - 3 класс"
        }
    ]
}


for firerate in [
    30,
    50,
    60,
    100,
    150,
    200,
    300,
    350,
    400,
    440,
    450,
    470,
    480,
    500
]:
    for polygon in ["Здание", "Лес"]:
        tth_data = tth_alldata[polygon]
        
        for firemode in ["ОД", "АВ"]:
            
            plot_title = f'{polygon} - {firerate} выстр/с. {firemode}'
            print(plot_title)

            y_cord = 1.9
            bar_height = 0.1
            shot_y_shift = 0.125
            toptext_y_shift = 0.15
            undertext_y_shift = 0.1
            x_length = 3 * 1000 # Ширина графика в мс

            plt.axis([-200, x_length, 0.2, 2.2])
            plt.box(on=None)


            for tth in tth_data:
                # Период выстрелов
                t_shot = 60 * 1000 / firerate
                if firemode == "ОД":
                    # Добавить 20 мс, если стрельба одиночными. Не в каждый тайминг попадет игрок
                    t_shot = t_shot + 30
                    
                shots_ts = [0]
                while shots_ts[-1] + t_shot <= x_length:
                    # Расчет времени выстрелов
                    shots_ts.append(shots_ts[-1] + t_shot)
                    
                shock_til_ts = 0
                invulnerability_til_ts = 0
                cur_ts = 0
                
                
                for ts in shots_ts:
                    # Если ранен и еще не вышел с неуязвимости - не обрабатываем ранение
                    if invulnerability_til_ts <= ts:
                        # Шок
                        plt.barh(y_cord-0.04, tth['shock'], height=bar_height, color='b', left=ts)
                        
                        plt.text(ts, y_cord-shot_y_shift, "•", ha='center', va='bottom', fontsize=30, color="y")
                        plt.barh(y_cord, tth['invulnerability'], height=bar_height, color='r', left=ts)
                        plt.text(ts, y_cord - undertext_y_shift, "ранен", ha='left', va='top', fontsize=10, color="#FFFFFF")
                        invulnerability_til_ts = ts + tth['invulnerability']
                        
                    else:
                        plt.text(ts, y_cord-shot_y_shift, "•", ha='center', va='bottom', fontsize=30, color="w")
                        
                    

                # Добавляем данные в график
                plt.axis([-200, x_length, 0, 2])
                # plt.barh(y_cord-0.04, series2, height=bar_height, color='b', left=3)
                # plt.barh(y_cord, series1, height=bar_height, color='r')
                # plt.barh(y_cord, series3, height=bar_height, color='g', left=6)

                plt.text(x_length*0.05, y_cord+toptext_y_shift, f"{tth['title']} | {round(tth['shock'] / 1000, 1)} с. ШОК, {round(tth['invulnerability'] / 1000, 1)} с. НЕУЯЗВИМОСТЬ", ha='left', va='top', fontsize=10, color="#FFFFFF")
                # plt.text(series1 / 2, y_cord-undertext_y_shift, "неуязвим", ha='center', va='top', fontsize=10, color="#FFFFFF")
                
                y_cord = y_cord - 0.5




            # get the axes object
            ax = plt.gca()
            # hide the y-axis
            ax.get_yaxis().set_visible(False)
            
            plt.title(plot_title, fontsize=15 , loc='left', color="w", pad=30) 

            plt.yticks(color="#FFFFFF")
            plt.xticks(color="#FFFFFF")
            ax.set_axisbelow(True)
            fig.tight_layout()
            ax.set_facecolor('#36393f')
            fig.patch.set_facecolor('#36393f')



            # Конвертировать график в объект изображения
            f_name = f"lt_shots_analysis/{polygon}/{firerate} выстр_с {firemode}.png"
            img_buf = BytesIO()
            plt.savefig(img_buf, format='png', facecolor=fig.get_facecolor(), transparent=True)
            plot_img = Image.open(img_buf)
            plot_img.save(f_name, "PNG")
            # plt.show()

            plt.clf()
            fig.clf()
            ax.cla()