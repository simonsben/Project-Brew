![](banner.png)

Project brew scrapes the information about all the beers offered by [The Beer Store](https://www.thebeerstore.ca/).
By default, it then compresses the data and saves it locally.
If the `bucket_name` environment variable is present it will instead attempt to save the compressed data to that S3 bucket.


## Usage

The code was meant to be executed periodically as an AWS Lambda function, but can also be run locally.


### Local

* Install dependencies with `pip install -r requirements`
* Make `data/` directory
* Run by executing `python -c "from collect_info import handler; handler(None, None)"`


### AWS Function (intended use)

From the root directory,

* Execute `./resources/make_function.sh`
* Execute `./resources/make_layer.sh`

In the AWS console

* Create an S3 bucket to save the result to
* Create a new role granting permission to push objects to your S3 bucket
* Create a new function with this role and a Python 3.7 environment
* Create and add a new layer, using `deployment_layer.zip`
* Upload the code from a zip file using `deployment_function.zip`
* Edit the runtime setting to specify `collect_info.handler` as the handler
* Add an environment variable called `bucket_name` specifying the name of the bucket you created
* Change the maximum execution time to something longer, like 5 min
* Optionally, add a recurring trigger to run this function periodically (i.e. EventBridge)
