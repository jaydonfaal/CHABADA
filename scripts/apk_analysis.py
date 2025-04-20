from androguard.misc import AnalyzeAPK

apk_path = 'your_app.apk'

a, d, dx = AnalyzeAPK(apk_path)

permissions = a.get_permissions()
apis_used = set()

for method in dx.get_methods():
    api_call = method.method.get_class_name() + "->" + method.method.get_name()
    apis_used.add(api_call)

print(permissions, apis_used)
