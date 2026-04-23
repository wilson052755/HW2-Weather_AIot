import os
import ssl
import json
import requests
import pandas as pd
from datetime import datetime

# Disable SSL warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==============================================================================
# 請在這裡填入您的氣象資料開放平臺授權碼 (API Key)
# ==============================================================================
CWA_API_KEY = "CWA-DD7439A1-A511-4D46-882C-068575FD9C55"

def fetch_weather_data():
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={CWA_API_KEY}"
    
    print("正在從氣象署 (CWA) API 取得資料...")
    try:
        # 處理 SSL 憑證驗證問題機制
        response = requests.get(url, verify=False)
        response.raise_for_status()
        data = response.json()
        
        if data.get("success") == "true" or data.get("success") == True:
            records = data.get("records", {}).get("location", [])
        else:
            print("API 回應失敗。請檢查您的 API Key 授權碼。")
            return
            
        parsed_data = []
        
        for loc in records:
            location_name = loc.get("locationName")
            weathers = loc.get("weatherElement", [])
            
            # Find MinT and MaxT
            min_t_data = []
            max_t_data = []
            
            for elem in weathers:
                if elem.get("elementName") == "MinT":
                    min_t_data = elem.get("time", [])
                elif elem.get("elementName") == "MaxT":
                    max_t_data = elem.get("time", [])
                    
            # 假設 min_t_data 和 max_t_data 長度與時段相同
            for i in range(len(min_t_data)):
                start_time = min_t_data[i].get("startTime")
                end_time = min_t_data[i].get("endTime")
                min_t = float(min_t_data[i].get("parameter", {}).get("parameterName", 0))
                max_t = float(max_t_data[i].get("parameter", {}).get("parameterName", 0))
                
                avg_t = (min_t + max_t) / 2.0
                
                # 簡化日期方便選擇
                date_str = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                
                parsed_data.append({
                    "Date": date_str,
                    "StartTime": start_time,
                    "EndTime": end_time,
                    "City": location_name,
                    "MinT": min_t,
                    "MaxT": max_t,
                    "AvgT": avg_t
                })
                
        df = pd.DataFrame(parsed_data)
        df.to_csv("weather_data.csv", index=False, encoding="utf-8-sig")
        print(f"成功將 {len(df)} 筆資料儲存至 weather_data.csv")
        return True
        
    except Exception as e:
        print(f"取得資料時傳回錯誤: {e}")
        print("由於可能缺少有效的 API Key，我們將產生一份模擬資料以便測試網頁應用程式。")
        create_mock_data()
        return False

def create_mock_data():
    cities = [
        "臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市", "基隆市",
        "新竹縣", "新竹市", "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣",
        "嘉義市", "屏東縣", "宜蘭縣", "花蓮縣", "臺東縣", "澎湖縣", "金門縣", "連江縣"
    ]
    import random
    from datetime import timedelta
    
    today = datetime.now()
    dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(3)]
    
    mock_data = []
    for d in dates:
        for c in cities:
            min_t = random.randint(15, 28)
            # 以確保最高溫大於等於最低溫
            max_t = random.randint(min_t + 2, 35)
            avg_t = (min_t + max_t) / 2.0
            mock_data.append({
                "Date": d,
                "StartTime": f"{d} 06:00:00",
                "EndTime": f"{d} 18:00:00",
                "City": c,
                "MinT": min_t,
                "MaxT": max_t,
                "AvgT": avg_t
            })
            
    df = pd.DataFrame(mock_data)
    df.to_csv("weather_data.csv", index=False, encoding="utf-8-sig")
    print("已產生模擬資料並儲存至 weather_data.csv")

if __name__ == "__main__":
    fetch_weather_data()
