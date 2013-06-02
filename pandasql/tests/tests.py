import pandas as pd
from pandasql import sqldf
import string
import unittest


class PandaSQLTest(unittest.TestCase):

    def setUp(self):
        return

    def test_select(self):
        df = pd.DataFrame({
                 "letter_pos": [i for i in range(len(string.ascii_letters))],
                 "l2": list(string.ascii_letters)
        })
        result = sqldf("select * from df LIMIT 10;", locals())
        self.assertEqual(len(result), 10)

    def test_join(self):

        df = pd.DataFrame({
            "letter_pos": [i for i in range(len(string.ascii_letters))],
            "l2": list(string.ascii_letters)
        })

        df2 = pd.DataFrame({
            "letter_pos": [i for i in range(len(string.ascii_letters))],
            "letter": list(string.ascii_letters)
        })

        result = sqldf("SELECT a.*, b.letter FROM df a INNER JOIN df2 b ON a.l2 = b.letter LIMIT 20;", locals())
        self.assertEqual(len(result), 20)

    def test_query_with_spacing(self):

        df = pd.DataFrame({
            "letter_pos": [i for i in range(len(string.ascii_letters))],
            "l2": list(string.ascii_letters)
        })

        df2 = pd.DataFrame({
            "letter_pos": [i for i in range(len(string.ascii_letters))],
            "letter": list(string.ascii_letters)
        })
        
        result = sqldf("SELECT a.*, b.letter FROM df a INNER JOIN df2 b ON a.l2 = b.letter LIMIT 20;", locals())
        self.assertEqual(len(result), 20)

        q = """
            SELECT
            a.*
        FROM
            df a
        INNER JOIN
            df2 b
        on a.l2 = b.letter
        LIMIT 20
        ;"""
        result = sqldf(q, locals())
        self.assertEqual(len(result), 20)

    def test_query_with_sqlite_parameters(self):
        mylist = [ ('a',1), ('b',  2)]
        myvariable=10

        #my dico is : a personal definition, then locals() , then globals()
        mydico=dict(globals(),**locals())
        mydico['myanswer']=42

        #sqlite will find parameters by name (:myvariable)
        result = sqldf("SELECT  max(:myanswer),sum(:myvariable)  FROM mylist", mydico)
        self.assertEqual(result.values.tolist(), [[42, 20]])

    def test_query_single_list(self):

        mylist = [i for i in range(10)]

        result = sqldf("SELECT * FROM mylist", locals())
        self.assertEqual(len(result), 10)

    def test_query_list_of_lists(self):

        mylist = [[i for i in range(10)], [i for i in range(10)]]

        result = sqldf("SELECT * FROM mylist", locals())
        self.assertEqual(len(result), 2)

    def test_query_list_of_tuples(self):

        mylist = [tuple([i for i in range(10)]), tuple([i for i in range(10)])]

        result = sqldf("SELECT * FROM mylist", locals())
        self.assertEqual(len(result), 2)

    def test_query_dictionary(self):

        mylist = {'a': 1, 'c': 3, 'b': 2}
        result = sqldf("SELECT max(c0),sum(c1) FROM mylist", locals())
        self.assertEqual(result.values.tolist(), [['c', 6]])

    def test_query_with_imported_table_as_parameters(self):
        "use ':' prefix convention to specify a python table"
        mylist = [ ('a',1), ('b',  2)]       
        result = sqldf("SELECT min(c0), sum(c1)  FROM :mylist", locals())
        self.assertEqual(result.values.tolist(), [['a', 3]])

    def test_query_with_several_requests_and_internal_tables(self):
        "several requests, using internal and external tables"
        mylist = [ ('a',1), ('b',  2)]       
        result = sqldf("""create table t_sql as SELECT sum(c1) c FROM :mylist;
        select c, c+1 from t_sql""", locals())
        self.assertEqual(result.values.tolist(), [[3, 4]])

    def test_table_with_prefix_versus_whithout(self):
        "t is different from :t"
        t = [ ('a',1), ('b',  2)]       
        result = sqldf("""drop table if exists t; -- compatibility need
        create table t as SELECT min(c0) c0,sum(c1) c1 FROM :t;
        select t.c1,:t.c1 from t inner join :t on t.c0=:t.c0""", {'t':t})
        self.assertEqual(result.values.tolist(), [[3, 1]])

if __name__=="__main__":
    unittest.main()

