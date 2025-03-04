from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from .models import Note, QuestionHistory  # 导入 QuestionHistory

def home(request):
    if request.method == 'POST':
        if 'question' in request.POST:
            question = request.POST.get('question', '')
            api_key = "sk-43ec592e383348309c12cf4e00d2fce0"  # 替换成你的 DeepSeek API Key
            url = "https://api.deepseek.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json; charset=utf-8"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": question}],
                "max_tokens": 500
            }
            try:
                response = requests.post(url, json=data, headers=headers)
                response.encoding = 'utf-8'
                if response.status_code == 200:
                    answer = response.json()['choices'][0]['message']['content']
                    # 保存到历史记录
                    QuestionHistory.objects.create(question=question, answer=answer)
                else:
                    answer = f"API 调用失败，状态码：{response.status_code}，错误信息：{response.text}"
            except Exception as e:
                answer = f"发生错误：{str(e)}"
            return render(request, 'home.html', {'question': question, 'answer': answer}, content_type="text/html; charset=utf-8")
        elif 'title' in request.POST:
            subject = request.POST.get('subject', 'math')
            title = request.POST.get('title', '')
            content = request.POST.get('content', '')
            if title and content:
                Note.objects.create(subject=subject, title=title, content=content)
            return redirect('home')
        elif 'edit_note_id' in request.POST:
            note_id = request.POST.get('edit_note_id')
            note = Note.objects.get(id=note_id)
            note.title = request.POST.get('edit_title', note.title)
            note.content = request.POST.get('edit_content', note.content)
            note.save()
            return redirect('home')
        elif 'delete_note_id' in request.POST:
            note_id = request.POST.get('delete_note_id')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                try:
                    Note.objects.get(id=note_id).delete()
                    print(f"已删除笔记 ID: {note_id}")
                    return JsonResponse({'status': 'success'})
                except Note.DoesNotExist:
                    print(f"笔记 ID {note_id} 不存在")
                    return JsonResponse({'status': 'error', 'message': '笔记不存在'}, status=400)
                except Exception as e:
                    print(f"删除笔记时出错: {str(e)}")
                    return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            else:
                Note.objects.get(id=note_id).delete()
                return redirect('home')

    notes = Note.objects.all()
    history = QuestionHistory.objects.all().order_by('-asked_at')  # 获取历史记录，按时间倒序
    edit_note = None
    if request.method == 'GET' and 'edit' in request.GET:
        note_id = request.GET.get('edit')
        edit_note = Note.objects.get(id=note_id)
    return render(request, 'home.html', {'question': '', 'answer': '', 'notes': notes, 'edit_note': edit_note, 'history': history}, content_type="text/html; charset=utf-8")