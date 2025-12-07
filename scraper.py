import requests
import pandas as pd
import os
from datetime import datetime, timezone, timedelta

# 設定 API 網址
URL = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

# 設定要存放資料的資料夾名稱
DATA_FOLDER = "data"

def main():
    try:
        # 1. 抓取資料
        response = requests.get(URL, timeout=10)
        response.encoding = 'utf-8' # 修正中文亂碼
        data = response.json()
        
        # 2. 處理時間 (轉為台灣時間 UTC+8)
        # 這樣換日才會是在台灣時間的半夜 12 點
        tw_time = datetime.now(timezone.utc) + timedelta(hours=8)
        current_date = tw_time.strftime("%Y-%m-%d")
        current_time_str = tw_time.strftime("%Y-%m-%d %H:%M:%S")

        # 3. 檢查資料夾是否存在，不存在就建立
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)
            print(f"已建立資料夾: {DATA_FOLDER}")

        # 4. 設定包含路徑的完整檔名 (例如: data/youbike_2025-12-07.csv)
        csv_filename = f"{DATA_FOLDER}/youbike_{current_date}.csv"

        # 5. 轉為 DataFrame 並加入時間欄位
        df = pd.DataFrame(data)
        df['collect_time'] = current_time_str

        # 6. 存檔 (針對「今天」的檔案做 Append)
        if os.path.exists(csv_filename):
            df_old = pd.read_csv(csv_filename)
            df_final = pd.concat([df_old, df], ignore_index=True)
        else:
            df_final = df

        # 存檔時指定路徑
        df_final.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"成功更新檔案: {csv_filename}, 目前筆數: {len(df_final)}")

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()
