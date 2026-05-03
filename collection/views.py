from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse
from .models import Location, Visitor, Book
from .forms  import BookForm, VisitorForm


# ── Locations ───────────────────────────────────────────────────────────────

class LocationListView(ListView):
    model               = Location
    template_name       = 'collection/location_list.html'
    context_object_name = 'locations'


class LocationDetailView(DetailView):
    model               = Location
    template_name       = 'collection/location_detail.html'
    context_object_name = 'location'

    # 🔑 KEY CONCEPT: add extra context from related models
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # location.books uses the related_name we set on Book.location
        ctx['books']    = self.object.books.all().select_related('visitor')
        return ctx


# ── Books ───────────────────────────────────────────────────────────────────

class BookListView(ListView):
    model               = Book
    template_name       = 'collection/book_list.html'
    context_object_name = 'books'
    # Eager-load location and visitor to avoid N+1 queries
    queryset            = Book.objects.select_related('location', 'visitor')


class BookCreateView(CreateView):
    model         = Book
    form_class    = BookForm
    template_name = 'collection/book_form.html'
    success_url   = reverse_lazy('book-list')


class BookUpdateView(UpdateView):
    model         = Book
    form_class    = BookForm
    template_name = 'collection/book_form.html'
    success_url   = reverse_lazy('book-list')


class BookDeleteView(DeleteView):
    model         = Book
    template_name = 'collection/book_confirm_delete.html'
    success_url   = reverse_lazy('book-list')


# ── HTMX: live search (returns a partial HTML fragment) ────────────────────

class BookSearchView(ListView):
    model               = Book
    # Returns a partial template, not a full page
    template_name       = 'collection/partials/book_table.html'
    context_object_name = 'books'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        qs = Book.objects.select_related('location', 'visitor')
        if q:
            qs = qs.filter(
                Q(author__icontains=q)  |
                Q(title__icontains=q) |
                Q(location__name__icontains=q)
            )
        return qs
    

    # ── Visitors ────────────────────────────────────────────────────────────────

class VisitorListView(ListView):
    model               = Visitor
    template_name       = 'collection/visitor_list.html'
    context_object_name = 'visitors'
    queryset            = Visitor.objects.prefetch_related('locations')


class VisitorDetailView(DetailView):
    model               = Visitor
    template_name       = 'collection/visitor_detail.html'
    context_object_name = 'visitor'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['books'] = self.object.books.select_related('location', 'visitor')
        return ctx


class VisitorCreateView(CreateView):
    model         = Visitor
    form_class    = VisitorForm
    template_name = 'collection/visitor_form.html'
    success_url   = reverse_lazy('visitor-list')


class VisitorUpdateView(UpdateView):
    model         = Visitor
    form_class    = VisitorForm
    template_name = 'collection/visitor_form.html'
    success_url   = reverse_lazy('visitor-list')


class VisitorDeleteView(DeleteView):
    model         = Visitor
    template_name = 'collection/visitor_confirm_delete.html'
    success_url   = reverse_lazy('visitor-list')


# ── HTMX: inline delete returns empty 200 so HTMX removes the row ──────────

class BookInlineDeleteView(DeleteView):
    model = Book
    http_method_names = ["post"]

    def form_valid(self, form):
        self.object.delete()
        # Return empty response — HTMX replaces the deleted row with nothing
        return HttpResponse('')