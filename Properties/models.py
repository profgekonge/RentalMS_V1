from django.db import models

# Create your models here.
class Property(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=25)
    property_manager = models.CharField(max_length=100)
    description = models.CharField(max_length=200,blank=True, null=True)
    # Add additional fields as necessary for the property

    
    def __str__(self):
        return self.name
    
class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="rooms")
    name = models.CharField(max_length=20, blank=True)  # Empty to be filled by save method
    size = models.CharField(max_length=20)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_occupied = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # Generate the room name with prefix and auto numbering
        if not self.name:
            # Get the first three letters of the property's name
            property_prefix = self.property.name[:4].upper()

            # Find the latest room number with that prefix
            last_room = Room.objects.filter(name__startswith=property_prefix).order_by('name').last()
            if last_room:
                # Extract the numeric part from the last room name
                last_number = int(last_room.name[len(property_prefix):])
                new_number = last_number + 1
            else:
                new_number = 1  # Start with 1 if no rooms exist with that prefix

            # Set the new room name
            self.name = f"{property_prefix}{new_number:03}"

        super(Room, self).save(*args, **kwargs)