import os
try:
    from PySide2 import *
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    import PySide2 as GuiCoreLib
    __GUICOREVERSION__ = "pyside2"
    print("use pyside2 as gui core")
except:
    from PySide2 import *
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    import PySide2 as GuiCoreLib
    __GUICOREVERSION__ = "pyside2"
    print("use pyside2 as gui core")

dirname = os.path.dirname(GuiCoreLib.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

import json
import re
import colorsys
import numpy as np
import pickle
import time

GUICOREVERSION = __GUICOREVERSION__
USER_CONFIG_DIR = ".user"
DUMP_HISTORY_DIR = ".history"


POINTCLOUD = "pointcloud"
IMAGE = "image"
BBOX3D = "bbox3d"
BBOX2D = "lane3d"
BBOX2D = "bbox2d"

INSTALL_MODE = 1
DEPLOY_MODE = 2
OTHER = 0

ERROR = 0
NORMAL = 1

info_color_list = [
    "#ff0000",
    "#00ff00",
]


KEYPRIVATE = "w09f*1l.kl~7tl-t0hmc-eizlsk3jo*+b72wjz*!"

# Regular expression for comments
comment_re = re.compile(
    '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
)
def parse_json(filename):
    # start = time.time()
    """ Parse a JSON file
        First remove comments and then use the json module package
        Comments look like :
            // ...
        or
            /*
            ...
            */
    """
    with open(filename, encoding="utf-8") as f:
        content = ''.join(f.readlines())
        ## Looking for comments
        match = comment_re.search(content)
        while match:
            # single line comment
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)
        # Return json file
    # print(filename, time.time()-start)
    return json.loads(content)


def check_setting_dims(val, dims):
    if not isinstance(dims, list):
        dims = [dims]
    if len(val) in dims:
        return True
    return False


def write_json(json_data,json_name):
    # Writing JSON data
    with open(json_name, 'w', encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii = False)


def serialize_data(data:dict, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

def deserialize_data(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data


def get_wall_time_str():
    return time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime())

def get_mac_address():
    import uuid
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac

def choose_file(ui_,info,ename,file_path = "./"):
    selected_file_path, _ = QFileDialog.getOpenFileName(ui_,
                                        info,
                                        file_path,
                                        ename)
    return selected_file_path

def choose_folder(ui_,info,file_path = "./"):
    directory = QFileDialog.getExistingDirectory(ui_, info, file_path)
    return directory

# 将列表递归创建成字典
def creat_dic_from_list(veh,key_value):
    dic = {}
    if veh == []:
        return key_value
    else:
        key = veh[0]
        veh.pop(0)
        dic[key] = creat_dic_from_list(veh,key_value)
    return dic

def unify_theta(theta, base=0):
    if theta + base > 0:
        return (theta + base) % (2*np.pi) - base
    else:
        if (theta + base) % (2*np.pi) != 0:
            return (theta + base) % (2*np.pi) - base
        else:
            return (theta + base) % (2*np.pi) - base + 2*np.pi

#  def cvt_pos_local_to_global(pos_local, pos_base):
    #  theta = pos_base[2]
    #  trans_mat = np.array([[np.sin(theta), np.cos(np.cos(theta))],
                          #  [-np.cos(theta), np.sin(theta)]])
    #  pos_global = trans_mat.dot(pos_local.transpose())
    #  pos_global.transpose()
    #  return pos_global + pos_base[:2]

def cvt_pos_local_to_global(pos_local, pos_base):
    theta = pos_base[2]
    trans_mat = np.array([[np.sin(theta), -np.cos(theta)],
                          [np.cos(theta), np.sin(theta)]])
    pos_global = pos_local.dot(trans_mat)
    return pos_global + pos_base[:2]


def cvt_pos_global_to_local(pos_global, pos_base):

    pos_local = pos_global - pos_base[:2]

    theta = pos_base[2]
    l_x = np.sin(theta) * pos_local[0] - np.cos(theta) * pos_local[1]
    l_y = np.cos(theta) * pos_local[0] + np.sin(theta) * pos_local[1]
    return np.array([l_x, l_y])


def cvt_theta_global_to_local(theta_global, pos_base):
    theta_local = np.pi / 2.0 + theta_global - pos_base[2]
    theta_local = unify_theta(theta_local, 0.0)
    return theta_local

def cvt_theta_local_to_global(theta_local, pos_base):
    theta_global = theta_local + pos_base[2] - np.pi * 0.5
    theta_global = unify_theta(theta_global, 0.0)
    return theta_global

def scale_lightness(rgb, scale_l):
    # convert rgb to hls
    h, l, s = colorsys.rgb_to_hls(*rgb)
    # manipulate h, l, s values and return as rgb
    return colorsys.hls_to_rgb(h, min(1, l * scale_l), s = s)

def rec_merge(d1, d2):
    for key, value in d2.items():
        if isinstance(value, dict):
            d1[key] = rec_merge(d1.get(key, {}), value)
        else:
            d1[key] = value
    return d1


def rec_exsit_merge(d1, d2):
    for key, value in d2.items():
        if key not in d1.keys(): continue
        if isinstance(value, dict):
            d1[key] = rec_exsit_merge(d1.get(key, {}), value)
        else:
            d1[key] = value
    return d1

def if_not_exist_create(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

if_not_exist_create(USER_CONFIG_DIR)
if_not_exist_create(DUMP_HISTORY_DIR)