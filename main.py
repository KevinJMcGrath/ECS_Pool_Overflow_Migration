import package_logging

import test
import sfdc.pool_mgmt as mgmt

def run_main():
    src_pool_name = 'CTT-472'
    dest_pool_name = 'CTT-520'
    calls_to_move = -1

    mgmt.move_overflow_calls(src_pool_name, dest_pool_name, calls_to_move)
    mgmt.force_pool_inactive(src_pool_name)


def run_test():
    test.test_connection()

if __name__ == '__main__':
    package_logging.initialize_logging()

    # run_main()

    run_test()
