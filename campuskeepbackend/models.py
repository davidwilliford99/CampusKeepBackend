from django.db import models
from django.contrib.auth.models import User




class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.TextField()
    question1 = models.TextField()
    answer1 = models.TextField()
    question2 = models.TextField()
    answer2 = models.TextField()
    question3 = models.TextField()
    answer3 = models.TextField()
    date_found = models.DateField()
    found_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name




class Message(models.Model):
    content = models.TextField()
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    time_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.from_user.username} to {self.to_user.username} at {self.time_sent}"
    

    

class Claim(models.Model):
    claimed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims_made')
    finder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items_found')
    claim_date = models.DateTimeField(auto_now_add=True)
    item_id = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='claims')
    answer1 = models.TextField(null=True)
    answer2 = models.TextField(null=True)
    answer3 = models.TextField(null=True)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return f"Item {self.item_id.id} claimed by {self.claimed_by.username}"
    
