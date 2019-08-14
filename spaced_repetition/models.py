from django.db import models

class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(blank=False, null=False, max_length=300)
    url = models.TextField(blank=True, null=True, max_length=500)
    comment = models.TextField(blank=True, null=True, max_length=2000)
    created_at = models.DateField(auto_now_add=True)
    last_review_at = models.DateField(blank=False, null=True)
    level = models.IntegerField(default=0)

    def is_due(self, today, schedule):
        # for first review
        if self.level == 0:
            return (today - self.created_at).days > 0

        # for next review
        if self.level < len(schedule):
            return (today - self.last_review_at).days >= schedule[self.level]

        # review out of schedule bounds
        return (today - self.last_review_at).days >= schedule[-1]


    def review(self, today, schedule):
        if not self.is_due(today, schedule):
            raise ReviewTooEarlyException

        self.level += 1
        self.last_review_at = today


    def __str__(self):
        return 'title="' + self.title + '"'


class ReviewTooEarlyException(Exception):
    pass
