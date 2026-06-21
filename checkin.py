"""
虚拟定位签到模式
配置从 checkin.json 读取，在指定坐标点附近随机漂移。
"""
import asyncio
import json
import os
import sys

from pymobiledevice3.remote.remote_service_discovery import RemoteServiceDiscoveryService
from pymobiledevice3.services.dvt.instruments.location_simulation import LocationSimulation
from pymobiledevice3.services.dvt.instruments.dvt_provider import DvtProvider

from core.wander import wander

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "checkin.json")


def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"[错误] 找不到配置文件: {CONFIG_FILE}")
        sys.exit(1)
    with open(CONFIG_FILE, encoding="utf-8") as f:
        cfg = json.load(f)

    required = ("host", "port", "lat", "lng")
    for key in required:
        if key not in cfg:
            print(f"[错误] checkin.json 缺少字段: {key}")
            sys.exit(1)

    return {
        "host":        str(cfg["host"]),
        "port":        int(cfg["port"]),
        "lat":         float(cfg["lat"]),
        "lng":         float(cfg["lng"]),
        "radius":      float(cfg.get("radius", 30)),
        "dt":          float(cfg.get("dt", 1.0)),
        "coord_type":  str(cfg.get("coord_type", "gcj02")),
        "spring_k":    float(cfg.get("spring_k", 0.015)),
        "damping":     float(cfg.get("damping", 0.80)),
        "noise_scale": float(cfg.get("noise_scale", 0.55)),
        "max_speed":   float(cfg.get("max_speed", 2.0)),
    }


async def main(cfg: dict):
    host, port = cfg["host"], cfg["port"]
    print(f"[连接] --rsd {host} {port}")

    rsd = RemoteServiceDiscoveryService((host, port))
    await rsd.connect()

    async with DvtProvider(rsd) as dvt, LocationSimulation(dvt) as location_simulation:
        print(f"[签到] 中心: ({cfg['lat']}, {cfg['lng']})  "
              f"半径: {cfg['radius']}m  间隔: {cfg['dt']}s  坐标系: {cfg['coord_type']}")
        await wander(
            location_simulation,
            cfg["lat"], cfg["lng"],
            radius=cfg["radius"],
            dt=cfg["dt"],
            coord_type=cfg["coord_type"],
            spring_k=cfg["spring_k"],
            damping=cfg["damping"],
            noise_scale=cfg["noise_scale"],
            max_speed=cfg["max_speed"],
        )


if __name__ == "__main__":
    asyncio.run(main(load_config()))
