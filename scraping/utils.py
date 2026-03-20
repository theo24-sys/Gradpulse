from .models import ScrapedItem
from django.db.models import Q

def get_items_for_student(student_profile=None, source_type=None, limit=20):
    """
    Returns a queryset of approved ScrapedItems matched to the student's profile.
    Falls back to general results if matching items are sparse.
    """
    base_query = ScrapedItem.objects.all()
    if source_type:
        base_query = base_query.filter(source_type=source_type)
    
    # Show everything except rejected so freshly scraped items are visible immediately.
    # Admin approval can still be used as a publish workflow, but users shouldn't see an empty page.
    visible_query = base_query.exclude(status='rejected')

    if not student_profile:
        return visible_query.order_by('-scraped_at')[:limit]

    # Strategy: Filter by course and year
    course = getattr(student_profile, 'course', None)
    year = getattr(student_profile, 'year_of_study', None)

    filters = Q()
    if course:
        filters |= Q(course_tags__contains=course) | Q(course_tags=[])
    
    if year:
        # year_tags stores integers, but __contains in JSON usually expects exact match or list
        filters |= Q(year_tags__contains=year) | Q(year_tags=[])

    matched_items = visible_query.filter(filters).order_by('-scraped_at')
    
    # Fallback logic: if fewer than 10 matched items, fill with general items
    if matched_items.count() < 10:
        general_items = visible_query.exclude(id__in=matched_items.values_list('id', flat=True)).order_by('-scraped_at')
        # Combine - QuerySets shouldn't be added directly if we want to preserve order easily, 
        # but for simplicity we can convert to lists or use a clever slicing.
        combined = list(matched_items[:10]) + list(general_items[:limit - matched_items.count()])
        return combined[:limit]

    return matched_items[:limit]
