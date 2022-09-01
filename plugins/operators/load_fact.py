from airflow.hooks.postgres_hook import PostgresHook
#from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    """
    Insert data into a table using provided SELECT Sql statement

    Args:
    sql: complete select SQL query
    conn_id: name of Redshift's Airflow connection
    table: table name
    truncate: (bool) Empty table before insert Sql, 
    False by default
    """

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 sql="",
                 conn_id = "",
                 table='',
                 truncate=False,
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.sql = sql
        self.table = table
        self.truncate = truncate

    def execute(self, context):
        rds_hook = PostgresHook(postgres_conn_id=self.conn_id)

        if self.truncate:
            self.log.info("Emptying table before running insert query")
            rds_hook.run(f"TRUNCATE {self.table}")
        
        rds_hook.run(
            f"""
            INSERT INTO {self.table}
            {self.sql};
            """
        )
