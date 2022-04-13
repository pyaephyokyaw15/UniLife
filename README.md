
# Project Title

A brief description of what this project does and who it's for


# REST API

## Get all posts

```http
  GET /api/post/list
```

## Get a certain post

```http
  GET /api/post/{id}
```
#### Path Parameters

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of item to fetch |

## Get a certain user's posts

```http
  GET /api/user/${id}/posts
```
#### Path Parameters 

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `integer` | **Required**. Id of user to fetch |

### Create a post

```http
  POST /api/post/create
```
#### Header Parameters

| Key                   | Value                             |
| :--------------       |:--------------------------------  |            |
| `Authorization`       |Token <token>                      |


### Update a post

```http
  PUT /api/post/${id}/update
```

#### Header Parameters

| Key                   | Value                             |
| :--------------       |:--------------------------------  |            |
| `Authorization`       |Token <token>                      |

### Delete a post

```http
  DELETE /api/post/${id}/delete
```
#### Header Parameters

| Key                   | Value                             |
| :--------------       |:--------------------------------  |            |
| `Authorization`       |Token <token>                      |


### Generate a Token

```http
  POST  /api/auth
```



