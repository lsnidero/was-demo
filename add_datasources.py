import sys
import os

global  AdminConfig

def create_auth(alias, username, password, description):
    AdminTask.createAuthDataEntry('[-alias ' + alias + ' -user "' + username + '" -password "' + password + '" -description "' + description + '" ]')
    print ("Created JAAS credentials for " + description + " with alias " + alias)

def update_env_var(var_name, new_value):
    node = AdminConfig.getid("/Node:DefaultNode01/")

    var_substitutions = AdminConfig.list("VariableSubstitutionEntry",node).split(java.lang.System.getProperty("line.separator"))

    for var_substitute in var_substitutions:
        current_var_name = AdminConfig.showAttribute(var_substitute, "symbolicName")
        if current_var_name == var_name:
            AdminConfig.modify(var_substitute,[["value", new_value]])
            print (current_var_name + " changed to " + new_value)
            break


def create_env_variables():

    update_env_var('ORACLE_JDBC_DRIVER_PATH','/work/wasconf/db-drivers/oracle')
    update_env_var('DB2UNIVERSAL_JDBC_DRIVER_PATH','/work/wasconf/db-drivers/db2')
    update_env_var('UNIVERSAL_JDBC_DRIVER_PATH','/work/wasconf/db-drivers/db2')

    print ("Created env vars")

def create_oracle_datasource(name, jndi_name, url, description):
    oracle_jdbc_provider_id = AdminTask.createJDBCProvider('[-scope Cell=DefaultCell01 -databaseType Oracle -providerType "Oracle JDBC Driver" -implementationType "Connection pool data source" -name "Oracle JDBC Driver" -description "Oracle JDBC Driver" -classpath [${ORACLE_JDBC_DRIVER_PATH}/ojdbc8.jar ] -nativePath "" ]')
    print ("Created Oracle JDBC provider")
    AdminTask.createDatasource(oracle_jdbc_provider_id, '[-name ' + name + ' -jndiName ' + jndi_name + ' -dataStoreHelperClassName com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias DefaultNode01/oracle-creds -configureResourceProperties [[URL java.lang.String ' + url + ']]]')
    print ("Created Oracle datasource for " + description)

def create_db2_datasource(name, jndi_name, database_name, server_name, port, description): 
    db2_jdbc_provider_id = AdminTask.createJDBCProvider('[-scope Cell=DefaultCell01 -databaseType DB2 -providerType "DB2 Universal JDBC Driver Provider" -implementationType "Connection pool data source" -name "DB2 Universal JDBC Driver Provider" -description "One-phase commit DB2 JCC provider that supports JDBC 3.0. Data sources that use this provider support only 1-phase commit processing, unless you use driver type 2 with the application server for z/OS. If you use the application server for z/OS, driver type 2 uses RRS and supports 2-phase commit processing." -classpath [${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc.jar ${UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cu.jar ${DB2UNIVERSAL_JDBC_DRIVER_PATH}/db2jcc_license_cisuz.jar ] -nativePath [${DB2UNIVERSAL_JDBC_DRIVER_NATIVEPATH} ] ]')
    print ("Created DB2 JDBC provider")   
    AdminTask.createDatasource(db2_jdbc_provider_id, '[-name '+ name + ' -jndiName ' + jndi_name + ' -dataStoreHelperClassName com.ibm.websphere.rsadapter.DB2UniversalDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias DefaultNode01/db2-creds -configureResourceProperties [[databaseName java.lang.String ' + database_name + '] [driverType java.lang.Integer 4] [serverName java.lang.String ' + server_name + '] [portNumber java.lang.Integer ' + port + ']]]')
    print ("Created DB2 datasource for " + description)

def create_jaas_auth():
    # alias,username,password,description
    conf_file = open('/tmp/custom-users.csv', 'r')
    i = 0
    for line in conf_file.readlines():
        if i == 0:
            i = i + 1 # skip first line
        else:    
            credential = line.split(",")
            alias = credential[0]
            username = credential[1]
            password = credential[2]
            description = credential[3]
            create_auth(alias, username, password, description)
    #AdminTask.listAuthDataEntries()  

def create_datasources():
    # database_type,name,jndi_name,database_name,servername,port,description
    conf_file = open('/tmp/custom-datasources.csv', 'r')
    i = 0
    for line in conf_file.readlines():
        if i == 0:
            i = i + 1 # skip first line
        else:    
            datasource = line.split(",")
            db_type = datasource[0]
            name = datasource[1]
            jndi_name = datasource[2]
            database_name = datasource[3]
            server_name = datasource[4]
            port = datasource[5]
            description = datasource[6]
            if db_type == 'ORACLE':
                create_oracle_datasource(name, jndi_name, 'jdbc:oracle:thin:@' + server_name + ':' + port + '/' + database_name, description)
            else:
                create_db2_datasource(name, jndi_name, database_name, server_name, port, description)



# Main

print ("Setting Datasources  ...")
create_env_variables()

create_jaas_auth()
create_datasources()

AdminConfig.save()

