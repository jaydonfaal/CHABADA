import os

api_methods = [
    "android.accounts.AccountManager.addAccountExplicitly",
    "android.accounts.AccountManager.getAccounts",
    "android.app.Activity.setContentView",
    "android.content.Intent.setAction",
    "android.location.LocationManager.getLastKnownLocation",
    "android.hardware.Camera.open",
    "android.net.ConnectivityManager.getActiveNetworkInfo",
    "android.os.Build.getSerial",
    "android.provider.Settings.Secure.getString",
    "android.telephony.TelephonyManager.getDeviceId",
    "android.telephony.TelephonyManager.getLine1Number",
    "android.view.Window.setFlags",
    # Add more APIs as needed
]

# Base path to the decompiled APKs
decompiled_apps_path = "/decompiled_apps"  


results = {}

for app_folder in os.listdir(decompiled_apps_path):
    app_path = os.path.join(decompiled_apps_path, app_folder)
    if not os.path.isdir(app_path):
        continue

    print(f"Checking: {app_folder}")
    found_apis = set()

    for root, dirs, files in os.walk(app_path):
        for file in files:
            if file.endswith(".smali") or file.endswith(".java"):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        for api in api_methods:
                            if api in content:
                                found_apis.add(api)
                except Exception as e:
                    print(f"Failed to read file {file}: {e}")

    results[app_folder] = found_apis

print("\n=== API Usage Results ===\n")
for app, apis in results.items():
    if apis:
        print(f"{app}:")
        for api in sorted(apis):
            print(f"  - {api}")
    else:
        print(f"{app}: No target APIs found.")
