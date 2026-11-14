"""Cross-platform desktop notification helper."""
import subprocess
import shutil
import sys


def notify(title, message):
    """Best-effort desktop notification. Fails silently if unsupported."""
    try:
        if sys.platform.startswith("linux"):
            # Try notify-send (works on Mint, Ubuntu, most desktops)
            if shutil.which("notify-send"):
                subprocess.run(
                    ["notify-send", "-a", "WiFi Intruder Detector",
                     "-i", "dialog-warning", title, message],
                    check=False, timeout=3,
                )
                return
        elif sys.platform == "darwin":
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], check=False, timeout=3)
            return
        elif sys.platform.startswith("win"):
            # Windows: use PowerShell toast (works on Win10+)
            ps = (
                f'[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, '
                f'ContentType=WindowsRuntime] | Out-Null; '
                f'$t = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent('
                f'[Windows.UI.Notifications.ToastTemplateType]::ToastText02); '
                f'$t.GetElementsByTagName("text").Item(0).AppendChild('
                f'$t.CreateTextNode("{title}")) | Out-Null; '
                f'$t.GetElementsByTagName("text").Item(1).AppendChild('
                f'$t.CreateTextNode("{message}")) | Out-Null; '
                f'[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('
                f'"WiFi Intruder Detector").Show('
                f'[Windows.UI.Notifications.ToastNotification]::new($t))'
            )
            subprocess.run(["powershell", "-Command", ps], check=False, timeout=5)
            return
    except Exception:
        pass  # never crash the app because a notification failed
