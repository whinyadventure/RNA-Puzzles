from django.test import TestCase

from rnapuzzles.models import CustomUser, Group, Submission, PuzzleInfo, Challenge, timezone


class TestSubmission(TestCase):
    def setUp(self):
        self.organizer: CustomUser = CustomUser.objects.create(email="a@a.pl", role=CustomUser.ORGANIZER)
        self.user = CustomUser.objects.create(email="user@a.pl")
        self.user_second = CustomUser.objects.create(email="user2@a.pl")

        self.puzzleInfo = PuzzleInfo.objects.create(author=self.organizer)
        self.challenge = Challenge.objects.create(puzzle_info=self.puzzleInfo, author=self.organizer,
                                                  start_date=timezone.now(), end_date=timezone.now(),
                                                  end_automatic=timezone.now())

    def test_single_submission(self):
        self.sub1 = Submission.objects.create(challenge=self.challenge, is_automatic=False, user=self.user, label="A")
        self.assertEqual(set(Submission.get_last_submissions(self.challenge.pk)), set([self.sub1]))

    def test_automatic_human(self):
        self.sub_human = Submission.objects.create(challenge=self.challenge, is_automatic=False, user=self.user,
                                                   label="A")
        self.sub_automatic = Submission.objects.create(challenge=self.challenge, is_automatic=True, user=self.user,
                                                       label="A")
        self.assertEqual(set(Submission.get_last_submissions(self.challenge.pk)),
                         set([self.sub_human, self.sub_automatic]))

    def test_labels(self):
        self.sub1 = Submission.objects.create(challenge=self.challenge, is_automatic=False, user=self.user, label="A")
        self.sub2 = Submission.objects.create(challenge=self.challenge, is_automatic=False, user=self.user, label="B")
        self.assertEqual(set(Submission.get_last_submissions(self.challenge.pk)), set([self.sub1, self.sub2]))

    def test_date(self):
        self.sub1 = Submission.objects.create(date="1-01-2000 10:10", challenge=self.challenge, is_automatic=False,
                                              user=self.user, label="A")
        self.sub2 = Submission.objects.create(date="1-01-2000 10:12", challenge=self.challenge, is_automatic=False,
                                              user=self.user, label="A")
        self.assertEqual(set(Submission.get_last_submissions(self.challenge.pk)), set([self.sub2]))

    def test_two_users(self):
        self.sub_first_automatic_A = Submission.objects.create(date="1-01-2000 10:10", challenge=self.challenge,
                                                               is_automatic=False,
                                                               user=self.user, label="A")
        self.sub_first_automatic_B = Submission.objects.create(date="1-01-2000 10:12", challenge=self.challenge,
                                                               is_automatic=False,
                                                               user=self.user, label="B")

        self.sub_first_human_A = Submission.objects.create(date="1-01-2000 10:10", challenge=self.challenge,
                                                           is_automatic=True,
                                                           user=self.user, label="A")
        self.sub_first_human_A_late = Submission.objects.create(date="1-01-2000 10:12", challenge=self.challenge,
                                                                is_automatic=True,
                                                                user=self.user, label="A")

        self.sub_second_automatic_A = Submission.objects.create(date="1-01-2000 10:10", challenge=self.challenge,
                                                                is_automatic=False,
                                                                user=self.user_second, label="A")
        self.sub_second_automatic_A_late = Submission.objects.create(date="1-01-2000 10:12", challenge=self.challenge,
                                                                     is_automatic=False,
                                                                     user=self.user_second, label="A")

        self.sub_second_human_C = Submission.objects.create(date="1-01-2000 10:10", challenge=self.challenge,
                                                            is_automatic=True,
                                                            user=self.user_second, label="C")
        self.sub_second_automatic_C = Submission.objects.create(date="1-01-2000 10:12", challenge=self.challenge,
                                                                is_automatic=False,
                                                                user=self.user_second, label="C")
        print(Submission.get_last_submissions(self.challenge.pk))
        self.assertEqual(set(Submission.get_last_submissions(self.challenge.pk)), {
            self.sub_first_automatic_A, self.sub_first_automatic_B, self.sub_first_human_A_late,
            self.sub_second_automatic_A_late, self.sub_second_human_C, self.sub_second_automatic_C})
