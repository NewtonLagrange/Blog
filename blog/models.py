from django.db import models


# Create your models here.
class User(models.Model):
    """ 用户: 拥有文章与评论 """
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name


class Paper(models.Model):
    """ 文章: 属于用户, 标签和分类 """
    name = models.CharField(max_length=20)
    content = models.TextField()

    category = models.ForeignKey(to='Category', on_delete=models.CASCADE)
    user = models.ForeignKey(to='User', on_delete=models.CASCADE)
    tag = models.ManyToManyField(to='Tag')

    toc = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    reading = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """ 评论: 属于用户和文章 """
    paper = models.ForeignKey(to='Paper', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class Category(models.Model):
    """ 分类: 拥有文章 """
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """ 标签: 与文章多对多 """
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
