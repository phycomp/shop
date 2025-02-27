from stUtil import rndrCode
from folium import Map as flmMap, Marker as flmMarker, Icon as flmIcon
from streamlit_folium import folium_static
#使用 OSMnx 獲取北台灣素食餐廳的地理位置信息。素食餐廳通常會標記爲 amenity=restaurant，并可能帶有額外的標簽如 diet:vegetarian=yes。
from osmnx import geometries_from_place
from streamlit import title as stTitle, dataframe

# 定義北台灣的範圍，例如：台北市、新北市、基隆市
north_taiwan = 'Taipei, Taiwan'

# 查詢 OSM 中的素食餐廳 POI 數據
tags = {'amenity': 'restaurant', 'diet:vegetarian': 'yes'}
vegePOI = geometries_from_place(north_taiwan, tags)

vegePOI
#dataframe() https://github.com/yichun-hub/Spatial-analysis_geopandas/tree/main
#rndrCode(vegePOI.head())    # 打印前幾行 POI 數據
#3. 使用 folium 在 Streamlit 中顯示地圖
# 創建地圖中心點 (例如台北101坐標)
台北101 = [25.033964, 121.564468]

#世貿 = flmMap(location=[25.03949721583935, 121.55957402734612], tiles='openstreetmap', zoom_start=15)

m=flmMap(location=台北101, zoom_start=12) # 創建 Folium 地圖

for idx, row in vegePOI.iterrows(): # 在地圖上添加素食餐廳 POI
    coords = row.geometry.centroid.y, row.geometry.centroid.x # 從 POI 數據中提取坐標
    flmMarker( location=coords, popup=row['name'] if 'name' in row else '素食餐廳', icon=flmIcon(color='green', icon='leaf')).add_to(m) # 添加標記

stTitle('北台灣素食餐廳地圖') # 在 Streamlit 應用中顯示地圖
folium_static(m)
#4. 優化與添加功能
#你可以爲用戶提供更多功能，例如：
#    • 過濾功能：允許用戶根據區域、評分等條件篩選餐廳。
#    • 餐廳信息展示：用戶點擊標記時顯示更多詳細信息（例如餐廳地址、營業時間、評分等）。
#    • 動態交互：例如讓用戶選擇不同的北台灣城市或區域來動態顯示不同區域的素食餐廳。
#完整 Streamlit 應用示例
#import streamlit as st
#import folium
#from streamlit_folium import folium_static
#import osmnx as ox

# 定義北台灣的範圍
#north_taiwan = 'Taipei, Taiwan'

# 獲取北台灣素食餐廳 POI 數據
#tags = {'amenity': 'restaurant', 'diet:vegetarian': 'yes'}
#vege_pois = ox.geometries_from_place(north_taiwan, tags)

# Streamlit 應用
#st.title('北台灣素食餐廳地圖')

# 地圖中心點
#map_center = [25.033964, 121.564468]  # 台北101

# 創建 Folium 地圖
#m = folium.Map(location=map_center, zoom_start=12)

# 在地圖上添加素食餐廳 POI 標記

# 顯示地圖
#folium_static(m)
