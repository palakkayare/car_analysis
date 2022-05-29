from django.urls import path
from .views import upload_file_view , analysis_view, show_csv_data, show_cleaned_csv_data, index_view, cluster_analysis_view, clustered_data_view

app_name = 'perform_analysis'

urlpatterns= [
    path('',upload_file_view, name='upload-view'),
    path('analysis_view/', analysis_view, name="analysis_view"),
    path('cluster_analysis_view/', cluster_analysis_view, name="cluster_analysis_view"),
    path('clustered_data_view', clustered_data_view, name="clustered_data_view"),
    path("show_csv_data/", show_csv_data, name="show_csv_data"),
    path("show_cleaned_csv_data", show_cleaned_csv_data, name="show_cleaned_csv_data"),
    path("index_view", index_view, name="index_view")    
]