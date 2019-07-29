import argparse

import templated_package.api
import templated_package.display


def main_procedure():
    parser = argparse.ArgumentParser(prog=templated_package.__info__.__package_name__, 
                                     description=templated_package.__info__.__description__)

    parser.add_argument('service_1')

    args = parser.parse_args()

    if args.service_1:
        ret_val = templated_package.api.service_1()
        templated_package.display.after_service_1(ret_val)

if __name__ == "__main__":
    main_procedure()