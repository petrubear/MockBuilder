import configparser
import json
import logging
import os
import sqlite3


class MockBuilder:
    def __init__(self):
        log_format = '%(asctime)-15s %(message)s'
        logging.basicConfig(format=log_format, level=logging.INFO)
        logger = logging.getLogger('mock.builder')
        self.logger = logger

        config = configparser.ConfigParser()
        config.read('mockbuilder.ini')
        default_config = config['PROCESS']
        self.output_path = default_config['OUTPUTPATH']
        self.db_name = default_config['DBNAME']

    def build(self, request_file, response_file):
        with open(request_file, 'r') as openFileObject:
            for line in openFileObject:
                if len(line) > 0:
                    self.process_line(line)

    def process_line(self, line):
        request = self.get_request_data(line)
        service = request['url']
        line_id = line[3:line.index('#Address:')]
        filename = self.get_filename(service, line_id)
        service_data = {'request': request, 'response': self.get_response_data(filename)}
        json_data = json.dumps(service_data)
        self.write_to_file(json_data, filename)
        self.logger.debug('************************************************************')
        self.logger.debug(json_data)
        self.logger.debug('LINE: ' + str(line))

    def get_request_data(self, line):
        # get url
        url_init = line.index(':9080/') + 5
        url_end = line.index('#Encoding')
        url = line[url_init:url_end]

        # get method
        method_init = line.index('#Http-Method: ') + 14
        method_end = line.index('#Content-Type:')
        method = line[method_init:method_end]

        # get equalTo
        equal_to_init = line.index('Payload: ') + 9
        equal_to_end = line.index('</soap:Envelope>#') + 16
        equal_to = line[equal_to_init:equal_to_end]

        equal_to_data = {'equalTo': equal_to}
        request_data = {'url': url, 'method': method, 'bodyPatterns': [equal_to_data]}

        return request_data

    # TODO EM: el response va quemado??
    def get_response_data(self, filename):

        headers = {'X-Powered-By': 'Servlet/3.0',
                   'Content-Type': 'text/xml; charset=UTF-8',
                   'Content-Language': 'en-US',
                   'Content-Length': 0,  # TODO Que pongo aqui!
                   'Date': 'Wed, 10 Feb 2016 17:18:28 GMT'}

        response_data = {'status': 200, 'bodyFileName': filename, 'headers': headers}
        return response_data

    def get_filename(self, service, line_id):
        return 'body' + service.replace('/', '-') + '-' + line_id.replace(' ', '')

    def write_to_file(self, data, filename):
        request_path = self.output_path + '/request/'
        extension = '.json'
        file_path = request_path + filename + extension
        self.logger.info('Writing File: ' + file_path)

        if not os.path.exists(request_path):
            os.makedirs(request_path)

        file = open(file_path, 'w')
        file.write(data)
        file.close()

    def setup_db(self):
        self.logger.info("Setup DB: " + self.db_name)
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS SERVICE_MOCK(ID TEXT, URL TEXT, METHOD text, BODYPATTERNS TEXT)''')
        c.execute('''DELETE FROM SERVICE_MOCK''')

        conn.commit()
        conn.close()


# TODO leer archivo de la linea de comandos
def main():
    mb = MockBuilder()
    mb.setup_db()
    request = '/Users/edison/Tmp/mock_test/out/request-20170928_101035.txt'
    response = '/Users/edison/Tmp/mock_test/out/response-20170928_101035.txt'
    mb.build(request, response)
    print("Done.")


if __name__ == '__main__':
    main()
