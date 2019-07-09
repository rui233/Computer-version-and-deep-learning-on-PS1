import surprise
import lightfm

from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import io
import pandas as pickle
import pickle



from surprise import KNNBaseline, Reader
from surprise import Dataset


# 重建歌单id到歌单名的映射字典
id_name_dic = pickle.load(open("popular_playlist.pkl","rb"))
print("加载歌单id到歌单名的映射字典完成...")
# 重建歌单名到歌单id的映射字典
name_id_dic = {}
for playlist_id in id_name_dic:
    name_id_dic[id_name_dic[playlist_id]] = playlist_id
print("加载歌单名到歌单id的映射字典完成...")


file_path = os.path.expanduser('./popular_music_suprise_format.txt')
# 指定文件格式
reader = Reader(line_format='user item rating timestamp', sep=',')
# 从文件读取数据
music_data = Dataset.load_from_file(file_path, reader=reader)
# 计算歌曲和歌曲之间的相似度
print("构建数据集...")
trainset = music_data.build_full_trainset()
#sim_options = {'name': 'pearson_baseline', 'user_based': False}

id_name_dic.keys()[2]

print(id_name_dic[id_name_dic.keys()[2]])

trainset.n_items

trainset.n_users

print("开始训练模型...")
#sim_options = {'user_based': False}
#algo = KNNBaseline(sim_options=sim_options)
algo = KNNBaseline()
algo.train(trainset)

current_playlist = name_id_dic.keys()[39]
print("歌单名称", current_playlist)

# 取出近邻
# 映射名字到id
playlist_id = name_id_dic[current_playlist]
print("歌单id", playlist_id)
# 取出来对应的内部user id => to_inner_uid
playlist_inner_id = algo.trainset.to_inner_uid(playlist_id)
print("内部id", playlist_inner_id)

playlist_neighbors = algo.get_neighbors(playlist_inner_id, k=10)

# 把歌曲id转成歌曲名字
# to_raw_uid映射回去
playlist_neighbors = (algo.trainset.to_raw_uid(inner_id)
                       for inner_id in playlist_neighbors)
playlist_neighbors = (id_name_dic[playlist_id]
                       for playlist_id in playlist_neighbors)

print()
print("和歌单 《", current_playlist, "》 最接近的10个歌单为：\n")
for playlist in playlist_neighbors:
    print(playlist, algo.trainset.to_inner_uid(name_id_dic[playlist]))

