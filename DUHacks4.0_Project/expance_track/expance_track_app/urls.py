from django.urls import path
from .import views
urlpatterns = [
    path('',views.loginPage,name='login'),   
    path('sign_up',views.signUp,name = 'signUp'),
    path('mainPage',views.mainPage,name = 'mainPage'),
    path('add_expence',views.add_expence,name = 'add_expence'),
    path('edit_expence/<int:expence_id>',views.edit_expence,name = 'edit_expence'),
     path("delete-expence/<int:expence_id>/", views.delete_expence, name="delete_expence"),
]