from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.city})"


class Visitor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # ManyToManyField: a  visitor can got to multiple Locations
    locations = models.ManyToManyField(
        Location,
        related_name="visitors",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    CATEGORY_CHOICES = [
        ("fantasy", "Fantasy"),
        ("thriller", "Thriller"),
        ("detective", "Detective"),
        ("novel", "Novel"),
        ('other', 'Other'),
    ]

    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default="other",
    )
    # ForeignKey: each book belongs to one location
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="books",  # location.books.all()
    )
    # ForeignKey: each book is managed by one visitor (user)
    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="books",  # visitor.books.all()
    )

    def __str__(self):
        return f"{self.author} {self.title} {self.category}"
    
    
