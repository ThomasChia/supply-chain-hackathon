import code
from evaluators.evaluator import Evaluator
import logging
from logs import setup_logs
from planners.cost_minimiser import CostMinimiserPlanner
from optimisers.optimiser import SupplyChainOptimisation
from optimisers.profit_maximiser import SupplyChainProfitMaximiser
import os
# from data.test_data import vendors, warehouses, restaurants, vehicles, supplier_warehouse_costs, warehouse_restaurant_costs
from readers.warehouse_reader import WarehouseReader

setup_logs()
logger = logging.getLogger(__name__)

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

    planner = CostMinimiserPlanner(vendors_input=[],
                                   warehouses_input=[],
                                   restaurants_input=[],
                                   vehicles_input=[],
                                   supplier_warehouse_distance_input=[],
                                   warehouse_restaurant_distance_input=[])
    planner.run()

    evaluator = Evaluator(supply_chain=planner.supply_chain, active_sites=[('F005', 'F005'),
                                                                           ('F014', 'F014'),
                                                                           ('F020', 'F020'),
                                                                           ('WH035', 'WH035'),
                                                                           ('WH038', 'WH038'),
                                                                           ('WH001', 'WH001'),
                                                                           ('WH002', 'WH002'),
                                                                           ('WH003', 'WH003'),
                                                                           ('WH005', 'WH005'),
                                                                           ('WH004', 'WH004'),
                                                                           ('R027', 'R027'),
                                                                           ('R010', 'R010'),
                                                                           ('R011', 'R011'),
                                                                           ('R001', 'R001'),
                                                                           ('R023', 'R023'),
                                                                           ('R029', 'R029'),
                                                                           ('R012', 'R012'),
                                                                           ])
    evaluator.calculate_new_supply_chain()
          
    code.interact(local=locals())
