# models.py
from django.db import models
from django.conf import settings
from django.db.models import Q



class Course(models.Model):
    COURSE_TYPE_CHOICES = (
        ('core', 'Core'),
        ('elective', 'Elective'),
        ('open_elective', 'Open Elective'),
        ('honor', 'Honor'),
        ('minor', 'Minor'),
        ('add_on', 'Add On')
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )
    SEMESTER_CHOICES = (
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8')
    )



    DEPARTMENT_CHOICES = (
        ('BE-BME', 'B.E. - BIOMEDICAL ENGINEERING'),
        ('BTECH-BT', 'B.Tech. - BIOTECHNOLOGY'),
        ('BE-EIE', 'B.E. - ELECTRONICS AND INSTRUMENTATION ENGINEERING'),
        ('BE-ECE', 'B.E. - ELECTRONICS AND COMMUNICATION ENGINEERING'),
        ('BE-EEE', 'B.E. - ELECTRICAL AND ELECTRONICS ENGINEERING'),
        ('BE-CSE', 'B.E. - COMPUTER SCIENCE AND ENGINEERING'),
        ('BE-CSD', 'B.E. - COMPUTER SCIENCE AND DESIGN'),
        ('BE-CIVIL', 'B.E. - CIVIL ENGINEERING'),
        ('BE-ISE', 'B.E. - INFORMATION SCIENCE AND ENGINEERING'),
        ('BE-MECH', 'B.E. - MECHANICAL ENGINEERING'),
        ('BE-MTE', 'B.E. - MECHATRONICS ENGINEERING'),
        ('BTECH-AE', 'B.Tech. - AGRICULTURAL ENGINEERING'),
        ('BTECH-AIDS', 'B.Tech. - ARTIFICIAL INTELLIGENCE AND DATA SCIENCE'),
        ('BTECH-AIML', 'B.Tech. - ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING'),
        ('BTECH-CSBS', 'B.Tech. - COMPUTER SCIENCE AND BUSINESS SYSTEMS'),
        ('BTECH-CT', 'B.Tech. - COMPUTER TECHNOLOGY'),
        ('BTECH-FT', 'B.Tech. - FASHION TECHNOLOGY'),
        ('BTECH-FOOD', 'B.Tech. - FOOD TECHNOLOGY'),
        ('BTECH-IT', 'B.Tech. - INFORMATION TECHNOLOGY'),
        ('ME-CS', 'M.E. - COMMUNICATION SYSTEMS'),
        ('ME-CSE', 'M.E. - COMPUTER SCIENCE AND ENGINEERING'),
        ('ME-ISE', 'M.E. - INDUSTRIAL SAFETY ENGINEERING'),
        ('ME-SE', 'M.E. - STRUCTURAL ENGINEERING'),
        ('MBA', 'M.B.A. - MASTER OF BUSINESS ADMINISTRATION'),
        ('PHD-BT', 'Ph.D BIOTECHNOLOGY'),
        ('PHD-CHEM', 'Ph.D CHEMISTRY'),
        ('PHD-CIVIL', 'Ph.D CIVIL ENGINEERING'),
        ('PHD-CSE', 'Ph.D COMPUTER SCIENCE AND ENGINEERING'),
        ('PHD-EEE', 'Ph.D ELECTRICAL AND ELECTRONICS ENGINEERING'),
        ('PHD-ECE', 'Ph.D ELECTRONICS AND COMMUNICATION ENGINEERING'),
        ('PHD-EIE', 'Ph.D ELECTRONICS AND INSTRUMENTATION ENGINEERING'),
        ('PHD-IT', 'Ph.D INFORMATION TECHNOLOGY'),
        ('PHD-MATH', 'Ph.D MATHEMATICS'),
        ('PHD-MECH', 'Ph.D MECHANICAL ENGINEERING'),
        ('PHD-MTE', 'Ph.D MECHATRONICS'),
        ('PHD-PHY', 'Ph.D PHYSICS'),
        ('PHD-MGT', 'Ph.D SCHOOL OF MANAGEMENT STUDIES')
    )

    YEAR_CHOICES = (
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year')
    )

    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=200)
    regulation = models.PositiveIntegerField()
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES)

    # Points
    lecture_points = models.DecimalField(max_digits=3, decimal_places=1,  verbose_name='L')
    tutorial_points = models.DecimalField(max_digits=3, decimal_places=1,  verbose_name='T')
    practical_points = models.DecimalField(max_digits=3, decimal_places=1,  verbose_name='P')
    credits = models.DecimalField(max_digits=3, decimal_places=1)
    hours_per_week = models.PositiveIntegerField()

    # Marks
    cia_marks = models.PositiveIntegerField()
    see_marks = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField(editable=False)

    # Classification
    category = models.CharField(max_length=20)
    semester = models.PositiveIntegerField(choices=SEMESTER_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    academic_year = models.CharField(max_length=9)  # Format: 2023-2024

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_marks = self.cia_marks + self.see_marks
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['course_code']








class UserProfile(models.Model):
    CATEGORY_CHOICES = (
        ('lateral', 'Lateral'),
        ('regular', 'Regular'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    YEAR_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year')
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    # Personal Information
    email_id = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    roll_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    enroll_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    # Academic Information - Using Course model choices
    department = models.CharField(
        max_length=50,
        choices=Course.DEPARTMENT_CHOICES,  # Using Course model's department choices
        null=True,
        blank=True
    )
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='regular')
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    # Electives Information
    total_electives = models.PositiveIntegerField(default=0)
    completed_electives = models.PositiveIntegerField(default=0)

    # Current Academic Status
    current_semester = models.PositiveIntegerField(null=True, blank=True)
    year_of_study = models.PositiveIntegerField(
        choices=YEAR_CHOICES,  # Using fixed year choices
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


#################


class CourseRule(models.Model):
    DEPARTMENT_CHOICES = Course.DEPARTMENT_CHOICES
    SEMESTER_CHOICES = Course.SEMESTER_CHOICES
    YEAR_CHOICES = Course.YEAR_CHOICES

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES
    )
    semester = models.PositiveIntegerField(
        choices=SEMESTER_CHOICES
    )
    year = models.PositiveIntegerField(
        choices=YEAR_CHOICES
    )
    regulation = models.PositiveIntegerField()

    # Core courses
    core_courses = models.ManyToManyField(
        'Course',
        related_name='core_course_rules',
        limit_choices_to={'course_type': 'core'},
        blank=True
    )
    core_min_credits = models.PositiveIntegerField(default=0)
    core_max_credits = models.PositiveIntegerField(default=0)

    # Elective courses
    elective_courses = models.ManyToManyField(
        'Course',
        related_name='elective_course_rules',
        limit_choices_to={'course_type': 'elective'},
        blank=True
    )
    elective_min_credits = models.PositiveIntegerField(default=0)
    elective_max_credits = models.PositiveIntegerField(default=0)

    # Open Elective courses
    open_elective_courses = models.ManyToManyField(
        'Course',
        related_name='open_elective_course_rules',
        limit_choices_to={'course_type': 'open_elective'},
        blank=True
    )
    open_elective_min_credits = models.PositiveIntegerField(default=0)
    open_elective_max_credits = models.PositiveIntegerField(default=0)

    # Honor courses
    honor_courses = models.ManyToManyField(
        'Course',
        related_name='honor_course_rules',
        limit_choices_to={'course_type': 'honor'},
        blank=True
    )
    honor_min_credits = models.PositiveIntegerField(default=0)
    honor_max_credits = models.PositiveIntegerField(default=0)

    # Minor courses
    minor_courses = models.ManyToManyField(
        'Course',
        related_name='minor_course_rules',
        limit_choices_to={'course_type': 'minor'},
        blank=True
    )
    minor_min_credits = models.PositiveIntegerField(default=0)
    minor_max_credits = models.PositiveIntegerField(default=0)

    # Add On courses
    add_on_courses = models.ManyToManyField(
        'Course',
        related_name='add_on_course_rules',
        limit_choices_to={'course_type': 'add_on'},
        blank=True
    )
    add_on_min_credits = models.PositiveIntegerField(default=0)
    add_on_max_credits = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['department', 'semester', 'year', 'regulation']
        ordering = ['department', 'semester']
        verbose_name = 'Course Rule'
        verbose_name_plural = 'Course Rules'

    def __str__(self):
        return f"{self.get_department_display()} - Sem {self.semester}, Year {self.year} (Reg {self.regulation})"

    def get_available_courses(self, course_type):
        """
        Fetch available courses for specific department, semester, and course type
        """
        return Course.objects.filter(
            department=self.department,
            semester=self.semester,
            course_type=course_type,
            status='active'
        )

