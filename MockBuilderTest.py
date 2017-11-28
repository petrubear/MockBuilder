import unittest
import MockBuilder


class RequestDataTest(unittest.TestCase):

    def test_karaf42_request(self):
        line = 'ID: 1#Address: http://127.0.0.1:9081/SAuthService/UserAuthWsService#HttpMethod: POST#Content-Type: text/xml#ExchangeId: 2cd46930-2539-4661-84ce-beeb98467f27#ServiceName: UserAuthImplService#PortName: UserAuthImplPort#PortTypeName: UserAuthImpl#Headers: {SOAPAction="http://bancointernacional.com.ec/wsdl/security/auth/user/UserAuthImpl/ibsValidateDefUserRequest", Accept=*/*}#Payload: <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ns2:ibsValidateDefUser xmlns:ns2="http://bancointernacional.com.ec/wsdl/security/auth/user"><arg0><ipAddress>127.0.0.1</ipAddress><channel>WEB</channel><customerId>000000000</customerId><additionalCusId>A000000000000</additionalCusId><sequential>306919</sequential><dateAndTime>2017-11-27 14:50:18.288</dateAndTime><userId>CANOMNIA</userId><productCode>1</productCode><serviceCode>10000</serviceCode><tranServiceCode>1101</tranServiceCode><bankId>01</bankId><username>lahjNCCscHBqPDC4NH7+gA==</username></arg0></ns2:ibsValidateDefUser></soap:Body></soap:Envelope>#'  # noqa
        soap = '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ns2:ibsValidateDefUser xmlns:ns2="http://bancointernacional.com.ec/wsdl/security/auth/user"><arg0><ipAddress>127.0.0.1</ipAddress><channel>WEB</channel><customerId>000000000</customerId><additionalCusId>A000000000000</additionalCusId><sequential>306919</sequential><dateAndTime>2017-11-27 14:50:18.288</dateAndTime><userId>CANOMNIA</userId><productCode>1</productCode><serviceCode>10000</serviceCode><tranServiceCode>1101</tranServiceCode><bankId>01</bankId><username>lahjNCCscHBqPDC4NH7+gA==</username></arg0></ns2:ibsValidateDefUser></soap:Body></soap:Envelope>'  # noqa
        mb = MockBuilder.MockBuilder()
        data = mb.get_request_data(line)
        post = data['method']
        url = data['url']
        body_patterns = data['bodyPatterns']
        print("URL: " + url)

        self.assertEqual('/SAuthService/UserAuthWsService', url)
        self.assertEqual('POST', post)
        self.assertEqual(soap, body_patterns)

    def test_karaf42_response(self):
        line = 'ID: 1#Content-Type: text/xml; charset=UTF-8#ResponseCode: 200#ExchangeId: 2cd46930-2539-4661-84ce-beeb98467f27#ServiceName: UserAuthImplService#PortName: UserAuthImplPort#PortTypeName: UserAuthImpl#Headers: {content-type=text/xml; charset=UTF-8, Content-Length=603, Content-Language=en-US, Date=Mon, 27 Nov 2017 20:02:44 GMT, X-Powered-By=Servlet/3.0}#Payload: <?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><dlwmin:ibsValidateDefUserResponse xmlns:dlwmin="http://bancointernacional.com.ec/wsdl/security/auth/user" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><UserAuthIBSCodeResponse><messageDescr>OK</messageDescr><messageId>0</messageId><additionalCusId></additionalCusId><customerGroup>G9</customerGroup><customerIdIBS>000000364</customerIdIBS><customerType>C</customerType></UserAuthIBSCodeResponse></dlwmin:ibsValidateDefUserResponse></soapenv:Body></soapenv:Envelope>#'  # noqa
        mb = MockBuilder.MockBuilder()
        data = mb.get_response_data(line)
        status = data['status']
        headers = data['headers']
        content_len = headers['Content-Length']
        response_body = data['response_body']

        self.assertEqual(200, status)
        self.assertEqual('603', content_len)
        self.assertTrue(str(response_body).startswith('<?xml version="1.0" encoding="UTF-8"?>'))
        self.assertTrue(str(response_body).endswith('</soapenv:Envelope>'))


if __name__ == '__main__':
    unittest.main()
