# admin.py
from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import path
from django.db.models import Count, Q
from django.contrib import admin
from .models import UserProfile,Course,CourseRule

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number','email_id', 'enroll_number', 'department',
                    'category', 'current_semester', 'year_of_study', 'cgpa', 'status_display',
                    'status_toggle', 'electives_display')

    search_fields = ('user__username', 'roll_number', 'enroll_number', 'email_id')

    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'profile_image', 'email_id', 'first_name',
                       'roll_number', 'enroll_number')
        }),
        ('Academic Details', {
            'fields': ('department', 'category', 'cgpa', 'status')
        }),
        ('Semester Information', {
            'fields': ('current_semester', 'year_of_study')
        }),
        ('Electives', {
            'fields': ('total_electives', 'completed_electives')
        }),
    )

    def save_model(self, request, obj, form, change):
        # First save the UserProfile object
        super().save_model(request, obj, form, change)

        # Now update the User model
        user = obj.user
        user.email = obj.email_id  # Sync email
        user.first_name = obj.first_name  # Sync first name
        user.save()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Double-check the synchronization after all related objects are saved
        obj = form.instance
        if obj.user.email != obj.email_id:
            obj.user.email = obj.email_id
            obj.user.save()

    # Your existing methods remain the same
    def status_display(self, obj):
        if obj.status == 'active':
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">Active</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">Inactive</span>'
        )

    status_display.short_description = 'Status'

    def status_toggle(self, obj):
        return format_html(
            '''
            <div style="width: 32px; height: 16px; background-color: {}; border-radius: 8px; position: relative; cursor: pointer;">
                <a href="{}?id={}" style="display: block; width: 100%; height: 100%; text-decoration: none;">
                    <span style="width: 12px; height: 12px; background-color: white; border-radius: 50%; position: absolute; top: 2px; {}"></span>
                </a>
            </div>
            ''',
            '#28a745' if obj.status == 'active' else '#dc3545',
            reverse('admin:toggle-user-status'),
            obj.id,
            'right: 2px;' if obj.status == 'active' else 'left: 2px;'
        )

    status_toggle.short_description = 'Toggle'

    def electives_display(self, obj):
        return f"{obj.completed_electives}/{obj.total_electives}"

    electives_display.short_description = 'Electives'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('toggle-status/',
                 self.admin_site.admin_view(self.toggle_status_view),
                 name='toggle-user-status'),
        ]
        return custom_urls + urls

    def toggle_status_view(self, request):
        user_id = request.GET.get('id')
        if user_id:
            profile = UserProfile.objects.get(id=user_id)
            profile.status = 'inactive' if profile.status == 'active' else 'active'
            profile.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('admin:home_userprofile_changelist')))




@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'department', 'year',
                    'semester', 'credits', 'course_type', 'status_display', 'status_toggle')

    search_fields = (
        'course_code',
        'course_name',
        'department',
    )

    list_filter = ('year', 'semester', 'course_type', 'status')

    readonly_fields = ('total_marks',)

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'course_code', 'course_name', 'department', 'year',
                'regulation', 'course_type', 'status'
            )
        }),
        ('Course Structure', {
            'fields': (
                ('lecture_points', 'tutorial_points', 'practical_points'),
                'credits', 'hours_per_week'  # Added credits field here
            )
        }),
        ('Marks Distribution', {
            'fields': (('cia_marks', 'see_marks'), 'total_marks')
        }),
        ('Classification', {
            'fields': (
                'category', 'semester', 'academic_year'
            )
        })
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            # Add additional search criteria
            year_query = queryset.model.objects.filter(year__icontains=search_term)
            course_type_query = queryset.model.objects.filter(course_type__icontains=search_term)

            # Combine queries using | operator
            queryset = queryset | year_query | course_type_query
            use_distinct = True

        return queryset, use_distinct

    def status_display(self, obj):
        if obj.status == 'active':
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">Active</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">Inactive</span>'
        )
    status_display.short_description = 'Status'

    def status_toggle(self, obj):
        return format_html(
            '''
            <div style="width: 32px; height: 16px; background-color: {}; border-radius: 8px; position: relative; cursor: pointer;">
                <a href="{}?id={}" style="display: block; width: 100%; height: 100%; text-decoration: none;">
                    <span style="width: 12px; height: 12px; background-color: white; border-radius: 50%; position: absolute; top: 2px; {}"></span>
                </a>
            </div>
            ''',
            '#28a745' if obj.status == 'active' else '#dc3545',
            reverse('admin:toggle-course-status'),
            obj.id,
            'right: 2px;' if obj.status == 'active' else 'left: 2px;'
        )
    status_toggle.short_description = 'Toggle'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('toggle-status/',
                 self.admin_site.admin_view(self.toggle_status_view),
                 name='toggle-course-status'),
        ]
        return custom_urls + urls

    def toggle_status_view(self, request):
        course_id = request.GET.get('id')
        if course_id:
            course = Course.objects.get(id=course_id)
            course.status = 'inactive' if course.status == 'active' else 'active'
            course.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('admin:home_course_changelist')))



#############################################
#############################################


@admin.register(CourseRule)
class CourseRuleAdmin(admin.ModelAdmin):
    list_display = (
        'department',
        'semester',
        'year',
        'regulation',
        'get_core_course_count',
        'get_elective_course_count',
        'get_open_elective_course_count',
        'get_honor_course_count',
        'get_minor_course_count',
        'get_add_on_course_count',
        'is_active',
        'status_display'
    )
    list_filter = ('department', 'semester', 'year', 'regulation', 'is_active')
    search_fields = ('department', 'regulation')

    filter_horizontal = (
        'core_courses', 'elective_courses', 'open_elective_courses',
        'honor_courses', 'minor_courses', 'add_on_courses'
    )

    fieldsets = (
        ('Basic Information', {
            'fields': ('department', 'semester', 'year', 'regulation', 'is_active')
        }),
        ('Core Courses', {
            'fields': ('core_courses', 'core_min_credits', 'core_max_credits'),
            'description': 'Available core courses will be filtered based on department, semester, year, and regulation.'
        }),
        ('Elective Courses', {
            'fields': ('elective_courses', 'elective_min_credits', 'elective_max_credits'),
            'description': 'Available elective courses will be filtered based on department, semester, year, and regulation.'
        }),
        ('Open Elective Courses', {
            'fields': ('open_elective_courses', 'open_elective_min_credits', 'open_elective_max_credits'),
            'description': 'Available open elective courses will be filtered based on department, semester, year, and regulation.'
        }),
        ('Honor Courses', {
            'fields': ('honor_courses', 'honor_min_credits', 'honor_max_credits'),
            'description': 'Available honor courses will be filtered based on department, semester, year, and regulation.'
        }),
        ('Minor Courses', {
            'fields': ('minor_courses', 'minor_min_credits', 'minor_max_credits'),
            'description': 'Available minor courses will be filtered based on department, semester, year, and regulation.'
        }),
        ('Add On Courses', {
            'fields': ('add_on_courses', 'add_on_min_credits', 'add_on_max_credits'),
            'description': 'Available add on courses will be filtered based on department, semester, year, and regulation.'
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'core_courses', 'elective_courses', 'open_elective_courses',
            'honor_courses', 'minor_courses', 'add_on_courses'
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        course_types = {
            'core_courses': 'core',
            'elective_courses': 'elective',
            'open_elective_courses': 'open_elective',
            'honor_courses': 'honor',
            'minor_courses': 'minor',
            'add_on_courses': 'add_on'
        }

        if db_field.name in course_types:
            course_rule_id = request.resolver_match.kwargs.get("object_id")
            department = request.GET.get('department') or request.POST.get('department')
            semester = request.GET.get('semester') or request.POST.get('semester')
            year = request.GET.get('year') or request.POST.get('year')
            regulation = request.GET.get('regulation') or request.POST.get('regulation')

            if course_rule_id:
                course_rule = CourseRule.objects.filter(pk=course_rule_id).first()
                if course_rule:
                    department = department or course_rule.department
                    semester = semester or course_rule.semester
                    year = year or course_rule.year
                    regulation = regulation or course_rule.regulation

            course_filter = Q(course_type=course_types[db_field.name], status='active')
            if department:
                course_filter &= Q(department=department)
            if semester:
                course_filter &= Q(semester=semester)
            if year:
                course_filter &= Q(year=year)
            if regulation:
                course_filter &= Q(regulation=regulation)

            kwargs["queryset"] = Course.objects.filter(course_filter)

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_course_count(self, obj, course_type, related_name):
        available_courses = Course.objects.filter(
            Q(department=obj.department) &
            Q(semester=obj.semester) &
            Q(year=obj.year) &
            Q(course_type=course_type) &
            Q(status='active')
        )
        selected_courses = getattr(obj, related_name).count()
        total_available = available_courses.count()

        return format_html(
            '<span style="color: {};">Available: {} | Selected: {}</span>',
            '#28a745' if total_available > 0 else '#dc3545',
            total_available,
            selected_courses
        )

    def get_core_course_count(self, obj):
        return self.get_course_count(obj, 'core', 'core_courses')

    get_core_course_count.short_description = 'Core Courses'

    def get_elective_course_count(self, obj):
        return self.get_course_count(obj, 'elective', 'elective_courses')

    get_elective_course_count.short_description = 'Elective Courses'

    def get_open_elective_course_count(self, obj):
        return self.get_course_count(obj, 'open_elective', 'open_elective_courses')

    get_open_elective_course_count.short_description = 'Open Elective Courses'

    def get_honor_course_count(self, obj):
        return self.get_course_count(obj, 'honor', 'honor_courses')

    get_honor_course_count.short_description = 'Honor Courses'

    def get_minor_course_count(self, obj):
        return self.get_course_count(obj, 'minor', 'minor_courses')

    get_minor_course_count.short_description = 'Minor Courses'

    def get_add_on_course_count(self, obj):
        return self.get_course_count(obj, 'add_on', 'add_on_courses')

    get_add_on_course_count.short_description = 'Add On Courses'

    # Add back the status_display method
    def status_display(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; '
                'border-radius: 3px; font-size: 11px;">Active</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px;">Inactive</span>'
        )

    status_display.short_description = 'Status'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['search_query'] = request.GET.get('search') or ''
        return super().changelist_view(request, extra_context)

    def change_form_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['search_query'] = request.GET.get('search') or ''
        return super().change_form_view(request, object_id, form_url, extra_context)

    def lookup_allowed(self, lookup, value):
        if lookup == 'search':
            return True
        return super().lookup_allowed(lookup, value)