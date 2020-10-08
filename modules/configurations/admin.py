from django.contrib import admin
from .models import Ratings, StaticPages, MusicGenre, Instrument, EmailTemplate, Setting
from django.utils.html import format_html
# Register your models here.



class EmailTemplateAdmin(admin.ModelAdmin):
	def edit(self, obj):
  		return format_html('<button type="button" class="btn btn-warning btn-xs"><a class="btn" href="/admin/configurations/emailtemplate/{}/change/">Edit</a></button>', obj.id)

	def delete(self, obj):
  		return format_html('<button type="button" class="btn btn-danger btn-xs"><a class="btn" href="/admin/configurations/emailtemplate/{}/delete/">Delete</a></button>', obj.id)

	list_display=['template_name', 'email_subject', 'created_at','edit','delete']

admin.site.register(EmailTemplate, EmailTemplateAdmin)


class StaticPagesAdmin(admin.ModelAdmin):

	def edit(self, obj):
  		return format_html('<button type="button" class="btn btn-warning btn-xs"><a class="btn" href="/admin/configurations/staticpages/{}/change/">Edit</a></button>', obj.id)

	def delete(self, obj):
  		return format_html('<button type="button" class="btn btn-danger btn-xs"><a class="btn" href="/admin/configurations/staticpages/{}/delete/">Delete</a></button>', obj.id)

	list_display=['template_name', 'created_at','edit','delete']

admin.site.register(StaticPages, StaticPagesAdmin)


class RatingAdmin(admin.ModelAdmin):
	list_display=['teacher', 'student', 'rating', 'comment', 'is_verified']

	def has_add_permission(self, obj):
		return False

admin.site.register(Ratings, RatingAdmin)


class MusicGenreAdmin(admin.ModelAdmin):
	def edit(self, obj):
  		return format_html('<button type="button" class="btn btn-warning btn-xs"><a class="btn" href="/admin/configurations/musicgenre/{}/change/">Edit</a></button>', obj.id)

	def delete(self, obj):
  		return format_html('<button type="button" class="btn btn-danger btn-xs"><a class="btn" href="/admin/configurations/musicgenre/{}/delete/">Delete</a></button>', obj.id)
	list_display=['name', 'created_at','edit','delete']

admin.site.register(MusicGenre, MusicGenreAdmin)

class InstrumentAdmin(admin.ModelAdmin):
	def edit(self, obj):
  		return format_html('<button type="button" class="btn btn-warning btn-xs"><a class="btn" href="/admin/configurations/instrument/{}/change/">Edit</a></button>', obj.id)

	def delete(self, obj):
  		return format_html('<button type="button" class="btn btn-danger btn-xs"><a class="btn" href="/admin/configurations/instrument/{}/delete/">Delete</a></button>', obj.id)

	list_display=['name', 'created_at', 'edit', 'delete']

admin.site.register(Instrument, InstrumentAdmin)

class SettingAdmin(admin.ModelAdmin):
	list_display = ('configuration', 'amount')

admin.site.register(Setting, SettingAdmin)

