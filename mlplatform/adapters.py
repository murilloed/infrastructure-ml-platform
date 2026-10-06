"""Optional adapters: pip install pymongo pyspark. Integration not validated here."""
def save_mongo(uri,events):
    from pymongo import MongoClient,UpdateOne
    from .core import validate
    validated=[validate(e) for e in events]
    with MongoClient(uri,serverSelectionTimeoutMS=5000) as client:
        collection=client.portfolio.events
        collection.create_index('id',unique=True)
        if validated:
            return collection.bulk_write([UpdateOne({'id':e['id']},{'$setOnInsert':e},upsert=True) for e in validated])

def spark_summary(input_path,output_path):
    from pyspark.sql import SparkSession,functions as F
    from pyspark.sql.types import StructType,StructField,StringType,DoubleType
    schema=StructType([StructField('id',StringType()),StructField('asset',StringType()),
                       StructField('timestamp',StringType()),StructField('cpu',DoubleType())])
    spark=SparkSession.builder.appName('InfrastructureML').getOrCreate()
    try:
        df=spark.read.schema(schema).json(input_path)
        clean=df.filter(F.col('id').isNotNull() & F.col('asset').isNotNull() &
                        F.to_timestamp('timestamp').isNotNull() & F.col('cpu').between(0,100)).dropDuplicates(['id'])
        clean.groupBy('asset').agg(F.avg('cpu').alias('mean_cpu'),F.count('*').alias('events')).write.mode('overwrite').parquet(output_path)
    finally: spark.stop()
