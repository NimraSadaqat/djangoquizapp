from django.urls import path
from . import views

app_name = 'mcqs'

urlpatterns = [
    path('', views.TestListView.as_view(), name='main-view'),
    path('results', views.ResultListView.as_view(), name='result-view'),
    path('user_results', views.UserResultListView.as_view(), name='user-result-view'),
    # path('result_detail/<str:test_name>/', views.Result_detailListView.as_view(), name='result-detail'),
    path('result_detail/<str:user_name>/<str:test_name>/', views.student_Result_detailListView.as_view(), name='steudent_result_view'),
    path('<pk>/', views.test_view, name='test-view'),
    path('<pk>/save/', views.save_test_view, name='save-view'),
    path('<pk>/data/', views.test_data_view, name='test-data-view'),
    path('test/new/', views.CreateTestView.as_view(), name='test_new'),
    path('test/<pk>/edit/', views.UpdateTestView.as_view(), name='test_edit'),
    path('test/<pk>/delete/', views.DeleteTestView.as_view(), name='test_delete'),
    path('test/upload/<pk>', views.upload_file, name='test_upload-view'),
]
