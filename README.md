# Edge 朗读自动录音工具

本工具用于在 Microsoft Edge 浏览器启动“大声朗读”功能时，自动录制电脑音频。

# 强烈推荐使用easyvoice, 免费，稳定，强大

1. https://easyvoice.ioplus.tech/
2. https://easyvoice.ioplus.tech/generate

## 工作原理

1. **音频监控**：使用 PyAudio 持续监听系统音频输入（需配置环回设备）或麦克风输入。
2. **语音活动检测 (VAD)**：通过能量阈值检测语音开始与结束。
3. **Edge 检测**：
   - 检查 Microsoft Edge 是否为前台应用程序（通过 AppleScript）。
   - 仅当 Edge 在前台且检测到语音时才开始录音。
4. **自动录音**：检测到语音后开始录制，无声超过设定时长后停止，保存为 WAV 文件。

## 系统要求

- macOS（已在 macOS Sonoma 测试）
- Python 3.6+
- Microsoft Edge 浏览器

## 安装

### 1. 克隆或下载本仓库

```bash
git clone https://github.com/Jaylee89/auto-generation.git && cd auto-generation
```

### 2. 使用安装脚本（推荐）

```bash
./install_deps.sh
```

### 3. 配置音频环回（可选）

若要录制系统音频（而非麦克风），需要安装虚拟音频设备，如 [BlackHole](https://github.com/ExistentialAudio/BlackHole) 或 Soundflower。

安装后，在“系统设置” → “声音” → “输出”中选择 BlackHole，然后在“输入”中选择 BlackHole 作为录音设备。

## 使用方法

### 基本使用

运行主检测器：

```bash
source venv/bin/activate
python edge_detector.py 2>&1
```

程序将开始监听，并在检测到 Edge 前台语音时自动录音。录音文件保存在 `edge_recordings/` 目录下。

### 参数调整

可在 `edge_detector.py` 中调整以下参数：

- `audio_threshold`: 语音检测能量阈值（默认 500）
- `silence_limit`: 无声持续时间（秒）后停止录音（默认 2.0）
- `rate`: 采样率（默认 16000）
- `chunk`: 音频块大小（默认 1024）

### 独立录音机

如果需要仅录音（不检测 Edge），可使用 `audio_recorder.py`：

```bash
python audio_recorder.py 2>&1
```

## 文件说明

- `edge_detector.py`：主检测与录音程序。
- `audio_recorder.py`：通用语音活动录音机。
- `check_read_aloud.applescript`：AppleScript 检测脚本（备用）。
- `install_deps.sh`：自动安装依赖并创建虚拟环境的脚本。
- `test_detector.py`、`quick_test.py`：测试脚本。

## 注意事项

1. **权限**：首次运行时需授予“辅助功能”权限（用于检测前台应用）和“麦克风”权限（用于录音）。
2. **音频设备**：确保选择正确的输入设备。若使用系统音频环回，请正确配置。
3. **阈值调整**：环境噪音可能导致误触发，请根据实际情况调整 `audio_threshold`。
4. **仅限 macOS**：本工具依赖 macOS 的 AppleScript 和 CoreAudio，暂不支持 Windows/Linux。

## 故障排除

### 无录音

- 检查 Edge 是否为前台窗口。
- 检查音频输入设备是否正常（可通过 `audio_recorder.py` 测试）。
- 调整能量阈值（可能语音能量较低）。

### 权限错误

- 前往“系统设置” → “隐私与安全性” → “辅助功能”，添加终端或 Python 解释器。
- 同样在“麦克风”中允许 Python。

### 导入错误

确保已安装所有依赖：

```bash
pip install -r requirements.txt
```

（可手动创建 requirements.txt 包含 pyaudio, numpy, psutil）

## 许可证

MIT