import azure.functions as func
import logging

app=func.FunctionApp()


@app.service_bus_queue_trigger(arg_name="message", queue_name="azappbusqueue",
                               connection="AZAppBus_SERVICEBUS") 
def servicebus_trigger(message: func.ServiceBusMessage):
    logging.info('Python ServiceBus Queue trigger processed a message: %s',
                message.get_body().decode('utf-8'))


@app.route(route="http_trigger", auth_level=func.AuthLevel.ANONYMOUS)
@app.service_bus_queue_output(arg_name="message", queue_name="azappbusqueue",
                               connection="AZAppBus_SERVICEBUS")
def http_trigger(req: func.HttpRequest, message: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        message.set(name)
        return func.HttpResponse(f"Sent {name}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )