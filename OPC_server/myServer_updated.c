#include <open62541/plugin/log_stdout.h>
#include <open62541/server.h>
#include <open62541/server_config_default.h>

#include <signal.h>
#include <stdlib.h>

static volatile UA_Boolean running = true;

static void stopHandler(int sign) {
	UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_SERVER, "received ctrl-c");
	running = false;

}


static void addVariable(UA_Server *server) 
{
	
	/* Define the attribute of myInteger variable node */
	UA_VariableAttributes attr = UA_VariableAttributes_default;
	UA_Int32 myInteger = 42;
	UA_Variant_setScalar(&attr.value, &myInteger, &UA_TYPES[UA_TYPES_INT32]);
	attr.description = UA_LOCALIZEDTEXT("en-US", "the answer");
	attr.displayName = UA_LOCALIZEDTEXT("en-US", "test");
	attr.dataType = UA_TYPES[UA_TYPES_INT32].typeId;
	attr.accessLevel = UA_ACCESSLEVELMASK_READ | UA_ACCESSLEVELMASK_WRITE;
	
	
	/* Add the variable node to the information model */
	UA_NodeId myIntegerNodeId = UA_NODEID_STRING(1, "me");
	UA_QualifiedName myIntegerName = UA_QUALIFIEDNAME(1, "the answer");
	UA_NodeId parentNodeId = UA_NODEID_NUMERIC(0, UA_NS0ID_OBJECTSFOLDER);
	UA_NodeId parentReferenceNodeId = UA_NODEID_NUMERIC(0, UA_NS0ID_ORGANIZES);
	UA_Server_addVariableNode(server, myIntegerNodeId, parentNodeId, parentReferenceNodeId, myIntegerName, UA_NODEID_NUMERIC(0,UA_NS0ID_BASEDATAVARIABLETYPE), attr, NULL, NULL);
	
	printf("Value = %d Description =  %s DisplayName = %s \n", attr.value, attr.description, attr.displayName);
}

static void addMatrixVariable(UA_Server *server)
{
	UA_VariableAttributes attr = UA_VariableAttributes_default;
	attr.displayName = UA_LOCALIZEDTEXT("en-US", "Double Matrix");
	attr.accessLevel = UA_ACCESSLEVELMASK_READ | UA_ACCESSLEVELMASK_WRITE;
	
	/* Set the variable value constraints */
	attr.dataType = UA_TYPES[UA_TYPES_DOUBLE].typeId;
	attr.valueRank = UA_VALUERANK_TWO_DIMENSIONS;
	UA_UInt32 arrayDims[2] = {2,2};
	attr.arrayDimensions = arrayDims;
	attr.arrayDimensionsSize = 2;
	
	/* Set the value. The array dimensions need to be the same for the value. */
	UA_Double zero[4] = {0.0, 0.0, 0.0, 0.0};
	UA_Variant_setArray(&attr.value, zero, 4, &UA_TYPES[UA_TYPES_DOUBLE]);
	attr.value.arrayDimensionsSize = 2;
	
	UA_NodeId myIntegerNodeId = UA_NODEID_STRING(1, "double matrix");
	UA_QualifiedName myIntegerName = UA_QUALIFIEDNAME(1, "double matrix");
	UA_NodeId parentNodeId = UA_NODEID_NUMERIC(0, UA_NS0ID_OBJECTSFOLDER);
	UA_NodeId parentReferenceNodeId = UA_NODEID_NUMERIC(0, UA_NS0ID_ORGANIZES);
	UA_Server_addVariableNode(server, myIntegerNodeId, parentNodeId, parentReferenceNodeId, myIntegerName, UA_NODEID_NUMERIC(0,UA_NS0ID_BASEDATAVARIABLETYPE), attr, NULL, NULL);
}

static void writeVariable(UA_Server *server)
{
	UA_NodeId myIntegerNodeId = UA_NODEID_STRING(1, "the answer");
	
	/* Write a different integer_value */
	UA_Int32 myInteger = 43;
	UA_Variant myVar;
	UA_Variant_init(&myVar);
	UA_Variant_setScalar(&myVar, &myInteger, &UA_TYPES[UA_TYPES_INT32]);
	UA_Server_writeValue(server, myIntegerNodeId, myVar);
	
	/* Set the status code of the value to an error code. The function
	 * UA_Server_write provides access to the raw service. The above
	 * UA_Server_writeValue is a syntactic sugar for writing a specific node 
	 * attribute with the raw serverice */
	 UA_WriteValue wv;
	 UA_WriteValue_init(&wv);
	 wv.nodeId = myIntegerNodeId;
	 wv.attributeId = UA_ATTRIBUTEID_VALUE;
	 wv.value.status = UA_STATUSCODE_BADNOTCONNECTED;
	 wv.value.hasStatus = true;
	 UA_Server_write(server, &wv);
	 
	 /* Reset the variable to a good statuscode with a value */
	 wv.value.hasStatus = false;
	 wv.value.value = myVar;
	 wv.value.hasValue = true;
	 UA_Server_write(server, &wv);
}

static void
manuallyDefineBarcodeApp(UA_Server *server) {
    UA_NodeId barcodeAppId; /* get the nodeid assigned by the server */
    UA_ObjectAttributes oAttr = UA_ObjectAttributes_default;
    oAttr.displayName = UA_LOCALIZEDTEXT("en-US", "Barcode App (Manual)");
    UA_Server_addObjectNode(server, UA_NODEID_NULL,
                            UA_NODEID_NUMERIC(0, UA_NS0ID_OBJECTSFOLDER),
                            UA_NODEID_NUMERIC(0, UA_NS0ID_ORGANIZES),
                            UA_QUALIFIEDNAME(1, "Barcode App (Manual)"), UA_NODEID_NUMERIC(0, UA_NS0ID_BASEOBJECTTYPE),
                            oAttr, NULL, &barcodeAppId);

    UA_VariableAttributes mnAttr = UA_VariableAttributes_default;
    UA_String barcodeNumber = UA_STRING("empty");
    UA_Variant_setScalar(&mnAttr.value, &manufacturerName, &UA_TYPES[UA_TYPES_STRING]);
    mnAttr.displayName = UA_LOCALIZEDTEXT("en-US", "Barcode Number");
    UA_Server_addVariableNode(server, UA_NODEID_NULL, pumpId,
                              UA_NODEID_NUMERIC(0, UA_NS0ID_HASCOMPONENT),
                              UA_QUALIFIEDNAME(1, "Barcode Number"),
                              UA_NODEID_NUMERIC(0, UA_NS0ID_BASEDATAVARIABLETYPE), mnAttr, NULL, NULL);

    UA_VariableAttributes modelAttr = UA_VariableAttributes_default;
    UA_String modelName = UA_STRING("Mega Pump 3000");
    UA_Variant_setScalar(&modelAttr.value, &modelName, &UA_TYPES[UA_TYPES_STRING]);
    modelAttr.displayName = UA_LOCALIZEDTEXT("en-US", "ModelName");
    UA_Server_addVariableNode(server, UA_NODEID_NULL, pumpId,
                              UA_NODEID_NUMERIC(0, UA_NS0ID_HASCOMPONENT),
                              UA_QUALIFIEDNAME(1, "ModelName"),
                              UA_NODEID_NUMERIC(0, UA_NS0ID_BASEDATAVARIABLETYPE), modelAttr, NULL, NULL);

    UA_VariableAttributes statusAttr = UA_VariableAttributes_default;
    UA_Boolean status = true;
    UA_Variant_setScalar(&statusAttr.value, &status, &UA_TYPES[UA_TYPES_BOOLEAN]);
    statusAttr.displayName = UA_LOCALIZEDTEXT("en-US", "Status");
    UA_Server_addVariableNode(server, UA_NODEID_NULL, pumpId,
                              UA_NODEID_NUMERIC(0, UA_NS0ID_HASCOMPONENT),
                              UA_QUALIFIEDNAME(1, "Status"),
                              UA_NODEID_NUMERIC(0, UA_NS0ID_BASEDATAVARIABLETYPE), statusAttr, NULL, NULL);

    UA_VariableAttributes rpmAttr = UA_VariableAttributes_default;
    UA_Double rpm = 50.0;
    UA_Variant_setScalar(&rpmAttr.value, &rpm, &UA_TYPES[UA_TYPES_DOUBLE]);
    rpmAttr.displayName = UA_LOCALIZEDTEXT("en-US", "MotorRPM");
    UA_Server_addVariableNode(server, UA_NODEID_NULL, pumpId,
                              UA_NODEID_NUMERIC(0, UA_NS0ID_HASCOMPONENT),
                              UA_QUALIFIEDNAME(1, "MotorRPMs"),
                              UA_NODEID_NUMERIC(0, UA_NS0ID_BASEDATAVARIABLETYPE), rpmAttr, NULL, NULL);
}

int main(void)
{
	signal(SIGINT, stopHandler);
	signal(SIGTERM, stopHandler);
	
	UA_Server *server = UA_Server_new();
	UA_ServerConfig_setDefault(UA_Server_getConfig(server));
	
	UA_StatusCode retval = UA_Server_run(server, &running);
	
	UA_Server_delete(server);
	return retval == UA_STATUSCODE_GOOD ? EXIT_SUCCESS : EXIT_FAILURE;
	
}


