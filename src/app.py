import code
from evaluators.evaluator import Evaluator
import logging
from logs import setup_logs
from planners.cost_minimiser import CostMinimiserPlanner
from optimisers.optimiser import SupplyChainOptimisation
from optimisers.profit_maximiser import SupplyChainProfitMaximiser
import os
from output.output import SupplyChain
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
    planner_supply_chain = planner.supply_chain.plan_to_list()
    test_supply_chain = SupplyChain.list_to_plan(planner_supply_chain['supply_chain'])

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
                                                                           ('R001', 'R001'), 
                                                                           ('R002', 'R002'), 
                                                                           ('R003', 'R003'), 
                                                                           ('R004', 'R004'), 
                                                                           ('R005', 'R005'), 
                                                                           ('R006', 'R006'), 
                                                                           ('R007', 'R007'), 
                                                                           ('R008', 'R008'), 
                                                                           ('R009', 'R009'), 
                                                                           ('R010', 'R010'), 
                                                                           ('R011', 'R011'), 
                                                                           ('R012', 'R012'), 
                                                                           ('R013', 'R013'), 
                                                                           ('R014', 'R014'), 
                                                                           ('R015', 'R015'), 
                                                                           ('R016', 'R016'), 
                                                                           ('R017', 'R017'), 
                                                                           ('R018', 'R018'), 
                                                                           ('R019', 'R019'), 
                                                                           ('R020', 'R020'), 
                                                                           ('R021', 'R021'), 
                                                                           ('R022', 'R022'), 
                                                                           ('R023', 'R023'), ('R024', 'R024'), ('R025', 'R025'), ('R026', 'R026'), ('R027', 'R027'), ('R028', 'R028'), ('R029', 'R029'),
                                                                           ('R030', 'R030')
                                                                           ])
    evaluator.calculate_new_supply_chain()
    evaluator_supply_chain = evaluator.new_supply_chain.plan_to_list()
          
    code.interact(local=locals())
