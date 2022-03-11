import logging
import paramiko
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    shcommand = "./test.sh"
    host = "20.119.212.235"
    username = "sqladmin"
    password = "sqladmin$1234"
    port = 22

    logging.info('Variable assignments completed succesfully')
    if not name:
        try:
            req_body = req.get_json()
                
            rmtClient = paramiko.SSHClient()
            logging.info('rmtClient variable created')
            rmtClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            rmtClient.connect(host, port, username, password)
            stdin, stdout, stderr = rmtClient.exec_command(shcommand)
            logging.info('rmtClient variable created')
            lines = stdout.readlines()
            exitstatus = stdout.channel.exit_status  
            logging.info(lines)
            logging.info("Exit Status : " + str(exitstatus))
            # print("exit status: %s" % stdout.channel.exit_status)
            # print(lines)

            stdin.close()
            stdout.close()
            stderr.close()
            rmtClient.close()

        except Exception as e:
            logging.info(e)

        
     

        else:
            name = req_body.get('name')

    
    if name:
        return func.HttpResponse("Hello, {name}. {stderr}. {stdout}.This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
