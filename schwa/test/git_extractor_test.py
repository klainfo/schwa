import unittest
import tempfile
import os
import git
import shutil
import time
from schwa.extraction import GitExtractor
from schwa.repository import *


class TestGitExtractor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = os.path.join(tempfile.gettempdir(), "repo-test")
        if os.path.exists(self.temp_dir):
                 shutil.rmtree(self.temp_dir)
        self.repo = git.Repo.init(self.temp_dir)
        self.repo.git.execute(["git", "config", "user.email", "petergriffin@familyguy.com"])
        self.repo.git.execute(["git", "config", "user.name", "Peter Griffin"])

    def testExtraction(self):
        code = """
            package org.feup.meoarenacustomer.app;
            import android.app.DownloadManager;

            import com.loopj.android.http.*;


            static class API {
                static String getUrl() {
                    return url;
                }

                static void setUrl(String url) {
                    this.url = url;
                }

                private String url;
                private final String PRODUCTION_URL = "http://neo.andrefreitas.pt:8081/api";
                private static AsyncHttpClient client = new AsyncHttpClient();

                static API(String url ){
                    this.url = url;
                }

                static API(){
                    this.url = PRODUCTION_URL;
                }


                static void login(String email, String password, AsyncHttpResponseHandler responseHandler){
                    RequestParams params = new RequestParams();
                    params.put("email", email);
                    params.put("password", password);
                    client.post(url + "/login", params, responseHandler);
                }

                static void register(String name, String email, String nif, String password, String ccNumber, String ccType, String ccValidity, AsyncHttpResponseHandler responseHandler){
                    RequestParams params = new RequestParams();
                    params.put("name", name);
                    params.put("email", email);
                    params.put("password", password);
                    params.put("nif", nif);
                    params.put("ccNumber", ccNumber);
                    params.put("ccType", ccType);
                    params.put("ccValidity", ccValidity);
                    client.post(url + "/customers", params, responseHandler);
                }

                static void getShows(AsyncHttpResponseHandler responseHandler) {
                    client.get(url + "/shows", responseHandler);
                }

            }

             private class SOAPAPI{
                private void login(String name){
                    params.put("email", email);
                }
            }"""

        """ First Commit """
        # Added API.java
        file_path = os.path.join(self.temp_dir, "API.java")
        f = open(file_path, "w")
        f.write(code)
        f.close()
        self.repo.git.add(file_path)
        # Added README.txt
        file_path = os.path.join(self.temp_dir, "README.txt")
        f = open(file_path, "w")
        f.write("TODO: Write readme")
        f.close()
        self.repo.git.add(file_path)
        self.repo.git.commit(m='First commit')
        creation_timestamp = time.time()

        code_b = """
            package org.feup.meoarenacustomer.app;
            import android.app.DownloadManager;

            import com.loopj.android.http.*;


            static class API {
                static String getUrl() {
                    return url;
                }

                static void setUrl(String url) {
                    this.url = url;
                }

                private String url;
                private final String PRODUCTION_URL = "http://neo.andrefreitas.pt:8081/api";
                private static AsyncHttpClient client = new AsyncHttpClient();

                static API(String url ){
                    this.url = url;
                }

                static API(){
                    this.url = PRODUCTION_URL;
                }

                // Modified method
                static void login(String email, String password, AsyncHttpResponseHandler responseHandler){
                    RequestParams params = new RequestParams();
                    params.put("email", email);
                    client.post(url + "/login", params, responseHandler);
                }

                // Removed method register()

                // Added method
                static void recover(String name){
                    RequestParams params = new RequestParams();
                    params.put("name", name);
                    params.put("email", email);
                }

                // Added method
                static void outputShows(AsyncHttpResponseHandler responseHandler) {
                    client.get(url + "/shows", responseHandler);
                }

                static void getShows(AsyncHttpResponseHandler responseHandler) {
                    client.get(url + "/shows", responseHandler);
                }

            }

            private class JSONAPI{
                private void recover(String name){
                    RequestParams params = new RequestParams();
                    params.put("name", name);
                    params.put("email", email);
                }
            }
            """

        """ Second commit """
        # Modified API.java
        file_path = os.path.join(self.temp_dir, "API.java")
        f = open(file_path, "w")
        f.write(code_b)
        f.close()
        self.repo.git.add(file_path)
        self.repo.git.commit(m='Second commit')

        code = """/* CallingMethodsInSameClass.java
         *
         * illustrates how to call static methods a class
         * from a method in the same class
         */

        public class CallingMethodsInSameClass
        {
            public static void main(String[] args) {
                printOne();
                printOne();
                printTwo();
            }

            public static void printOne() {
                System.out.println("Hello World");
            }

            public static void printTwo() {
                printOne();
                printOne();
            }
        }"""

        """ Third commit """
        # Added CallingMethodsInSameClass.java
        file_path = os.path.join(self.temp_dir, "CallingMethodsInSameClass.java")
        f = open(file_path, "w")
        f.write(code)
        f.close()
        self.repo.git.add(file_path)
        # Modified README.txt
        file_path = os.path.join(self.temp_dir, "README.txt")
        f = open(file_path, "w")
        f.write("AUTHORS: Peter Griffin - peter@familyguy.com")
        f.close()
        self.repo.git.add(file_path)
        self.repo.git.commit(m='Third commit')

        """ Fourth Commit """
        # Deleted CallingMethodsInSameClass.java
        file_path = os.path.join(self.temp_dir, "CallingMethodsInSameClass.java")
        self.repo.git.rm(file_path)
        # Renamed API.java to API2.java
        file_path_a = os.path.join(self.temp_dir, "API.java")
        file_path_b = os.path.join(self.temp_dir, "API2.java")
        self.repo.git.mv(file_path_a, file_path_b)
        self.repo.git.commit(m='Fourth commit')

        """ Fifth Commit"""
        # Modified README.txt
        file_path = os.path.join(self.temp_dir, "README.txt")
        f = open(file_path, "w")
        f.write("AUTHORS: Peter Griffin and Louis Griffin")
        f.close()
        self.repo.git.add(file_path)
        self.repo.git.commit(m='Fifth commit')

        """ Extract """
        extractor = GitExtractor(self.temp_dir)
        repository = extractor.extract(method_granularity=True, parallel=False)

        """ Tests """
        self.assertEqual(len(repository.commits), 4, msg="It should only extract commits related to code")
        self.assertTrue(repository.timestamp < creation_timestamp, msg="It should extract the timestamp of first commit")

        self.assertEqual(repository.commits[0].message, "First commit\n")
        self.assertEqual(repository.commits[0].author, "petergriffin@familyguy.com")
        diffs = repository.commits[0].diffs
        self.assertEqual(len(diffs), 11)
        self.assertTrue(DiffFile(file_b="API.java", added=True) in diffs)
        self.assertTrue(DiffClass(file_name="API.java", class_b="SOAPAPI", added=True) in diffs)
        self.assertTrue(DiffClass(file_name="API.java", class_b="API", added=True) in diffs)
        self.assertTrue(DiffMethod(file_name="API.java", class_name="API", method_b="getUrl", added=True) in diffs)
        self.assertTrue(DiffMethod(file_name="API.java", class_name="API", method_b="setUrl", added=True) in diffs)
        self.assertTrue(DiffMethod(file_name="API.java", class_name="API", method_b="API", added=True) in diffs)
        self.assertTrue(DiffMethod(file_name="API.java", class_name="API", method_b="login", added=True) in diffs)
        self.assertTrue(DiffMethod(file_name="API.java", class_name="API", method_b="register", added=True) in diffs)
        self.assertTrue(DiffMethod(file_name="API.java", class_name="API", method_b="getShows", added=True) in diffs)
        self.assertTrue(DiffMethod(file_name="API.java", class_name="SOAPAPI", method_b="login", added=True) in diffs)

        self.assertEqual(repository.commits[1].message, "Second commit\n")
        diffs = repository.commits[1].diffs
        self.assertEqual(len(diffs), 10)
        self.assertTrue(DiffFile(file_a="API.java", file_b="API.java", modified=True) in diffs)
        self.assertTrue(DiffClass("API.java", class_a="API", class_b="API", modified=True) in diffs,
                        msg="It should recognize modified classes")
        self.assertTrue(DiffMethod("API.java", class_name="API", method_a="login", method_b="login", modified=True)
                        in diffs, msg="It should recognize modified methods")
        self.assertTrue(DiffMethod("API.java", class_name="API", method_a="register", removed=True) in diffs,
                        msg="It should recognize removed methods")
        self.assertTrue(DiffMethod("API.java", class_name="API", method_b="recover", added=True) in diffs,
                        msg="It should recognize added methods")
        self.assertTrue(DiffMethod("API.java", class_name="API", method_b="outputShows", added=True) in diffs,
                        msg="It should recognize added methods")
        self.assertTrue(DiffClass("API.java", class_a="SOAPAPI", removed=True) in diffs,
                        msg="It should recognize removed classes")
        self.assertTrue(DiffClass("API.java", class_b="JSONAPI", added=True) in diffs,
                        msg="It should recognize added classes")
        self.assertTrue(DiffMethod("API.java", class_name="SOAPAPI", method_a="login", removed=True) in diffs,
                        msg="It should recognize removed methods")
        self.assertTrue(DiffMethod("API.java", class_name="JSONAPI", method_b="recover", added=True) in diffs,
                        msg="It should recognize added methods")

        self.assertEqual(repository.commits[2].message, "Third commit\n")
        diffs = repository.commits[2].diffs
        self.assertEqual(len(diffs), 5)
        self.assertTrue(DiffFile(file_b="CallingMethodsInSameClass.java", added=True) in diffs)
        self.assertTrue(DiffClass(file_name="CallingMethodsInSameClass.java", class_b="CallingMethodsInSameClass",
                                  added=True) in diffs)
        self.assertTrue(DiffMethod(file_name="CallingMethodsInSameClass.java", class_name="CallingMethodsInSameClass",
                                   method_b="main", added=True) in diffs)
        self.assertTrue(DiffMethod(file_name="CallingMethodsInSameClass.java", class_name="CallingMethodsInSameClass",
                                   method_b="printOne", added=True) in diffs)
        self.assertTrue(DiffMethod(file_name="CallingMethodsInSameClass.java", class_name="CallingMethodsInSameClass",
                                   method_b="printTwo", added=True) in diffs)

        self.assertEqual(repository.commits[3].message, "Fourth commit\n")
        diffs = repository.commits[3].diffs
        self.assertEqual(len(diffs), 2)
        self.assertTrue(DiffFile(file_a="API.java", file_b="API2.java", renamed=True) in diffs)
        self.assertTrue(DiffFile(file_a="CallingMethodsInSameClass.java", removed=True) in diffs)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

