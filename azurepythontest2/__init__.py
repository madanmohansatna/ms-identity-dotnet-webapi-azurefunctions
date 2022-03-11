import logging
import paramiko
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    shcommand = "./test.sh"
    host = "20.119.212.235"
    username = "sqladmin"
    password = "sqladmin$12345"
    port = 22

    logging.info('Variable assignments completed succesfully')
    try:
               
        rmtClient = paramiko.SSHClient()
        logging.info('rmtClient variable created')
        rmtClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        rmtClient.connect(host, port, username, password)
        stdin, stdout, stderr = rmtClient.exec_command(shcommand)
        logging.info('rmtClient variable created')

    except Exception as e:
            logging.info(e)

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
     
    if exitstatus == 0:
        return func.HttpResponse("Execution Completed Successfully..", status_code=200)
    else:
        errorstring = "Something Failed.. :" + str(exitstatus)
        return func.HttpResponse(errorstring, status_code=200)

