# config.py
import os
APP_NAME = "素食餐廳查找器"
DATABASE_PATH = "restaurants.db"
OFFLINE_MAP_PATH = "offline_maps"
MAP_TILE_SERVER = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
DEFAULT_CENTER = (25.0330, 121.5654)  # 台北市中心
# main.py
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import sqlite3
from datetime import datetime
import hashlib
import json
import requests
from pathlib import Path
import threading
from math import radians, sin, cos, sqrt, atan2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
class VeganFinderApp(toga.App):
    def __init__(self):
        super().__init__()
        self.title = APP_NAME
        self.db = DatabaseManager(DATABASE_PATH)
        self.map_manager = OfflineMapManager(OFFLINE_MAP_PATH)
        self.current_location = None
        self.current_user = None
        self.route_manager = RouteManager()
    def startup(self):
        """應用程序啟動入口"""
        if not self.current_user:
            self.show_login_window()
        else:
            self.show_main_window()
    def show_login_window(self):
        """顯示登入窗口"""
        self.login_window = LoginWindow(self)
        self.login_window.show()
    def show_main_window(self):
        """顯示主窗口"""
        self.main_window = MainWindow(self)
        self.main_window.show()
# auth.py
class LoginWindow:
    def __init__(self, app):
        self.app = app
        self.window = toga.MainWindow(title="登入")
        self.build()
    def build(self):
        """建立登入界面"""
        box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        # 登入表單
        self.username_input = toga.TextInput(placeholder='用戶名')
        self.password_input = toga.PasswordInput(placeholder='密碼')
        login_button = toga.Button('登入', on_press=self.login)
        register_button = toga.Button('註冊', on_press=self.show_register)
        box.add(self.username_input)
        box.add(self.password_input)
        box.add(login_button)
        box.add(register_button)
        self.window.content = box
    def login(self, widget):
        """處理登入邏輯"""
        username = self.username_input.value
        password = self.password_input.value
        # 密碼加密
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = self.app.db.verify_user(username, hashed_password)
        if user:
            self.app.current_user = user
            self.window.close()
            self.app.show_main_window()
        else:
            self.window.error_dialog('錯誤', '用戶名或密碼錯誤')
    def show_register(self, widget):
        """顯示註冊窗口"""
        RegisterWindow(self.app).show()
# main_window.py
class MainWindow:
    def __init__(self, app):
        self.app = app
        self.window = toga.MainWindow(title=APP_NAME)
        self.build()
    def build(self):
        """建立主界面"""
        main_box = toga.Box(style=Pack(direction=COLUMN))
        # 添加功能區域
        main_box.add(self.build_search_box())
        main_box.add(self.build_filter_box())
        main_box.add(self.build_map_view())
        main_box.add(self.build_restaurant_list())
        self.window.content = main_box
    def build_search_box(self):
        """建立搜索區域"""Box, TextInput, Button, Selection, 
        box = toga.Box(style=Pack(direction=ROW, padding=5))
        self.search_input = toga.TextInput(placeholder='搜索餐廳')
        search_button = toga.Button('搜索', on_press=self.search)
        recommend_button = toga.Button('推薦', on_press=self.show_recommendations)
        box.add(self.search_input)
        box.add(search_button)
        box.add(recommend_button)
        return box
    def build_filter_box(self):
        """建立過濾選項"""
        box = toga.Box(style=Pack(direction=ROW, padding=5))
        # 價格範圍
        self.price_filter = toga.Selection(items=['全部價格', '$', '$$', '$$$'])
        # 距離範圍
        self.distance_filter = toga.Selection(items=['全部距離', '1公里內', '3公里內', '5公里內'])
        # 評分範圍
        self.rating_filter = toga.Selection(items=['全部評分', '4星以上', '3星以上'])
        box.add(self.price_filter)
        box.add(self.distance_filter)
        box.add(self.rating_filter)
        return box
# map_manager.py
class OfflineMapManager:
    def __init__(self, map_dir):
        self.map_dir = Path(map_dir)
        self.map_dir.mkdir(exist_ok=True)
    def download_map_tiles(self, bbox, zoom_levels):
        """下載指定區域的地圖瓦片"""
        for zoom in zoom_levels:
            for x, y in self._get_tile_coordinates(bbox, zoom):
                self._download_tile(zoom, x, y)
    def _get_tile_coordinates(self, bbox, zoom):
        """獲取指定範圍內的瓦片坐標"""
        min_lat, min_lon, max_lat, max_lon = bbox
        # 計算瓦片範圍
        min_x, min_y = self._deg2num(max_lat, min_lon, zoom)
        max_x, max_y = self._deg2num(min_lat, max_lon, zoom)
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                yield (x, y\)
    def _download_tile(self, zoom, x, y):
        """下載單個地圖瓦片"""
        tile_path = self.map_dir / f"{zoom}/{x}/{y}.png"
        if tile_path.exists():
            return
        url = MAP_TILE_SERVER.format(z=zoom, x=x, y=y)
        response = requests.get(url)
        if response.status_code == 200:
            tile_path.parent.mkdir(parents=True, exist_ok=True)
            tile_path.write_bytes(response.content)
# route_manager.py
class RouteManager:
    def __init__(self):
        self.osrm_server = "http://router.project-osrm.org"
    def get_route(self, start_point, end_point, transport_mode='foot'):
        """獲取路線規劃"""
        url = (f"{self.osrm_server}/route/v1/{transport_mode}/"
               f"{start_point[1]},{start_point[0]};"
               f"{end_point[1]},{end_point[0]}"
               "?overview=full&geometries=geojson")
        try:
            response = requests.get(url)
            data = response.json()
            if data['code'] == 'Ok':
                route = data['routes'][0]
                return {'distance':route['distance'], 'duration':route['duration'], 'geometry':route['geometry']}
        except:
            return None
        return None
class RestaurantRecommender: # recommendation.py
    def __init__(self, db):
        self.db = db
    def get_recommendations(self, user_id):
        #""基於協同過濾的餐廳推薦""" # 獲取用戶-餐廳評分矩陣
        ratings = self.db.get_all_ratings()
        # 轉換為矩陣格式
        users = list(set(r[0] for r in ratings))
        restaurants = list(set(r[1] for r in ratings))
        # 建立評分矩陣
        rating_matrix = np.zeros((len(users), len(restaurants)))
        user_idx = {u: ndx for ndx, u in enumerate(users)}
        rest_idx = {r: ndx for ndx, r in enumerate(restaurants)}
        for user_id, rest_id, rating in ratings:
            i = user_idx[user_id]
            j = rest_idx[rest_id]
            rating_matrix[i, j] = rating
        # 計算相似度
        user_similarities = cosine_similarity(rating_matrix)
        # 獲取目標用戶的相似用戶
        target_idx = user_idx[user_id]
        similar_users = np.argsort(user_similarities[target_idx])[-5:]
        # 獲取推薦餐廳
        recommendations = []
        user_ratings = rating_matrix[target_idx]
        for rest_id, rest_idx in rest_idx.items():
            if not user_ratings[rest_idx]:  # == 0 用戶未評價過
                weighted_rating = 0
                weight_sum = 0
                for similar_idx in similar_users:
                    sim_score = user_similarities[target_idx][similar_idx]
                    rating = rating_matrix[similar_idx][rest_idx]
                    if rating > 0:
                        weighted_rating += sim_score * rating
                        weight_sum += sim_score
                if weight_sum > 0:
                    recommendations.append((rest_id, weighted_rating/weight_sum))
        # 排序並返回推薦結果
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in recommendations[:10]]
# database.py
class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    def create_tables(self):
        """創建數據表"""
        cursor = self.conn.cursor()
        # 用戶表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """)
        # 用戶喜好表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (user_id INTEGER, preference_type TEXT, preference_value TEXT, FOREIGN KEY (user_id) REFERENCES users (id))
        """)
        # 搜索歷史表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        self.conn.commit()
    def verify_user(self, username, password_hash): #驗證用戶登入
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT id, username FROM users WHERE username = '{username}' AND password = '{password_hash}';")
        return cursor.fetchone()
    def create_user(self, username, password_hash):
        """創建新用戶"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password_hash}');")
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
def main():
    return VeganFinderApp()
if __name__ == '__main__':
    main().main_loop()
