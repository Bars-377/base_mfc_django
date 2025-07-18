from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib import messages
from asgiref.sync import sync_to_async
from .models import Services, Services_Two, Services_Three
import asyncio
from .common import format_number, log_user_action, errors
from django.shortcuts import render
from django.db.models import Sum

class ContractProcessor:
    def __init__(self, context_data=None, request=None):
        self.context_data = context_data
        self.request = request

    async def validate_execution_plan(self):
        execution_contract_plan = await self.calculate_execution_plan()
        if self.context_data['contract_price']:
            if f"{execution_contract_plan:.2f}" != f"{float(self.context_data['contract_price']):.2f}":
                # print('POPAL 1')
                return False
        # print('POPAL 2')
        return True

    async def validate_execution_plan_message(self):
        # await sync_to_async(messages.error)(self.request, 'Значение поля «Исполнение контракта (план) должно равняться полю «Цена контракта»')
        messages.error(self.request, 'Значение поля «Исполнение контракта (план) должно равняться полю «Цена контракта»')

    async def validate_execution_fact(self):
        execution_contract_plan = await self.calculate_execution_plan()
        execution_contract_fact = await self.calculate_execution_fact()
        if execution_contract_plan != execution_contract_fact and self.context_data['status'] == 'Исполнено':
            return False
        return True

    async def validate_execution_fact_message(self):
        # await sync_to_async(messages.error)(self.request, 'Нельзя выставить статус "Исполнено" при неравенстве ячеек «Исполнение контракта (факт)» и «Исполнение контракта (план)»')
        messages.error(self.request, 'Нельзя выставить статус "Исполнено" при неравенстве ячеек «Исполнение контракта (факт)» и «Исполнение контракта (план)»')

    async def validate_Services_Two(self):
        try:
            from django.db.models import Q

            Services_Two_ = await sync_to_async(Services_Two.objects.get, thread_sensitive=True)(
                Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
            )
            return Services_Two_
        except:
            return False

    async def validate_Services_Two_message(self):
        # await sync_to_async(messages.error)(self.request, 'Нет сопоставления КОСГУ с ДопФК')
        messages.error(self.request, 'Нет сопоставления КОСГУ с ДопФК')

    async def validate_Services(self):
        from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
        # Создаем новый словарь с ключами, добавляющими '__iexact'
        # Удаляем ненужные ключи из self.context_data
        if isinstance(self.context_data, list):
            first_row = self.context_data[0]  # теперь это словарь
            page = first_row.get('page', 1)
            page_user = first_row.get('page_user', 1)
            page_user_two = first_row.get('page_user_two', 1)
        else:
            page = self.context_data.get('page', 1)
            page_user = self.context_data.get('page_user', 1)
            page_user_two = self.context_data.get('page_user_two', 1)
            statuses = self.context_data.get('statuses', None)
        # keys_to_remove = ['execution',
        #                     'contract_balance',
        #                     'execution_contract_fact',
        #                     'execution_contract_plan',
        #                     'color',
        #                     'page',
        #                     'keyword_one',
        #                     'keyword_two',
        #                     'keyword_three',
        #                     'keyword_four',
        #                     'selected_end_date',
        #                     'selected_column_one',
        #                     'selected_column_two',
        #                     'page_user',
        #                     # 'KOSGU_user',
        #                     # 'keyword_one_user',
        #                     # 'keyword_two_user',
        #                     # 'selected_column_one_user',
        #                     # 'selected_column_two_user',
        #                     'page_user_two',
        #                     # 'KOSGU_user_two',
        #                     # 'keyword_one_user_two',
        #                     # 'keyword_two_user_two',
        #                     # 'selected_column_one_user_two',
        #                     # 'selected_column_two_user_two',
        #                     'connection_websocket',
        #                     'statuses']

        # Получаем список полей модели Services
        model_fields = {f.name for f in Services._meta.get_fields()}

        if isinstance(self.context_data, list):
            # filter_kwargs = {f"{key}__iexact": value for key, value in self.context_data[0].items()}

            filter_kwargs = {
                f"{k}__iexact": v
                for k, v in self.context_data[0].items()
                if k in model_fields
            }

        else:
            # for key in keys_to_remove:
            #     self.context_data.pop(key, None)  # Удаляем ключ, если он существует
            # filter_kwargs = {f"{key}__iexact": value for key, value in self.context_data.items()}

            filter_kwargs = {
                f"{k}__iexact": v
                for k, v in self.context_data.items()
                if k in model_fields
            }

            self.context_data['page'] = page
            self.context_data['page_user'] = page_user
            self.context_data['page_user_two'] = page_user_two
            self.context_data['statuses'] = statuses
        try:
            Services_ = await sync_to_async(Services.objects.get, thread_sensitive=True)(**filter_kwargs)
            return False
        except MultipleObjectsReturned:
            Services_ = await sync_to_async(lambda: Services.objects.filter(**filter_kwargs).first())()
            return False
        except ObjectDoesNotExist:
            return True

    async def validate_Services_message(self):
        # await sync_to_async(messages.error)(self.request, 'Вы добавляете дубликат в Наименовании')
        messages.error(self.request, 'Вы добавляете дубликат Закупки')

    async def calculate_execution_plan(self):
        """Суммирование исполнение контракта (план)"""
        months = [self.context_data[month] for month in [
            'january_one', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december',
            # 'january_two'
        ]]
        cleaned_numbers = await asyncio.gather(*(format_number(month) for month in months))
        return sum(cleaned_numbers)

        # cleaned_numbers = await format_number(self.context_data['remainder_old_year']) - await format_number(self.context_data['january_two'])
        # return sum(cleaned_numbers)

    async def calculate_execution_fact(self):
        """Суммирование исполнение контракта (факт)"""
        sum_months = [self.context_data[month] for month in [
            'sum_january_one', 'sum_february', 'sum_march', 'sum_april', 'sum_may', 'sum_june',
            'sum_july', 'sum_august', 'sum_september', 'sum_october', 'sum_november', 'sum_december',
            # 'sum_january_two'
        ]]
        cleaned_numbers = await asyncio.gather(*(format_number(month) for month in sum_months))
        return sum(cleaned_numbers) + await format_number(self.context_data['paid_last_year'])
        # return sum(cleaned_numbers)

    async def update_service(self, saving, execution_contract_plan, execution_contract_fact):
        """Подсчёт Исполнение контракта (план) (формула) и Исполнение контракта (факт) (формула) и обновление записи"""
        service = self.context_data['service']

        # Обновляем значения в self.context_data
        self.context_data['saving'] = saving
        self.context_data['execution_contract_plan'] = execution_contract_plan
        self.context_data['execution_contract_fact'] = execution_contract_fact

        for key, value in self.context_data.items():
            setattr(service, key, value)

        if (await format_number(service.execution_contract_fact) > await format_number(service.execution_contract_plan)) \
            or (await format_number(service.january_one) < await format_number(service.sum_january_one)) \
            or (await format_number(service.february) < await format_number(service.sum_february)) \
            or (await format_number(service.march) < await format_number(service.sum_march)) \
            or (await format_number(service.april) < await format_number(service.sum_april)) \
            or (await format_number(service.may) < await format_number(service.sum_may)) \
            or (await format_number(service.june) < await format_number(service.sum_june)) \
            or (await format_number(service.july) < await format_number(service.sum_july)) \
            or (await format_number(service.august) < await format_number(service.sum_august)) \
            or (await format_number(service.september) < await format_number(service.sum_september)) \
            or (await format_number(service.november) < await format_number(service.sum_november)) \
            or (await format_number(service.december) < await format_number(service.sum_december)) \
            or (await format_number(service.january_two) < await format_number(service.sum_january_two)):
            service.color = '#ffebeb'
        elif service.color == '#ffebeb':
            service.color = ''

        await sync_to_async(service.save)()

    async def creation_new_service(self, saving, execution_contract_plan, execution_contract_fact, new_service):
        """Формируем запрос для новой записи"""
        from django.db import connection

        # Сделать синхронную функцию асинхронной
        @sync_to_async
        # Получаем следующий ID
        def get_latest_service():
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id_id FROM services
                    WHERE id_id REGEXP '^[0-9]+$'
                    ORDER BY CAST(id_id AS UNSIGNED) DESC
                    LIMIT 1
                """)
                row = cursor.fetchone()
                return row

        latest_service = await get_latest_service()

        try:
            id_id = (int(latest_service[0]) + 1) if latest_service and latest_service[0].isdigit() else 1
        except ValueError:
            # В случае некорректного значения установить id_id на 1
            id_id = 1

        await log_user_action(self.request.user, f'Добавил запись в "Закупки" с ID {id_id}')

        contract_balance = await format_number(self.context_data['contract_price']) - await format_number(execution_contract_fact)

        # Добавляем id_id в объект new_service
        setattr(new_service, 'id_id', id_id)
        for key, value in self.context_data.items():
            if key == saving:
                setattr(new_service, key, saving)
            elif key == execution_contract_plan:
                setattr(new_service, key, execution_contract_plan)
            elif key == execution_contract_fact:
                setattr(new_service, key, execution_contract_fact)
            else:
                setattr(new_service, key, value)
        # Добавляем contract_balance в объект new_service
        setattr(new_service, 'contract_balance', contract_balance)

        if (await format_number(new_service.execution_contract_fact) > await format_number(new_service.execution_contract_plan)) \
            or (await format_number(new_service.january_one) < await format_number(new_service.sum_january_one)) \
            or (await format_number(new_service.february) < await format_number(new_service.sum_february)) \
            or (await format_number(new_service.march) < await format_number(new_service.sum_march)) \
            or (await format_number(new_service.april) < await format_number(new_service.sum_april)) \
            or (await format_number(new_service.may) < await format_number(new_service.sum_may)) \
            or (await format_number(new_service.june) < await format_number(new_service.sum_june)) \
            or (await format_number(new_service.july) < await format_number(new_service.sum_july)) \
            or (await format_number(new_service.august) < await format_number(new_service.sum_august)) \
            or (await format_number(new_service.september) < await format_number(new_service.sum_september)) \
            or (await format_number(new_service.november) < await format_number(new_service.sum_november)) \
            or (await format_number(new_service.december) < await format_number(new_service.sum_december)) \
            or (await format_number(new_service.january_two) < await format_number(new_service.sum_january_two)):
            new_service.color = '#ffebeb'
        elif new_service.color == '#ffebeb':
            new_service.color = ''

        return new_service

    async def creation_new_service_two(self):

        new_service_Two = Services_Two()
        new_service_Three = Services_Three()

        """Формируем запрос для новой записи"""
        from django.db import connection

        # print('POPAL')
        # print(self.context_data)

        # Сделать синхронную функцию асинхронной
        @sync_to_async
        # Получаем следующий ID
        def get_latest_service(string):
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    SELECT id_id FROM {string}
                    WHERE id_id REGEXP '^[0-9]+$'
                    ORDER BY CAST(id_id AS UNSIGNED) DESC
                    LIMIT 1
                """)
                row = cursor.fetchone()
                return row

        latest_service_two, latest_service_three = await get_latest_service('services_two'), await get_latest_service('services_three')

        try:
            id_id_two = (int(latest_service_two[0]) + 1) if latest_service_two and latest_service_two[0].isdigit() else 1
        except ValueError:
            # В случае некорректного значения установить id_id на 1
            id_id_two = 1

        try:
            id_id_three = (int(latest_service_three[0]) + 1) if latest_service_three and latest_service_three[0].isdigit() else 1
        except ValueError:
            # В случае некорректного значения установить id_id на 1
            id_id_three = 1

        await log_user_action(self.request.user, f'Добавил запись в "Свод" с ID {id_id_two}')

        # Добавляем id_id в объект new_service
        setattr(new_service_Two, 'id_id', id_id_two)
        for key, value in self.context_data.items():
            setattr(new_service_Two, key, value)

        # Добавляем id_id в объект new_service
        self.context_data.pop('name', None)
        setattr(new_service_Three, 'id_id', id_id_three)
        for key, value in self.context_data.items():
            setattr(new_service_Three, key, value)

        await sync_to_async(new_service_Two.save)()
        await sync_to_async(new_service_Three.save)()

        return

    async def calculate_contract_sums(self, KTSSR, status):
        """Получаем сумму всех contract_price либо execution_contract_fact"""
        from django.db.models import Q

        # Общий фильтр для обоих случаев
        filters = Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC']) & Q(KTSSR=KTSSR)

        if status:
            filters &= Q(status=status)
            # field_to_sum = 'contract_price'

            months_contract_price = (
                'january_one', 'february', 'march', 'april', 'may', 'june',
                'july', 'august', 'september', 'october', 'november', 'december',
                # 'january_two'
            )

            answer = 0
            for contract_price in months_contract_price:
                total_sum = await sync_to_async(self._aggregate_sum)(filters, contract_price)
                answer += await format_number(total_sum if total_sum not in [None, 'None', ''] else 0)
                # if KTSSR == '2046102280' and status == 'Запланировано':
                #     print('answer', answer)

        else:
            # field_to_sum = 'execution_contract_fact'

            months_execution_contract_fact = (
                'sum_january_one', 'sum_february', 'sum_march', 'sum_april', 'sum_may', 'sum_june',
                'sum_july', 'sum_august', 'sum_september', 'sum_october', 'sum_november', 'sum_december',
                # 'sum_january_two'
            )

            answer = 0
            for execution_contract_fact in months_execution_contract_fact:
                total_sum = await sync_to_async(self._aggregate_sum)(filters, execution_contract_fact)
                answer += await format_number(total_sum if total_sum not in [None, 'None', ''] else 0)

        # # Асинхронно выполняем агрегацию
        # total_sum = await sync_to_async(self._aggregate_sum)(filters, field_to_sum)

        # Очищаем число, если это необходимо
        return round(answer, 2)
        # return await clean_number(total_sum if total_sum not in [None, 'None', ''] else 0)

    def _aggregate_sum(self, filters, field_to_sum):
        return Services.objects.filter(filters).aggregate(total_sum=Sum(field_to_sum, default=0))['total_sum']

    async def process_budget_services_two(self, Services_Two_):
        """Обновление второй базы"""
        # Создаем список месяцев
        budget = [
            Services_Two_.budget_limit if Services_Two_.budget_limit not in [None, 'None', ''] else 0,
            Services_Two_.budget_bargaining if Services_Two_.budget_bargaining not in [None, 'None', ''] else 0,
            Services_Two_.budget_concluded if Services_Two_.budget_concluded not in [None, 'None', ''] else 0,
            Services_Two_.budget_completed if Services_Two_.budget_completed not in [None, 'None', ''] else 0
        ]

        # Асинхронно обрабатываем все месяцы
        cleaned_numbers = await asyncio.gather(*(format_number(number) for number in budget))

        # print('--------------------------------')
        # print(cleaned_numbers[0])
        # print(sum(cleaned_numbers[1:]))
        # print('--------------------------------')

        # Суммируем результат
        Services_Two_.budget_remainder = round(await format_number(cleaned_numbers[0] - sum(cleaned_numbers[1:])), 2)

        # Создаем список месяцев
        off_budget = [
            Services_Two_.off_budget_limit if Services_Two_.off_budget_limit not in [None, 'None', ''] else 0,
            Services_Two_.off_budget_bargaining if Services_Two_.off_budget_bargaining not in [None, 'None', ''] else 0,
            Services_Two_.off_budget_concluded if Services_Two_.off_budget_concluded not in [None, 'None', ''] else 0,
            Services_Two_.off_budget_completed if Services_Two_.off_budget_completed not in [None, 'None', ''] else 0
        ]

        # Асинхронно обрабатываем все месяцы
        cleaned_numbers = await asyncio.gather(*(format_number(number) for number in off_budget))

        # Суммируем результат
        Services_Two_.off_budget_remainder = round(await format_number(cleaned_numbers[0] - sum(cleaned_numbers[1:])), 2)

        # Расчет планов
        Services_Two_.budget_plans = round(await format_number(await format_number(Services_Two_.budget_remainder) - await format_number(Services_Two_.budget_planned)), 2)
        Services_Two_.off_budget_plans = round(await format_number(await format_number(Services_Two_.off_budget_remainder) - await format_number(Services_Two_.off_budget_planned)), 2)

        # def has_more_than_two_decimals(number):
        #     # Преобразуем число в строку
        #     s = str(number)

        #     # Проверяем, есть ли десятичная точка
        #     if '.' in s:
        #         # Получаем количество знаков после десятичной точки
        #         decimal_part = s.split('.')[1]
        #         return len(decimal_part) > 2
        #     else:
        #         return False
        # if has_more_than_two_decimals(await clean_number(Services_Two_.budget_remainder) - await clean_number(Services_Two_.budget_planned)):
        #     print(f"Число {await clean_number(Services_Two_.budget_remainder) - await clean_number(Services_Two_.budget_planned)} имеет больше двух знаков после запятой.")
        #     exit()

        if any(x < 0 for x in [await format_number(Services_Two_.budget_remainder),
                            await format_number(Services_Two_.off_budget_remainder)
                            # await clean_number(Services_Two_.budget_plans),
                            # await clean_number(Services_Two_.off_budget_plans)
                            ]):
            Services_Two_.color = '#ffebeb'
        else:
            Services_Two_.color = ''

        await sync_to_async(Services_Two_.save)()

    async def process_budget_services_three(self, budget_concluded):
        """Обновление третьей базы"""
        try:

            from django.db.models import Q

            Services_Three_ = await sync_to_async(Services_Three.objects.get, thread_sensitive=True)(
                Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC'])
            )

            if budget_concluded:
                contract_price_sum_way = await self.Services_way()

                if self.context_data['KTSSR'] == '2046100092':
                    Services_Three_.off_budget_concluded = contract_price_sum_way
                elif self.context_data['KTSSR'] == '2046102280':
                    Services_Three_.budget_concluded = contract_price_sum_way

            Services_Three_.budget_remainder = round(await format_number(await format_number(Services_Three_.budget_planned) + await format_number(Services_Three_.budget_planned_old) - await format_number(Services_Three_.budget_concluded)), 2)
            Services_Three_.off_budget_remainder = round(await format_number(await format_number(Services_Three_.off_budget_planned) + await format_number(Services_Three_.off_budget_planned_old) - await format_number(Services_Three_.off_budget_concluded)), 2)

            if any(x < 0 for x in [await format_number(Services_Three_.budget_remainder),
                                await format_number(Services_Three_.off_budget_remainder)
                                # await clean_number(Services_Three_.budget_planned),
                                # await clean_number(Services_Three_.off_budget_planned)
                                ]):
                Services_Three_.color = '#ffebeb'
            else:
                Services_Three_.color = ''

            await sync_to_async(Services_Three_.save)()

        except Exception as e:
            errors(e)

    async def message_service_update(self):
        # await sync_to_async(messages.success)(self.request, "Редактирование прошло успешно!")
        messages.success(self.request, "Редактирование прошло успешно!")

    async def message_service_add(self):
        # await sync_to_async(messages.success)(self.request, "Данные успешно добавлены!")
        messages.success(self.request, "Данные успешно добавлены!")

    async def message_service_delete(self):
        # await sync_to_async(messages.success)(self.request, "Данные успешно удалены!")
        messages.success(self.request, "Данные успешно удалены!")

    # async def aggregate_fields(self, fields):
    #     """Суммирование столбцов"""
    #     filters = {
    #         'KOSGU': self.context_data.get('KOSGU'),
    #         'DopFC': self.context_data.get('DopFC'),
    #         # 'KTSSR': self.context_data.get('KTSSR'),
    #     }
    #     results = {}
    #     # for field in fields:
    #     #     # Асинхронно выполняем агрегацию по каждому полю
    #     #     result = await sync_to_async(lambda: Services_Two.objects.aggregate(**{f'{field}__sum': Sum(field)}), thread_sensitive=True)()
    #     #     # Получаем значение суммы или 0, если оно None
    #     for field in fields:
    #         result = await sync_to_async(
    #             lambda: Services_Two.objects.filter(**filters).aggregate(**{f'{field}__sum': Sum(field)}),
    #             thread_sensitive=True
    #         )()
    #         results[field] = result[f'{field}__sum'] or 0.0
    #     return results

    async def aggregate_fields(self, fields):
        """Получение фильтрованных данных без агрегации"""
        filters = {
            'KOSGU': self.context_data.get('KOSGU'),
            'DopFC': self.context_data.get('DopFC'),
            # 'KTSSR': self.context_data.get('KTSSR'),
        }

        results = {}
        for field in fields:
            # Получаем значения поля по фильтру
            values = await sync_to_async(
                lambda: list(Services_Two.objects.filter(**filters).values_list(field, flat=True)),
                thread_sensitive=True
            )()
            # results[field] = float(values[0])
            value_str = values[0] if values[0] != '' else None
            if value_str is not None:
                results[field] = float(value_str)
            else:
                results[field] = 0.00
        return results

    async def total_costs(self, new_service):
        """Удаление новой записи если условия соответствуют"""
        # Определите список всех полей, которые нужно агрегировать
        fields = [
            'budget_limit',
            'off_budget_limit',
            'budget_planned',
            'off_budget_planned',
            'budget_bargaining',
            'off_budget_bargaining',
            'budget_concluded',
            'off_budget_concluded',
            'budget_completed',
            'off_budget_completed'
        ]

        # Вызов функции для выполнения агрегации
        aggregated_results = await self.aggregate_fields(fields)

        # Теперь вы можете получить значения из aggregated_results
        total_costs_calc = {
        'total_cost_1': aggregated_results['budget_limit'],
        'total_cost_2': aggregated_results['off_budget_limit'],
        'total_cost_3': aggregated_results['budget_planned'],
        'total_cost_4': aggregated_results['off_budget_planned'],
        'total_cost_5': aggregated_results['budget_bargaining'],
        'total_cost_6': aggregated_results['off_budget_bargaining'],
        'total_cost_7': aggregated_results['budget_concluded'],
        'total_cost_8': aggregated_results['off_budget_concluded'],
        'total_cost_9': aggregated_results['budget_completed'],
        'total_cost_10': aggregated_results['off_budget_completed']
        }

        # print(total_costs_calc['total_cost_2'])
        # print('--------------------')
        # print(total_costs_calc['total_cost_4'])
        # print(total_costs_calc['total_cost_6'])
        # print(total_costs_calc['total_cost_8'])
        # print(total_costs_calc['total_cost_10'])
        # print('--------------------')
        # print('--------------------')
        # print(total_costs_calc['total_cost_1'])
        # print('--------------------')
        # print(total_costs_calc['total_cost_3'])
        # print(total_costs_calc['total_cost_5'])
        # print(total_costs_calc['total_cost_7'])
        # print(total_costs_calc['total_cost_9'])

        if total_costs_calc['total_cost_1'] < (total_costs_calc['total_cost_3'] or total_costs_calc['total_cost_5'] or total_costs_calc['total_cost_7'] or total_costs_calc['total_cost_9']):
            if new_service:
                await sync_to_async(new_service.delete)()
                await log_user_action(self.request.user, f'Отменилось добавление записи в "Закупки" с ID {new_service.id_id}')
            # print('TEST 1')
            # print(total_costs_calc['total_cost_1'])
            # print('--------------------')
            # print(total_costs_calc['total_cost_3'])
            # print(total_costs_calc['total_cost_5'])
            # print(total_costs_calc['total_cost_7'])
            # print(total_costs_calc['total_cost_9'])
            return False

        if total_costs_calc['total_cost_2'] < (total_costs_calc['total_cost_4'] or total_costs_calc['total_cost_6'] or total_costs_calc['total_cost_8'] or total_costs_calc['total_cost_10']):
            if new_service:
                await sync_to_async(new_service.delete)()
                await log_user_action(self.request.user, f'Отменилось добавление записи в "Закупки" с ID {new_service.id_id}')
            # print('TEST 2')
            return False
        return True

    async def total_costs_message(self):
        # await sync_to_async(messages.error)(self.request, 'Запрещено вносить новую строку, если после ее ввода сумма контрактов по соответствующему КЦСР, КОСГУ и ДопФК превысит значение поля «Лимиты»')
        messages.error(self.request, 'Запрещено вносить новую строку, если после ее ввода сумма контрактов по соответствующему КЦСР, КОСГУ и ДопФК превысит значение поля «Лимиты»')

    async def Services_way(self):
        """Подсчёт Цена контракта если есть way='п.4 ч.1 ст.93'"""
        from django.db.models import Q

        # Services_way_ = await sync_to_async(list)(Services.objects.filter(
        #     Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC']) & Q(KTSSR=self.context_data['KTSSR']) & Q(status=self.context_data['status']) & Q(way='п.4 ч.1 ст.93')
        # ))
        # contract_price_sum_way = 0
        # for service in Services_way_:
        #     contract_price_sum_way += await format_number(service.contract_price if service.contract_price not in [None, 'None', ''] else 0)

        # Общий фильтр для обоих случаев
        filters = Q(KOSGU=self.context_data['KOSGU']) & Q(DopFC=self.context_data['DopFC']) & Q(KTSSR=self.context_data['KTSSR']) & ~Q(status='Запланировано') & Q(way='п.4 ч.1 ст.93')

        months_contract_price = (
            'january_one', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december',
            # 'january_two'
        )

        answer = 0
        for contract_price in months_contract_price:
            total_sum = await sync_to_async(self._aggregate_sum)(filters, contract_price)
            answer += await format_number(total_sum if total_sum not in [None, 'None', ''] else 0)

        return round(answer, 2)

    async def Services_Two_save(self, Services_Two_):
        """Обновление второй базы"""

        # Services_Two_.off_budget_planned = await self.calculate_contract_sums('2046100092', 'Запланировано')

        # Services_Two_.budget_planned = await self.calculate_contract_sums('2046102280', 'Запланировано')

        # Services_Two_.off_budget_bargaining = await self.calculate_contract_sums('2046100092', 'В торгах')

        # Services_Two_.budget_bargaining = await self.calculate_contract_sums('2046102280', 'В торгах')

        # Services_Two_.off_budget_concluded = await self.calculate_contract_sums('2046100092', 'Заключено')

        # Services_Two_.budget_concluded = await self.calculate_contract_sums('2046102280', 'Заключено')

        # Services_Two_.off_budget_completed = await self.calculate_contract_sums('2046100092', 'Исполнено')

        # Services_Two_.budget_completed = await self.calculate_contract_sums('2046102280', 'Исполнено')

        # Services_Two_.off_budget_execution = await self.calculate_contract_sums('2046100092', None)

        # Services_Two_.budget_execution = await self.calculate_contract_sums('2046102280', None)

        categories = [
            ('off_budget', '2046100092'),
            ('budget', '2046102280')
        ]

        statuses = [
            ('planned', 'Запланировано'),
            ('bargaining', 'В торгах'),
            ('concluded', 'Заключено'),
            ('completed', 'Исполнено'),
            ('execution', None)
        ]

        for prefix, code in categories:
            for status_attr, status_value in statuses:
                attr_name = f"{prefix}_{status_attr}"
                setattr(Services_Two_, attr_name, await self.calculate_contract_sums(code, status_value))

        return Services_Two_

    async def process_update_user(self):

        # await self.count_dates()

        Services_Two_ = await self.validate_Services_Two()

        if not await self.validate_Services_Two():
            await self.validate_Services_Two_message()
            return render(self.request, 'edit.html', self.context_data)

        await self.process_budget_services_two(Services_Two_)

        await self.message_service_update()

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

    async def process_update_user_two(self):

        # await self.count_dates()

        await self.process_budget_services_three(False)

        await self.message_service_update()

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

    async def count_dates(self, mode):
        """Предварительные вычислительные операции после обновления или добавления записей"""

        @sync_to_async(thread_sensitive=True)
        def update_Services_Two():
            Services_Two.objects.all().update(
                # budget_limit='0',
                # off_budget_limit='0',
                budget_planned='0',
                off_budget_planned='0',
                budget_bargaining='0',
                off_budget_bargaining='0',
                budget_concluded='0',
                off_budget_concluded='0',
                budget_completed='0',
                off_budget_completed='0',
                budget_execution='0',
                off_budget_execution='0',
                budget_remainder='0',
                off_budget_remainder='0',
                budget_plans='0',
                off_budget_plans='0',
                color='0'
            )

        @sync_to_async(thread_sensitive=True)
        def update_Services_Three():
            Services_Three.objects.all().update(
                # budget_planned_old='0',
                # off_budget_planned_old='0',
                # budget_planned='0',
                # off_budget_planned='0',
                budget_concluded='0',
                off_budget_concluded='0',
                budget_remainder='0',
                off_budget_remainder='0',
                color='0',
            )

        # Асинхронная функция для получения данных
        @sync_to_async
        def get_services_two_data():
            services_two_records = Services_Two.objects.all()

            # Сохраняем все записи в список
            KOSGU_and_DopFC = [(record.KOSGU, record.DopFC) for record in services_two_records]

            return KOSGU_and_DopFC  # Список с повторяющимися ключами

        async def process_context(KTSSR, status, context_data, request):
            # Обновляем context_data
            context_data.update({'KTSSR': KTSSR, 'status': status})

            # Инициализация и обработка контекста
            processor = ContractProcessor(context_data, request)
            await processor.process_count_dates()

        async def handle_multiple_statuses(context_data, request):
            # Список статусов для обработки
            statuses = ['Запланировано', 'В торгах', 'Заключено', 'Исполнено']

            # Обработка для KTSSR 2046102280
            for status in statuses:
                await process_context('2046102280', status, context_data, request)

            # Обработка для KTSSR 2046100092
            for status in statuses:
                await process_context('2046100092', status, context_data, request)

        if not mode:

            await update_Services_Two()
            await update_Services_Three()

            # Вызов функции
            KOSGU_and_DopFC = await get_services_two_data()

            context_data = {}

            for key, value in KOSGU_and_DopFC:

                # Добавляем ключ и значение в context_data
                context_data.update({'KOSGU': key})
                context_data.update({'DopFC': value})

                await handle_multiple_statuses(context_data, self.request)

        elif mode:

            # context_data = {}

            # # Добавляем ключ и значение в context_data
            # context_data.update({'KOSGU': self.context_data['KOSGU']})
            # context_data.update({'DopFC': self.context_data['DopFC']})
            # context_data.update({'KTSSR': self.context_data['KTSSR']})
            # context_data.update({'status': self.context_data['status']})

            # Инициализация и обработка контекста
            # processor = ContractProcessor(self.context_data, self.request)
            if not (self.context_data.get('KTSSR') and self.context_data.get('status')):
                # print('POPALO SUDA')
                await handle_multiple_statuses(self.context_data, self.request)
            else:
                await self.process_count_dates()

    async def process_count_dates(self):
        """Продолжение предварительных вычислительних операций после обновления или добавления записей"""

        Services_Two_ = await self.validate_Services_Two()

        if not Services_Two_:
            await self.validate_Services_Two_message()
            return render(self.request, 'data_table.html', self.context_data)

        Services_Two_ = await self.Services_Two_save(Services_Two_)

        await self.process_budget_services_two(Services_Two_)

        await self.process_budget_services_three(True)

    async def execution_balance_saving_calculation(self):
        """Расчет контракта исполнения, баланса контракта и сбережений"""
        execution_contract_plan = await self.calculate_execution_plan()
        execution_contract_fact = await self.calculate_execution_fact()
        saving = round(await format_number(self.context_data['NMCC']) - await format_number(self.context_data['contract_price']), 2)

        if await format_number(self.context_data['contract_price']) == 0:
            self.context_data['execution'] = 0  # Или любое другое значение по умолчанию, например `None` или сообщение об ошибке
        else:
            self.context_data['execution'] = round(await format_number(execution_contract_fact) / await format_number(self.context_data['contract_price']), 2) * 100

        self.context_data['contract_balance'] = round(await format_number(self.context_data['contract_price']) - await format_number(execution_contract_fact), 2)
        return execution_contract_plan, execution_contract_fact, saving

    async def process_update(self):
        if not await self.validate_Services_Two():
            await self.validate_Services_Two_message()
            return render(self.request, 'edit.html', self.context_data)
        if not await self.validate_execution_plan():
            await self.validate_execution_plan_message()
            return render(self.request, 'edit.html', self.context_data)
        elif not await self.validate_execution_fact():
            await self.validate_execution_fact_message()
            return render(self.request, 'edit.html', self.context_data)

        execution_contract_plan, execution_contract_fact, saving = await self.execution_balance_saving_calculation()

        from django.forms.models import model_to_dict
        service_dict = model_to_dict(self.context_data['service'])

        await log_user_action(self.request.user, f'Отредактировал запись в "Закупки" с ID {service_dict['id_id']},\nБыло: {service_dict}')

        await self.update_service(saving, execution_contract_plan, execution_contract_fact)

        # print('-------------------------')
        # print(self.context_data['KOSGU'])
        # print(self.context_data['DopFC'])
        # print(self.context_data['KTSSR'])
        # print(self.context_data['status'])
        # print('-------------------------')

        await self.count_dates(True)

        if not await self.total_costs(None):

            # self.context_data['contract_price'] = '0'

            months_contract_price = (
                            'january_one', 'february', 'march', 'april', 'may', 'june',
                            'july', 'august', 'september', 'october', 'november', 'december',
                            # 'january_two'
                        )

            for contract_price in months_contract_price:
                self.context_data[contract_price] = '0'

            await self.update_service(saving, execution_contract_plan, execution_contract_fact)

            await self.count_dates(True)

            await self.total_costs_message()
            return render(self.request, 'edit.html', self.context_data)

        await log_user_action(self.request.user, f'Отредактировал запись в "Закупки" с ID {self.context_data['id_id']},\nСтало: {self.context_data}')

        await self.message_service_update()

        context_data_copy = self.context_data.copy()  # Создаем копию, чтобы не изменять оригинал

        # Список ключей, которые нужно удалить
        keys_to_remove = ['service', 'id_id',
                            'name', 'status',
                            'way', 'initiator',
                            'KTSSR', 'KOSGU',
                            'DopFC', 'NMCC',
                            'counterparty', 'registration_number',
                            'contract_number', 'contract_date',
                            'end_date', 'contract_price',
                            'january_one', 'february',
                            'march', 'april',
                            'may', 'june',
                            'july', 'august',
                            'september', 'october',
                            'november', 'december',
                            'january_two', 'date_january_one',
                            'sum_january_one', 'date_february',
                            'sum_february', 'date_march',
                            'sum_march', 'date_april',
                            'sum_april', 'date_may',
                            'sum_may', 'date_june',
                            'sum_june', 'date_july',
                            'sum_july', 'date_august',
                            'sum_august', 'date_september',
                            'sum_september', 'date_october',
                            'sum_october', 'date_november',
                            'sum_november', 'date_december',
                            'sum_december', 'date_january_two',
                            'sum_january_two', 'execution',
                            'contract_balance', 'execution_contract_fact',
                            'execution_contract_plan', 'saving',
                            'color']

        # Удаляем ключи из словаря
        for key in keys_to_remove:
            context_data_copy.pop(key, None)  # Удаляем ключ, если он существует

        # Кодируем query-параметры
        query_string = urlencode(context_data_copy)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

    async def process_add(self):
        if not await self.validate_Services():
            await self.validate_Services_message()
            return render(self.request, 'add.html', self.context_data)
        elif not await self.validate_Services_Two():
            await self.validate_Services_Two_message()
            return render(self.request, 'add.html', self.context_data)
        elif not await self.validate_execution_plan():
            await self.validate_execution_plan_message()
            return render(self.request, 'add.html', self.context_data)
        elif not await self.validate_execution_fact():
            await self.validate_execution_fact_message()
            return render(self.request, 'add.html', self.context_data)

        # execution_contract_plan = await self.calculate_execution_plan()
        # execution_contract_fact = await self.calculate_execution_fact()
        # saving = round(await format_number(self.context_data['NMCC']) - await format_number(self.context_data['contract_price']), 2)

        # if await format_number(self.context_data['contract_price']) == 0:
        #     self.context_data['execution'] = 0  # Или любое другое значение по умолчанию, например `None` или сообщение об ошибке
        # else:
        #     self.context_data['execution'] = round(await format_number(execution_contract_fact) / await format_number(self.context_data['contract_price']), 2) * 100

        # self.context_data['contract_balance'] = round(await format_number(self.context_data['contract_price']) - await format_number(execution_contract_fact), 2)

        execution_contract_plan, execution_contract_fact, saving = await self.execution_balance_saving_calculation()

        new_service = Services()
        new_service = await self.creation_new_service(saving, execution_contract_plan, execution_contract_fact, new_service)

        # # Services_Two_ = await sync_to_async(lambda: Services_Two.objects.all())()
        # Services_Two_ = await sync_to_async(list, thread_sensitive=True)(Services_Two.objects.all())

        await sync_to_async(new_service.save)()

        # Services_Two_ = await self.validate_Services_Two()

        if not await self.validate_Services_Two():
            await self.validate_Services_Two_message()
            return render(self.request, 'data_table.html', self.context_data)

        # await self.Services_Two_save(Services_Two_)
        await self.count_dates(True)

        if not await self.total_costs(new_service):
            await self.count_dates(True)

            await self.total_costs_message()
            return render(self.request, 'add.html', self.context_data)

        await self.message_service_add()

        # print(self.context_data)

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

    async def process_add_two(self):

        await self.creation_new_service_two()

        await self.count_dates(False)

        await self.message_service_add()

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

    async def process_delete(self):

        await self.count_dates(True)

        await self.message_service_delete()

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.

    async def process_delete_two(self):

        await self.count_dates(True)

        await self.message_service_delete()

        # Кодируем query-параметры
        query_string = urlencode(self.context_data)

        # Формируем URL с query-параметрами
        redirect_url = f"{reverse('data_table_view')}?{query_string}"  # Замените 'index' на имя вашего URL-шаблона

        # Перенаправляем пользователя
        return HttpResponseRedirect(redirect_url)

        # Другие операции, такие как сохранение сервиса и т.д.