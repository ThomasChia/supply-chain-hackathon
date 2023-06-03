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
        SELECT farm.id as name,
               supplier.name as company,
               farm.location as location,
               supplier.add_qty_1st_week_kg as capacity,
               supplier.add_qty_after_1st_week_kg as additional_capacity,
               supplier.sla_period_days as sla_period,
               supplier.onboarding_period as onboarding_period,
               supplier.price_kg as cost_per_kg,
               supplier.co2_emissions_per_kg as co2_emissions_per_kg
        FROM supplier
        LEFT JOIN farm
        ON farm.supplier_id = supplier.id
        WHERE location.farm_id != 'nan'
        AND supplier.is_active = TRUE
        """
        self.query = query

    def read_query(self):
        vendors = self.connection.reader(self.query)
        self.data = [Vendor(**vendor) for vendor in vendors]