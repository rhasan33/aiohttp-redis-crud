## User CRUD application using aiohttp and redis

### Installation

`docker-compose up`

### Endpoints 

Please import `User CRUD.postman_collection.json` as postman dump

### Authorization Headers

```
{
    'create': ['93a5fcba-c31b-482e-8177-41b469cdb4f8'],
    'update': ['7643b5f3-5ec7-48a2-8ad7-5fc6e198e5fd', '93a5fcba-c31b-482e-8177-41b469cdb4f8'],
    'get': [
        '93a5fcba-c31b-482e-8177-41b469cdb4f8',
        '7643b5f3-5ec7-48a2-8ad7-5fc6e198e5fd',
        'ced29724-0ef7-4e5a-9f8f-b8404f142553'
    ],
    'delete': ['93a5fcba-c31b-482e-8177-41b469cdb4f8']
}
```