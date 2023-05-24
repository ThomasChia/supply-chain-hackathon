from connectors.connection import DbConnection
from data_objects.sites import Vendor
from readers.reader import Reader


class VendorReader(Reader):
    def __init__(self, filters=[]):
        self.connection = DbConnection(Reader.USER, Reader.PASSWORD, Reader.HOST, Reader.PORT)
        self.query = ""
        self.filters = filters
        self.data = []

    def run(self):
        self.build_query()
        self.read_query()

    def build_query(self):
        query = f"""
        SELECT location.farm_id as name,
                location.company_name as company,
                location.nearest_city as location,
                supply.additional_quantity_available_1st_week_kg_ as capacity,
                supply.additional_quantity_available_per_week_after_1st_week_kg_ as additional_capacity,
                supply.SLA_period__days_ as sla_period,
                supply.onboarding_period as onboarding_period,
                supply.price_per_kg as cost_per_kg,
                supply.co2_Emissions_per_kg as co2_emissions_per_kg
        FROM supplier_farms as location
        LEFT JOIN supplier_farms_supply as supply
        ON location.farm_id = supply.farm_id
        WHERE location.farm_id != 'nan'
        """
        self.query = query

    def read_query(self):
        vendors = self.connection.reader(self.query)
        self.data = [Vendor(**vendor) for vendor in vendors]