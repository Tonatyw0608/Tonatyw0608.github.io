from django.db import models

class Note(models.Model):
    SUBJECT_CHOICES = [
        ('math', '数学'),
        ('science', '科学'),
        ('language', '语文'),
        ('english', '英语'),
    ]
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='math')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.title}"

class QuestionHistory(models.Model):
    question = models.TextField()
    answer = models.TextField()
    asked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question[:20]} - {self.asked_at}"