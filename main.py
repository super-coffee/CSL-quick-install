import os
import requests
import hashlib
import re


OLDURL = 'https://drive.xiao-jin.xyz/littleskin/CustomSkinLoader_1.7.10-14.6a.jar'
LATESTURL = 'https://csl.littleservice.cn/mods/CustomSkinLoader_Forge-14.11.jar'
OLDNAME = 'CustomSkinLoader_1.7.10-14.6a.jar'
LATESTNAME = 'CustomSkinLoader_Forge-14.11.jar'
MODSPATH = './mods/'
CSLJSONPATH = os.path.abspath('./CustomSkinLoader/CustomSkinLoader.json')
LATESTJSON = 'https://drive.xiao-jin.xyz/littleskin/csl-latest/CustomSkinLoader.json'
OLDJSON = 'https://drive.xiao-jin.xyz/littleskin/csl-14.6a/CustomSkinLoader.json'
HASHDICT = 'https://drive.xiao-jin.xyz/littleskin/csl-hashs.json'
HASHLIST = \
    [
            'D02E754CC0A4973444D12EFB28CE159182DED8A8',
            'A846E1090E159B89F732508EF021006631BB2876',
            '5FEA57D6CF81B365173660EA2865B416DA16A203',
            '38F2C607953D36FF2EBCB68574BA0B69F988CD32',
            '88D5E32752D946BFA84CF7980325C2A826E0C4A0',
            '74703AC0F541924B6AEDBD8BD8432C752EE50154',
            '4533AE53F98EB8D05E0E3F3B411A92DE6ABB695D',
            '270C5EDF2B2A52F06DCCDFCED22C688DAC41826C',
            'C2FF14C9473BFB3B4C6E1592E69696C669114932',
            '3435C73FC653DEC8E66F94CB0CA21D5E957B472C',
            '7472ECEEBACBFE0C1EFBE3CF24F33C8905C7A644',
            '9AFFE23132155F94AA8207C10E8054107A1A0902',
            'F3C6BFA35F0D3DB98860E079158B039FAD76B130'
    ]


def load_hash_list():
    hash_list = list()
    try:
        hash_dict_least = requests.get(HASHDICT)
        hashs = hash_dict_least.json()
        for Hash in hashs:
            hash_list.append(Hash['hash'])
    except Exception as e:
        print(e)
        hash_list = HASHLIST
    return hash_list


def cal_sha1(path):
    with open(path, 'rb') as f:
        SHA_1 = hashlib.sha1()
        SHA_1.update(f.read())
        result = SHA_1.hexdigest()
    return result


def find(path, suffix):
    file_list = list()
    for filename in os.listdir(path):
        if filename.endswith(suffix):
            _path = path + filename
            name = filename.rstrip(suffix)
            file_list.append({
                'name': name,
                'path': _path
            })
    return file_list


def find_suspected_mods(mod_list):
    suspected_mod_list = list()
    for mod in mod_list:
        if re.search('c*s*l', mod['name'].lower()):
            suspected_mod_list.append(mod)
    return suspected_mod_list


def del_csl(_mod_list, _hash_list):
    for mod in _mod_list:
        for Hash in _hash_list:
            if cal_sha1(mod['path']) == Hash.lower():
                os.remove(mod['path'])
                break


def download_bin(url, path):
    req = requests.get(url)
    with open(path, 'wb') as bfile:
        bfile.write(req.content)


def download_text(url, path):
    req = requests.get(url)
    with open(path, 'w') as tfile:
        tfile.write(req.text)


def check_path():
    absPath = os.path.abspath('.').split(os.sep)
    if not absPath[-1] == '.minecraft':
        e = '请将此程序放至 .minecraft 目录下运行！'
        input(e)
        raise Exception(e)
        
    modsPath = os.path.abspath('./mods/')
    if not os.path.exists(modsPath):
        os.makedirs(modsPath)
    cslPath = os.path.abspath('./CustomSkinLoader/')
    if not os.path.exists(cslPath):
        os.makedirs(cslPath)


def main():
    check_path()
    print('正在查找 CustomSkinLoader')
    mod_list = find_suspected_mods(find("./mods/", ".jar"))
    if not mod_list:
        print('未找到 CustomSkinLoader')
    else:
        print('正在删除 CustomSkinLoader')
        hash_list = load_hash_list()
        del_csl(mod_list, hash_list)
        print('[ok] 删除完成')
    print('Minecraft 版本是否为 1.7.10 及以下？ [y]是 [n]不是')
    isOld = True if input('>>>') == 'y' else False
    fileName = OLDNAME if isOld else LATESTNAME
    jarUrl = OLDURL if isOld else LATESTURL
    print('正在下载 CustomSkinLoader')
    download_bin(jarUrl, os.path.abspath(MODSPATH+fileName))
    jsonUrl = OLDJSON if isOld else LATESTJSON
    print('正在下载 CustomSkinLoader 配置文件')
    download_bin(jsonUrl, CSLJSONPATH)
    input('[ok] 全部完成，按下回车退出。（请启动游戏查看效果）')


if __name__ == "__main__":
    main()
