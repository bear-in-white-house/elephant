# from django.db import models
# from account.models import Account
#
#
# class Bar(models.Model):
#     name = models.CharField(unique=True, max_length=100)
#     avatar = models.FileField(null=True, blank=True)
#     admins = models.ManyToManyField(Account, related_name='admins_bars')
#     vice_admins = models.ManyToManyField(Account, related_name='vice_admins_bars')
#
#
# class Article(models.Model):
#     bar = models.ForeignKey(Bar, on_delete=models.CASCADE, related_name='articles')
#     title = models.CharField(max_length=100)
#     text = models.TextField()