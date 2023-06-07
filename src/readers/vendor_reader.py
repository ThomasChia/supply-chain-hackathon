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
        # number of farms per supplier
        # divide the capacity amount for a supplier by the number of farms they have

        query = f"""
        with supplier_farms as (
            select supplier_id,
                    count(id) as supplier_farms
            from farm
            group by supplier_id
        )
        SELECT farm.id as id,
            farm.name as name,
            supplier.name as company,
            farm.location as location,
            supplier.add_qty_1st_week_kg / supplier_farms as capacity,
            supplier.add_qty_after_1st_week_kg / supplier_farms as additional_capacity,
            supplier.sla_period_days as sla_period,
            supplier.price_kg as cost_per_kg,
            supplier.co2_emissions_per_kg as co2_emissions_per_kg,
            farm.lat as lat,
            farm.long as long
        FROM farm
        LEFT JOIN supplier ON farm.supplier_id = supplier.id
        left join supplier_farms on farm.supplier_id = supplier_farms.supplier_id
        WHERE supplier.is_active = true
        """
        self.query = query

    def read_query(self):
        vendors = self.connection.reader(self.query)
        self.data = [Vendor(**vendor) for vendor in vendors]


class VendorIDReader(Reader):
    def __init__(self, suppliers):
        self.connection = DbConnection(Reader.USER, Reader.PASSWORD, Reader.HOST, Reader.PORT)
        self.query = ""
        self.suppliers = suppliers
        self.data = []

    def run(self):
        self.build_query()
        self.read_query()

    def build_query(self):
        suppliers_list = super().list_to_sql(self.suppliers)
        suppliers_filter = '' if suppliers_list == '' else f"WHERE distributor.id in {suppliers_list}"

        query = f"""
        SELECT farm.name
        FROM farm
        LEFT JOIN supplier
        ON farm.supplier_id = supplier.id
        {suppliers_filter}
        """
        self.query = query

    def read_query(self):
        vendor_ids = self.connection.reader(self.query)
        self.data = [vendor_id for vendor_id in vendor_ids]