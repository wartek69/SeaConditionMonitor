import logging

logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')


class SeaConditionMonitorCore:
    def __init__(self):
        logging.info('Created Sea Condition Monitor Core')
    
    

if __name__ == '__main__':
    sea_condition_monitor_core = SeaConditionMonitorCore()