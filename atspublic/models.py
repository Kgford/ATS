from django.db import models
 
# Create your models here.
#https://www.skysilk.com/blog/2017/how-to-make-a-blog-with-django/#:~:text=Django%20Blog%201%20Installing%20Django.%20First%20login%20to,small%20handful%20of%20its%20functionality%20in%20this%20example.
 
class Blog(models.Model):
   title = models.CharField(max_length=100, unique=True)
   slug = models.SlugField(max_length=100, unique=True)
   body = models.TextField()
   posted = models.DateTimeField(db_index=True, auto_now_add=True)
   category = models.ForeignKey('blog.Category')
 
   def __unicode__(self):
       return '%s' % self.title
 
  
   def get_absolute_url(self):
       return ('view_blog_post', None, { 'slug': self.slug })
 
class Category(models.Model):
   title = models.CharField(max_length=100, db_index=True)
   slug = models.SlugField(max_length=100, db_index=True)
 
   def __unicode__(self):
       return '%s' % self.title
 
  
   def get_absolute_url(self):
       return ('view_blog_category', None, { 'slug': self.slug })