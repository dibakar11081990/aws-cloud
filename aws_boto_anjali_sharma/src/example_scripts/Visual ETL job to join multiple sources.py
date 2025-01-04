import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Plans
Plans_node1685352206564 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://aws-bigdata-blog/artifacts/telco-data-monetization-configs-us-east-2/data/tariff_plan_desc_20190501.csv.gz"], "recurse": True}, transformation_ctx="Plans_node1685352206564")

# Script generated for node Plan assignment
Planassignment_node1685352066932 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://aws-bigdata-blog/artifacts/telco-data-monetization-configs-us-east-2/data/customer_subscription_map_20190501.csv.gz"], "recurse": True}, transformation_ctx="Planassignment_node1685352066932")

# Script generated for node Subscribers
Subscribers_node1 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://aws-bigdata-blog/artifacts/telco-data-monetization-configs-us-east-2/data/crm_demographics_20190501.csv.gz"], "recurse": True}, transformation_ctx="Subscribers_node1")

# Script generated for node Join
Join_node1685352536679 = Join.apply(frame1=Planassignment_node1685352066932, frame2=Subscribers_node1, keys1=["msisdn"], keys2=["msisdn"], transformation_ctx="Join_node1685352536679")

# Script generated for node Join
Join_node1685352743084 = Join.apply(frame1=Join_node1685352536679, frame2=Plans_node1685352206564, keys1=["plan_id"], keys2=["plan_id"], transformation_ctx="Join_node1685352743084")

# Script generated for node Select Fields
SelectFields_node1685353779136 = SelectFields.apply(frame=Join_node1685352743084, paths=["plan_id", "gender", "birth_date", "is_vip", "plan_desc", "plan_price"], transformation_ctx="SelectFields_node1685353779136")

# Script generated for node Change Schema
ChangeSchema_node1685353487597 = ApplyMapping.apply(frame=SelectFields_node1685353779136, mappings=[("plan_id", "string", "plan_id", "bigint"), ("gender", "string", "gender", "string"), ("birth_date", "string", "birth_date", "string"), ("is_vip", "string", "is_vip", "boolean"), ("plan_desc", "string", "plan_desc", "string"), ("plan_price", "string", "plan_price", "int")], transformation_ctx="ChangeSchema_node1685353487597")

# Script generated for node Catalog
Catalog_node1685352920969 = glueContext.getSink(path="s3://aws-glue-temporary-245491356924-us-east-2/example/subscriber_plans/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=["plan_id"], enableUpdateCatalog=True, transformation_ctx="Catalog_node1685352920969")
Catalog_node1685352920969.setCatalogInfo(catalogDatabase="default",catalogTableName="subscriber_plans")
Catalog_node1685352920969.setFormat("glueparquet", compression="snappy")
Catalog_node1685352920969.writeFrame(ChangeSchema_node1685353487597)
job.commit()