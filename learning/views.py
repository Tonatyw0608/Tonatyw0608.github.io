from django.shortcuts import render
from django.http import JsonResponse
import requests
from .models import Note, QuestionHistory
import os

def home(request):
    if request.method == 'POST':
        if 'question' in request.POST:
            question = request.POST.get('question', '')
            api_key = os.environ.get('DEEPSEEK_API_KEY')
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
                    QuestionHistory.objects.create(question=question, answer=answer)
                    return JsonResponse({'answer': answer})
                else:
                    return JsonResponse({'error': 'API 调用失败'}, status=500)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        elif 'title' in request.POST:
            subject = request.POST.get('subject', 'math')
            title = request.POST.get('title', '')
            content = request.POST.get('content', '')
            if title and content:
                Note.objects.create(subject=subject, title=title, content=content)
            return JsonResponse({'status': 'success'})
        elif 'edit_note_id' in request.POST:
            note_id = request.POST.get('edit_note_id')
            note = Note.objects.get(id=note_id)
            note.title = request.POST.get('edit_title', note.title)
            note.content = request.POST.get('edit_content', note.content)
            note.save()
            return JsonResponse({'status': 'success'})
        elif 'delete_note_id' in request.POST:
            note_id = request.POST.get('delete_note_id')
            Note.objects.get(id=note_id).delete()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_notes(request):
    notes = Note.objects.all().values('id', 'subject', 'title', 'content')
    return JsonResponse(list(notes), safe=False)

def get_history(request):
    history = QuestionHistory.objects.all().order_by('-asked_at').values('question', 'answer')
    return JsonResponse(list(history), safe=False)