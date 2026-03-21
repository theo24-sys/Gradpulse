from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LibraryItem
from django.db.models import Q

@login_required
def library_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    items = LibraryItem.objects.filter(is_public=True)
    
    if query:
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(course_name__icontains=query))
    if category:
        items = items.filter(category=category)
        
    context = {
        'items': items,
        'query': query,
        'category': category,
        'categories': LibraryItem.CATEGORY_CHOICES,
    }
    return render(request, 'library/list.html', context)

@login_required
def upload_item(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        file = request.FILES.get('file')
        external_link = request.POST.get('external_link')
        institution = request.POST.get('institution', request.user.institution)
        course_name = request.POST.get('course_name', request.user.course)
        
        if not title or not file:
            messages.error(request, "Title and File are required.")
        else:
            LibraryItem.objects.create(
                uploader=request.user,
                title=title,
                description=description,
                category=category,
                file=file,
                external_link=external_link,
                institution=institution,
                course_name=course_name
            )
            messages.success(request, "Resource uploaded successfully!")
            return redirect('library_list')
            
    return render(request, 'library/upload.html', {'categories': LibraryItem.CATEGORY_CHOICES})

@login_required
def item_detail(request, pk):
    item = get_object_or_404(LibraryItem, pk=pk)
    return render(request, 'library/detail.html', {'item': item})

@login_required
def delete_item(request, pk):
    item = get_object_or_404(LibraryItem, pk=pk)
    if item.uploader == request.user or request.user.is_staff:
        item.delete()
        messages.success(request, "Resource deleted.")
    else:
        messages.error(request, "You are not authorized to delete this.")
    return redirect('library_list')
