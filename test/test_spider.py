import requests
from bs4 import BeautifulSoup
import logging
import re
import datetime
import urllib
from flask import current_app
import math
import pandas as pd

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,  # 设置最低日志级别为INFO
    format='%(asctime)s.%(msecs)03d %(levelname)s [%(name)s] %(message)s',  # 设置日志格式
    datefmt='%Y-%m-%d %H:%M:%S',  # 设置时间格式
    handlers=[
        logging.StreamHandler(),  # 只添加控制台输出handler
        logging.FileHandler('log/test_spider.log', encoding='utf-8')  # 添加文件处理器并指定编码为utf-8
    ]
)

# 获取logger实例
logger = logging.getLogger(__name__)

# 测试日志输出
logger.info("程序开始运行")
logger.error("这是一条测试错误信息")

def statistical(languageType):
    url = "https://api.fastbsv.com/v1/match/statistical"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,id;q=0.6",
        "Authorization": "tt_6106zvDrksdzzTkXbABHIwEiApcTu6z2.3066f7f1ff252e1881f38f6a3c6e58ab",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json;charset=UTF-8",
        "Dnt": "1",
        "Origin": "https://pc1.w.fbs6668.com",
        "Pragma": "no-cache",
        "Referer": "https://pc1.w.fbs6668.com/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }
    payload = {
    "languageType":languageType
    }
    max_retries = 10
    timeout = 10

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers = headers, json=payload, timeout=timeout)
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched statistical data on attempt {attempt + 1}")
                return response.json()

            logger.error(f"更新LiveMatchList数据失败, 状态码: {response.status_code}")
        
        except requests.Timeout:
            logger.error(f"请求LiveMatchList超时，第 {attempt + 1}/{max_retries} 次重试")
        
        except requests.RequestException as e:
            logger.error(f"请求LiveMatchList发生错误：{e}, 第 {attempt + 1}/{max_retries} 次重试")

    logger.error(f"更新Live数据失败，重试了 {max_retries} 次，仍未成功")
    return {}

def createTask():
    statisticalResponse = statistical('CMN')
    statisticalData = statisticalResponse.get('data', {})
    statisticalSport = statisticalData.get('sl', [])
    slList = []
    for i in statisticalSport:
        if i.get('des') not in ["今日","滚球","早盘"]:
            continue
        type= i.get('ty')
        des = i.get('des')
        for j in i.get('ssl'):
            slInfo = {}
            if j.get('c') == 0:
                continue
            slInfo['type'] = type
            slInfo['des'] = des
            slInfo['sportId'] = j.get('sid',None)
            slInfo['count'] = j.get('c',None)
            slInfo['pageTotal'] = math.ceil(j.get('c',None) / 50)
            slList.append(slInfo)
            print(slInfo)
    return slList

def getList(sportId,current,languageType,orderBy,type):
    url = "https://api.fastbsv.com/v1/match/getList"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,id;q=0.6",
        "Authorization": "tt_6106zvDrksdzzTkXbABHIwEiApcTu6z2.3066f7f1ff252e1881f38f6a3c6e58ab",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json;charset=UTF-8",
        "Dnt": "1",
        "Origin": "https://pc1.w.fbs6668.com",
        "Pragma": "no-cache",
        "Referer": "https://pc1.w.fbs6668.com/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }
    payload = {
    "sportId":sportId,
    "current": current,
    "isPc":True,
    "languageType":languageType,
    "orderBy":orderBy,
    "type":type
    }
    max_retries = 10
    timeout = 10

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers = headers, json=payload, timeout=timeout)
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched list sportId: {sportId} data on attempt {attempt + 1}")
                return response.json()

            logger.error(f"更新LiveMatchList数据失败, 状态码: {response.status_code}")
        
        except requests.Timeout:
            logger.error(f"请求LiveMatchList超时，第 {attempt + 1}/{max_retries} 次重试")
        
        except requests.RequestException as e:
            logger.error(f"请求LiveMatchList发生错误：{e}, 第 {attempt + 1}/{max_retries} 次重试")

    logger.error(f"更新Live数据失败，重试了 {max_retries} 次，仍未成功")
    return {}

def createMatch_info(matchList):
    match_info_list = []
    for match in matchList:
        match_info = {}
        match_info['match_time'] = match.get('bt', None)/1000
        match_info['regionName'] = match.get('lg', None).get('rnm', None)
        match_info['regionId'] = match.get('lg', None).get('rid', None)
        match_info['regionUrl'] = match.get('lg', None).get('rlg', None)
        match_info['leagueName'] = match.get('lg', None).get('na', None)
        match_info['leagueId'] = match.get('lg', None).get('id', None)
        match_info['leagueUrl'] = match.get('lg', None).get('lurl', None)
        match_info['match_id'] = match.get('id', None)
        match_info['match_name'] = match.get('nm', None)
        match_info['homeTeam'] = match.get('ts', None)[0]['na']
        match_info['homeTeamUrl'] = match.get('ts', None)[0]['lurl']
        match_info['homeTeamId'] = match.get('ts', None)[0]['id']
        match_info['awayTeam'] = match.get('ts', None)[1]['na']
        match_info['awayTeamUrl'] = match.get('ts', None)[1]['lurl']
        match_info['awayTeamId'] = match.get('ts', None)[1]['id']
        animation_list = match.get('as', [])
        # match_info['animation_list'] = animation_list
        if not animation_list:
            match_info_list.append(match_info)
            continue
        elif len(animation_list) == 1:
            match_info['animation1'] = None
            match_info['animation2'] = animation_list[0]
        elif len(animation_list) == 2:
            match_info['animation1'] = animation_list[0]
            match_info['animation2'] = animation_list[1]
        match_info['web'] = match.get('vs', None).get('web', None)
        match_info['flvHD'] = match.get('vs', None).get('flvHD', None)
        match_info['flvSD'] = match.get('vs', None).get('flvSD', None)
        match_info['m3u8HD'] = match.get('vs', None).get('m3u8HD', None)
        match_info['m3u8SD'] = match.get('vs', None).get('m3u8SD', None)
        match_info_list.append(match_info)
    logger.info(f"Created match info for {len(match_info_list)} matches")
    return match_info_list

def getStatscore(url,lang,eventId,config_id):
    url = f'https://widgets.statscore.com/api/ssr/render-widget/{config_id}'
    headers = {
        'authority': 'widgets.statscore.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,id;q=0.6',
        'cache-control': 'no-cache',
        'dnt': '1',
        'origin': 'https://animation.byanimxyz.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://animation.byanimxyz.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    inputData = {
        "language":lang,
        "eventId":str(eventId),
        "timezone":"-480"
    }
    input_data_json = str(inputData).replace("'", '"')
    encoded_data = urllib.parse.quote(input_data_json)
    full_url = f"{url}?inputData={encoded_data}"
    params = {'inputData': inputData}
    
    max_retries = 10
    timeout = 10
    
    for attempt in range(max_retries):
        try:
            response = requests.get(full_url, headers=headers, timeout=timeout)
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched Statscore data on attempt {attempt + 1}")
                return response.json()
        
            logger.error(f"更新Statscore数据失败, 状态码: {response.status_code}")
        
        except requests.Timeout:
            logger.error(f"请求Statscore超时，第 {attempt + 1}/{max_retries} 次重试")
        
        except requests.RequestException as e:
            logger.error(f"请求Statscore发生错误：{e}, 第 {attempt + 1}/{max_retries} 次重试")
    
    logger.error(f"更新Statscore数据失败，重试了 {max_retries} 次，仍未成功")
    return None

def getStatscore_id(matchInfo,lang):
    try:
        if matchInfo['animation1'] is None:
            logger.info(f"{matchInfo['match_name']}的animation1为空")
            statscore_id = 0
            return statscore_id
        startTime = datetime.datetime.now()
        match = re.search(r'matchId=(\d+)', matchInfo['animation1'])
        config = re.search(r'configId=([a-fA-F0-9]+)', matchInfo['animation1'])
        if not match or not config:
            logger.error(f"{matchInfo['match_name']} 正则匹配 match 或 config 失败: {matchInfo['animation_list']}")
            return None
        match_id = match.group(1)
        config_id = config.group(1)
        Statscore = getStatscore(matchInfo['animation1'],'en',match_id,config_id)
        key = f'event|eventId:{match_id}|language:{lang}|timezoneOffset:-480'
        statscore_id = Statscore.get('state', {}).get('fetchHistory', {}).get(key, {}).get('result', {}).get('season', {}).get('stage', {}).get('group', {}).get('event', {}).get('ls_id', None)
        endTime = datetime.datetime.now()
        logger.info(f"{matchInfo['match_name']}获取Statscore ID成功: {statscore_id} 用时{endTime - startTime}")
        return statscore_id
    except Exception as e:
        logger.error(f"{matchInfo['match_name']}获取Statscore ID失败: {e}")
        return None

# getList(sportId,current,languageType,orderBy,type):
def fetch_data(mode):
    matchList = []
    slList = createTask()
    slListMode = [i for i in slList if i.get('des') == mode]
    for sl in slListMode:
        for i in range(1,sl.get('pageTotal')+1):
            listResponse = getList(sl.get('sportId'),i,'CMN',1,sl.get('type'))
            listData = listResponse.get('data', {})
            listRecods = listData.get('records', [])
            matchList.extend(listRecods)
    match_info_list = createMatch_info(matchList)
    for match_info in match_info_list:
        statscore_id = getStatscore_id(match_info,'en')
        match_info['statscore_id'] = statscore_id
    return match_info_list

def get_token(clientId,password):
  url = 'https://wintokens-dev-tradeart-api.trading.io/api/Account/login'
  payload = {'clientId': clientId, 'password': password}
  response = requests.post(url, json=payload)
  if response.status_code == 200:
    print("token获取成功")
    data = response.text
    return data
  else:
    print(f"获取Token失败,状态码: {response.status_code}")
    print("响应内容:", response.text)
    return response.status_code

def getSchedule(startDate, sportId, token):
    url = f"https://wintokens-dev-tradeart-api.trading.io/api/events/schedule/v2"
    payload = {
        "startDate": startDate,
        "sportIds": [sportId]
    }
    headers = {'Authorization': f'Bearer {token}'}
    max_retries = 10
    timeout = 10
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched schedule data on attempt {attempt + 1}")
                return response.json()
        
            logger.error(f"Failed to fetch schedule data, status code: {response.status_code}")
        
        except requests.Timeout:
            logger.error(f"Request to fetch schedule data timed out, attempt {attempt + 1}/{max_retries}")
        
        except requests.RequestException as e:
            logger.error(f"Error occurred while fetching schedule data: {e}, attempt {attempt + 1}/{max_retries}")
    
    logger.error(f"Failed to fetch schedule data after {max_retries} attempts")
    return None

def get_metadata(token, eventId):
    url = f'https://wintokens-dev-tradeart-api.trading.io/api/Metadata/event/all/{eventId}'
    headers = {'Authorization': f'Bearer {token}'}
    max_retries = 10
    timeout = 10
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched metadata on attempt {attempt + 1}")
                return response.json()
        
            logger.error(f"Failed to fetch metadata, status code: {response.status_code}")
        
        except requests.Timeout:
            logger.error(f"Request to fetch metadata timed out, attempt {attempt + 1}/{max_retries}")
        
        except requests.RequestException as e:
            logger.error(f"Error occurred while fetching metadata: {e}, attempt {attempt + 1}/{max_retries}")
    
    logger.error(f"Failed to fetch metadata after {max_retries} attempts")
    return None

def getStatscoreId(datalist):
    for i in datalist:
        if i['dataType'] == 'StatsCoreIntegration':
            return i.get('data', None).get('Id', None)
    return None

def extract_number(text):
    match = re.search(r'm:(\d+)', text)
    if match:
        return match.group(1)
    return None

# df = pd.read_json(r'test/pwd.json')
# clientId = df['clientId'][0]
# password = df['password'][0]
# token = get_token(clientId, password)
# scheduleResponse = getSchedule('2024-12-27',1,token)
# eventIds = [i['id'] for i in scheduleResponse]
# logger.info(f"Found {len(eventIds)} events")
# metadataList = []
# for i in eventIds:
#     metadata = {}
#     metadata['eventId'] = i
#     try:
#         statscoreId = extract_number(getStatscoreId(get_metadata(token,i)))
#     except Exception as e:
#         logger.error(f"Error fetching Statscore ID for event {i}: {e}")
#         statscoreId = None
#     logger.info(f"Statscore ID for event {i}: {statscoreId}")
#     metadata['statscoreId'] = statscoreId
#     metadataList.append(metadata)
# for i in metadataList:
#     print(i)

def getMatchResultList(languageType):
    url = "https://api.fastbsv.com/v1/match/matchResultList"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,id;q=0.6",
        "Authorization": "tt_6106zvDrksdzzTkXbABHIwEiApcTu6z2.3066f7f1ff252e1881f38f6a3c6e58ab",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json;charset=UTF-8",
        "Dnt": "1",
        "Origin": "https://pc1.w.fbs6668.com",
        "Pragma": "no-cache",
        "Referer": "https://pc1.w.fbs6668.com/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }
    payload = {
    "sportId":1,
    # "current": current,
    "isPc":True,
    "languageType":languageType,
    # "orderBy":orderBy,
    "type":0
    }
    max_retries = 10
    timeout = 10

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers = headers, json=payload, timeout=timeout)
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched list sportId:  data on attempt {attempt + 1}")
                return response.json()

            logger.error(f"更新LiveMatchList数据失败, 状态码: {response.status_code}")
        
        except requests.Timeout:
            logger.error(f"请求LiveMatchList超时，第 {attempt + 1}/{max_retries} 次重试")
        
        except requests.RequestException as e:
            logger.error(f"请求LiveMatchList发生错误：{e}, 第 {attempt + 1}/{max_retries} 次重试")

    logger.error(f"更新Live数据失败，重试了 {max_retries} 次，仍未成功")
    return {}

def getfileStreamByType(languageType):
    url = "https://api.fastbsv.com/language/fileStreamByType"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,id;q=0.6",
        # "Authorization": "tt_6106zvDrksdzzTkXbABHIwEiApcTu6z2.3066f7f1ff252e1881f38f6a3c6e58ab",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json;charset=UTF-8",
        "Dnt": "1",
        "Origin": "https://pc1.w.fbs6668.com",
        "Pragma": "no-cache",
        "Referer": "https://pc1.w.fbs6668.com/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }
    payload = {
    "languageType":languageType
    }
    max_retries = 10
    timeout = 10

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers = headers, json=payload, timeout=timeout)
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched list sportId:  data on attempt {attempt + 1}")
                return response.json()

            logger.error(f"更新LiveMatchList数据失败, 状态码: {response.status_code}")
        
        except requests.Timeout:
            logger.error(f"请求LiveMatchList超时，第 {attempt + 1}/{max_retries} 次重试")
        
        except requests.RequestException as e:
            logger.error(f"请求LiveMatchList发生错误：{e}, 第 {attempt + 1}/{max_retries} 次重试")

    logger.error(f"更新Live数据失败，重试了 {max_retries} 次，仍未成功")
    return {}

# MatchResultListResponse = getMatchResultList('CMN')
# MatchResultListData = MatchResultListResponse.get('data', {})
# for k,v in MatchResultListResponse.items():
#     if k == 'data':
#         continue
#     print(k,v)

def fetch_basic_data(table):
    basicResponse = getfileStreamByType('CMN')
    basicData = basicResponse.get(table, {})
    basicList = []
    for i,j in basicData.items():
        for k,v in j.items():
            data = {}
            data['id'] = i
            data['lang'] = k
            data['name'] = v
            basicList.append(data)
    return basicList

# basicResponse = getfileStreamByType('CMN')
# for k,v in basicResponse.items():
#     for i,j in v.items():
#         for lang,name in j.items():
#             print(f"table:{k} id:{i} lang:{lang} name:{name}")

basicList = fetch_basic_data('Match Status')
for i in basicList:
    print(i)