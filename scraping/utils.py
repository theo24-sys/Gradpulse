from .models import ScrapedItem
from django.db.models import Q

def get_items_for_student(student=None, source_type=None, limit=20):
    """
    Returns a list of approved ScrapedItems matched to the student's profile.
    Falls back to general results if matching items are sparse.
    """
    base_query = ScrapedItem.objects.all()
    if source_type:
        base_query = base_query.filter(source_type=source_type)
    
    # Show everything except rejected so freshly scraped items are visible immediately.
    visible_query = base_query.exclude(status='rejected')

    if not student:
        return visible_query.order_by('-scraped_at')[:limit]

    # Strategy: Filter by course and year
    course = getattr(student, 'course', None)
    year = getattr(student, 'year_of_study', None)

    filters = Q()
    if course:
        filters |= Q(course_tags__contains=course) | Q(course_tags=[])
    
    if year:
        # year_tags stores integers in JSON
        filters |= Q(year_tags__contains=year) | Q(year_tags=[])

    matched_items = visible_query.filter(filters).order_by('-scraped_at')
    match_count = matched_items.count()
    
    # Fallback logic: if fewer than 10 matched items, fill with general items
    if match_count < 10:
        matched_list = list(matched_items[:10])
        general_items = visible_query.exclude(id__in=[i.id for i in matched_list]).order_by('-scraped_at')
        combined = matched_list + list(general_items[:limit - len(matched_list)])
        return combined[:limit]

    return matched_items[:limit]
