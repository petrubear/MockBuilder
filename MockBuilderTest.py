import unittest
import MockBuilder


class RequestDataTest(unittest.TestCase):

    def testRequest(self):
        line = 'ID: 1#Address: http://172.16.72.143:9080/consultationIbs/CustomerConsultationWsService#Encoding: UTF-8#Http-Method: POST#Content-Type: text/xml#Headers: {Accept=[*/*], SOAPAction=["http://bancointernacional.com.ec/wsdl/consultation/customer/CustomerConsultationImpl/ibsGetCustomerProductsRequest"]}#Payload: <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ns2:ibsGetCustomerProducts xmlns:ns2="http://bancointernacional.com.ec/wsdl/consultation/customer"><arg0><ipAddress>192.168.2.31</ipAddress><channel>WEB</channel><customerId>000000364</customerId><additionalCusId></additionalCusId><sequential>6167005</sequential><dateAndTime>2017-09-27 12:01:23.118</dateAndTime><userId>CANOMNIA</userId><productCode>1</productCode><serviceCode>10003</serviceCode><tranServiceCode>1111</tranServiceCode><groupId>G9</groupId><bankId>01</bankId></arg0></ns2:ibsGetCustomerProducts></soap:Body></soap:Envelope>#'
        soap = '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ns2:ibsGetCustomerProducts xmlns:ns2="http://bancointernacional.com.ec/wsdl/consultation/customer"><arg0><ipAddress>192.168.2.31</ipAddress><channel>WEB</channel><customerId>000000364</customerId><additionalCusId></additionalCusId><sequential>6167005</sequential><dateAndTime>2017-09-27 12:01:23.118</dateAndTime><userId>CANOMNIA</userId><productCode>1</productCode><serviceCode>10003</serviceCode><tranServiceCode>1111</tranServiceCode><groupId>G9</groupId><bankId>01</bankId></arg0></ns2:ibsGetCustomerProducts></soap:Body></soap:Envelope>'
        mb = MockBuilder.MockBuilder()
        data = mb.get_request_data(line)
        post = data['method']
        url = data['url']
        body_patterns = data['bodyPatterns']
        body = [{'equalTo': soap}]
        self.assertEqual('/consultationIbs/CustomerConsultationWsService', url)
        self.assertEqual('POST', post)
        self.assertEqual(body, body_patterns)

    def testResponse(self):
        service = '/consultationIbs/CustomerConsultationWsService'
        line_id = ' 1'
        mb = MockBuilder.MockBuilder()
        data = mb.get_response_data(mb.get_filename(service, line_id))
        status = data['status']
        body_filename = data['bodyFileName']
        self.assertEqual(200, status)
        self.assertEqual('body-consultationIbs-CustomerConsultationWsService-1', body_filename)

    def testDB(self):
        mb = MockBuilder.MockBuilder()
        mb.setup_db()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
