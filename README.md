# PC Builder API
![Logo](misc/logo.jpg)

## Пример использования автосборщика
curl -X POST http://127.0.0.1:5000/build -H "Content-Type: application/json" -d '{"price": "50000", "cfg": "Gaming"}'

### Вывод
![Screen1](misc/screen1.png)

## Отдельная часть в зависимости от уже установленных
### Запросы (GET)
- filter_mb
- filter_cpu
- filter_gpu
- filter_ram
- filter_psu
### Примеры
- curl -X GET http://127.0.0.1:5000/filter_mb -H "Content-Type: application/json" -d '{"MB": "None", "CPU": 1, "GPU": 7, "RAM": 0, "PSU": "None"}'
- curl -X GET http://127.0.0.1:5000/filter_cpu -H "Content-Type: application/json" -d '{"MB": 15, "CPU": "None", "GPU": "None", "RAM": "None", "PSU": "None"}'
- curl -X GET http://127.0.0.1:5000/get_id_by_name -H "Content-Type: application/json" -d '{"name": "Samsung SSD 980 PRO 1TB"}'
### Вывод
![Screen2](misc/screen2.png)