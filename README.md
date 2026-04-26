# iOSRealRun

通过 pymobiledevice3 模拟 iOS 设备 GPS 位置，实现跑步软件的路线模拟（如校园跑）。

## 环境要求

- Windows 10/11
- Conda（Miniconda 或 Anaconda）
- Python 3.11（通过 conda 环境管理）
- iOS 设备（需信任电脑）

## 安装

### 1. 创建 conda 环境并安装依赖

```bash
conda create -n realrun python=3.11 -y
conda activate realrun
pip install -r requirements.txt
```

### 2. iTunes / Apple 设备驱动

确保已安装 iTunes 或 Apple 设备驱动，以便系统识别 iOS 设备。

---

## 使用步骤

> **三个 bat 文件需要按顺序执行，每次使用都需要重新执行。**

### 第一步：挂载开发者镜像

双击运行 `1) mount_device.bat`

- 将 iPhone 通过 USB 连接到电脑
- 脚本会自动挂载 Developer Disk Image
- 出现 `Press any key` 后说明挂载成功，按任意键退出

### 第二步：创建隧道

**以管理员身份**运行 `2) create_tunnel.bat`

- 创建与设备之间的 RSD 隧道
- 运行后会输出类似以下内容，**不要关闭此窗口**：
  ```
  HOST: fd12:3456:789a::1
  PORT: 54321
  ```
- 记录下 `HOST` 和 `PORT` 的值，下一步会用到

### 第三步：运行位置模拟

双击运行 `3) run.bat`

- 脚本启动后会提示输入：
  ```
  HOST: <输入第二步中的 HOST>
  PORT: <输入第二步中的 PORT>
  ```
- 连接成功后，程序会读取 `route.txt` 中的路线并开始循环模拟跑步

---

## 路线文件

### route.txt

程序默认读取根目录下的 `route.txt` 作为跑步路线。

格式为一系列经纬度坐标点（百度坐标系 BD-09）：

```
{"lng":"120.733...","lat":"30.528..."},{"lng":"...","lat":"..."},...
```

### 预置路线

`routes/` 目录下提供了两条预置路线：

| 文件 | 说明 |
|------|------|
| `routes/NKU_BLT.txt` | 南开大学北洛塘路线（天津） |
| `routes/ZJU_HN.txt` | 浙江大学华家池路线（杭州） |

使用预置路线时，将对应文件的内容复制到 `route.txt` 中即可。

---

## 模拟参数说明

- **速度**：约 1500 m / (1000/3 s) ≈ 4.5 m/s（约 3:42/km 配速），加入 ±15 随机扰动
- **随机化**：每圈路线会随机偏移，避免轨迹完全重合被检测
- **坐标转换**：自动将 BD-09（百度）坐标转换为 WGS-84（标准 GPS）坐标

---

## 常见问题

**Q: 第一步挂载失败？**
A: 检查手机是否已信任该电脑，USB 连接是否正常，或尝试重新插拔。

**Q: 第二步提示权限不足？**
A: `create_tunnel.bat` 必须以**管理员身份**运行。

**Q: 第三步连接失败？**
A: 确认第二步的窗口仍然保持打开，HOST 和 PORT 输入正确。

**Q: 想使用自定义路线？**
A: 可通过百度地图等工具导出路线坐标（BD-09 格式），整理成上述格式写入 `route.txt`。