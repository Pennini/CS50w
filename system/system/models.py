from django.db import models
from django.contrib.auth.models import AbstractUser


DAY_CHOICES = (
    ("0", "Monday"),
    ("1", "Tuesday"),
    ("2", "Wednesday"),
    ("3", "Thursday"),
    ("4", "Friday"),
    ("5", "Saturday"),
    ("6", "Sunday"),
)

POSITION_CHOICES = (
    ("member", "Member"),
    ("trainee", "Trainee"),
    ("director", "Director"),
    ("leader", "Leader"),
    ("vice-president", "Vice-President"),
    ("president", "President"),
)

# Create your models here.
class Group(models.Model):
    ai = "Artificial Intelligence"
    cs = "Cybersecurity"
    ds = "Data Science"
    wd = "Web Development"
    GROUP_CHOICES = (
        (ai, "Artificial Intelligence"),
        (cs, "Cybersecurity"),
        (ds, "Data Science"),
        (wd, "Web Development"),
    )
    name = models.CharField(max_length=30, choices=GROUP_CHOICES)
    description = models.TextField(max_length=500, blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    meeting_day = models.CharField(max_length=20, choices=DAY_CHOICES)

    def __str__(self):
        return f"{self.name}"


class Area(models.Model):
    rh = "Human Resources"
    mkt = "Marketing"
    project = "Project Management"
    AREA_CHOICES = (
        (rh, "Human Resources"),
        (mkt, "Marketing"),
        (project, "Project Management"),
    )
    name = models.CharField(max_length=30, choices=AREA_CHOICES)
    description = models.TextField(max_length=500, blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    meeting_day = models.CharField(max_length=20, choices=DAY_CHOICES)

    def __str__(self):
        return f"{self.name}"

class Position(models.Model):
    name = models.CharField(max_length=30, choices=POSITION_CHOICES)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):
    position = models.ForeignKey("Position", on_delete=models.CASCADE, related_name="user_position", default=None, blank=True, null=True)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="user_group", blank=True, null=True, default=None)
    area = models.ForeignKey("Area", on_delete=models.CASCADE, related_name="user_area", default=None, blank=True, null=True)
    biography = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.username}"

class Event(models.Model):
    area = models.ForeignKey("Area", on_delete=models.CASCADE, related_name="event_area")
    responsible = models.ForeignKey("User", on_delete=models.CASCADE, related_name="event_responsible")
    members_planned = models.ManyToManyField("User", blank=True, related_name="event_members_planned")
    members_present = models.ManyToManyField("User", blank=True, related_name="event_members_present", default=None, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    start_day = models.DateTimeField()
    end_day = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Project(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="project_group")
    responsible = models.ForeignKey("User", on_delete=models.CASCADE, related_name="project_responsible")
    members = models.ManyToManyField("User", blank=True, related_name="project_members")
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True, null=True)
    start_day = models.DateTimeField()
    end_day = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Meeting(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="meeting_group", default=None, blank=True, null=True)
    area = models.ForeignKey("Area", on_delete=models.CASCADE, related_name="meeting_area", default=None, blank=True, null=True)
    members_present = models.ManyToManyField("User", blank=True, related_name="meeting_members_present")
    day = models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day}"


class Availabilty(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="availability_user")
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.IntegerField(default=0, choices=[(0, "Not Available"), (1, "Medium"), (2, "Available")])

    def __str__(self):
        return f"{self.user} - {self.day}"
