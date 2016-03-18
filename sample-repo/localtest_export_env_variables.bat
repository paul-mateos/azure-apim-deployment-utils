REM For Windows

REM You can use such a BAT file in order to set your environment variables
REM to suitable values for local testing. In Build server environments, the
REM build agents usually get those env variables set by the Build server,
REM but for local testing, this file can be convenient.

REM For instances.json
set APIM_ID=acbdbf783478db83bdface883
set APIM_PRIMARY_KEY=VGhpcyBpcyBqdXN0IGEgYnVuY2ggb2YgdGV4dCBzYXlpbmcgbm90aGluZy4gQW5kIG5vLCBpdCdzIG5vdCBhIHZhbGlkIGtleS4=
set APIM_MGMT_URL=https://myapiminstance.management.azure-api.net/
set APIM_SCM_HOST=myapiminstance.scm.azure-api.net
set APIM_GATEWAY_HOST=myapiminstance.azure-api.net

REM For certificates.json
set APIM_CLIENT_CERT_PFX=C:\path\to\pfx\client_certificate.pfx
set APIM_CLIENT_CERT_PASSWORD=cleartext_cert_password

REM For properties.json
set APIM_CERT_THUMBPRINT=AC9823BF7EA86C3AB8120073BCFEDB288322BF0
set APIM_BACKEND_1=https://backendservice1.contoso.com/fullpath/v1:8080
set APIM_BACKEND_2=https://backendservice2.contoso.com/fullpath/v1:8080

REM For swaggerfiles.json
set APIM_SWAGGER_API1=C:\path\to\swagger1\swagger.json
set APIM_SWAGGER_API1=C:\path\to\swagger2\swagger.json
