
CMD commands :

to update the clustering fields to the existing table :

bq update --clustering_fields=natinality cap_dataset.driver_cmd

column name = nationality and dataset = cap_dataset
to update the clustering fields to the existing table with multiple fields :

bq update --clustering_fields=natinality,dob cap_dataset.driver_cmd


-- To remane the table :

not directly we cant do so we will copy the table to a new table with the new name 
and then delete the old table

bq cp cap_dataset.driver_cmd cap_dataset.driver_cmd_new

-- to delete the table :

bq rm -f cap_dataset.driver_cmd

-- for default region name change 

[gcloud config set compute/zone NAME].

-- the sql command for the end to end a partition to remaning the original table :

-- creating a backup before the starting of the procedure:

create table drivers_backup as select * from cap_dataset.driver_cmd;

create table drivers_partitioned_clustered
partition by date(dob)
cluster by natinality
as select * from cap_dataset.driver_cmd;

drop table cap_dataset.drivers_cmd;

alter table cap_dataset.drivers_cmd_new rename drivers_cmd;