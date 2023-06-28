import pymongo
from datetime import datetime, timedelta


class GetMongoData:

    def __init__(self, host_type=None, db_url=None, db_user=None, db_password=None, source_db=None):
        self.my_db = self.get_mongo_database(host_type=host_type, db_url=db_url, db_user=db_user,
                                             db_password=db_password, source_db=source_db)

    def get_mongo_database(self, host_type=None, db_url=None, db_user=None, db_password=None, source_db=None):
        if host_type is not None and host_type == 'on_premise':
            my_db_obj = self.get_mongo_onpremise_database(db_url=db_url, db_user=db_user, db_password=db_password,
                                                          source_db=source_db)
            return my_db_obj
        my_db_obj = self.get_mongo_cloud_database(db_url=db_url, db_user=db_user, db_password=db_password,
                                                  source_db=source_db)
        return my_db_obj

    def get_mongo_cloud_database(self, db_url=None, db_user=None, db_password=None, source_db=None):
        print('connecting to mongodb...')
        my_client = pymongo.MongoClient('mongodb+srv://' + db_user +
                                        ':' + db_password + '@' + db_url
                                        + '/' + source_db + '?retryWrites=true&w=majority')
        print("connected...")
        my_db_obj = my_client[source_db]
        return my_db_obj

    def get_mongo_onpremise_database(self, db_url=None, db_user=None, db_password=None, source_db=None):
        print('connecting to mongodb...')
        my_client = pymongo.MongoClient('mongodb://' + db_user + ':' + db_password + '@' + db_url
                                        + '/?authSource=admin&readPreference=primary&directConnection'
                                          '=true&ssl=false')
        print("connected...")
        my_db_obj = my_client[source_db]
        return my_db_obj

    def get_kpi_list(self, collection_name=None, identifier_key=None, identifier=None):
        collection = self.my_db[collection_name]
        if collection is None:
            return None
        document_list = collection.find({identifier_key: identifier})
        document_list = list(document_list)
        return document_list

    def get_test_list(self, collection_name=None, required_key=None, start_time=None, end_time=None, time_key=None):
        collection = self.my_db[collection_name]
        if collection is None:
            return None
        # document_list = list(collection.find({identifier_key: identifier}))
        document_list = None
        if collection is None:
            return None
        if start_time is not None and end_time is not None:
            # print({"$and": [{time_key: {"$gte": start_time}}, {time_key: {"$lte": end_time}}]})
            document_list = collection.distinct(required_key, {
                "$and": [
                    {
                        time_key: {
                            "$gte": start_time
                        }
                    },
                    {
                        time_key: {
                            "$lte": end_time
                        }
                    }
                ]
            })
        elif start_time is not None:
            document_list = collection.distinct(required_key, {
                time_key: {
                    "$gte": start_time
                }
            })

        elif end_time is not None:
            document_list = collection.distinct(required_key, {
                time_key: {
                    "$lte": end_time
                }
            })

        else:
            document_list = collection.find(required_key)

        document_list = list(document_list)
        print(document_list)
        return document_list

    def get_test_list1(self, collection_name=None, required_key=None, start_time=None, end_time=None, time_key=None):
        collection = self.my_db[collection_name]
        if collection is None:
            return None

        document_list = None
        test_ids = []
        if collection is None:
            return None
        if start_time is not None and end_time is not None:
            # print({"$and": [{time_key: {"$gte": start_time}}, {time_key: {"$lte": end_time}}]})
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            start_time = start_time - timedelta(minutes=30)
            pipeline = [
                {
                    '$addFields': {
                        'dateTime1': {
                            '$toDate': '$' + time_key
                        }
                    }
                }, {
                    '$match': {
                        'dateTime1': {
                            '$gte': datetime.fromisoformat(start_time.isoformat().format("%Y-%m-%dT%H:%M:%SZ")),
                            '$lte': datetime.fromisoformat(end_time.isoformat().format("%Y-%m-%dT%H:%M:%SZ"))
                        }
                    }
                }, {
                    '$project': {
                        required_key: 1,
                        '_id': 0
                    }
                }, {
                    '$group': {
                        '_id': None,
                        required_key: {
                            '$addToSet': '$' + required_key
                        }
                    }
                }
            ]
        elif start_time is not None:
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            start_time = start_time - timedelta(minutes=30)
            pipeline = [
                {
                    '$addFields': {
                        'dateTime1': {
                            '$toDate': '$' + time_key
                        }
                    }
                }, {
                    '$match': {
                        'dateTime1': {
                            '$gte': datetime.fromisoformat(start_time.isoformat().format("%Y-%m-%dT%H:%M:%SZ")),
                        }
                    }
                }, {
                    '$project': {
                        required_key: 1,
                        '_id': 0
                    }
                }, {
                    '$group': {
                        '_id': None,
                        required_key: {
                            '$addToSet': '$' + required_key
                        }
                    }
                }
            ]

        elif end_time is not None:
            end_time = datetime.fromisoformat(end_time.isoformat().format("%Y-%m-%dT%H:%M:%SZ"))
            pipeline = [
                {
                    '$addFields': {
                        'dateTime1': {
                            '$toDate': '$' + time_key
                        }
                    }
                }, {
                    '$match': {
                        'dateTime1': {
                            '$lte': end_time.isoformat(),
                        }
                    }
                }, {
                    '$project': {
                        required_key: 1,
                        '_id': 0
                    }
                }, {
                    '$group': {
                        '_id': None,
                        required_key: {
                            '$addToSet': '$' + required_key
                        }
                    }
                }
            ]
        else:
            print("start or end time not found ------------")
            return test_ids
        print('---------------------------')
        print(pipeline)
        document_list = collection.aggregate(pipeline)

        for doc in document_list:
            print("+++++++++++++++++++++++++")
            test_ids = list(doc[required_key])
        print(test_ids)
        return test_ids

    def get_test_details(self, collection_name=None, identifier=None, identifier_key=None):
        collection = self.my_db[collection_name]
        print(collection_name)
        if collection is None:
            return None
        document = collection.find_one({identifier_key: identifier})
        return document
