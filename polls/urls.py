from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'polls'
urlpatterns = [
    # # http://127.0.0.1:8000/list/ (Generic Class-Based Views) 
    path('', views.QuestionListView.as_view(), name='list'),  # question_list.html
    path('list', views.QuestionListView.as_view(), name='list'),  # question_list.html
    # # http://127.0.0.1:8000/new_post/ (Generic Class-Based Views) 
    path('questions/new', views.NewPostView.as_view(), name='new_post'),  # question_form.html
    # # http://127.0.0.1:8000/edit/ (Generic Class-Based Views) 
    path('questions/<int:pk>', views.EditView.as_view(), name='edit'),  # edit_form.html
    # # http://127.0.0.1:8000/delete/ (Generic Class-Based Views)
    path('questions/<int:pk>/delete', views.RemoveView.as_view(), name='delete'),  # post_confirm_delete.html
    # http://127.0.0.1:8000/2/addChoices/ on click Addvote btn opens a AddChoice View (Function-Based Views)
    path('choices/<int:question_id>/new', views.AddChoices.as_view(), name='addChoices'),

    #http://127.0.0.1:8000/ show frontend index (Class-Based Views) 
    path('index', views.IndexView.as_view(), name='index'),  # index.html
    #http://127.0.0.1:8000/5/ show detail of question with id 5 (Class-Based Views) 
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),  # detail.html
    # http://127.0.0.1:8000/5/results/ show result/votes count for each choices (Class-Based Views)
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'), # result.html
    # http://127.0.0.1:8000/2/vote/ on click vote btn sends a request and apply vote to the choice selected (Function-Based Views)
    path('<int:question_id>/vote/', views.vote, name='vote'), 

    # About & Contacts
    #http://127.0.0.1:8000/about  (Class-Based Views)
    path('about', views.AboutView.as_view(), name='about'),  # about.html
    #http://127.0.0.1:8000/contact (Class-Based Views)
    path('contact', views.ContactView.as_view(), name='contact'),  # contact.html
]
