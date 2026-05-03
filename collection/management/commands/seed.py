from django.core.management.base import BaseCommand
from collection.models import Location, Visitor, Book


class Command(BaseCommand):
    def handle(self, *args, **options):

        # ── Locations
        l1 = Location.objects.create(name="Central Library", city="Edmonton")
        l2 = Location.objects.create(name="North Branch", city="Edmonton")
        l3 = Location.objects.create(name="Downtown Hub", city="Calgary")
        l4 = Location.objects.create(name="Westside Library", city="Calgary")

        # ── Visitors
        v1 = Visitor.objects.create(first_name="Bob", last_name="Marley")
        v2 = Visitor.objects.create(first_name="Anna", last_name="Smith")
        v3 = Visitor.objects.create(first_name="Alex", last_name="Brown")
        v4 = Visitor.objects.create(first_name="Emily", last_name="Roy")
        v5 = Visitor.objects.create(first_name="Sara", last_name="Parker")
        v6 = Visitor.objects.create(first_name="Taylor", last_name="Swift")
        v7 = Visitor.objects.create(first_name="Daniel", last_name="Lee")
        v8 = Visitor.objects.create(first_name="Sophia", last_name="Martin")

        # ManyToMany (Visitor ↔ Location)
        v1.locations.set([l1, l2])
        v2.locations.set([l1, l3])
        v3.locations.set([l2, l3])
        v4.locations.set([l1, l4])
        v5.locations.set([l2])
        v6.locations.set([l3, l4])
        v7.locations.set([l1, l2, l3])
        v8.locations.set([l4])

        # ── Books
        books_data = [
            ("George Orwell", "1984", "novel", l1, v1),
            ("J.K. Rowling", "Harry Potter 1", "fantasy", l1, v2),
            ("J.K. Rowling", "Harry Potter 2", "fantasy", l2, v3),
            ("Tolkien", "The Hobbit", "fantasy", l2, v6),
            ("Tolkien", "Lord of the Rings", "fantasy", l3, v7),
            ("Agatha Christie", "Murder on the Orient Express", "thriller", l3, v4),
            ("Dan Brown", "The Da Vinci Code", "thriller", l1, v8),
            ("Stephen King", "The Shining", "thriller", l4, v2),
            ("Harper Lee", "To Kill a Mockingbird", "novel", l2, v8),
            ("Isaac Asimov", "Foundation", "novel", l2, v1),
        ]

        for author, title, category, location, visitor in books_data:
            Book.objects.create(
                author=author,
                title=title,
                category=category,
                location=location,
                visitor=visitor,
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))