import imageio.v2 as iio #写入视频
import numpy as np
import os
import time #获取当前时间
import shutil
from natsort import natsorted # 按1，2，3，..., 10，11，12的自然数顺序对文件进行排序，而非 1 10，11,...,19,2,21,22的顺序。
# All images must be of the same size

def write_videos_from_png_images(dir_input_images=None, dir_output_video=None, video_name=None, fps=25):
    if dir_input_images == None: 
        dir_input_images = os.getcwd() + '/'
    if dir_output_video == None:
        dir_output_video = os.getcwd() + '/'
    if video_name == None:
        video_name = str(int(time.time()))
    output_video_fullpath = dir_output_video +"/"+ video_name + ".mp4"  # 导出路径

    video = iio.get_writer(output_video_fullpath, format='FFMPEG', mode='I', fps=fps, codec='libx264', macro_block_size=1)

    filelist = os.listdir(dir_input_images)
    filelist_sort = natsorted(filelist)
    for item in filelist_sort:
        if item.endswith('.png'):  # 判断图片后缀是否是.png
            item = dir_input_images + item
            print(item)
            img = iio.imread(item) 
            video.append_data(img)  # 把图片写进视频
    video.close()
    return output_video_fullpath

## 可以指定:
## 输入图片的文件夹，默认是当前文件夹。
## 输出视频的文件夹，默认是当前文件夹。
## 输出视频的文件名，默认是当前时间作为文件名。
## 输出视频的帧率，默认是25.

# if __name__ == '__main__':
#     for CBP_idx in range(249):
#         dir_input_images = '/home/hcp/work/MFL_solo/figure/No_' + str(CBP_idx) + '/'
#         dir_output_video = '/home/hcp/work/MFL_solo/video/'
#         video_name = 'No_' + str(CBP_idx)
#         fps = 25
#         write_videos_from_png_images(dir_input_images=dir_input_images,\
#                                      dir_output_video=dir_output_video,\
#                                      video_name=video_name,\
#                                      fps=fps)
## 或者使用默认参数:
# write_videos_from_png_images()