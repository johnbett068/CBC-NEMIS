from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/', include('accounts.urls', namespace='accounts')),  # <-- include namespace

    # Your apps
    path('', include('home.urls', namespace='home')),
    path('teachers/', include('teachers.urls', namespace='teachers')),
    path('learners/', include('learners.urls', namespace='learners')),
    path('schools/', include('schools.urls', namespace='schools')),
    path('subjects/', include('subjects.urls', namespace='subjects')),
    path('accounts/', include('accounts.urls', namespace='accounts')),

]
