import code
from optimisers.optimiser import SupplyChainOptimisation
from optimisers.profit_maximiser import SupplyChainProfitMaximiser
import os
# from data.test_data import vendors, warehouses, restaurants, vehicles, supplier_warehouse_costs, warehouse_restaurant_costs
from readers.warehouse_reader import WarehouseReader

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

    reader = WarehouseReader()
    reader.build_query()
    restaurant_distance = reader.read_query()
          
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
