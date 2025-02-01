(function ($) {
    $(document).ready(function () {
        // Detect changes in the dependent fields
        $('#id_department, #id_semester, #id_year, #id_regulation').on('change', function () {
            const department = $('#id_department').val();
            const semester = $('#id_semester').val();
            const year = $('#id_year').val();
            const regulation = $('#id_regulation').val();

            // Perform AJAX request to fetch filtered courses
            $.ajax({
                url: '/admin/fetch-courses/', // URL to fetch filtered courses
                type: 'GET',
                data: {
                    department: department,
                    semester: semester,
                    year: year,
                    regulation: regulation,
                },
                success: function (response) {
                    // Update the core_courses dropdown
                    const coreCoursesSelect = $('#id_core_courses');
                    coreCoursesSelect.empty(); // Clear existing options
                    response.core_courses.forEach(function (course) {
                        coreCoursesSelect.append(
                            $('<option>', { value: course.id, text: course.name })
                        );
                    });

                    // Update the elective_courses dropdown
                    const electiveCoursesSelect = $('#id_elective_courses');
                    electiveCoursesSelect.empty(); // Clear existing options
                    response.elective_courses.forEach(function (course) {
                        electiveCoursesSelect.append(
                            $('<option>', { value: course.id, text: course.name })
                        );
                    });
                },
                error: function () {
                    alert('Error fetching courses. Please try again.');
                },
            });
        });
    });
})(django.jQuery);
