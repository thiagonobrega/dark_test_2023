python -m pytest -n auto


python -m pytest -n auto ./tests --reportportal --dist loadscope

pip freeze 

```bash
curl --location --request POST 'http://0.0.0.0:5000//api/people' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data-raw '{
   "fname": "TAU",
   "lname": "User"
 }'
```