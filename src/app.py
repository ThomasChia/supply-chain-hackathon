from optimisers.optimiser import SupplyChainOptimisation
from optimisers.profit_maximiser import SupplyChainProfitMaximiser
from data.test_data import vendors, warehouses, restaurants, vehicles, supplier_warehouse_costs, warehouse_restaurant_costs



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
          

    # supply_chain_optimizer = SupplyChainOptimisation(vendors=vendors,
    #                                                  warehouses=warehouses,
    #                                                  restaurants=restaurants,
    #                                                  vehicles=vehicles,
    #                                                  supplier_warehouse_distances=supplier_warehouse_costs,
    #                                                  warehouse_restaurant_distances=warehouse_restaurant_costs)
    
    # supply_chain_optimizer.solve()
    
    supply_chain_optimizer = SupplyChainProfitMaximiser(vendors=vendors,
                                                        warehouses=warehouses,
                                                        restaurants=restaurants,
                                                        vehicles=vehicles,
                                                        supplier_warehouse_distances=supplier_warehouse_costs,
                                                        warehouse_restaurant_distances=warehouse_restaurant_costs)
    
    supply_chain_optimizer.solve()
