from connectors.connection import DbConnection
from data_objects.sites import Vendor
from readers.reader import Reader


class VendorReader(Reader):
    def __init__(self, filters=[]):
        self.connection = DbConnection(Reader.USER, Reader.PASSWORD, Reader.HOST, Reader.PORT)
        self.query = ""
        self.filters = filters

    def build_query(self):
        query = f"""
        SELECT location.name as name,
                location.company as company,
                supply.'additional quantity available 1st week(kg)' as capacity,
                supply.'additional quantity available per week after 1st week(kg)' as additional_capacity,
                supply.'SLA period (days)' as sla_period,
                supply.'Onboarding Period' as onboarding_period,
                supply.'price per kg' as cost_per_kg,
                supply.'CO2 Emissions per kg' as co2_emissions_per_kg
        FROM supplier_farms as location
        LEFT JOIN supplier_farms_supply as supply
        ON supplier_farms.farm_id = supplier_farms.farm_id
        """
        self.query = query

    def read_query(self):
        restaurants = self.connection.reader(self.query)
        return [Vendor(**restaurant) for restaurant in restaurants]