# coding=utf-8
'''
@File    :   sign.py
@Time    :   2024/02/05 10:53:14
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   西山居技术中心服务，签名算法
'''
import hashlib
import hmac
import urllib.parse
import urllib.request


def tc_build_sign(secret, tonce, query, body):
    """
    签名算法。

    :param secret: 分配的密码
    :param tonce: Unix时间戳（整数秒）
    :param query: URL查询参数
    :param body: POST body
    :return: 签名
    """
    # 解析query参数
    params = urllib.parse.parse_qsl(query)
    sorted_params = sorted(params, key=lambda x: (x[0], x[1]))

    # 构造签名字符串
    buffer = bytearray()
    buffer += secret.encode()
    buffer += tonce.encode('utf-8')
    buffer += urllib.parse.urlencode(sorted_params).encode('utf-8')
    if body:
        if isinstance(body, str):
            body = body.encode('utf-8')
        buffer += body[:1048576]

    # 计算签名
    to_sign = bytes(buffer)
    print('to_sign: %s' % to_sign)
    h = hmac.new(secret.encode(), to_sign, hashlib.sha256)
    sign = h.hexdigest()

    return sign

