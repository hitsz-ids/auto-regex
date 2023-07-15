import os
import pandas as pd
from auto_regex.generator import generate

if __name__ == '__main__':
    data_dir = './data/'
    regex_names = ['ID_CARD', 'TELEPHONE', 'MOBILE_PHONE', 'EMAIL', 'LICENSE_PLATE',
                   'BANK_CARD', 'PASSPORT', 'SOCIAL_CREDIT_CODE', 'IPV4', 'IPV6', 'MAC',
                   'DOMAIN_NAME', 'POSTCODE', 'DATE']
    regex_names = ['ID_CARD']
    result_dict = {'regex_name': [], 'regex_pattern':[]}
    for regex_name in regex_names:
        train_data_file = os.path.join(data_dir, regex_name + '.csv')
        result = generate(regex_name, train_data_file)
        print('result: ', result)
        print('\n')

        result_dict['regex_name'].append(result['regex_name'])
        result_dict['regex_pattern'].append(result['regex_pattern'])

    df = pd.DataFrame(result_dict)
    df.to_csv('result.csv', index=False)