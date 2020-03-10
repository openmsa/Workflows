The purpose of this workflow is to generate the PHP code necessary to call a microservice function (CREATE/UPDATE/DELETE) from a microservice definition.
It takes a repository path to a micoservice definition (the .xml file) and generate 3 php files under the Workflow repository, in a path similar to the path of the microservice
* Task_Create.php
* Task_Update.php
* Task_Delete.php
The PHP files can then be resused as is or simply used as a base code sample for developing more complex workflow tasks
