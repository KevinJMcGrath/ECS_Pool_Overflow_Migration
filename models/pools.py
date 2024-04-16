import logging

class Pool:
    def __init__(self, pool_data):
        self.id = pool_data['Id']
        self.name = pool_data['Name']
        self.purchase_count = pool_data['Calls_Purchased_Generalized__c']
        self.completed_count = pool_data['Total_Calls_Completed__c']
        self.cost_direct = pool_data["Baseline_Cost_Direct__c"]
        self.cost_managed = pool_data["Baseline_Cost_Managed__c"]

        self.overflow_count = 0

        self.calc_overflow()

    def calc_overflow(self):
        ovf = self.completed_count - self.purchase_count

        if ovf > 0:
            self.overflow_count = ovf
        else:
            logging.warning(f"Pool {self.name} does not have overflow calls (Purchased: {self.purchase_count}) | "
                            f"Completed: {self.completed_count}")

