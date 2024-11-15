import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import pandas as pd
from tools.strip_fill import process_all_files  # 使用相对导入

@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')

        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        for file in files:
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

        # 调用strip_fill.py中的处理函数
        df = process_all_files(upload_dir)

        # 删除临时文件
        for file in files:
            file_path = os.path.join(upload_dir, file.name)
            os.remove(file_path)

        # 将DataFrame转换为JSON格式
        results = df.to_dict(orient='records')

        return JsonResponse(results, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)