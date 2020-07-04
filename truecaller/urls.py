from django.urls import path
from . import views

urlpatterns = [
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('spam',views.report_spam,name='report_spam'),
    path('search-number/<str:number>',views.search_number,name='search_number'),
    path('search-name/<str:name>',views.search_name,name='search_name'),
    path('person-details/<str:number>',views.person_details,name='person_details'),
    path('post-contact',views.post_data,name='post_data')
]