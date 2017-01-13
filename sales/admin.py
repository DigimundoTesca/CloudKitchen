from django.contrib import admin

from sales.models import TicketDetail, Ticket


class TicketDetailInline(admin.TabularInline):
    model = TicketDetail
    extra = 1


@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    list_display = ('created_at', 'seller', 'cash_register',)
    inlines = [TicketDetailInline, ]
