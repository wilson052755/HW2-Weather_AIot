# HW2-Weather_AIot (台灣氣象視覺化儀表板)

這是一個基於 Streamlit 與 Folium 建立的互動式台灣氣象視覺化儀表板專案，負責從「中央氣象署 (CWA)」自動抓取各縣市氣象資料，並將資料轉換為網頁地圖顯示。

## 專案功能

- **自動化資料擷取**：透過 `requests` 從 CWA API 獲取最新的「36小時天氣預報」資料，並避開 SSL 憑證問題。自動計算各縣市的預測最高/最低及平均氣溫。
- **左側 - 互動式地圖**：利用 `folium` 生成台灣地圖，根據平均溫度為各縣市加上「高低溫分色圓點」(藍、綠、黃、紅)。點擊圓點可檢視更詳細的溫度數值。
- **右側 - 數據表格**：列出特定日期之所有縣市的天氣圖表，並支援日期動態下拉過濾。
- **防呆預備機制**：未來三天的隨機氣候資料模擬功能 (若 API Key 未提供或無效)。

## 系統需求

- Python 3.9+ 
- 以下 Python 套件：
  - `requests`
  - `pandas`
  - `streamlit`
  - `folium`
  - `streamlit-folium`

## 安裝與執行

1. **建立並啟動虛擬環境 (建議)**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **安裝所需套件**
   ```powershell
   pip install requests pandas streamlit folium streamlit-folium
   ```

3. **取得最新的天氣資料**
   請在 `fetch_data.py` 將 `CWA_API_KEY` 替換為您的中央氣象署授權碼，然後執行：
   ```powershell
   python fetch_data.py
   ```

4. **啟動網頁儀表板**
   ```powershell
   streamlit run app.py
   ```
   瀏覽器將會自動跳轉至儀表板畫面。

## 授權
This project is for educational purposes.
