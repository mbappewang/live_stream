import requests
from bs4 import BeautifulSoup
import logging
import re
import datetime
import urllib
from flask import current_app
import math
from datetime import datetime, timezone

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,  # 设置最低日志级别为INFO
    format='%(asctime)s.%(msecs)03d %(levelname)s [%(name)s] %(message)s',  # 设置日志格式
    datefmt='%Y-%m-%d %H:%M:%S',  # 设置时间格式
    handlers=[
        logging.StreamHandler(),  # 只添加控制台输出handler
        logging.FileHandler('log/spider.log', encoding='utf-8')  # 添加文件处理器并指定编码为utf-8
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
        "Authorization": current_app.config.get('AUTHORIZATION'),
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
    return slList

def getList(sportId,current,languageType,orderBy,type):
    url = "https://api.fastbsv.com/v1/match/getList"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,id;q=0.6",
        "Authorization": current_app.config.get('AUTHORIZATION'),
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
                logger.info(f"Successfully fetched list data on attempt {attempt + 1}")
                return response.json()

            logger.error(f"更新LiveMatchList数据失败, 状态码: {response.status_code}")
        
        except requests.Timeout:
            logger.error(f"请求LiveMatchList超时，第 {attempt + 1}/{max_retries} 次重试")
        
        except requests.RequestException as e:
            logger.error(f"请求LiveMatchList发生错误：{e}, 第 {attempt + 1}/{max_retries} 次重试")

    logger.error(f"更新Live数据失败，重试了 {max_retries} 次，仍未成功")
    return {}

def createMatch_info(matchList,lang):
    match_info_list = []
    for match in matchList:
        match_info = {}
        match_info['match_time_unix'] = match.get('bt', 0) / 1000
        match_info['start_time'] = datetime.fromtimestamp(match_info['match_time_unix'], tz=timezone.utc)
        match_info['nm'] = match.get('nm', '')
        if match.get('id', 0) == 0:
            continue
        match_info['lang'] = lang
        match_info['id'] = match.get('id')
        match_info['animation'] = match.get('as', '')
        match_info['fid'] = match.get('fid', None)
        match_info['fmt'] = match.get('fmt', None)
        match_info['lg'] = match.get('lg', '')
        match_info['mc'] = match.get('mc', '')
        match_info['mg'] = match.get('mg', '')
        match_info['ms'] = match.get('ms', None)
        match_info['ne'] = match.get('ne', None)
        match_info['nsg'] = match.get('nsg', '')
        match_info['pl'] = match.get('pl', None)
        match_info['sb'] = match.get('sb', '')
        match_info['sid'] = match.get('sid', None)
        match_info['smt'] = match.get('smt', None)
        match_info['tms'] = match.get('tms', None)
        match_info['tps'] = match.get('tps', '')
        match_info['ts'] = match.get('ts', '')
        match_info['ty'] = match.get('ty', None)
        match_info['vs'] = match.get('vs', '')
        match_info_list.append(match_info)
    logger.info(f"Created match info for {len(match_info_list)} matches")
    return match_info_list

def new_createMatch_info(matchList,lang):
    match_info_list = []
    for match in matchList:
        match_info = {}
        match_info['id'] = match.get('id', '')
        match_info['lang'] = lang
        match_info['match_time_unix'] = match.get('bt', 0)/1000
        match_info['start_time'] = datetime.fromtimestamp(match_info['match_time_unix'], tz=timezone.utc)
        match_info['match_name'] = match.get('nm', '')
        match_info['period_id'] = match.get('mc', {}).get('pe', '')
        match_info['status_id'] = match.get('ms', '')
        match_info['sportId'] = match.get('sid', '')
        match_info['regionId'] = match.get('lg', {}).get('rid', '')
        match_info['leagueId'] = match.get('lg', {}).get('id', '')
        match_info['league_order'] = match.get('lg', {}).get('or', '')
        match_info['is_hot'] = match.get('lg', {}).get('hot', '')
        match_info['hometeamId'] = match.get('ts', {})[0].get('id', '')
        match_info['hometeamUrl'] = match.get('ts', {})[0].get('lurl', '')
        match_info['hometeamName'] = match.get('ts', {})[0].get('na', '')
        match_info['awayteamId'] = match.get('ts', {})[1].get('id', '')
        match_info['awayteamUrl'] = match.get('ts', {})[1].get('lurl', '')
        match_info['awayteamName'] = match.get('ts', {})[1].get('na', '')
        match_info['match_stats'] = match.get('nsg', {})
        match_info['market'] = match.get('mg', {})
        if len(match.get('as', [])) == 0:
            match_info['animation1'] = ''
            match_info['animation2'] = ''
        elif len(match.get('as', [])) == 1:
            match_info['animation1'] = ''
            match_info['animation2'] = match.get('as', [])[0]
        else:
            match_info['animation1'] = match.get('as', [])[0]
            match_info['animation2'] = match.get('as', [])[1]
        match_info['web'] = match.get('vs', {}).get('web', '')
        match_info['flvHD'] = match.get('vs', {}).get('flvHD', '')
        match_info['flvSD'] = match.get('vs', {}).get('flvSD', '')
        match_info['m3u8HD'] = match.get('vs', {}).get('m3u8HD', '')
        match_info['m3u8SD'] = match.get('vs', {}).get('m3u8SD', '')
        match_info_list.append(match_info)
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

def getStatscore_id(id,animation1):
    try:
        startTime = datetime.now()
        match = re.search(r'matchId=(\d+)', animation1)
        config = re.search(r'configId=([a-fA-F0-9]+)', animation1)
        if not match or not config:
            logger.error(f"{id}正则匹配 match 或 config 失败: {animation1}")
            return None
        match_id = match.group(1)
        config_id = config.group(1)
        Statscore = getStatscore(animation1,'en',match_id,config_id)
        key = f'event|eventId:{match_id}|language:en|timezoneOffset:-480'
        statscore_id = Statscore.get('state', {}).get('fetchHistory', {}).get(key, {}).get('result', {}).get('season', {}).get('stage', {}).get('group', {}).get('event', {}).get('ls_id', None)
        endTime = datetime.now()
        logger.info(f"{id}获取Statscore ID成功: {statscore_id} 用时{endTime - startTime}")
        return statscore_id
    except Exception as e:
        logger.error(f"{id}获取Statscore ID失败: {e}")
        return None

# getList(sportId,current,languageType,orderBy,type):
def fetch_data(mode,language,lang):
    matchList = []
    slList = createTask()
    slListMode = [i for i in slList if i.get('des') == mode]
    for sl in slListMode:
        logger.info(f"Fetching data for {sl}")
        for i in range(1,sl.get('pageTotal')+1):
            listResponse = getList(sl.get('sportId'),i,language,1,sl.get('type'))
            listData = listResponse.get('data', {})
            listRecods = listData.get('records', [])
            matchList.extend(listRecods)
    match_info_list = createMatch_info(matchList,lang)
    # for match_info in match_info_list:
    #     match_info['status'] = mode
    #     statscore_id = getStatscore_id(match_info,'en')
    #     match_info['statscore_id'] = statscore_id
    return match_info_list

def getfileStreamByType(languageType):
    url = "https://api.fastbsv.com/language/fileStreamByType"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,id;q=0.6",
        "Authorization": current_app.config.get('AUTHORIZATION'),
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