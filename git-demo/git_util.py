# coding=utf-8
'''
@File    :   git.py
@Time    :   2024/02/29 11:48:47
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   用GitPython库操作git项目
'''
import pathlib
import shutil
import zipfile
import os
from typing import List
from urllib.parse import urlparse, urlunparse

import git


def git_clone_to_path(path: str, git_url: str, token: str = None):
    """
    在path目录git clone项目
    @param auth: 令牌字符串 使用令牌时只允许使用https地址
    """
    # Parse the URL
    parsed_url = urlparse(git_url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        raise ValueError("Invalid URL")
    path = pathlib.Path(path)
    if token:
        netloc = f"oauth2:{token}@{parsed_url.netloc}"
        repo_url = urlunparse((parsed_url.scheme, netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))
    else:
        repo_url = git_url
    
    print(repo_url)
    repo = git.Repo.clone_from(repo_url, path)

def zipdir(path: str, ziph: zipfile.ZipFile, exclude: List[str]):
    """
    压缩
    @param path: 需要被压缩的目标文件夹路径
    @param ziph: 压缩文件句柄
    @param exclude: 排除的文件路径
    """
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            if any(ex in full_path for ex in exclude):
                continue
            ziph.write(full_path, arcname=full_path.replace(path + '/', ''))


if __name__ == "__main__":
    temporary_path = "./data/"

    temporary_path = pathlib.Path(temporary_path)
    git_clone_to_path(temporary_path.__str__(), "https://ngitlab.testplus.cn/xiezhihong/tgame-config-check.git", "glpat-e52ZQ6EWA5XHXcDT7tG8")
    exclude = [
        temporary_path.joinpath(".git/").__str__(),
        temporary_path.joinpath("tgame-localization-check.exe").__str__(),
    ]  # folders to exclude
    zipf = zipfile.ZipFile('data.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(temporary_path.__str__(), zipf, exclude)
    zipf.close()
