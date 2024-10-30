"""Constants for the aqualia integration."""

DOMAIN = "aqualia"

#Custom configuration entries
MODEL_CAC_CODE="CacCode"
MODEL_CONTRACT_CODE="ContractCode"
MODEL_INSTALLATION_CODE="InstallationCode"
MODEL_CONTRACT_NUMBER="ContractNumber"
MODEL_SUPPLY_ADDRESS="SupplyAddress"
MODEL_CONTRACT_LIST="ContractList"
MODEL_CONTRACT_DETAILS="ContractDetails"
MODEL_CONTRACT="Contract"
MODEL_ENTRY_DATE="EntryDate"
MODEL_CONTRACT_INFO="ContractInfo"
MODEL_DATE_TIME_CONSUMPTION_CURVE="DateTimeConsumptionCurve"
MODEL_READING_INDEX="ReadingIndex"
MODEL_CONSUMPTION_VALUE="ConsumptionValue"
MODEL_UNIT_OF_MEASUREMENT="UnitOfMeasurement"
MODEL_TOKEN="Token"
MODEL_TOKEN_EXPIRATION_DATE="TokenExpirationDate"
MODEL_CONSUMPTION_CURVES="ConsumptionCurves"

TOTAL_CONSUMPTION_SUM="TotalConsumptionSum"

SERVICE_RESET_STATISTICS="reset_statistics"

#Statistics
STATS_METADATA="metadata"
STATS_STATISTICS="statistics"

#Aqualia API constants
AQUALIA_API_BASE_URL = "https://oficinavirtualapi.aqualia.es"
AQUALIA_LOGIN_PATH="ofcvirtual/auth/v1/api/auth/Auth/Login"
AQUALIA_CONSUMPTION_PATH="ofcvirtual/meter/v1/api/meter/Meter/GetContractConsumptionCurve"
AQUALIA_CONTRACTS_PATH="ofcvirtual/contract/v1/api/contract/Contract/GetUserLinkedContracts"
AQUALIA_HEADERS={
            "Content-Type": "application/json; charset=utf-8",
            "Accept":"application/json, text/plain, */*",
            "Application-Id":"1",
            "Country":"34",
            "Origin":"https://oficinavirtual.aqualia.es",
            "Referer":"https://oficinavirtual.aqualia.es/",
            "X-Content-Type-Options":"nosniff",
            "Accept-Language":"es-es"
        }

FAKE_CONTRACTS='''{
    "ContractDetails":
    [
        {"ClientTypeCode": "1",
        "MunicipalityCode": "39075000500",
        "ContractInfo": {
            "CacCode": 25862610,
            "ContractCode": 163790,
            "InstallationCode": 13905,
            "ContractNumber": "13905-1/1-163769"},
            "MunicipalityName": "SANTANDER",
            "SupplyAddress": "Calle, JOSE ANTONIO MAZA, 9, CHALA,",
            "SupplyPedaniaName":"",
            "Telemeasurement": "True",
            "ClientTypeText": "Doméstica",
            "ElectronicInvoice": "True",
            "ContractStatus": "Alta definitiva",
            "EntryDate": "25/06/2024 9:23:06",
            "Language": "Castellano",
            "CorrespondenceEmail": "j.lujanp@gmail.com",
            "CorrespondencePhone": "600860762"
        }
    ],
    "ResponseCode": "00001",
    "ResponseDescription": "OK"
}
'''

FAKE_CONSUMPTION='''{
    "UnitOfMeasurement" : "Litros",
    "ResponseCode" :"00001",
    "ResponseDescription" :"OK",
    "ConsumptionCurves":
    [{
        "DateTimeConsumptionCurve": "2024-06-29T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 0
      },
      {
        "DateTimeConsumptionCurve": "2024-06-30T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 468.33
      },
      {
        "DateTimeConsumptionCurve": "2024-07-02T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 463.63
      },
      {
        "DateTimeConsumptionCurve": "2024-07-03T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 336.3
      },
      {
        "DateTimeConsumptionCurve": "2024-07-05T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 3191.72
      },
      {
        "DateTimeConsumptionCurve": "2024-07-06T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 309.63
      },
      {
        "DateTimeConsumptionCurve": "2024-07-07T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 241.46
      },
      {
        "DateTimeConsumptionCurve": "2024-07-08T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 277.95
      },
      {
        "DateTimeConsumptionCurve": "2024-07-09T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 407.36
      },
      {
        "DateTimeConsumptionCurve": "2024-07-11T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 307.53
      },
      {
        "DateTimeConsumptionCurve": "2024-07-13T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 279.33
      },
      {
        "DateTimeConsumptionCurve": "2024-07-14T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 317.43
      },
      {
        "DateTimeConsumptionCurve": "2024-07-16T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 387.07
      },
      {
        "DateTimeConsumptionCurve": "2024-07-17T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 325.56
      },
      {
        "DateTimeConsumptionCurve": "2024-07-19T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 254.23
      },
      {
        "DateTimeConsumptionCurve": "2024-07-20T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 130.28
      },
      {
        "DateTimeConsumptionCurve": "2024-07-22T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 373.54001
      },
      {
        "DateTimeConsumptionCurve": "2024-07-23T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 88.64
      },
      {
        "DateTimeConsumptionCurve": "2024-07-25T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 376.21
      },
      {
        "DateTimeConsumptionCurve": "2024-07-26T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 396.54
      },
      {
        "DateTimeConsumptionCurve": "2024-07-28T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 201.62
      },
      {
        "DateTimeConsumptionCurve": "2024-07-29T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 404.04
      },
      {
        "DateTimeConsumptionCurve": "2024-07-31T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 442.18
      },
      {
        "DateTimeConsumptionCurve": "2024-08-01T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 168.71
      },
      {
        "DateTimeConsumptionCurve": "2024-08-03T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 1192.15
      },
      {
        "DateTimeConsumptionCurve": "2024-08-04T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 394.12
      },
      {
        "DateTimeConsumptionCurve": "2024-08-06T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 375.67
      },
      {
        "DateTimeConsumptionCurve": "2024-08-07T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 323.2
      },
      {
        "DateTimeConsumptionCurve": "2024-08-09T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 253.21001
      },
      {
        "DateTimeConsumptionCurve": "2024-08-10T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 275.76
      },
      {
        "DateTimeConsumptionCurve": "2024-08-12T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 903.42999
      },
      {
        "DateTimeConsumptionCurve": "2024-08-14T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 262.79999
      },
      {
        "DateTimeConsumptionCurve": "2024-08-15T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 297.51
      },
      {
        "DateTimeConsumptionCurve": "2024-08-17T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 465.18
      },
      {
        "DateTimeConsumptionCurve": "2024-08-18T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 554.85
      },
      {
        "DateTimeConsumptionCurve": "2024-08-20T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 410.51001
      },
      {
        "DateTimeConsumptionCurve": "2024-08-21T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 288.93
      },
      {
        "DateTimeConsumptionCurve": "2024-08-23T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 369.16
      },
      {
        "DateTimeConsumptionCurve": "2024-08-24T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 598.74
      },
      {
        "DateTimeConsumptionCurve": "2024-08-26T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 575.54999
      },
      {
        "DateTimeConsumptionCurve": "2024-08-27T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 443.08
      },
      {
        "DateTimeConsumptionCurve": "2024-08-29T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 328.45
      },
      {
        "DateTimeConsumptionCurve": "2024-08-30T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 282.32
      },
      {
        "DateTimeConsumptionCurve": "2024-09-01T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 167.75
      },
      {
        "DateTimeConsumptionCurve": "2024-09-02T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 352.17
      },
      {
        "DateTimeConsumptionCurve": "2024-09-04T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 356.35
      },
      {
        "DateTimeConsumptionCurve": "2024-09-05T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 436.54
      },
      {
        "DateTimeConsumptionCurve": "2024-09-07T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 346.1
      },
      {
        "DateTimeConsumptionCurve": "2024-09-08T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 258.09
      },
      {
        "DateTimeConsumptionCurve": "2024-09-10T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 568.59003
      },
      {
        "DateTimeConsumptionCurve": "2024-09-11T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 520.32
      },
      {
        "DateTimeConsumptionCurve": "2024-09-12T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 451.35
      },
      {
        "DateTimeConsumptionCurve": "2024-09-13T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 414.74
      },
      {
        "DateTimeConsumptionCurve": "2024-09-15T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 554.03003
      },
      {
        "DateTimeConsumptionCurve": "2024-09-16T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 409.13
      },
      {
        "DateTimeConsumptionCurve": "2024-09-18T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 200.46001
      },
      {
        "DateTimeConsumptionCurve": "2024-09-19T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 381.02
      },
      {
        "DateTimeConsumptionCurve": "2024-09-21T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 351.34
      },
      {
        "DateTimeConsumptionCurve": "2024-09-22T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 289.93
      },
      {
        "DateTimeConsumptionCurve": "2024-09-24T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 462.01
      },
      {
        "DateTimeConsumptionCurve": "2024-09-25T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 156.37
      },
      {
        "DateTimeConsumptionCurve": "2024-09-27T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 477.35001
      },
      {
        "DateTimeConsumptionCurve": "2024-09-28T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 269.91
      },
      {
        "DateTimeConsumptionCurve": "2024-09-30T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 350.56
      },
      {
        "DateTimeConsumptionCurve": "2024-10-01T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 447.88
      },
      {
        "DateTimeConsumptionCurve": "2024-10-03T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 686.87
      },
      {
        "DateTimeConsumptionCurve": "2024-10-04T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 459.33
      },
      {
        "DateTimeConsumptionCurve": "2024-10-06T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 297.72
      },
      {
        "DateTimeConsumptionCurve": "2024-10-07T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 209.6
      },
      {
        "DateTimeConsumptionCurve": "2024-10-09T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 293.03
      },
      {
        "DateTimeConsumptionCurve": "2024-10-10T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 491.19
      },
      {
        "DateTimeConsumptionCurve": "2024-10-12T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 259.94
      },
      {
        "DateTimeConsumptionCurve": "2024-10-14T00:00:00",
        "ReadingIndex": 0,
        "ConsumptionValue": 247.98
      }
    ]
}'''
