def copy_week(queryset, username, from_week, week):
    for data in queryset.filter(group__username=username, week_id=from_week).all():
        queryset.create(
            number_pair=data.number_pair,
            subject=data.subject,
            teacher=data.teacher,
            audience=data.audience,
            week=week,
            group=data.group,
            type_pair=data.type_pair,
            day=data.day,
            start_time=data.start_time,
            end_time=data.end_time,
        )
