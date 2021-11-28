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
    if "dealerId" in dict.keys():
        reviews = []
        databaseName = "reviews"
        try:
            client = Cloudant.iam(
                account_name=dict["COUCH_USERNAME"],
                api_key=dict["IAM_API_KEY"],
                connect=True,
            )
            databaseName = "reviews"
            database = client[databaseName]
            for document in database:
                """
                review = {}
                review["id"] = document['id'];
                review["name"] = document['name'];
                review["dealership"] = document['dealership'];
                review["review"] = document['review'];
                review["purchase"] = document['purchase'];
                if (document['purchase']):
                    review["purchase_date"] = document['purchase_date'];
                    review["car_make"] = document['car_make'];
                    review["car_model"] = document['car_model'];
                    review["car_year"] = document['car_year'];
                """
                if(dict["dealerId"] and int(dict["dealerId"]) == document['dealership']):
                    review = {k:v for k,v in document.items() if k not in ['_id','_rev']}
                    reviews.append(review);
            if len(reviews) == 0:
                return {"error": "dealerId does not exist"} 
        except CloudantException as ce:
            print("unable to connect")
            return {"error": ce}
        except (requests.exceptions.RequestException, ConnectionResetError) as err:
            print("connection error")
            return {"error": err}
    
        return { "reviews": reviews}
    else:
        return {"error": "dealerId missing"}
