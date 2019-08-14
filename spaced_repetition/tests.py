from datetime import date, timedelta
from django.test import TestCase
from .models import Topic, ReviewTooEarlyException

schedule = (1, 7, 30)

class TopicTest(TestCase):
    def test_is_not_due_right_after_creation(self):
        today = date(2019, 1, 30)
        subject = Topic(created_at=today)

        result = subject.is_due(today, schedule)

        self.assertFalse(result)


    def test_is_due_one_day_after_creation(self):
        yesterday = date(2019, 1, 29)
        today = date(2019, 1, 30)
        subject = Topic(created_at=yesterday)
        
        result = subject.is_due(today, schedule)
        
        self.assertTrue(result)


    def test_is_not_due_right_after_first_review(self):
        yesterday = date(2019, 1, 29)
        today = date(2019, 1, 30)
        subject = Topic(created_at=yesterday)

        subject.review(today, schedule)
        result = subject.is_due(today, schedule)

        self.assertFalse(result)

    def test_is_due_week_after_first_review(self):
        eight_days_ago = date(2019, 1, 22)
        seven_days_ago = date(2019, 1, 23)
        today = date(2019, 1, 30)
        subject = Topic(created_at=eight_days_ago)

        subject.review(seven_days_ago, schedule)
        result = subject.is_due(today, schedule)

        self.assertTrue(result)


    def test_raises_exception_when_reviewing_too_early(self):
        today = date(2019, 1, 30)
        subject = Topic(created_at=today)

        self.assertFalse(subject.is_due(today, schedule))
        with self.assertRaises(ReviewTooEarlyException):
            subject.review(today, schedule)


    def test_after_defined_schedule_and_review_too_early(self):
        today = date(2019, 1, 1)
        third_review_date = today - timedelta(days=1)
        second_review_date = third_review_date - timedelta(days=30)
        first_review_date = second_review_date - timedelta(days=7)
        created_date = first_review_date - timedelta(days=1)

        subject = Topic(created_at=created_date)

        subject.review(first_review_date, schedule)
        subject.review(second_review_date, schedule)
        subject.review(third_review_date, schedule)

        result = subject.is_due(today, schedule)

        self.assertFalse(result)


    def test_after_defined_schedule_and_review_too_early(self):
        today = date(2019, 1, 1)
        third_review_date = today - timedelta(days=30)
        second_review_date = third_review_date - timedelta(days=30)
        first_review_date = second_review_date - timedelta(days=7)
        created_date = first_review_date - timedelta(days=1)

        subject = Topic(created_at=created_date)

        subject.review(first_review_date, schedule)
        subject.review(second_review_date, schedule)
        subject.review(third_review_date, schedule)

        result = subject.is_due(today, schedule)

        self.assertTrue(result)


