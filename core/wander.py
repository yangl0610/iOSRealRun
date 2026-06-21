import asyncio
import math


async def wander(location_simulation, center_lat, center_lng, radius=30, dt=1.0, coord_type="gcj02", **_):
    """
    阿基米德螺旋：从中心向外展开到 radius，再收回中心，循环。
    """
    from utils import bd09Towgs84, gcj02Towgs84

    LAT_M = 111000.0
    LNG_M = LAT_M * math.cos(math.radians(center_lat))

    update_dt     = 0.3   # 位置更新间隔（秒），越小越流畅
    angular_speed = 1.2   # rad/s，一圈约 5 秒
    radial_speed  = 1.5   # m/s，30m 半径来回各 20 秒

    r = 0.0
    theta = 0.0
    expanding = True

    while True:
        # 更新半径
        delta_r = radial_speed * update_dt
        if expanding:
            r = min(r + delta_r, radius)
            if r >= radius:
                expanding = False
        else:
            r = max(r - delta_r, 0.0)
            if r <= 0.0:
                expanding = True

        theta += angular_speed * update_dt

        # 极坐标 → 经纬度偏移
        pos_x = r * math.cos(theta)
        pos_y = r * math.sin(theta)
        lat = center_lat + pos_y / LAT_M
        lng = center_lng + pos_x / LNG_M

        p = {"lat": lat, "lng": lng}
        if coord_type == "bd09":
            wgs = bd09Towgs84(p)
        elif coord_type == "gcj02":
            wgs = gcj02Towgs84(p)
        else:
            wgs = p

        await location_simulation.set(wgs["lat"], wgs["lng"])

        direction = "→外" if expanding else "←内"
        print(f"[螺旋] r={r:5.1f}m  θ={math.degrees(theta)%360:5.1f}°  {direction}")

        await asyncio.sleep(update_dt)
