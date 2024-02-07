# 先请求https://api.bilibili.com/x/native_page/dynamic/index?page_id=169153&jsonp=jsonp，每页秒评所在地址
# data-cards-[2]-item-[n]-itemid
# 请求https://api.bilibili.com/x/native_page/dynamic/inline?page_id={itemid}
# data-cards-[3]~[n]前三个为页头-item-item-url-一串av号和comment_root_id
# https://api.bilibili.com/x/web-interface/view?aid={av号}
# data-bvid
# https://api.bilibili.com/x/v2/reply/wbi/main?oid=数字&type=1&mode=3&pagination_str=%7B%22offset%22:%22%22%7D&plat=1&seek_rpid=&web_location=1315875&w_rid=74ec8ad746ead90dca2c6a8888879887&wts=1707284900
# rpid=comment_root_id

from json import loads
from requests import exceptions, get, post
from typing import Any, Dict, List, Optional, Tuple

HEADERS: Dict[str, str] = {  # 设置请求头
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
}
def write(text: Any) -> None:
    with open("F:\\qwq.txt", "a+", encoding="utf-8") as file:
        file.write(str(text) + "\n")

def send_request(
    url: str,
    method: str,
    data: Optional[Dict[str, Any]] = None,
    headers: Dict[str, str] = HEADERS,
) -> Optional[str]:
    try:
        
        response = (
            get(url, params=data, data=data, headers=headers)
            if method.upper() == "GET"
            else post(url, data=data, headers=headers)
            if method.upper() == "POST"
            else None
        )
        

        response.raise_for_status()

    except exceptions.HTTPError as err:
        print("HTTP错误:", err)
    except exceptions.ConnectionError as err:
        print("连接错误:", err)
        exit()
    except exceptions.Timeout as err:
        print("超时错误:", err)
    except exceptions.RequestException as err:
        print("其他错误:", err)
    else:
        return response
    return None

page_list = loads(send_request("https://api.bilibili.com/x/native_page/dynamic/index?page_id=169153", "get").text)["data"]["cards"][2]["item"][0]["item"]
title_list = [page_list[i]["title"] for i in range(len(page_list))]
item_id_list = [page_list[i]["item_id"] for i in range(len(page_list))]
for i in range(len(item_id_list)):
    comment_id_list = loads(send_request("https://api.bilibili.com/x/native_page/dynamic/inline?page_id={}".format(item_id_list[i]), "get").text)["data"]["cards"]
    write(title_list[i])
    url_old = comment_num = 0
    for i in range(3,len(comment_id_list)):
        try:
            url = comment_id_list[i]["item"][0]["item"][0]["uri"]
            if not url_old == url:
                url_old = url
                comment_id = url.split("=")[-1]
                start_index = url.find("video/") + len("video/")  # 找到"video/"的位置，并加上它的长度
                end_index = url.find("?")  # 找到"?"的位置
                video_id = url[start_index:end_index]

                comments_detail = loads(send_request("https://api.bilibili.com/x/v2/reply/main?oid={}&type=1".format(video_id),"get").text)
                #旧的api
                for i in range(len(comments_detail["data"]["replies"])):
                    if str(comments_detail["data"]["replies"][i]["rpid"]) == comment_id:
                        comment = comments_detail["data"]["replies"][i]["content"]["message"]
                        if not comment :
                            break
                        comment_num += 1
                        write(comment_num)
                        write(comment)
                        print(comment_num)
                        print(comment)
                        break
        except:
            pass
