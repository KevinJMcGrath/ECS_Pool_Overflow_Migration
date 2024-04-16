import logging

import sfdc

from models.pools import Pool

def force_pool_inactive(pool_name: str):
    logging.info(f"Setting pool {pool_name} to inactive...")
    soql = ("SELECT Id, Name, Active__c "
            "FROM Click_to_Talk_Pool__c "
            f"WHERE Name = '{pool_name}'")

    records = sfdc.vizier.exec_soql(soql)
    pool_id = records[0]['Id']
    is_active = records[0]['Active__c']

    if is_active:
        sfdc.vizier.client.Click_to_Talk_Pool__c.update(pool_id, {'Force_Inactive__c': True})

        logging.info('Pool marked as "Force Inactive"')
    else:
        logging.info('Pool is already inactive. Skipping.')

def move_overflow_calls(src_pool_name: str, dest_pool_name: str, calls_to_move: int=-1):
    logging.info(f"Moving calls from {src_pool_name} to {dest_pool_name}...")
    src_pool, dest_pool = get_pools(src_pool_name, dest_pool_name)
    calls = get_src_calls(src_pool.id)

    max_completed_calls = calls_to_move

    if calls_to_move == -1:
        max_completed_calls = src_pool.overflow_count


    logging.info(f"Max number of completed calls to move: {max_completed_calls}")

    for_update = []

    completed_call_count = 0
    scheduled_call_count = 0
    for c in calls:

        if c['Status__c'] in ('Call Scheduled', 'In Scheduling'):
            p = {
                'Id': c['Id'],
                'Click_to_Talk_Pool__c': dest_pool.id,
            }

            for_update.append(p)
            scheduled_call_count += 1

        if completed_call_count < max_completed_calls and c['Status__c'] == 'Complete':
            cost = dest_pool.cost_direct if c['Type__c'] == 'Direct' else dest_pool.cost_managed

            p = {
                'Id': c['Id'],
                'Click_to_Talk_Pool__c': dest_pool.id,
                'Call_Value__c': cost,
                'Call_Value_Rev_Rec__c': cost,
                'Total_Call_Value__c': cost
            }

            for_update.append(p)
            completed_call_count += 1

    logging.info(f"Scheduled calls to be moved: {scheduled_call_count}")
    logging.info(f"Completed calls to be moved: {completed_call_count}")
    logging.info(f"Total number of calls for update: {len(for_update)}")

    sfdc.vizier.client.bulk.Click_to_Talk_Request__c.update(for_update)

    logging.info('Done!')


def get_src_calls(src_pool_id: str):
    soql = ("SELECT Id, Call_Value__c, Status__c, Call_Conducted_On__c, Type__c "
            "FROM Click_to_Talk_Request__c "
            "WHERE Status__c IN ('Complete', 'Call Scheduled', 'In Scheduling') "
            f"AND Click_to_Talk_Pool__c = '{src_pool_id}'"
            "ORDER By Call_Conducted_On__c DESC")

    records = sfdc.vizier.exec_soql(soql)

    return records


def get_pools(src_pool_name: str, dest_pool_name: str):
    soql = ("SELECT Id, Name, Calls_Purchased_Generalized__c, Total_Calls_Completed__c, Baseline_Cost_Direct__c,"
            "Baseline_Cost_Managed__c "
            "FROM Click_to_Talk_Pool__c "
            f"WHERE Name IN ('{src_pool_name}', '{dest_pool_name}')")

    records = sfdc.vizier.exec_soql(soql)
    src_pool = None
    dest_pool = None

    for r in records:
        if r['Name'] == src_pool_name:
            src_pool = Pool(r)

        if r['Name'] == dest_pool_name:
            dest_pool = Pool(r)

    return src_pool, dest_pool