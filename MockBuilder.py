import argparse
import configparser
import json
import logging
import os
import sqlite3
import re


class MockBuilder:
    def __init__(self):
        log_format = '%(asctime)-15s %(message)s'
        logging.basicConfig(format=log_format, level=logging.INFO)
        logger = logging.getLogger('mock.builder')
        self.logger = logger
        self.config_file = 'mockbuilder.ini'
        self.conn = None

        config = configparser.ConfigParser()
        config.read(self.config_file)
        default_config = config['PROCESS']
        self.output_path = default_config['OUTPUT_PATH']
        self.request_dir = default_config['REQUEST_DIR']
        self.response_dir = default_config['RESPONSE_DIR']
        self.db_name = default_config['DBNAME']

    def build(self, request_file, response_file):
        self.conn = sqlite3.connect(self.db_name)
        self.logger.info('Reading request file: ' + request_file)
        with open(request_file, 'r') as openFileObject:
            for line in openFileObject:
                # verifico que la linea no este en blanco
                if len(line.strip()) > 0:
                    # verifico que la linea contenga la entrada que considero un request (ID: 71#Address: )
                    if re.search("ID: [0-9]+#Address:", line):
                        # verifico que el payload contenga un mensaje SOAP
                        if re.search("</soap:Envelope>", line):
                            self.process_request_line(line)
        self.conn.commit()
        self.logger.info('Reading response file: ' + response_file)
        with open(response_file, 'r') as openFileObject:
            for line in openFileObject:
                # verifico que la linea no este en blanco
                if len(line.strip()) > 0:
                    # verifico que la linea contenga la entrada que considero un request (ID: 71#Response-Code:)
                    if re.search("ID: [0-9]+#Response-Code:", line):
                        # verifico que el payload contenga un mensaje SOAP
                        if re.search("</soapenv:Envelope>", line):
                            self.process_response_line(line)
        self.conn.commit()
        self.conn.close()
        self.logger.info('Writing output files...')
        self.write_request_response_files()

    def process_request_line(self, line):
        request = self.get_request_data(line)
        line_id = str(line[:line.index('#Address:')]).replace('ID: ', '')
        self.write_request_db(line_id, request)

    def get_request_data(self, line):
        # get url
        # url_init = line.index(':9080/') + 5
        url_init = re.search(":[0-9][0-9][0-9][0-9]/", line).start() + 5
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

        request_data = {'url': url, 'method': method, 'bodyPatterns': equal_to}

        return request_data

    def process_response_line(self, line):
        line_id = str(line[:line.index('#Response-Code:')]).replace('ID: ', '')
        response = self.get_response_data(line)
        self.write_response_db(line_id, response)

    def get_response_data(self, line):
        # get status
        status_init = line.index('#Response-Code: ') + 16
        status_end = line.index('#Encoding')
        status = line[status_init:status_end]

        response_init = line.index('#Payload: ') + 10
        response_end = line.index('</soapenv:Envelope>#') + 19
        response_body = line[response_init:response_end]

        content_len_init = line.index('Content-Length=[') + 16
        content_len_end = line.index('], content-type')
        content_len = line[content_len_init:content_len_end]

        headers = {'X-Powered-By': 'Servlet/3.0',
                   'Content-Type': 'text/xml; charset=UTF-8',
                   'Content-Language': 'en-US',
                   'Content-Length': content_len,
                   'Date': 'Wed, 10 Feb 2016 17:18:28 GMT'}

        response_data = {'status': int(status), 'headers': headers, 'response_body': response_body}
        return response_data

    def get_filename(self, service, line_id):
        return 'body' + service.replace('/', '-') + '-' + line_id.replace(' ', '')

    def write_request_response_files(self):
        self.logger.debug("Writing request files...")
        self.conn = sqlite3.connect(self.db_name)
        c = self.conn.cursor()
        sql = '''SELECT * FROM SERVICE_MOCK'''
        c.execute(sql)
        rows = c.fetchall()

        for row in rows:
            filename = row[4]
            body = row[7]
            equal_to_data = {'equalTo': row[3]}
            request = {'url': row[1], 'method': row[2], 'bodyPatterns': [equal_to_data]}
            headers = {'X-Powered-By': 'Servlet/3.0',
                       'Content-Type': 'text/xml; charset=UTF-8',
                       'Content-Language': 'en-US',
                       'Content-Length': row[6],
                       'Date': 'Wed, 10 Feb 2016 17:18:28 GMT'}
            response = {'status': row[5], 'bodyFileName': filename, 'headers': headers}
            service_data = {'request': request, 'response': response}
            json_data = json.dumps(service_data)
            self.write_file(self.request_dir, filename, json_data)
            self.write_file(self.response_dir, filename, body)

    def write_file(self, path, filename, data):
        self.logger.debug('Writing File: ' + filename)
        file_path = self.output_path + path
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file = open(file_path + filename, 'w')
        file.write(data)
        file.close()

    def setup_db(self):
        self.logger.info("Setup DB: " + self.db_name)
        self.conn = sqlite3.connect(self.db_name)
        c = self.conn.cursor()

        sql_drop = '''DROP TABLE IF EXISTS SERVICE_MOCK'''
        sql_create = '''CREATE TABLE SERVICE_MOCK(ID TEXT, URL TEXT, METHOD TEXT, BODYPATTERNS TEXT, FILENAME TEXT, STATUS INT, CONTENTLEN TEXT, RESPONSE TEXT)'''
        c.execute(sql_drop)
        c.execute(sql_create)

        self.conn.commit()
        self.conn.close()

    def write_request_db(self, line_id, data):
        self.logger.debug("Writing request to DB")
        c = self.conn.cursor()
        sql = '''INSERT INTO SERVICE_MOCK (ID, URL, METHOD, BODYPATTERNS, FILENAME) VALUES (?, ?, ?, ?, ?)'''
        url = str(data['url'])
        method = str(data['method'])
        body = str(data['bodyPatterns'])
        filename = self.get_filename(url, line_id) + '.json'
        parameters = (line_id, url, method, body, filename)
        c.execute(sql, parameters)

    def write_response_db(self, line_id, data):
        self.logger.debug("Writing response to DB")
        c = self.conn.cursor()
        status = int(data['status'])
        headers = data['headers']
        content_len = headers['Content-Length']
        response = data['response_body']
        parameters = (status, content_len, response, line_id)
        sql = '''UPDATE SERVICE_MOCK SET STATUS = ?, CONTENTLEN = ?, RESPONSE = ? WHERE ID = ?'''
        c.execute(sql, parameters)


# def main():
#     mb = MockBuilder()
#     mb.setup_db()
#     request = '/Users/edison/Tmp/mock_test/out/request-20170928_101035.txt'
#     response = '/Users/edison/Tmp/mock_test/out/response-20170928_101035.txt'
#     mb.build(request, response)
#
#
# if __name__ == '__main__':
#     main()

parser = argparse.ArgumentParser()
parser.add_argument('request_file')
parser.add_argument('response_file')
args = parser.parse_args()


def main(request, response):
    mb = MockBuilder()
    mb.setup_db()
    mb.build(request, response)


if __name__ == '__main__':
    main(args.request_file, args.response_file)
