# This file is the actual code for the custom Python dataset first-plugin_algolia

# import the base class for the custom dataset
from six.moves import xrange
from dataiku.connector import Connector

"""
A custom Python dataset is a subclass of Connector.

The parameters it expects and some flags to control its handling by DSS are
specified in the connector.json file.

Note: the name of the class itself is not relevant.
"""
class MyConnector(Connector):

    def __init__(self, config, plugin_config):
        """
        The configuration parameters set up by the user in the settings tab of the
        dataset are passed as a json object 'config' to the constructor.
        The static configuration parameters set up by the developer in the optional
        file settings.json at the root of the plugin directory are passed as a json
        object 'plugin_config' to the constructor
        """
        Connector.__init__(self, config, plugin_config)  # pass the parameters to the base class

        # perform some more initialization
        self.theparam1 = self.config.get("parameter1", "defaultValue")

    def get_read_schema(self):
        """
        Returns the schema that this connector generates when returning rows.

        The returned schema may be None if the schema is not known in advance.
        In that case, the dataset schema will be infered from the first rows.

        If you do provide a schema here, all columns defined in the schema
        will always be present in the output (with None value),
        even if you don't provide a value in generate_rows

        The schema must be a dict, with a single key: "columns", containing an array of
        {'name':name, 'type' : type}.

        Example:
            return {"columns" : [ {"name": "col1", "type" : "string"}, {"name" :"col2", "type" : "float"}]}

        Supported types are: string, int, bigint, float, double, date, boolean
        """

        # In this example, we don't specify a schema here, so DSS will infer the schema
        # from the columns actually returned by the generate_rows method
        return None

    def generate_rows(self, dataset_schema=None, dataset_partitioning=None,
                            partition_id=None, records_limit = -1):
        """
        The main reading method.

        Returns a generator over the rows of the dataset (or partition)
        Each yielded row must be a dictionary, indexed by column name.

        The dataset schema and partitioning are given for information purpose.        
        for i in xrange(1,10):
            yield { "first_col" : str(i), "my_string" : "Yes" }
        """
        
        # Get a handle on the Algolia index
        index = self._get_index()

        search_settings = {}

        if dataset_partitioning is not None:
            facetFilters = []
            idx = 0

            # Split the partition identifiers by dimension
            id_chunks = partition_id.split("|")

            for dim in dataset_partitioning["dimensions"]:

                # For each dimension, define a facet filter in the form
                # dimension_name:value
                facetFilters.append(dim["name"] + ":" + id_chunks[idx])
                idx += 1

            search_settings["facetFilters"] = ",".join(facetFilters)

        print "Final settings : %s" % search_settings

        res = index.search("*", search_settings)

        for hit in res["hits"]:
            yield hit

    # As for generate_rows, we receive here the partitioning and the partition
    # id to write
    def get_writer(self, dataset_schema=None, dataset_partitioning=None, partition_id=None):
          return AlgoliaSearchConnectorWriter(self.config, self._get_index(),
                  dataset_schema, dataset_partitioning, partition_id)


    def get_partitioning(self):
        """
        Return the partitioning schema that the connector defines.
        """
        raise Exception("Unimplemented")


    def list_partitions(self, dataset_partitioning):
        assert dataset_partitioning is not None

        # Ask Algolia to facet on the name of each dimension
        facets = [dim["name"] for dim in dataset_partitioning["dimensions"]]
        search_settings = {}
        search_settings["facets"] = facets

        # Perform the faceted search
        index = self._get_index()
        res = index.search("*", search_settings)

        # Gather the various values of each dimension in a list of list
        vals =[]
        for dim in dataset_partitioning["dimensions"]:
            facet = res["facets"][dim["name"]]
            vals.append(facet.keys())

        # Make the cartesian products of the lists of lists.
        # For example, if we had [ [cat1, cat2], [author1, author2] ]
        # in vals, we'll end up in ret with:
        # ["cat1|author1", "cat1|author2", "cat2|author1", "cat2|author2"]

        ret = []
        import itertools
        for element in itertools.product(*vals):
            ret.append("|".join(element))
        print ret
        return ret


    def partition_exists(self, partitioning, partition_id):
        """Return whether the partition passed as parameter exists

        Implementation is only required if the corresponding flag is set to True
        in the connector definition
        """
        raise Exception("unimplemented")


    def get_records_count(self, partitioning=None, partition_id=None):
        """
        Returns the count of records for the dataset (or a partition).

        Implementation is only required if the corresponding flag is set to True
        in the connector definition
        """
        raise Exception("unimplemented")


class CustomDatasetWriter(object):
    def __init__(self):
        pass

    def write_row(self, row):
        """
        Row is a tuple with N + 1 elements matching the schema passed to get_writer.
        The last element is a dict of columns not found in the schema
        """
        raise Exception("unimplemented")

    def close(self):
        pass
