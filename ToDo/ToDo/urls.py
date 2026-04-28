from django.urls import path, include

urlpatterns = [
    path('', include('tasks.urls')),
    path('', include('accounts.urls'))
]