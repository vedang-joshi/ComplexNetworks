# filepaths
import os
import moviepy.video.io.ImageSequenceClip
import re
image_folder='/Users/vedangjoshi/PycharmProjects/Complex_Networks_Presentation'
fps=10

image_files = [os.path.join(image_folder,img)
               for img in os.listdir(image_folder)
               if img.endswith(".png")]
image_files = sorted(image_files, key=lambda x:float(re.findall("(\d+)",x)[0]))
print(image_files)
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
clip.write_videofile('convergence_15_nodes_30_edges_133_iter.mp4')