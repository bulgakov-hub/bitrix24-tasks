""" ЗАДАЧА: Найти все сделки с 01.07.2022 по текущий момент времени, которые
    побывали в стадиях (СТО-Тамара, СТО-Александра, СТО-Анастасия) изменить
    пользовательское поле сделки sto_field_choice на соответствующий селект
"""

from fast_bitrix24 import Bitrix

webhook = "https://ercs.bitrix24.ru/rest/{your code bitrix}"
b = Bitrix(webhook)

deals = b.get_all(
    'crm.deal.list',
    params={
        'select': ['ID'],
        'filter': {'>DATE_CREATE': '2022-07-01', '<DATE_CREATE': '2022-09-15'}
})

sto_field_choice = 'UF_CRM_1663141433'  # ID CHOICE FILED

search_stage = {'UC_UY6WWI': "1178",    # ID_STAGE (СТО-Тамара) / ID select field
                'UC_EUIE0O': "1180",    # ID_STAGE (СТО-Александра) / ID select field
                'UC_0V202Y': "1182"}    # ID_STAGE (СТО-Анастасия) / ID select field

for id_stage, code in search_stage.items():
    
    history = b.get_by_ID(
        method='crm.stagehistory.list',
        ID_list = [d['ID'] for d in deals],
        ID_field_name = "filter[OWNER_ID]",
        params={
            'entityTypeId': 2,
            'order': { "OWNER_ID": "ASC" },
            'select': ['ID','STAGE_ID','OWNER_ID', 'CREATED_TIME'],
            'filter[STAGE_ID]': id_stage
        })
    
    print(id_stage, len(history))

    uniq_id=list(set([d['OWNER_ID']for d in history]))

    tasks = [
        {
            'ID': d,
            'fields': {
                sto_field_choice : code
            }
        }
        for d in uniq_id
    ]

    b.call('crm.deal.update', tasks)



