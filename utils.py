import json
import datetime
import os
import re


def mkpath(path):
    if not os.path.exists(path):
        os.mkdir(path)


def print_now(return_flag=0):
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    now = now.strftime('%Y/%m/%d %H:%M:%S')
    if return_flag == 0:
        print(now)
    elif return_flag == 1:
        return now
    else:
        pass


def print_exp(args, return_flag=0):
    info = ''
    for k, v in vars(args).items():
        info += '{}:{}\n'.format(k, v)
    print('---------------experiment args---------------')
    print(info)
    print('---------------------------------------------')
    if return_flag == 0:
        return
    elif return_flag == 1:
        return info
    else:
        pass                                                               
    
def write_json(data, path):
    f = open(path, mode='a', encoding='utf-8')
    json.dump(data, f, indent=4, ensure_ascii=False)
    f.close()

def standardize(string):
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9^_]")
    string = res.sub("_", string)
    string = re.sub(r"(_)\1+","_", string).lower()
    while True:
        if len(string) == 0:
            return string
        if string[0] == "_":
            string = string[1:]
        else:
            break
    while True:
        if len(string) == 0:
            return string
        if string[-1] == "_":
            string = string[:-1]
        else:
            break
    if string[0].isdigit():
        string = "get_" + string
    return string

def change_name(name):
    change_list = ["from", "class", "return", "false", "true", "id", "and"]
    if name in change_list:
        name = "is_" + name
    return name

# def fix_seed(seed):
#     # random
#     random.seed(seed)
#     # Numpy
#     np.random.seed(seed)
#     # Pytorch
#     torch.manual_seed(seed)
#     torch.cuda.manual_seed_all(seed)
#     torch.backends.cudnn.deterministic = True
