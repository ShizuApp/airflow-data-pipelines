from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """
    Run and fetch records from a Sql statement and compare it
    to expected results, raise ValueError if different

    Args:
    conn_id: name of Redshift's Airflow connection
    cases: dict{'sql': str, 'answer': int} Sql and expected answer
    """

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 conn_id="",
                 cases=[{}],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)

        self.conn_id = conn_id
        self.cases = cases


    def execute(self, context):
        rds_hook = PostgresHook(postgres_conn_id=self.conn_id)
        passed = 0

        for case in self.cases:
            records = rds_hook.get_records(case['sql'])[0]
        
            if records[0] == case['answer']:
                passed += 1
            else:
                raise ValueError("Unexpected value during quality check")

        self.log.info(f"Test cases passed: {passed}/{len(self.cases)}")
