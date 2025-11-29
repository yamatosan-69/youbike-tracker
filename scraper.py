import requests
import pandas as pd
import os
from datetime import datetime

# 設定 API 與 存檔名稱
URL = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
CSV_FILE = "youbike_data.csv"

def main():
    try:
        # 抓取資料
        response = requests.get(URL, timeout=10)
        response.encoding = 'utf-8'
        data = response.json()
        
        # 轉成 DataFrame
        df = pd.DataFrame(data)
        # 加入時間戳記 (UTC 時間，因為 GitHub 主機在國外)
        # 如果想要台灣時間，可以之後分析時再加 8 小時，或是現在用 pytz 處理
        # 這裡為了簡單，先存 UTC 時間
        df['collect_time'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # 讀取舊資料 (如果有的話) 並合併
        if os.path.exists(CSV_FILE):
            df_old = pd.read_csv(CSV_FILE)
            df_final = pd.concat([df_old, df], ignore_index=True)
        else:
            df_final = df

        # 存檔 (覆蓋舊檔，因為已經包含舊資料了)
        df_final.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')
        print(f"成功更新！目前累積 {len(df_final)} 筆資料。")

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()