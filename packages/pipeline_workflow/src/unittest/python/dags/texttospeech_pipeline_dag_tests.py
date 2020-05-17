import unittest
from airflow.models import DagBag


class TestTTSPipelineDAG(unittest.TestCase):
    """Check TTSPipelineDAG expectation"""

    def setUp(self):
        self.dagbag = DagBag()

    def test_task_count(self):
        """Check task count of texttospeech_pipeline dag"""
        dag_id = 'texttospeech_pipeline'
        dag = self.dagbag.get_dag(dag_id)
        self.assertEqual(len(dag.tasks), 1)

    def test_contain_tasks(self):
        """Check task contains in texttospeech_pipeline dag"""
        dag_id = 'texttospeech_pipeline'
        dag = self.dagbag.get_dag(dag_id)
        tasks = dag.tasks
        task_ids = list(map(lambda task: task.task_id, tasks))
        self.assertListEqual(sorted(task_ids), sorted(['curation-component']))

    def test_dependencies_of_listbucket_task(self):
        """Check the task dependencies of sample_list_bucket in texttospeech_pipeline dag"""
        dag_id = 'texttospeech_pipeline'
        dag = self.dagbag.get_dag(dag_id)
        listbucket_task = dag.get_task('curation-component')

        upstream_task_ids = list(map(lambda task: task.task_id, listbucket_task.upstream_list))
        self.assertListEqual(upstream_task_ids, [])
        downstream_task_ids = list(map(lambda task: task.task_id, listbucket_task.downstream_list))
        self.assertListEqual(downstream_task_ids,[])

