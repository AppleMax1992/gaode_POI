import requests
import pandas as pd
# 这里的 AK 是高德样例中内置的 key. 不需要再申请key.
AK = '6e79f6d236e295632f21b385e363b6e8'


def get_boundary_from_gaode_demo(level: str, keyword: str) -> dict:
    """
    功能: 获取某省市区的边界 gis 坐标

    level: 行政级别 district 区、 city 市、 province 省
    keywords: 某个具体的省, 市, 区

    return: 返回网页响应.
    """

    # 模拟浏览器
    headers = {
        'Referer': 'https://lbs.amap.com/',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'accept-encoding': 'gzip, deflate, br'
    }

    # 设置参数
    params = (
        # 获取边界不需要返回下级行政区
        ('subdistrict', '0'),
        # 返回行政区边界坐标组等具体信息
        ('extensions', 'all'),
        # 行政级别 district、city、province
        ('level', level),
        # AK, 这里是高德样例提供的 key
        ('key', AK),
        ('s', 'rsv3'),
        # 返回结果为json格式
        ('output', 'json'),
        # 检索的行政区划名称
        ('keywords', keyword),
        ('platform', 'JS'),
        ('logversion', '2.0'),
        ('appname', 'https://lbs.amap.com/demo/javascript-api/example/district-search/draw-district-boundaries'),
        ('sdkversion', '1.4.15'),
    )

    # 发起请求,获得响应.
    response = requests.get('https://restapi.amap.com/v3/config/district', headers=headers, params=params)

    # 返回响应结果.
    res = response.json()
    boundary = res['districts'][0]['polyline']

    return boundary


if __name__ == '__main__':
    
    # 参数1 : 行政级别 district 区、 city 市、 province 省
    level = 'district'
    
    # 参数2 : 待查询边界的行政区
    keyword = '上海市'

    # 调用函数 get_boundary_from_gaode_demo() 获取边界经纬度
    boundary = get_boundary_from_gaode_demo(level, keyword)

    # 查看边界有多少个经纬度点组成
    print(len(boundary))
    boundary_list = boundary.split(";")
    jingdu = []
    weidu = []
    for item in boundary_list:
        sub_item = item.split(",")
        print(sub_item)
        jingdu.append(sub_item[0])
        weidu.append(sub_item[1])
    csvpd =  pd.DataFrame({'经度':jingdu,'纬度':weidu})
    csvpd.to_csv('./amap_boundary.csv',index=None,encoding='utf_8_sig')