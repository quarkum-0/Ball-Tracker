# 🎯 Ball-Tracker

**A real-time ball tracking application using OpenCV and Python, with options to use a webcam or mobile camera.**

## 🚀 Features
- **Web Mode**: Use your laptop's webcam to track objects.
- **Mobile Mode**: Connect your mobile camera for tracking.
- **Real-Time Detection**: Tracks the ball and provides directions (Left, Right, Straight, Stop).
- **Customizable**: Easily adjust the HSV range for different colors.

## 🛠️ Setup

### 1. Clone the Repository
```bash
git clone https://github.com/quarkum-0/Ball-Tracker.git
cd Ball-Tracker
```

### 2. Create a Virtual Environment
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 📸 Usage

### Web Mode (Default)
1. **Run the script**:
   ```bash
   python main.py --mode web
   ```
2. The application will use your laptop's webcam to start tracking.

### Mobile Mode 📱
1. **Install IP Webcam on your mobile**: Download the [IP Webcam app](https://play.google.com/store/apps/details?id=com.pas.webcam) from the Google Play Store.
2. **Start the server**: Open the app, start the server, and note the IP address.
3. **Run the script**:
   ```bash
   python main.py --mode mobile --ip <Your_Mobile_IP>
   ```
4. The application will use your mobile camera to start tracking.

## ⚙️ Configuration

You can customize the color range for tracking by modifying the `GREEN_LOWER` and `GREEN_UPPER` variables in the `main.py` file:

```python
GREEN_LOWER = (25, 50, 50)
GREEN_UPPER = (75, 255, 255)
```

## 🤖 Commands and Options

- `--mode`: Selects the mode of operation (`web` or `mobile`).
- `--ip`: Specifies the IP address of your mobile camera (only required for mobile mode).

---
