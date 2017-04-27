# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import json
from datetime import date, datetime, timedelta
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Max, Min

from helpers import Helper
from .models import AccessLog, Diner, ElementToEvaluate, SatisfactionRating
from cloudkitchen.settings.base import PAGE_TITLE


class DinersHelper(object):
    def __init__(self):
        super(DinersHelper, self).__init__()
        self.helper = Helper()

    def get_diners(self, initial_date, final_date):
        diners_logs_list = []

        diners_logs_objects = self.get_access_logs(initial_date, final_date)

        for diner_log in diners_logs_objects:
            diner_log_object = {
                'rfid': diner_log.RFID,
                'access': datetime.strftime(timezone.localtime(diner_log.access_to_room), "%B %d, %I, %H:%M:%S %p"),
                'number_day': self.helper.get_number_day(diner_log.access_to_room),
            }
            if diner_log.diner:
                diner_log_object['SAP'] = diner_log.diner.employee_number
                diner_log_object['name'] = diner_log.diner.name
            else:
                diner_log_object['SAP'] = ''
                diner_log_object['name'] = ''
            diners_logs_list.append(diner_log_object)
        return diners_logs_list

    def get_access_logs(self, dt):
        initial_date = self.helper.naive_to_datetime(dt)
        final_date = self.helper.naive_to_datetime(initial_date + timedelta(days=1))
        return AccessLog.objects.filter(access_to_room__range=(initial_date, final_date)).order_by('-access_to_room')

    def get_access_logs_today(self):
        year = int(datetime.now().year)
        month = int(datetime.now().month)
        day = int(datetime.now().day)
        initial_date = self.helper.naive_to_datetime(date(year, month, day))
        final_date = self.helper.naive_to_datetime(initial_date + timedelta(days=1))
        return AccessLog.objects.filter(access_to_room__range=(initial_date, final_date)).order_by('-access_to_room')

    def get_diners_per_hour(self):
        hours_list = []
        hours_to_count = 12
        start_hour = 5
        customer_count = 0
        logs = self.get_access_logs_today()

        while start_hour <= hours_to_count:

            hour = {
                'count': None,
            }

            for log in logs:
                log_datetime = str(log.access_to_room)
                log_date, time = log_datetime.split(" ")
                if time.startswith("0" + str(start_hour)):
                    customer_count += 1
                hour['count'] = customer_count

            hours_list.append(hour)
            customer_count = 0
            start_hour += 1

        return json.dumps(hours_list)

    def get_diners_actual_week(self):
        week_diners_list = []
        total_entries = 0
        days_to_count = self.helper.get_number_day(date.today())
        day_limit = days_to_count
        start_date_number = 0

        while start_date_number <= day_limit:
            day_object = {
                'date': str(self.helper.start_datetime(days_to_count).date().strftime('%d-%m-%Y')),
                'day_name': None,
                'entries': None,
                'number_day': self.helper.get_number_day(self.helper.start_datetime(days_to_count).date())
            }

            logs = AccessLog.objects.filter(
                access_to_room__range=[
                    self.helper.start_datetime(days_to_count), self.helper.end_datetime(days_to_count)
                ])

            for _ in logs:
                total_entries += 1

            day_object['entries'] = str(total_entries)
            day_object['day_name'] = self.helper.get_name_day(self.helper.start_datetime(days_to_count).date())

            week_diners_list.append(day_object)

            # restarting counters
            days_to_count -= 1
            total_entries = 0
            start_date_number += 1

        return json.dumps(week_diners_list)

    @staticmethod
    def get_access_logs(initial_date, final_date):
        return AccessLog.objects.filter(access_to_room__range=(initial_date, final_date)).order_by('-access_to_room')

    @staticmethod
    def get_all_access_logs():
        return AccessLog.objects.all().order_by('-access_to_room')


def diners_paginator(request, queryset, num_pages):
    result_list = Paginator(queryset, num_pages)
    context = {}

    num_page = request.POST.get('num_page', 1)

    if num_page <= 0:
        num_page = 1

    if num_page > result_list.num_pages:
        num_page = result_list.num_pages

    if result_list.num_pages >= num_page:
        page = result_list.page(num_page)

        context = {
            'queryset': page.object_list,
            'num_page': num_page,
            'pages': result_list.num_pages,
            'has_next': page.has_next(),
            'has_prev': page.has_previous(),
            'next_page': num_page + 1,
            'prev_page': num_page - 1,
            'first_page': 1,
        }
    return context


# ------------------------- Django Views ----------------------------- #
@csrf_exempt
def rfid_view(request):
    diners_helper = DinersHelper()
    if request.method == 'POST':
        rfid = str(request.body).split('"')[3].replace(" ", "")
        if settings.DEBUG:
            print(rfid)

        if rfid is None:
            if settings.DEBUG:
                print('no se recibio rfid')
            return HttpResponse('No se recibió RFID\n')
        else:
            access_logs = diners_helper.get_access_logs_today()
            exists = False

            for log in access_logs:
                if rfid == log.RFID:
                    exists = True
                    break

            if exists:
                if settings.DEBUG:
                    print('El usuario ya se ha registrado')
                return HttpResponse('El usuario ya se ha registrado')
            else:
                if len(rfid) < 7:
                    try:
                        diner = Diner.objects.get(RFID=rfid)
                        new_access_log = AccessLog(diner=diner, RFID=rfid)
                        new_access_log.save()
                    except Diner.DoesNotExist:
                        new_access_log = AccessLog(diner=None, RFID=rfid)
                        new_access_log.save()
                else:
                    if settings.DEBUG:
                        print('RFID Inválido\n')
                    return HttpResponse('RFID Inválido\n')

        return HttpResponse('Acceso almacenado\n')

    else:
        return redirect('diners:diners')


@login_required(login_url='users:login')
def diners(request):
    diners_helper = DinersHelper()
    access_logs_today = diners_helper.get_access_logs_today()
    total_diners = access_logs_today.count()

    if request.method == 'POST':
        if request.POST['type'] == 'diners_logs_today':

            diners_queryset = Diner.objects.all()

            diners_objects = {
                'total_diners': total_diners,
                'diners_list': [],
            }

            for diner_log in access_logs_today:
                diner_object = {
                    'rfid': diner_log.RFID,
                    'sap': '',
                    'name': '',
                    'date': timezone.localtime(diner_log.access_to_room).strftime("%B %d, %Y, %I:%M:%S %p"),
                }

                for diner in diners_queryset:
                    if diner_log.RFID == diner.RFID:
                        diner_object['sap'] = diner.employee_number
                        diner_object['name'] = diner.name
                        break

                diners_objects['diners_list'].append(diner_object)

            return JsonResponse(diners_objects)

    else:
        template = 'diners.html'
        title = 'Accesos de hoy'

        context = {
            'title': PAGE_TITLE + ' | ' + title,
            'page_title': title,
            'diners': access_logs_today,
            'total_diners': total_diners,
        }
        return render(request, template, context)


# -------------------------------------- SATISFACTION RATING ------------------------------------------
@login_required(login_url='users:login')
def diners_logs(request):
    helper = Helper()
    diners_helper = DinersHelper()
    all_entries = AccessLog.objects.all()
    all_diners = Diner.objects.all()

    def get_entries(initial_date, final_date):
        """
        Gets the following properties for each week's day: Name, Date and Earnings
        """
        limit_day = initial_date + timedelta(days=1)
        week_diners_list = []
        count = 1
        total_days = (final_date - initial_date).days

        while count <= total_days:
            diners_query = all_entries.filter(access_to_room__range=[initial_date, limit_day])
            day_object = {'date': str(timezone.localtime(initial_date).date().strftime('%d-%m-%Y')),
                          'day_name': helper.get_name_day(initial_date.date()), 'entries': diners_query.count(),
                          'number_day': helper.get_number_day(initial_date)}

            week_diners_list.append(day_object)

            # Reset datas
            limit_day += timedelta(days=1)
            initial_date += timedelta(days=1)
            count += 1

        return week_diners_list

    if request.method == 'POST':
        if request.POST['type'] == 'diners_logs_week':
            initial_date = request.POST['dt_week'].split(',')[0]
            final_date = request.POST['dt_week'].split(',')[1]
            initial_date = helper.parse_to_datetime(initial_date)
            final_date = helper.parse_to_datetime(final_date) + timedelta(days=1)

            diners_logs = diners_helper.get_diners(initial_date, final_date)
            entries = get_entries(initial_date, final_date)
            data = {
                'diners': diners_logs,
                'entries': entries,
            }
            return JsonResponse(data)

        elif request.POST['type'] == 'diners_logs_day':
            """
            Returns a list with objects:
            Each object has the following characteristics
            """
            access_logs_day_list = []
            start_date = helper.naive_to_datetime(datetime.strptime(request.POST['date'], '%d-%m-%Y').date())
            end_date = helper.naive_to_datetime(start_date + timedelta(days=1))
            access_logs = all_entries.filter(access_to_room__range=[start_date, end_date])

            for access_log in access_logs:
                """
                Filling in the sales list of the day
                """
                earnings_sale_object = {
                    'access_id': access_log.id,
                    'datetime': timezone.localtime(access_log.access_to_room),
                    'number_day': helper.get_number_day(start_date),
                }

                access_logs_day_list.append(earnings_sale_object)
            return JsonResponse({'access_logs_day_list': access_logs_day_list})

        elif request.POST['type'] == 'diners_logs':
            diners_objects_list = []

            for entry in all_entries:
                diner_object = {
                    'id': entry.id,
                    'Nombre': '',
                    'RFID': entry.RFID,
                    'SAP': '',
                    'Fecha de Acceso': timezone.localtime(entry.access_to_room).date(),
                    'Hora de Acceso': timezone.localtime(entry.access_to_room).time(),
                }
                for diner in all_diners:
                    if entry.RFID == diner.RFID:
                        diner_object['SAP'] = diner.employee_number
                        diner_object['Nombre'] = diner.name

                diners_objects_list.append(diner_object)

            return JsonResponse({'diner_logs': diners_objects_list})

    else:
        all_diners_objects = diners_helper.get_all_access_logs()
        today_diners_objects = diners_helper.get_access_logs_today()
        total_diners = all_diners_objects.count()
        total_diners_today = today_diners_objects.count()

        def get_dates_range():
            """
            Returns a JSON with a years list.
            The years list contains years objects that contains a weeks list
                and the Weeks list contains a weeks objects with two attributes: 
                start date and final date. Ranges of each week.
            """
            try:
                min_year = all_diners_objects.aggregate(Min('access_to_room'))['access_to_room__min'].year
                max_year = all_diners_objects.aggregate(Max('access_to_room'))['access_to_room__max'].year
                years_list = []  # [2015:object, 2016:object, 2017:object, ...]
            except Exception as e:
                if settings.DEBUG:
                    print('Error:', e)
                return HttpResponse('No hay registros')

            while max_year >= min_year:
                year_object = {  # 2015:object or 2016:object or 2017:object ...
                    'year': max_year,
                    'weeks_list': []
                }

                diners_per_year = all_diners_objects.filter(
                    access_to_room__range=[helper.naive_to_datetime(date(max_year, 1, 1)),
                                           helper.naive_to_datetime(date(max_year, 12, 31))])

                for diner in diners_per_year:
                    if len(year_object['weeks_list']) == 0:
                        """
                        Creates a new week_object in the weeks_list of the actual year_object
                        """
                        week_object = {
                            'week_number': diner.access_to_room.isocalendar()[1],
                            'start_date': diner.access_to_room.date().strftime("%d-%m-%Y"),
                            'end_date': diner.access_to_room.date().strftime("%d-%m-%Y"),
                        }
                        year_object['weeks_list'].append(week_object)

                        # End if
                    else:
                        """
                        Validates if exists some week with an indentical week_number of the actual year
                        If exists a same week in the list validates the start_date and the end_date,
                        In each case valid if there is an older start date or a more current end date 
                            if it is the case, update the values.
                        Else creates a new week_object with the required week number
                        """
                        existing_week = False
                        for week_object in year_object['weeks_list']:
                            if week_object['week_number'] == diner.access_to_room.isocalendar()[1]:
                                # There's a same week number
                                if datetime.strptime(week_object['start_date'],
                                                     "%d-%m-%Y").date() > diner.access_to_room.date():
                                    week_object['start_date'] = diner.access_to_room.date().strftime("%d-%m-%Y")
                                elif datetime.strptime(week_object['end_date'],
                                                       "%d-%m-%Y").date() < diner.access_to_room.date():
                                    week_object['end_date'] = diner.access_to_room.date().strftime("%d-%m-%Y")
                                existing_week = True
                                break

                        if not existing_week:
                            # There's a different week number
                            week_object = {
                                'week_number': diner.access_to_room.isocalendar()[1],
                                'start_date': diner.access_to_room.date().strftime("%d-%m-%Y"),
                                'end_date': diner.access_to_room.date().strftime("%d-%m-%Y"),
                            }
                            year_object['weeks_list'].append(week_object)

                            # End else
                years_list.append(year_object)
                max_year -= 1
            # End while
            return json.dumps(years_list)

        pag = diners_paginator(request, all_diners_objects, 50)
        template = 'diners_logs.html'
        title = 'Registro de Accesos'

        context = {
            'title': PAGE_TITLE + ' | ' + title,
            'page_title': title,
            'diners': pag['queryset'],
            'paginator': pag,
            'total_diners': total_diners,
            'total_diners_today': total_diners_today,
            'diners_hour': diners_helper.get_diners_per_hour(),
            'diners_week': diners_helper.get_diners_actual_week(),
            'dates_range': get_dates_range(),
        }
        return render(request, template, context)


def satisfaction_rating(request):
    if request.method == 'POST':
        if request.POST['type'] == 'satisfaction_rating':
            satisfaction_rating_value = request.POST['satisfaction_rating']
            elements_list = json.loads(request.POST['elements_id'])

            if request.POST['suggestion']:
                new_satisfaction_rating = SatisfactionRating.objects.create(
                    satisfaction_rating=satisfaction_rating_value,
                    suggestion=request.POST['suggestion'],
                )
            else:
                new_satisfaction_rating = SatisfactionRating.objects.create(
                    satisfaction_rating=satisfaction_rating_value
                )
            new_satisfaction_rating.save()

            for element in elements_list:
                new_element = ElementToEvaluate.objects.get(id=element)
                new_satisfaction_rating.elements.add(new_element)
                new_satisfaction_rating.save()
            return JsonResponse({'status': 'ready'})

    template = 'satisfaction_rating.html'
    title = 'Rating'
    elements = ElementToEvaluate.objects.all()
    context = {
        'title': PAGE_TITLE + ' | ' + title,
        'page_title': title,
        'elements': elements,
    }
    return render(request, template, context)


@login_required(login_url='users:login')
def analytics(request):
    helper = Helper()
    all_suggestions = SatisfactionRating.objects.all()
    all_elements = ElementToEvaluate.objects.all()

    def get_dates_range():
        """
        Returns a JSON with a years list.
        The years list contains years objects that contains a weeks list
            and the Weeks list contains a weeks objects with two attributes: 
            start date and final date. Ranges of each week.
        """
        try:
            min_year = all_suggestions.aggregate(Min('creation_date'))['creation_date__min'].year
            max_year = all_suggestions.aggregate(Max('creation_date'))['creation_date__max'].year
            years_list = []  # [2015:object, 2016:object, 2017:object, ...]
        except:
            min_year = datetime.now().year
            max_year = datetime.now().year
            years_list = []  # [2015:object, 2016:object, 2017:object, ...]

        while max_year >= min_year:
            year_object = {  # 2015:object or 2016:object or 2017:object ...
                'year': max_year,
                'weeks_list': []
            }

            ratings_per_year = all_suggestions.filter(
                creation_date__range=[helper.naive_to_datetime(date(max_year, 1, 1)),
                                      helper.naive_to_datetime(date(max_year, 12, 31))])
            for rating in ratings_per_year:
                if len(year_object['weeks_list']) == 0:
                    """
                    Creates a new week_object in the weeks_list of the actual year_object
                    """
                    week_object = {
                        'week_number': rating.creation_date.isocalendar()[1],
                        'start_date': rating.creation_date.date().strftime("%d-%m-%Y"),
                        'end_date': rating.creation_date.date().strftime("%d-%m-%Y"),
                    }
                    year_object['weeks_list'].append(week_object)
                    # End if
                else:
                    """
                    Validates if exists some week with an indentical week_number of the actual year
                    If exists a same week in the list validates the start_date and the end_date,
                    In each case valid if there is an older start date or a more current end date 
                        if it is the case, update the values.
                    Else creates a new week_object with the required week number
                    """
                    existing_week = False
                    for week_object in year_object['weeks_list']:

                        if week_object['week_number'] == rating.creation_date.isocalendar()[1]:
                            # There's a same week number
                            existing_week = True
                            if datetime.strptime(week_object['start_date'],
                                                 "%d-%m-%Y").date() > rating.creation_date.date():
                                exists = True
                                week_object['start_date'] = rating.creation_date.date().strftime("%d-%m-%Y")
                            elif datetime.strptime(week_object['end_date'],
                                                   "%d-%m-%Y").date() < rating.creation_date.date():
                                week_object['end_date'] = rating.creation_date.date().strftime("%d-%m-%Y")

                            existing_week = True
                            break

                    if not existing_week:
                        # There's a different week number
                        week_object = {
                            'week_number': rating.creation_date.isocalendar()[1],
                            'start_date': rating.creation_date.date().strftime("%d-%m-%Y"),
                            'end_date': rating.creation_date.date().strftime("%d-%m-%Y"),
                        }
                        year_object['weeks_list'].append(week_object)

                        # End else
            years_list.append(year_object)
            max_year -= 1
        # End while
        return json.dumps(years_list)

    def get_suggestions_actual_week():
        """
        Gets the following properties for each week's day: Name, Date and suggestions
        """
        week_suggestions_list = []
        total_suggestions = 0
        days_to_count = helper.get_number_day(datetime.now())
        day_limit = days_to_count
        start_date_number = 0

        while start_date_number <= day_limit:
            day_object = {
                'date': str(helper.start_datetime(days_to_count).date().strftime('%d-%m-%Y')),
                'day_name': None,
                'total_suggestions': None,
                'number_day': helper.get_number_day(helper.start_datetime(days_to_count).date()),
            }

            suggestions = all_suggestions.filter(
                creation_date__range=[helper.start_datetime(days_to_count), helper.end_datetime(days_to_count)])

            for suggestion in suggestions:
                if suggestion.suggestion:
                    total_suggestions += 1

            day_object['total_suggestions'] = str(total_suggestions)
            day_object['day_name'] = helper.get_name_day(helper.start_datetime(days_to_count).date())

            week_suggestions_list.append(day_object)

            # restarting counters
            days_to_count -= 1
            total_suggestions = 0
            start_date_number += 1

        return json.dumps(week_suggestions_list)

    def get_suggestions(initial_date, final_date):
        return all_suggestions.filter(
            creation_date__range=(initial_date, final_date)).order_by('-creation_date')

    if request.method == 'POST':
        if request.POST['type'] == 'reactions_day':
            start_date = helper.naive_to_datetime(datetime.strptime(request.POST['date'], '%d-%m-%Y').date())
            end_date = helper.naive_to_datetime(start_date + timedelta(days=1))
            today_suggestions = get_suggestions(start_date, end_date)
            reactions_list = []
            for element_to_evaluate in all_elements:
                """ For every element chart """
                element_object = {
                    'id': element_to_evaluate.id,
                    'name': element_to_evaluate.element,
                    'reactions': {
                        0: {'reaction': 'Enojado', 'quantity': 0},
                        1: {'reaction': 'Triste', 'quantity': 0},
                        2: {'reaction': 'Feliz', 'quantity': 0},
                        3: {'reaction': 'Encantado', 'quantity': 0},
                    },
                }
                for suggestion in today_suggestions:
                    for element_in_suggestion in suggestion.elements.all():
                        if element_in_suggestion == element_to_evaluate:
                            element_object['reactions'][suggestion.satisfaction_rating - 1]['quantity'] += 1

                reactions_list.append(element_object)
            return JsonResponse(reactions_list, safe=False)
    template = 'analytics.html'
    title = 'Analytics'
    context = {
        'title': PAGE_TITLE + ' | ' + title,
        'page_title': title,
        'dates_range': get_dates_range(),
        'suggestions_week': get_suggestions_actual_week(),
        'elements': all_elements,
        'total_elements': all_elements.count(),
    }
    return render(request, template, context)


@login_required(login_url='users:login')
def suggestions(request):
    template = 'suggestions.html'
    title = 'Analytics'
    tests = SatisfactionRating.objects.order_by('-creation_date')
    context = {
        'title': PAGE_TITLE + ' | ' + title,
        'page_title': title,
        'tests': tests,
    }
    return render(request, template, context)


# --------------------------- TEST ------------------------
def test(request):
    diners = Diner.objects.all()
    rfids = []
    for diner in diners:
        if diner.RFID not in rfids:
            rfids.append(diner.RFID)
        else:
            print('malas noticias :( ')
            print(diner.RFID)
    return HttpResponse('Hola')