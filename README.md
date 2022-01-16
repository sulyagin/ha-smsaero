# SMSAero.ru Notify

Компонент Home Assistant для отправки SMS сообщений через сервис [smsaero.ru](https://smsaero.ru)

# Установка и настройка
Для установки поместите папку smsaero в *.homeassistant/custom_components* или добавьте этот репозиторий через [HACS](https://hacs.xyz)  

# Настройка
Пример конфигурации Home Assistant:
```yaml
notify:
  - name: smsaero
    platform: smsaero
    email: <SMSAERO_EMAIL>
    api_key: <SMSAERO_API_KEY>
```
Для получения API ключа необходимо зарегистрироваться в сервисе [smsaero.ru](https://smsaero.ru)

# Использование
Пример использования службы notify.smsaero для отправки SMS сообщений:
```yaml
service: notify.smsaero
  message: 'тестовое уведомление'
  target: 
    - '79990000000'
    - '79990000001'
    - '79990000002'
```
Пример сценария автоматизации:
```yaml
alias: 'SMS Test'
description: 'СМС уведомление'
trigger:
  - platform: state
    entity_id: input_boolean.sms_test_1
    to: 'on'
condition: []
action:
  - service: notify.smsaero
    data:
      message: 'тестовое уведомление'
      target:
        - '79990000000'
mode: single
```