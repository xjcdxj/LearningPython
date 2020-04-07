import json

cid_api = 'https://api.bilibili.com/x/web-interface/view?aid=%s'

with open('cid_response', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(data['data']['durl'][0]['url'])

# https://api.bilibili.com/x/player/playurl?avid=89136699&cid=152244418&otype=json
# cid_response = {"code": 0, "message": "0", "ttl": 1,
#                 "data": {"from": "local", "result": "suee", "message": "", "quality": 64, "format": "flv720",
#                          "timelength": 469235, "accept_format": "flv720,flv480,mp4",
#                          "accept_description": ["高清 720P", "清晰 480P", "流畅 360P"], "accept_quality": [64, 32, 16],
#                          "video_codecid": 7, "seek_param": "start", "seek_type": "offset",
#                          "durl": [
#                         {"order": 1, "length": 469235, "size": 20597580, "ahead": "", "vhead": "",
#                          "url": "http://upos-sz-mirrorhw.bilivideo.com/upgcxcode/84/04/153880484/153880484-1-64.flv?e=ig8euxZM2rNcNbRV7zUVhoM1hwuBhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNo8g2ENvNo8i8o859r1qXg8xNEVE5XREto8GuFGv2U7SuxI72X6fTr859r1qXg8gNEVE5XREto8z5JZC2X2gkX5L5F1eTX1jkXlsTXHeux_f2o859IB_\u0026uipk=5\u0026nbs=1\u0026deadline=1582384264\u0026gen=playurl\u0026os=hwbv\u0026oi=2029184944\u0026trid=292ab73272ee44d0b98934fb98b91e4bu\u0026platform=pc\u0026upsig=649266531ae9c48d978c00213be847d7\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform\u0026mid=14372643",
#                          "backup_url": [
#                              "http://upos-sz-mirrorks3.bilivideo.com/upgcxcode/84/04/153880484/153880484-1-64.flv?e=ig8euxZM2rNcNbRV7zUVhoM1hwuBhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNo8g2ENvNo8i8o859r1qXg8xNEVE5XREto8GuFGv2U7SuxI72X6fTr859r1qXg8gNEVE5XREto8z5JZC2X2gkX5L5F1eTX1jkXlsTXHeux_f2o859IB_\u0026uipk=5\u0026nbs=1\u0026deadline=1582384264\u0026gen=playurl\u0026os=ks3bv\u0026oi=2029184944\u0026trid=292ab73272ee44d0b98934fb98b91e4bu\u0026platform=pc\u0026upsig=715b3c7847cf2566be3d20761a475a8b\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform\u0026mid=14372643"]}]}}
