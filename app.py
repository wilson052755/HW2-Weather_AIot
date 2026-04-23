import os
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="台灣天氣資訊網", layout="wide")

# 準備縣市座標字典
CITY_COORDS = {
    "臺北市": [25.0329694, 121.5654177],
    "新北市": [25.0112268, 121.461652],
    "桃園市": [24.9930777, 121.3009787],
    "臺中市": [24.1477358, 120.6736482],
    "臺南市": [22.9997281, 120.2270277],
    "高雄市": [22.6272784, 120.3014353],
    "基隆市": [25.1276033, 121.7391833],
    "新竹縣": [24.8197771, 121.0321307],
    "新竹市": [24.8138287, 120.9675798],
    "苗栗縣": [24.5601586, 120.821427],
    "彰化縣": [24.0815779, 120.5384666],
    "南投縣": [23.9030612, 120.6901844],
    "雲林縣": [23.7092033, 120.4313373],
    "嘉義縣": [23.4518428, 120.2554615],
    "嘉義市": [23.4800751, 120.4491113],
    "屏東縣": [22.6739989, 120.4870444],
    "宜蘭縣": [24.7308365, 121.7618037],
    "花蓮縣": [23.9769368, 121.6043681],
    "臺東縣": [22.7583328, 121.1444149],
    "澎湖縣": [23.5673685, 119.5695886],
    "金門縣": [24.4328574, 118.3228807],
    "連江縣": [26.1555546, 119.9324683]
}

def get_color(avg_temp):
    if avg_temp < 20:
        return 'blue'
    elif 20 <= avg_temp < 25:
        return 'green'
    elif 25 <= avg_temp <= 30:
        return 'yellow'
    else:
        return 'red'

def load_data():
    if not os.path.exists("weather_data.csv"):
        # 若未找到檔案，可能未執行 fetch_data.py
        import fetch_data
        fetch_data.fetch_weather_data()
        
    try:
        df = pd.read_csv("weather_data.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def main():
    st.title("台灣各縣市氣溫儀表板")
    
    df = load_data()
    if df.empty:
        st.warning("目前沒有氣象資料，請確認 API 狀態或重新執行程式。")
        return

    # 篩選功能：提供日期下拉選單
    dates = sorted(df['Date'].unique().tolist())
    selected_date = st.selectbox("選擇日期 (Date Selector)", dates)
    
    # 過濾資料
    filtered_df = df[df['Date'] == selected_date]
    
    # 如果同一天有多筆(例如不同時間段)，我們這裡為了顯示地圖取第一筆平均或其他邏輯
    # 這裡我們簡單針對每個縣市選出一筆來畫圖 (或者原始資料就是一天一筆)
    # 取每個縣市第一筆
    map_df = filtered_df.drop_duplicates(subset=['City'])

    # 佈局設計：採用左右分割介面
    col_left, col_right = st.columns([6, 4])

    with col_left:
        st.subheader("互動式地圖")
        st.markdown("低於 20°C：藍色 | 20-25°C：綠色 | 25-30°C：黃色 | 高於 30°C：紅色")
        
        # 建立台灣地圖
        m = folium.Map(location=[23.6978, 120.9605], zoom_start=7)
        
        for idx, row in map_df.iterrows():
            city = row['City']
            avg_temp = row['AvgT']
            min_temp = row['MinT']
            max_temp = row['MaxT']
            
            if city in CITY_COORDS:
                coords = CITY_COORDS[city]
                color = get_color(avg_temp)
                
                # 詳細資訊的彈出視窗
                popup_html = f"""
                <div style='width: 150px;'>
                    <b>{city}</b><br/>
                    日期: {selected_date}<br/>
                    平均溫度: {avg_temp:.1f}°C<br/>
                    最低溫度: {min_temp}°C<br/>
                    最高溫度: {max_temp}°C
                </div>
                """
                
                folium.CircleMarker(
                    location=coords,
                    radius=12,
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=city,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7
                ).add_to(m)
                
        # 顯示地圖
        st_folium(m, width=700, height=500, returned_objects=[])

    with col_right:
        st.subheader(f"{selected_date} 資料明細")
        
        # 設計要在右側呈現的表格
        display_df = filtered_df[['City', 'StartTime', 'EndTime', 'MinT', 'MaxT', 'AvgT']].copy()
        display_df.rename(columns={
            'City': '縣市',
            'StartTime': '開始時間',
            'EndTime': '結束時間',
            'MinT': '最低溫 (°C)',
            'MaxT': '最高溫 (°C)',
            'AvgT': '平均溫 (°C)'
        }, inplace=True)
        
        st.dataframe(display_df, use_container_width=True, height=500)

if __name__ == "__main__":
    main()
