#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(dict):
    
    reviews = []
    databaseName = "reviews"
    if('review' in dict.keys()):
        try:
            client = Cloudant.iam(
                account_name=dict["COUCH_USERNAME"],
                api_key=dict["IAM_API_KEY"],
                connect=True,
            )
            databaseName = "reviews"
            database = client[databaseName]
            my_document = database.create_document(dict['review'])
            if my_document.exists():
                print('SUCCESS!!')
                return { "message": 'SUCCESS!!'}
            else:
                return {"error": "FAILED"}
        except CloudantException as ce:
            print("unable to connect")
            return {"error": ce}
        except (requests.exceptions.RequestException, ConnectionResetError) as err:
            print("connection error")
            return {"error": err}
    else:
        return {"error": "review missing"}
