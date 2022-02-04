# MATHAPI server
The mathapi server is a small django aplication that exposes a RESTAPI
to perform different math operations.


###Setup

 * Before building the image, please make sure that the startup.sh script has UNIX line endings (LF), else it will throw errors!
 * First you'll need to install Docker
 * Use docker to create the image based off the Dockerfile:
 ```docker build -t python-django .``` when you are in the same 
 directory with the Dockerfile/project
 * Run the container based on that image and publish the right port: 
 
   ```docker run --name Django -p 8000:8000 python-django```

### Currently supported operations are:
* factorial: http POST to https://localhost:8000/mathapi/factorial/
* fibonacci: http POST to https://localhost:8000/mathapi/fibonacci/
* power: http POST to https://localhost:8000/mathapi/power/

#### Usage example for the function 'power'
#####The input arguments for each function will be provided as a json in the body of the post:
```
{
    "arg1": 3,
    "arg2": 2
}
```

#####The returned response will be similar:
```
{
    "arg1": 3,
    "arg2": 2,
    "ret_code": 0,
    "result": 9
}
```
