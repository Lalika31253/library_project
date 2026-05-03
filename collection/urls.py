from django.urls import path
from . import views

urlpatterns = [
    # Locations
    path('',                 views.LocationListView.as_view(),  name='location-list'),
    path('location/<int:pk>/', views.LocationDetailView.as_view(), name='location-detail'),

    # Books
    path('books/',                    views.BookListView.as_view(),       name='book-list'),
    path('books/<int:pk>/',           views.BookDetailView.as_view(),     name='book-detail'),
    path('book/add/',                views.BookCreateView.as_view(),     name='book-create'),
    path('books/<int:pk>/edit/',      views.BookUpdateView.as_view(),     name='book-update'),
    path('books/<int:pk>/delete/',    views.BookDeleteView.as_view(),     name='book-delete'),
    path('books/<int:pk>/inline-delete/',
                                     views.BookInlineDeleteView.as_view(),
                                     name='book-inline-delete'),
    # HTMX search endpoint
    path('books/search/',             views.BookSearchView.as_view(),     name='book-search'),

    # Visitors
    path('visitors/',                 views.VisitorListView.as_view(),    name='visitor-list'),
    path('visitors/<int:pk>/',        views.VisitorDetailView.as_view(),  name='visitor-detail'),
    path('visitors/add/',             views.VisitorCreateView.as_view(),  name='visitor-create'),
    path('visitors/<int:pk>/edit/',   views.VisitorUpdateView.as_view(),  name='visitor-update'),
    path('visitors/<int:pk>/delete/', views.VisitorDeleteView.as_view(),  name='visitor-delete'),
]