import json
import sys
from collections import Counter

with open(sys.argv[1], "r") as fr, open("out_company.json", "a") as fa:
    for i in fr:
        record = json.loads(i)
        record = record["_source"]
        #Build Parent Key:Value
##################################################################################
        build_parent_record = {}
        build_parent_map = {"domain":"company_domain", "name":"company_name_exact", "company_names":"company_name_all", "company_type":"company_type", "status":"company_operating_status", "revenue_range":"company_revenue_range", "categories":"company_categories", "location_identifiers":"company_location_identifiers"}
        build_parent_linkedin_map = {"company_names":"company_names_all", "country":"company_country", "founded":"company_founded", "overview":"company_description", "size":"company_employees_range", "url":"company_url", "image_url":"company_image_url"}
        build_parent_cb_map = {"contact_email":"company_email", "founded_on":"company_founded", "description":"company_description", "employees_range":"company_employees_range", "number_of_board_members":"company_number_of_board_members"}
        build_parent_websitedata_map = {"url":"company_url"}
        build_parent = {}
        for k,v in build_parent_map.items():
            if v not in build_parent_record:
                build_parent_record[v] = ""
            if k in record:
                build_parent_record[v] = record[k]

        for k,v in build_parent_cb_map.items():
            if v not in build_parent_record:
                build_parent_record[v] = ""
            if "crunchbase" in record and k in record["crunchbase"]:
                build_parent_record[v] = record["crunchbase"][k]

        for k,v in build_parent_linkedin_map.items():
            if v not in build_parent_record:
                build_parent_record[v] = ""
            if  "linkedin" in record and k in record["linkedin"]:
                build_parent_record[v] = record["linkedin"][k]
        #Build Crunchbase Key:Value
####################################################################################
        build_cb_record = {}  
        build_crunchbase_map = {"last_funding_amount":"last_funding_amount", "last_funding_type":"last_funding_type", "last_funding_rounds":"last_funding_rounds", "number_of_investors":"number_of_investors", "number_of_funding_rounds":"number_of_funding_rounds", "company_funding":"company_funding"}

        if "crunchbase" in record:
            for k,v in build_crunchbase_map.items():
                if v not in build_cb_record:
                    build_cb_record[v] = ""
                if k in record["crunchbase"]:
                    build_cb_record[v] = record["crunchbase"][k]
              
        # Build Crunchbase Aquisitions Key:Value
###################################################################################
        build_aquired = {}
        build_aquiredby = {}

        build_acquired_map = {"acquired_on":"acquired_on", "acquiree_cb_url":"acquiree_cb_url", "acquiree_city":"acquiree_city", "acquiree_country_code":"acquiree_country_code", "acquiree_name":"acquiree_name", "acquiree_region":"acquiree_region", "acquisition_type" :"acquisition_type", "price": "price", "price_currency_code":"price_currency_code", "price_usd":"price_usd", "state_code":"state_code"} 
        if "crunchbase" in record and "acquisitions" in record["crunchbase"]:
            recordacquired = record["crunchbase"]["acquisitions"]
            for i in recordacquired["acquired"]: # For each list item in acquired
                for k,v in build_acquired_map.items():
                    if v not in build_aquired:
                        build_aquired[v] = ""
                    if k in i:
                        build_aquired[v] = i[k]

        build_acquiredby_map = {"acquisition_type":"acquisition_type", "acquirer_country_code":"acquirer_country_code", "acquirer_name":"acquirer_name", "acquired_on":"acquired_on", "acquirer_city":"acquirer_city", "acquirer_cb_url":"acquirer_cb_url", "acquirer_region": "acquirer_region", "acquirer_state_code": "acquirer_state_code"}
        if "crunchbase" in record and "acquisitions" in record["crunchbase"]:
            recordacquiredby = record["crunchbase"]["acquisitions"]
            for i in recordacquiredby["acquiredBy"]: # For each list item in acquiredby
                for k,v in build_acquiredby_map.items():
                    if v not in build_aquiredby:
                        build_aquiredby[v] = ""
                    if k in i:
                        build_aquiredby[v] = i[k]

        build_cb_record.update({"aquisitions":[{"acquired":build_aquired, "acquiredby":build_aquiredby}]})
        build_parent_record.update({"crunchbase":build_cb_record})
        if "crunchbase" in record and "acquisitions" in record["crunchbase"] and "acquired" in record["crunchbase"]["acquisitions"]:
            print(json.dumps(build_parent_record))
       
