
# Unilife

Unilife app is a mobile app where we share our unilife with others.


## REST API

### Get all posts

```
  GET /api/post/list/
```

### Get a certain post

```
  GET /api/post/{id}/
```
#### Path Parameters

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of item to fetch |


### Get a certain user's posts

```
  GET /api/user/${id}/posts/
```
#### Path Parameters 

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of user to fetch |

### Create a post

```
  POST /api/post/create/
```
#### Header Parameters

| Key                   | Value                             |
| :--------------       |:--------------------------------  |            
| `Authorization`       |Token {token}                      |


### Update a post

```
  PUT /api/post/${id}/update/
```

#### Header Parameters

| Key                   | Value                             |
| :--------------       |:--------------------------------  |            
| `Authorization`       |Token {token}                      |

### Delete a post

```
  DELETE /api/post/${id}/delete/
```
#### Header Parameters

| Key                   | Value                             |
| :--------------       |:--------------------------------  |            
| `Authorization`       |Token {token}                      |


### Generate a Token

```
  POST  /api/auth/
```



