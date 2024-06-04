from django.urls import path
import conversion_management.views as views

urlpatterns = [
    path('conversion-history/get-all', views.ConversionHistoryListView.as_view(), name='conversion-history-list'),
    path('conversion-history/get/<uuid:id>', views.ConversionHistoryRetrieveByIdView.as_view(), name='conversion-history-retrieve-by-id'),
    path('conversion-history/update', views.ConversionHistoryUpdateView.as_view(), name='conversion-history-update'),
    path('conversion-history/delete/<uuid:id>', views.ConversionHistoryDeleteView.as_view(), name='conversion-history-delete'),
]