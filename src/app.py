import code
from optimisers.optimiser import SupplyChainOptimisation
from optimisers.profit_maximiser import SupplyChainProfitMaximiser
import os
from data.test_data import vendors, warehouses, restaurants, vehicles, supplier_warehouse_costs, warehouse_restaurant_costs
from readers.supplier_warehouse_distances_reader import SupplierWarehouseDistanceReader


if __name__ == '__main__':
    print("""
   .-'''-.   ___    _ .-------. .-------.   .---.       ____     __ .---.  .---.   ___    _  _______    
  / _     \.'   |  | |\  _(`)_ \\  _(`)_ \  | ,_|       \   \   /  /|   |  |_ _| .'   |  | |\  ____  \  
 (`' )/`--'|   .'  | || (_ o._)|| (_ o._)|,-./  )        \  _. /  ' |   |  ( ' ) |   .'  | || |    \ |  
(_ o _).   .'  '_  | ||  (_,_) /|  (_,_) /\  '_ '`)       _( )_ .'  |   '-(_{;}_).'  '_  | || |____/ /  
 (_,_). '. '   ( \.-.||   '-.-' |   '-.-'  > (_)  )   ___(_ o _)'   |      (_,_) '   ( \.-.||   _ _ '.  
.---.  \  :' (`. _` /||   |     |   |     (  .  .-'  |   |(_,_)'    | _ _--.   | ' (`. _` /||  ( ' )  \ 
\    `-'  || (_ (_) _)|   |     |   |      `-'`-'|___|   `-'  /     |( ' ) |   | | (_ (_) _)| (_{;}_) | 
 \       /  \ /  . \ //   )     /   )       |        \\      /      (_{;}_)|   |  \ /  . \ /|  (_,_)  / 
  `-...-'    ``-'`-'' `---'     `---'       `--------` `-..-'       '(_,_) '---'   ``-'`-'' /_______.'  
                                                                                                                                                                                                       
    """)

    USER = os.getenv('CSCUSER')
    PASSWORD = os.getenv('CSCPASSWORD')
    HOST = os.getenv('CSCHOST')
    PORT = os.getenv('CSCPORT')

    reader = SupplierWarehouseDistanceReader(user=USER,
                             password=PASSWORD, 
                             host=HOST, 
                             port=PORT)
    reader.build_query()
    warehouses = reader.read_query()
          
    code.interact(local=locals())

    # supply_chain_optimizer = SupplyChainOptimisation(vendors=vendors,
    #                                                  warehouses=warehouses,
    #                                                  restaurants=restaurants,
    #                                                  vehicles=vehicles,
    #                                                  supplier_warehouse_distances=supplier_warehouse_costs,
    #                                                  warehouse_restaurant_distances=warehouse_restaurant_costs)
    
    # supply_chain_optimizer.solve()
    
    # supply_chain_optimizer = SupplyChainProfitMaximiser(vendors=vendors,
    #                                                     warehouses=warehouses,
    #                                                     restaurants=restaurants,
    #                                                     vehicles=vehicles,
    #                                                     supplier_warehouse_distances=supplier_warehouse_costs,
    #                                                     warehouse_restaurant_distances=warehouse_restaurant_costs)
    
    # supply_chain_optimizer.solve()
