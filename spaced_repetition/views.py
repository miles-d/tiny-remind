from datetime import datetime, date
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Topic
from django.conf import settings


def index(request):
    topics = []
    for t in Topic.objects.all():
        topics.append({
            'id': t.id,
            'title': t.title,
            'url': t.url,
            'is_due': t.is_due(datetime.now().date(), settings.REMIND_SCHEDULE)
            })
    topics.sort(key=(lambda t: t['is_due']), reverse=True)
    return render(request, 'spaced_repetition/index.html', { 'topics': topics })


def add_topic(request):
    if request.POST:
        topic = Topic(
                title=request.POST['title'],
                url=request.POST['url'],
                comment=request.POST['comment']
                )

        try:
            topic.save()
            return HttpResponseRedirect('/')
        except Exception:
            return render(request, 'spaced_repetition/add_topic.html')
    else:
        return render(request, 'spaced_repetition/add_topic.html')


def view_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    is_due = topic.is_due(datetime.now().date(), settings.REMIND_SCHEDULE)
    return render(request, 'spaced_repetition/view_topic.html', { 'topic': topic,
        'is_due': is_due })


def review_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    topic.review(datetime.now().date(), settings.REMIND_SCHEDULE)
    try:
        topic.save()
        return HttpResponseRedirect('/')
    except Exception:
        return HttpResponseRedirect('/topic/' + topic_id)


def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if request.POST:
        topic.title = request.POST['title']
        topic.url = request.POST['url']
        topic.comment = request.POST['comment']

        try:
            topic.save()
        except Exception:
            return HttpResponseRedirect('/topic/' + str(topic_id) + '/edit')
        return HttpResponseRedirect('/topic/' + str(topic_id))
    else:
        return render(request, 'spaced_repetition/edit_topic.html', { 'topic': topic })


def confirm_deletion(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    return render(request, 'spaced_repetition/confirm_deletion.html', { 'topic': topic })


def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    try:
        topic.delete()
    except Exception:
        return HttpResponseRedirect('/topic/' + str(topic_id) + '/confirm_deletion')

    return HttpResponseRedirect('/')
